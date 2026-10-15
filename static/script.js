
const form = document.getElementById("chat-form");
const input = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");
const status = document.getElementById("status");
const sendButton = form.querySelector("button");

const messages = [];

function addMessage(text, sender) {
    const element = document.createElement("div");
    element.className = "message " + sender;
    element.textContent = text;
    chatBox.appendChild(element);
    chatBox.scrollTop = chatBox.scrollHeight;
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const text = input.value.trim();
    if (!text) return;

    addMessage(text, "user");
    messages.push({ role: "user", content: text });

    input.value = "";
    input.disabled = true;
    sendButton.disabled = true;
    status.textContent = "AI is thinking...";

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ messages })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.reply || "Request failed.");
        }

        addMessage(data.reply, "bot");
        messages.push({
            role: "assistant",
            content: data.reply
        });

    } catch (error) {
        addMessage(
            error.message || "Could not connect to the local AI.",
            "bot"
        );
    } finally {
        status.textContent = "";
        input.disabled = false;
        sendButton.disabled = false;
        input.focus();
    }
});
