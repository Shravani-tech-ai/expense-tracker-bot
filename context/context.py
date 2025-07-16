# context/context.py

class AgentContext:
    def __init__(self, user_id: str = "default_user"):
        self.user_id = user_id
        self.session_id = None  # optional, can be used for multi-session tracking
        self.chat_history = []
        self.memory_log = []
        self.current_state = {}
