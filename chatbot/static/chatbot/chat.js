const textarea = document.querySelector('.chat-input');

textarea.addEventListener('input', function () {
    this.style.height = 'auto';
    this.style.height = this.scrollHeight + 'px';
});
const form = document.getElementById("chat-form");
const chatBox = document.getElementById("chat-box");
const input = document.getElementById("message-input");
const conversationInput = document.getElementById("conversation_id");

// CSRF helper
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}
// error message function
function showError(message) {
    const div = document.createElement("div");
    div.className = "error-toast";
    div.innerText = message;

    document.body.appendChild(div);

    setTimeout(() => div.remove(), 3000);
}
// progress bar function
function updateProgressBar(tokensUsed, tokenLimit) {
    const percent = (tokensUsed / tokenLimit) * 100;

    const progressBar = document.getElementById("progress-bar");
    progressBar.style.width = percent + "%";
}
function scrollDown() {
    const chatBox = document.getElementById("chat-box");
    chatBox.scrollTop = chatBox.scrollHeight;
}

form.addEventListener("submit", function (e) {
    e.preventDefault();

    const message = input.value.trim();
    if (!message) return;

    //Show user message instantly
    const userDiv = document.createElement("div");
    userDiv.className = "user-msg";
    userDiv.innerText = message;
    chatBox.appendChild(userDiv);

    input.value = "";
    input.style.height = "auto";

    chatBox.scrollTop = chatBox.scrollHeight;

    //  2. Show "typing..." placeholder
    const botDiv = document.createElement("div");
    botDiv.className = "bot-msg";
    botDiv.innerText = "Typing...";
    chatBox.appendChild(botDiv);
    scrollDown();

    fetch("", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken(),
        },
        body: new URLSearchParams({
            message: message,
            conversation_id: conversationInput.value
        })
    })
        .then(res => {
            if (!res.ok) {
                return res.json().then(err => {
                    throw new Error(err.error || "Something went wrong");
                });
            }
            return res.json();
        })
        .then(data => {
            conversationInput.value = data.conversation_id;
            //  Update usage
            const tokensUsedEl = document.getElementById("tokens-used");
            const tokenLimitEl = document.getElementById("token-limit");

            tokensUsedEl.innerText = data.tokens_used;

            const tokenLimit = parseInt(tokenLimitEl.innerText);
            updateProgressBar(data.tokens_used, tokenLimit);

            if (data.is_new) {
                const convoList = document.querySelector(".conversation-list");
                const newConvo = document.createElement("a");
                const newUrl = `?conversation_id=${data.conversation_id}`;
                window.history.pushState({}, "", newUrl);
                newConvo.href = newUrl;
                newConvo.className = "conversation-item";
                newConvo.innerText = data.conversation_title || "New Chat";

                convoList.prepend(newConvo);
            }

            // Replace typing with bot response
            botDiv.innerHTML = data.bot_response;

            chatBox.scrollTop = chatBox.scrollHeight;
        })
        .catch(err => {
            botDiv.remove();
            showError(err.message);
        });
});

window.addEventListener("load", function () {
    const tokensUsed = parseInt(document.getElementById("tokens-used").innerText);
    const tokenLimit = parseInt(document.getElementById("token-limit").innerText);

    updateProgressBar(tokensUsed, tokenLimit);
    scrollDown();
});