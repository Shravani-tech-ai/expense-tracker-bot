from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os
import requests
import mimetypes
from PIL import Image
from requests.auth import HTTPBasicAuth

from ocr.image_ocr import extract_text_from_image
from ocr.pdf_ocr import extract_text_from_pdf
from agent.tracker_agent import invoke_agent  # handles text prompts

# Load Twilio credentials from environment variables
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get('Body', '').strip()
    media_url = request.values.get('MediaUrl0', '')
    media_type = request.values.get('MediaContentType0', '')

    resp = MessagingResponse()
    msg = resp.message()

    print(f"📷 Media Type: {media_type}")
    print(f"🌐 Media URL: {media_url}")

    # Case 1: Media (Image or PDF)
    if media_url:
        try:
            ext = mimetypes.guess_extension(media_type)
            if not ext:
                msg.body("❌ Unsupported media type.")
                return str(resp)
            filename = f"bill_input{ext}"

            # 🔐 Download with Twilio auth
            r = requests.get(media_url, auth=HTTPBasicAuth(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN))
            if r.status_code != 200:
                msg.body(f"❌ Failed to download media (status {r.status_code}).")
                print(r.text)
                return str(resp)

            with open(filename, 'wb') as f:
                f.write(r.content)
            print(f"📥 Media downloaded and saved as: {filename}")

            if not os.path.exists(filename) or os.path.getsize(filename) == 0:
                msg.body("❌ File could not be saved correctly.")
                return str(resp)

            # Validate and process media
            if "image" in media_type:
                try:
                    with Image.open(filename) as img:
                        img.verify()
                except Exception as e:
                    msg.body(f"❌ Image verification failed: {e}")
                    return str(resp)

                text = extract_text_from_image(filename)

            elif "pdf" in media_type:
                text = extract_text_from_pdf(filename)

            else:
                msg.body("❌ Unsupported file type.")
                return str(resp)

            print(f"📑 Extracted text:\n{text}")

            cleaned_text = text.strip().replace("|", "I")
            print(f"🧾 Cleaned Text: {cleaned_text}")

            response = invoke_agent(cleaned_text)
            msg.body(response)

        except Exception as e:
            print("❌ Error during processing:", e)
            msg.body(f"❌ Error while processing media:\n{e}")

        return str(resp)

    # Case 2: Text-only message
    elif incoming_msg:
        try:
            print(f"💬 Text input: {incoming_msg}")
            response = invoke_agent(incoming_msg)
            msg.body(response)
        except Exception as e:
            print("❌ Error during agent call:", e)
            msg.body(f"❌ Error: {e}")
        return str(resp)

    else:
        msg.body("🤖 Please send a message or a photo/pdf of the bill.")
        return str(resp)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
