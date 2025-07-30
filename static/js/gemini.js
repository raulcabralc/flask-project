document.addEventListener("DOMContentLoaded", function () {
  const userInput = document.getElementById("user-input");
  const messagesArea = document.getElementById("messages-area");
  const sendButton = document.getElementById("send-button");

  function addMessage(text, isUser = false) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${isUser ? "user-message" : "ai-message"}`;
    messageDiv.innerHTML = text;
    messagesArea.appendChild(messageDiv);
    messagesArea.scrollTop = messagesArea.scrollHeight;
  }

  function addLoadingMessage() {
    const messageDiv = document.createElement("div");
    messageDiv.className = "message ai-message loading";
    messageDiv.id = "loading-message";
    messageDiv.innerHTML = "Gemini is thinking...";
    messagesArea.appendChild(messageDiv);
    messagesArea.scrollTop = messagesArea.scrollHeight;
  }

  function removeLoadingMessage() {
    const loadingMsg = document.getElementById("loading-message");
    if (loadingMsg) {
      loadingMsg.remove();
    }
  }

  sendButton.addEventListener("click", () => {
    handleSubmit();
  });

  async function handleSubmit() {
    const message = userInput.value.trim();
    if (!message) return;

    addMessage(message, true);

    userInput.value = "";
    sendButton.disabled = true;

    addLoadingMessage();

    try {
      const response = await fetch("/gemini", {
        method: "POST",
        headers: {
          "Content-type": "application/json",
        },
        body: JSON.stringify({
          message,
        }),
      });

      if (!response.ok) {
        throw new Error(`Erro HTTP | Status: ${response.status}`);
      }

      const data = await response.json();

      removeLoadingMessage();
      addMessage(
        data.response || "Sorry, I couldn't process your information."
      );
    } catch (error) {
      console.error("Error sending message:", error);
      removeLoadingMessage();
      addMessage("Error connecting to server. Try again.", false);
    } finally {
      sendButton.disabled = false;
      userInput.focus();
    }
  }

  userInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      handleSubmit(e);
    }
  });
});
