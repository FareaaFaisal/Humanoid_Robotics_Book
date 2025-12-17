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

  const FASTAPI_BACKEND_URL = "https://fareaafaisal-rag-final.hf.space";

  // ------------------- Scroll & selection handler -------------------
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });

    const handleSelectionChange = () => {
      const selection = window.getSelection();
      setSelectedText(selection ? selection.toString() : '');
    };

    document.addEventListener('selectionchange', handleSelectionChange);
    return () => document.removeEventListener('selectionchange', handleSelectionChange);
  }, [messages]);

  // ------------------- Backend error handling -------------------
  const handleBackendError = async (errorMessage: string) => {
    console.warn("Backend connection failed:", errorMessage);
    setMessages(prev => [
      ...prev,
      { role: 'assistant', content: "Error: Cannot reach RAG backend. Please try again later." }
    ]);
    setIsLoading(false);
  };

  // ------------------- Send message -------------------
  const sendMessage = async (message: string, useSelectedText: boolean = false) => {
    if (!message.trim()) return;

    const newUserMessage = { role: 'user', content: message };
    setMessages(prev => [...prev, newUserMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const requestBody: any = {
        user_message: message,
        chat_history: messages.slice(-5),
        ...(useSelectedText && selectedText && { selected_text_context: selectedText }),
      };

      const response = await fetch(`${FASTAPI_BACKEND_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      let assistantResponse = '';
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
              setMessages(prev => [
                ...prev.slice(0, -1),
                { role: 'assistant', content: assistantResponse }
              ]);

            } else if (parsedData.type === 'citations') {
              setMessages(prev => {
                const lastMessage = { ...prev[prev.length - 1] };
                const formattedCitations = parsedData.value.map((c: any) => {
                  const title = c.chapter_title?.trim();
                  if (title) return `- [${title}](${c.url})`;
                  return `- ${c.url}`; // show URL if no title
                }).join('\n');
                lastMessage.content += formattedCitations ? `\n\n**Citations:**\n${formattedCitations}` : '';
                return [...prev.slice(0, -1), lastMessage];
              });

            } else if (parsedData.type === 'done') {
              setIsLoading(false); // unlock input

            } else if (parsedData.type === 'error') {
              console.error("Error from backend:", parsedData.value);
              setIsLoading(false);
            }
          } catch (e) {
            console.error("SSE parse error:", e, line);
          }
        }
      }

    } catch (error) {
      await handleBackendError(error.message);
    } finally {
      setSelectedText('');
    }
  };

  // ------------------- Input handlers -------------------
  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !isLoading) sendMessage(input);
  };

  const handleAskSelectedText = () => {
    if (selectedText && !isLoading) sendMessage(input || `Explain this selection`, true);
  };

  // ------------------- Render -------------------
  return (
    <div className={styles.chatbotContainer}>
      <button className={styles.toggleButton} onClick={() => setIsOpen(!isOpen)}>
        {isOpen ? 'Close' : 'Ask AI Assistant'}
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
            <button onClick={() => sendMessage(input)} disabled={isLoading}>
              {isLoading ? "Thinking..." : "Send"}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default RAGChatbotWidget;
