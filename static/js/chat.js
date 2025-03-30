document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const typingIndicator = document.getElementById('typing-indicator');
    
    // Chat history
    let chatHistory = [];
    
    // Initialize with a welcome message
    addBotMessage("Hello! I'm Nexus.AI, your intelligent assistant. How can I help you today?");
    
    // Event Listeners
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    // Focus input field on page load
    userInput.focus();
    
    /**
     * Send user message to the server and get response
     */
    function sendMessage() {
        const message = userInput.value.trim();
        
        if (!message) return;
        
        // Add user message to chat
        addUserMessage(message);
        
        // Clear input field
        userInput.value = '';
        
        // Show typing indicator
        showTypingIndicator();
        
        // Send to server
        fetchBotResponse(message);
    }
    
    /**
     * Add a user message to the chat display
     * @param {string} message - The user's message
     */
    function addUserMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', 'user-message');
        messageElement.textContent = message;
        
        chatMessages.appendChild(messageElement);
        
        // Add to chat history
        chatHistory.push({ sender: 'user', text: message });
        
        // Scroll to bottom
        scrollToBottom();
    }
    
    /**
     * Add a bot message to the chat display
     * @param {string} message - The bot's response message
     */
    function addBotMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', 'bot-message');
        messageElement.textContent = message;
        
        chatMessages.appendChild(messageElement);
        
        // Add to chat history
        chatHistory.push({ sender: 'bot', text: message });
        
        // Scroll to bottom
        scrollToBottom();
    }
    
    /**
     * Show the typing indicator in the chat
     */
    function showTypingIndicator() {
        typingIndicator.classList.remove('d-none');
        scrollToBottom();
    }
    
    /**
     * Hide the typing indicator in the chat
     */
    function hideTypingIndicator() {
        typingIndicator.classList.add('d-none');
    }
    
    /**
     * Scroll the chat area to the bottom
     */
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    /**
     * Fetch response from the chatbot API
     * @param {string} message - The user's message
     */
    async function fetchBotResponse(message) {
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message }),
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Simulate a slight delay for more natural response timing
            setTimeout(() => {
                // Hide typing indicator
                hideTypingIndicator();
                
                // Add bot response to chat
                if (data.response) {
                    addBotMessage(data.response);
                } else if (data.error) {
                    showError(data.error);
                }
            }, 1000);
            
        } catch (error) {
            console.error('Error fetching response:', error);
            
            // Hide typing indicator
            hideTypingIndicator();
            
            // Show error message in chat
            addBotMessage("Sorry, I'm having trouble connecting right now. Please try again later.");
            
            // Show error toast
            showError("Failed to connect to the chatbot service.");
        }
    }
});
