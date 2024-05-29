document.getElementById('send-button').addEventListener('click', function() {
    let messageInput = document.getElementById('message-input');
    let messageText = messageInput.value;

    if (messageText.trim() !== '') {
        appendMessage(messageText, 'user');
        messageInput.value = '';

        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: messageText })
        })
        .then(response => response.json())
        .then(data => {
            appendMessage(data.response, 'bot');
        });
    }
});

function appendMessage(text, sender) {
    let chatBox = document.getElementById('chat-box');
    let messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender);
    messageDiv.innerText = text;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}
