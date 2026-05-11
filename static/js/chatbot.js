// lkhdma d  Ilyass haaa
console.log("Chatbot JS chargé");
class EDTChatbot {
  constructor() {
    this.chatBody = document.getElementById('aiChatBody');
    this.chatInput = document.querySelector('.ai-input');
    this.sendBtn = document.querySelector('.ai-send-btn');
    this.toggleBtn = document.getElementById('aiToggleBtn');
    this.closeBtn = document.getElementById('aiCloseBtn');
    this.chatBox = document.getElementById('aiChatBox');
    this.isLoading = false;
 
    this.initEventListeners();
    this.loadHistory();
  }
 
  /**
   * Initialize all event listeners
   */
  initEventListeners() {
    // Toggle chat window
    if (this.toggleBtn) {
      this.toggleBtn.addEventListener('click', () => this.toggleChat());
    }
 
    // Close chat window
    if (this.closeBtn) {
      this.closeBtn.addEventListener('click', () => this.closeChat());
    }
 
    // Send message on button click
    if (this.sendBtn) {
      this.sendBtn.addEventListener('click', () => this.sendMessage());
    }
 
    // Send message on Enter key
    if (this.chatInput) {
      this.chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          this.sendMessage();
        }
      });
    }
 
    // Suggestion buttons
    const suggestionBtns = document.querySelectorAll('.ai-suggestion-btn');
    suggestionBtns.forEach((btn) => {
      btn.addEventListener('click', (e) => {
        const text = e.target.textContent;
        this.chatInput.value = text;
        this.sendMessage();
      });
    });
  }
 
  /**
   * Get CSRF token from cookies (required for Django POST)
   */
  getCsrfToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      document.cookie.split(';').forEach((cookie) => {
        const c = cookie.trim();
        if (c.startsWith('csrftoken=')) {
          cookieValue = decodeURIComponent(c.slice(10));
        }
      });
    }
    return cookieValue;
  }
 
  /**
   * Toggle chat window visibility
   */
  toggleChat() {
    if (!this.chatBox) return;
    const isVisible = this.chatBox.classList.contains('show');
    if (isVisible) {
      this.closeChat();
    } else {
      this.openChat();
    }
  }
 
  /**
   * Open chat window with animation
   */
  openChat() {
    if (!this.chatBox) return;
    this.chatBox.classList.add('show');
    this.chatInput?.focus();
  }
 
  /**
   * Close chat window
   */
  closeChat() {
    if (!this.chatBox) return;
    this.chatBox.classList.remove('show');
  }
 
  /**
   * Send message to Django backend
   */
  async sendMessage() {
    const message = this.chatInput?.value.trim();
 
    if (!message || this.isLoading) return;
 
    // Display user message immediately
    this.addMessage(message, 'user');
    this.chatInput.value = '';
 
    // Hide suggestion buttons once conversation starts
    const suggestions = document.querySelector('.ai-suggestions');
    if (suggestions) {
      suggestions.style.display = 'none';
    }
 
    // Show typing indicator
    this.showTyping(true);
    this.isLoading = true;
 
    try {
      const response = await fetch('/chatbot/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': this.getCsrfToken(),
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `message=${encodeURIComponent(message)}`,
      });
 
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
 
      const data = await response.json();
      this.showTyping(false);
      this.addMessage(data.reply || 'Pas de réponse reçue.', 'bot');
    } catch (error) {
      console.error('Chatbot Error:', error);
      this.showTyping(false);
      this.addMessage(
        'Désolé, une erreur s\'est produite. Vérifie ta connexion internet.',
        'bot'
      );
    } finally {
      this.isLoading = false;
      this.chatInput?.focus();
    }
  }
 
  /**
   * Add a message bubble to the chat
   */
  addMessage(text, type) {
    if (!this.chatBody) return;
 
    const msgDiv = document.createElement('div');
    msgDiv.className = `ai-message ai-message-${type}`;
 
    // Create text content with line breaks preserved
    const textNode = document.createElement('div');
    textNode.textContent = text;
    msgDiv.appendChild(textNode);
 
    // Add animation class
    msgDiv.classList.add('message-animate-in');
 
    this.chatBody.appendChild(msgDiv);
    this.autoScroll();
  }
 
  /**
   * Show/hide typing indicator
   */
  showTyping(show) {
    const typingDiv = document.querySelector('.ai-typing-indicator');
    if (!typingDiv) {
      if (show) {
        const indicator = document.createElement('div');
        indicator.className = 'ai-message ai-message-bot ai-typing-indicator';
        indicator.innerHTML = `
          <div class="typing-dots">
            <span></span>
            <span></span>
            <span></span>
          </div>
        `;
        this.chatBody?.appendChild(indicator);
        this.autoScroll();
      }
    } else {
      typingDiv.style.display = show ? 'flex' : 'none';
    }
  }
 
  /**
   * Auto-scroll chat to bottom
   */
  autoScroll() {
    if (this.chatBody) {
      setTimeout(() => {
        this.chatBody.scrollTop = this.chatBody.scrollHeight;
      }, 0);
    }
  }
 
  /**
   * Load conversation history from backend
   */
  async loadHistory() {
    try {
      const response = await fetch('/chatbot/history/');
      if (!response.ok) return;
 
      const data = await response.json();
      const history = data.history || [];
 
      // Load last 5 messages
      history.slice(0, 5).reverse().forEach((msg) => {
        this.addMessage(msg.question, 'user');
        this.addMessage(msg.reponse, 'bot');
      });
 
      // Hide suggestions if there's history
      if (history.length > 0) {
        const suggestions = document.querySelector('.ai-suggestions');
        if (suggestions) {
          suggestions.style.display = 'none';
        }
      }
    } catch (error) {
      console.error('Failed to load history:', error);
    }
  }
}
 
/**
 * Initialize chatbot when DOM is ready
 */
document.addEventListener('DOMContentLoaded', () => {
  // Only initialize if user is authenticated (check for chatbot HTML)
  if (document.getElementById('aiChatBox')) {
    window.chatbot = new EDTChatbot();
  }
});