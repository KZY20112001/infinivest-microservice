from typing import Optional
from app.openai_client import generate_chat_response


def get_chat_response(user_message: str, context: dict) -> str:
    """
    Get the reply given a user input and context
    """
    try: 
        return generate_chat_response(user_message, context)
    except Exception as e:
        return  f"failed to get a reply: {str(e)}"