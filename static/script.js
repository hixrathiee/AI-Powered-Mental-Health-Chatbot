document.addEventListener('DOMContentLoaded', function () {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');
    const sendBtn = document.getElementById('send-btn');
    const voiceBtn = document.getElementById('voice-btn');
    const typingIndicator = document.getElementById('typing-indicator');

    // Initialize speech recognition
    let recognition = null;
    if ('webkitSpeechRecognition' in window) {
        recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        recognition.onresult = function (event) {
            const transcript = event.results[0][0].transcript;
            userInput.value = transcript;
            voiceBtn.innerHTML = '<i class="fas fa-microphone"></i>';
            voiceBtn.classList.remove('active');
        };

        recognition.onend = function () {
            voiceBtn.innerHTML = '<i class="fas fa-microphone"></i>';
            voiceBtn.classList.remove('active');
        };
    }

    function formatTime() {
        const now = new Date();
        return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    function addMessage(text, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', isUser ? 'user-message' : 'bot-message');

        const messageInfo = document.createElement('div');
        messageInfo.classList.add('message-info');

        const icon = document.createElement('i');
        icon.classList.add('fas', isUser ? 'fa-user' : 'fa-robot');

        const timestamp = document.createElement('span');
        timestamp.classList.add('timestamp');
        timestamp.textContent = formatTime();

        const messagePara = document.createElement('p');
        messagePara.textContent = text;

        messageInfo.appendChild(icon);
        messageInfo.appendChild(timestamp);
        messageDiv.appendChild(messageInfo);
        messageDiv.appendChild(messagePara);
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function showTypingIndicator() {
        typingIndicator.classList.remove('hidden');
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function hideTypingIndicator() {
        typingIndicator.classList.add('hidden');
    }

    async function sendMessage(message) {
        try {
            showTypingIndicator();

            const response = await fetch('http://localhost:5000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            hideTypingIndicator();
            addMessage(data.response, false);

            if (data.emotion) {
                const emotionDiv = document.createElement('div');
                emotionDiv.classList.add('emotion-info');
                emotionDiv.textContent = `🧠 Detected Emotion: ${data.emotion}`;
                chatMessages.appendChild(emotionDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
        } catch (error) {
            console.error('Error:', error);
            hideTypingIndicator();
            addMessage("Oops! Something went wrong. Please try again later.", false);
        }
    }

    chatForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const message = userInput.value.trim();
        if (!message) return;

        addMessage(message, true);
        userInput.value = '';
        sendMessage(message);
    });

    if (recognition) {
        voiceBtn.addEventListener('click', function () {
            if (voiceBtn.classList.contains('active')) {
                recognition.stop();
                voiceBtn.innerHTML = '<i class="fas fa-microphone"></i>';
                voiceBtn.classList.remove('active');
            } else {
                recognition.start();
                voiceBtn.innerHTML = '<i class="fas fa-microphone-slash"></i>';
                voiceBtn.classList.add('active');
            }
        });
    } else {
        voiceBtn.style.display = 'none';
    }

    userInput.addEventListener('input', function () {
        if (userInput.value.trim()) {
            sendBtn.removeAttribute('disabled');
        } else {
            sendBtn.setAttribute('disabled', 'disabled');
        }
    });

    sendBtn.setAttribute('disabled', 'disabled');
});
