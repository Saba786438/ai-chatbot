
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2:3b"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    messages = data.get("messages", [])

    if not isinstance(messages, list) or not messages:
        return jsonify({"reply": "Please enter a message."}), 400

    # Accept only user and assistant messages.
    safe_messages = []
    for item in messages[-20:]:
        if not isinstance(item, dict):
            continue

        role = item.get("role")
        content = item.get("content")

        if role not in ("user", "assistant"):
            continue

        if not isinstance(content, str) or not content.strip():
            continue

        safe_messages.append({
            "role": role,
            "content": content[:4000]
        })

    if not safe_messages or safe_messages[-1]["role"] != "user":
        return jsonify({"reply": "Please send a valid message."}), 400

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a helpful AI assistant. "
                    "Answer clearly and naturally. "
                    "Use previous messages to understand follow-up questions."
                )
            },
            *safe_messages
        ],
        "stream": False
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=300
        )
        response.raise_for_status()

        result = response.json()
        reply = result.get("message", {}).get("content", "")

        return jsonify({
            "reply": reply or "The model returned an empty response."
        })

    except requests.exceptions.ConnectionError:
        return jsonify({
            "reply": "Ollama is not running. Start Ollama and try again."
        }), 503

    except requests.exceptions.Timeout:
        return jsonify({
            "reply": "The model is taking too long. Please try again."
        }), 504

    except requests.exceptions.RequestException:
        app.logger.exception("Ollama request failed")
        return jsonify({
            "reply": "Unable to get an answer from the local AI model."
        }), 502


if __name__ == "__main__":
    app.run(debug=True)

