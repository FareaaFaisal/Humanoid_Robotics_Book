import React, { useState, useEffect, useRef } from 'react';
import { useLocation } from '@docusaurus/router';
import styles from './styles.module.css';

const RAGChatbotWidget: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<{ role: string; content: string }[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const location = useLocation();

  const FASTAPI_BACKEND_URL = process.env.NODE_ENV === 'production'
    ? "YOUR_PROD_FASTAPI_URL"
    : "http://localhost:8000"; // Make sure FastAPI runs on this port

  useEffect(() => {
    // Scroll to the latest message
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });

    // Track selected text
    const handleSelectionChange = () => {
      const selection = window.getSelection();
      setSelectedText(selection ? selection.toString() : '');
    };
    document.addEventListener('selectionchange', handleSelectionChange);
    return () => document.removeEventListener('selectionchange', handleSelectionChange);
  }, [messages]);

  const sendMessage = async (message: string, useSelectedText: boolean = false) => {
    if (!message.trim()) return;

    setMessages(prev => [...prev, { role: 'user', content: message }]);
    setInput('');
    setIsLoading(true);

    try {
      const chatHistory = messages.slice(-5); // Last 5 messages as context
      const requestBody: any = {
        user_message: message,
        chat_history: chatHistory,
      };
      if (useSelectedText && selectedText) requestBody.selected_text_context = selectedText;

      const response = await fetch(`${FASTAPI_BACKEND_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      let assistantResponse = '';

      // Add empty message for streaming
      setMessages(prev => [...prev, { role: 'assistant', content: '' }]);

      while (true) {
        const { done, value } = await reader!.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n').filter(line => line.startsWith('data: '));
        for (const line of lines) {
          try {
            const parsedData = JSON.parse(line.substring(6));
            if (parsedData.type === 'content') {
              assistantResponse += parsedData.value;
              setMessages(prev => {
                const lastMessage = { ...prev[prev.length - 1] };
                lastMessage.content = assistantResponse;
                return [...prev.slice(0, prev.length - 1), lastMessage];
              });
            } else if (parsedData.type === 'citations') {
              setMessages(prev => {
                const lastMessage = { ...prev[prev.length - 1] };
                lastMessage.content += `\n\n**Citations:**\n${parsedData.value.map((c: any) => `- [${c.chapter} - ${c.section}](${c.url})`).join('\n')}`;
                return [...prev.slice(0, prev.length - 1), lastMessage];
              });
            }
          } catch (e) {
            console.error("SSE parse error:", e, line);
          }
        }
      }
    } catch (error) {
      console.error('Failed to fetch from backend:', error);
      setMessages(prev => [...prev, { role: 'assistant', content: 'Error: Could not connect to the RAG backend.' }]);
    } finally {
      setIsLoading(false);
      setSelectedText(''); // Clear selected text after sending
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !isLoading) sendMessage(input);
  };

  const handleAskSelectedText = () => {
    if (selectedText && !isLoading) {
      sendMessage(input || `Explain this section (from ${location.pathname})`, true);
    }
  };

  return (
    <div className={styles.chatbotContainer}>
      <button className={styles.toggleButton} onClick={() => setIsOpen(!isOpen)}>
        {isOpen ? 'Close Chat' : 'Ask AI Assistant'}
      </button>

      {isOpen && (
        <div className={styles.chatWindow}>
          <div className={styles.messagesContainer}>
            {messages.map((msg, index) => (
              <div key={index} className={`${styles.message} ${styles[msg.role]}`}>
                {msg.content}
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          {selectedText && (
            <div className={styles.selectedTextPrompt}>
              Selected: "{selectedText.substring(0, 50)}"...
              <button onClick={handleAskSelectedText}>Ask about this</button>
            </div>
          )}

          <div className={styles.inputContainer}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask a question..."
              disabled={isLoading}
            />
            <button onClick={() => sendMessage(input)} disabled={isLoading}>Send</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default RAGChatbotWidget;
