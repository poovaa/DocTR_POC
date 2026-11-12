
const fileInput = document.getElementById("fileInput");
const uploadStatus = document.getElementById("uploadStatus");
const chatMessages = document.getElementById("chatMessages");
const questionInput = document.getElementById("questionInput");
const sendBtn = document.getElementById("sendBtn");
const welcome = document.getElementById("welcome");
const newChatBtn = document.getElementById("newChatBtn");

// Upload document
fileInput.addEventListener("change", async function () {
    const file = fileInput.files[0];

    if (!file) return;

    const formData = new FormData();
    formData.append("files", file);

    uploadStatus.textContent = "Uploading and processing document...";

    try {
        const response = await fetch("/upload-files", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Document upload failed");
        }

        uploadStatus.textContent =
            "✓ " + file.name + " uploaded successfully!";

    } catch (error) {
        uploadStatus.textContent = "Error: " + error.message;
    }

    fileInput.value = "";
});

// Display message safely
function addMessage(text, type) {
    const message = document.createElement("div");
    message.className = "message " + type;
    message.textContent = text;

    chatMessages.appendChild(message);

    return message;
}

// Send question to FastAPI
async function sendQuestion() {
    const question = questionInput.value.trim();

    if (!question) return;

    welcome.style.display = "none";

    addMessage(question, "user-message");

    questionInput.value = "";
    questionInput.style.height = "auto";

    sendBtn.disabled = true;

    const loadingMessage = addMessage(
        "Thinking... Searching your documents.",
        "ai-message"
    );

    try {
        const response = await fetch("/query", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Something went wrong");
        }

        // Display only AI-generated answer
        loadingMessage.textContent =
            data.answer || data.response || "No answer returned.";

    } catch (error) {
        loadingMessage.textContent = "Error: " + error.message;
    }

    sendBtn.disabled = false;
    questionInput.focus();

    chatMessages.scrollIntoView({
        behavior: "smooth",
        block: "end"
    });
}

// Send button
sendBtn.addEventListener("click", sendQuestion);

// Press Enter to send; Shift + Enter for new line
questionInput.addEventListener("keydown", function (event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendQuestion();
    }
});

// Auto-adjust textarea height
questionInput.addEventListener("input", function () {
    this.style.height = "auto";
    this.style.height = Math.min(this.scrollHeight, 120) + "px";
});

// New chat
newChatBtn.addEventListener("click", function () {
    chatMessages.innerHTML = "";
    welcome.style.display = "block";
    questionInput.value = "";
    uploadStatus.textContent = "";
});
