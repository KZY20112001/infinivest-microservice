
from flask import Blueprint,  request, jsonify
from app.services import get_chat_response

chat_bp = Blueprint('chat', __name__)



@chat_bp.route("/", methods=["POST"])
def chat():
    """
    Endpoint to get the reply given a user input
    """
    print("HIT")
    data = request.get_json()
    print("data:", data)
    user_message = data.get("input")
    context = data.get("context", {})
    response = get_chat_response(user_message, context)
    return jsonify({"message": response}), 200