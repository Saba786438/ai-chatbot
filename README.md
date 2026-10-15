# AI Chatbot Web Application

A simple web-based chatbot built with Python and Flask. It uses a local Ollama model to generate responses, so messages can be processed on your own computer instead of through a hosted AI API.

## Features

- Browser-based chat interface
- Flask backend with a `/chat` endpoint
- Local AI responses through Ollama
- Conversation context for follow-up questions
- Typing status and helpful connection/model error messages

## Requirements

- Python 3.9 or newer
- Ollama installed and running
- The `llama3.2:3b` model downloaded in Ollama

## Setup

Open a terminal in the project folder and install the Python packages:

```bash
python -m pip install Flask requests
```

Download the model:

```bash
ollama pull llama3.2:3b
```

Start Ollama if it is not already running as a background service:

```bash
ollama serve
```

## Run the application

In a second terminal, from the project folder, run:

```bash
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

## Project structure

```text
ai-chatbot/
├── app.py
├── requirements.txt.txt
├── templates/
│   └── index.html
└── static/
    ├── script.js
    └── style.css
```

`app.py` serves the page and sends conversation messages to Ollama. `templates/index.html` contains the chat page. `static/script.js` sends messages and displays responses, and `static/style.css` styles the interface.

## Configuration

The Ollama address and model are set near the top of `app.py`:

```python
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2:3b"
```

Change `MODEL` to a model installed in Ollama if needed. The application expects Ollama's API to be available at `OLLAMA_URL`.

## Troubleshooting

- **Ollama is not running:** Start Ollama, then retry your message.
- **Model not found:** Run `ollama pull llama3.2:3b`, or change `MODEL` to an installed model.
- **Python package missing:** Run `python -m pip install Flask requests`.

## Deployment note

This project is configured for local development. Before making it publicly accessible, turn off Flask debug mode and configure a production web server and appropriate security settings.
