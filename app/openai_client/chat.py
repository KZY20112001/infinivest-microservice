from .openai import get_response, format_message
from typing import Optional


def generate_chat_response(user_message: str, context: dict) -> str:
    """
    Generate the reply given a user input and context.
    """
    system_message = """
    You are called Infini-Assistant. You are an assistant for an application called InfiniVest which helps with wealth management and portfolio management. 
    Answer the user's questions based on the available context. 
    Only use the context if that is relevant to the user's query. The user's query may not be related to the context (and could be different subject entirely).
    """

    messages = [format_message("system", system_message)]
    messages.append(format_message("user", user_message))  

    if context == {}: 
        return get_response(messages)

    if context.get("profile"):
        messages.append(format_message("system", f"User profile: {context['profile']}"))

    if context.get("roboPortfolio"):
        messages.append(format_message("system", f"Robo-portfolio data: {context['roboPortfolio']}"))

    if context.get("manualPortfolio"):
        messages.append(format_message("system", f"Manual portfolio: {context['manualPortfolio']}"))

    return get_response(messages)