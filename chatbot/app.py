from flask import Flask, jsonify, request
from flask_cors import CORS

from chatbot.chat import call_chat

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return "Welcome to TensionChat!"


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    response = call_chat(data["prompt_input"], data["context"])
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
