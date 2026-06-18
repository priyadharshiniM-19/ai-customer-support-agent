async function sendMessage() {

    const input = document.getElementById("question");

    const question = input.value.trim();

    if (!question) return;

    const chatBox = document.getElementById("chat-box");

    chatBox.innerHTML += `
        <div class="user-message">
            ${question}
        </div>
    `;

    input.value = "";

    chatBox.innerHTML += `
        <div class="bot-message" id="loading">
            Thinking...
        </div>
    `;

    chatBox.scrollTop = chatBox.scrollHeight;

    const response = await fetch("/ask", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            question: question
        })
    });

    const data = await response.json();

    document.getElementById("loading").remove();

    chatBox.innerHTML += `
        <div class="bot-message">
            ${data.answer}
        </div>
    `;

    chatBox.scrollTop = chatBox.scrollHeight;
}

document.addEventListener("DOMContentLoaded", () => {

    const input = document.getElementById("question");

    input.addEventListener("keydown", function(event) {

        if (event.key === "Enter") {

            event.preventDefault();

            sendMessage();
        }
    });

});