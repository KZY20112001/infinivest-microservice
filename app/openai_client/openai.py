from flask import current_app
from openai import OpenAI


def format_message(role: str, content: str) -> dict:
    """Formats a message for OpenAI API request."""
    return {"role": role, "content": content}


def get_response(messages: list) -> str:
    """Calls OpenAI API to get a response based on the provided messages."""
    
    client = OpenAI(
    api_key= current_app.config['OPENAI_API_KEY'],
    )
    completion = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=messages,
    ) 
    return completion.choices[0].message.content



