from langchain_core.chat_history import InMemoryChatMessageHistory

__session_memory = {}

def get_session_memory(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in __session_memory:
        __session_memory[session_id] = InMemoryChatMessageHistory()
    return __session_memory[session_id]