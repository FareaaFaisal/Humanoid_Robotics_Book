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

  const FASTAPI_BACKEND_URL = "http://localhost:8000";


  // --- Fallback Configuration ---
  // WARNING: Exposing API keys on the client-side is a security risk.
  // This is for demonstration/fallback purposes only.
  const GEMINI_API_KEY = "";
  const GEMINI_MODEL_NAME = "gemini-1.5-flash-latest";

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    const handleSelectionChange = () => {
      const selection = window.getSelection();
      setSelectedText(selection ? selection.toString() : '');
    };
    document.addEventListener('selectionchange', handleSelectionChange);
    return () => document.removeEventListener('selectionchange', handleSelectionChange);
  }, [messages]);

  const handleBackendError = async (errorMessage: string) => {
    console.warn("Backend connection failed. Using client-side LLM fallback.", errorMessage);
    
    if (!GEMINI_API_KEY || GEMINI_API_KEY === "YOUR_GEMINI_API_KEY_HERE") {
        setMessages(prev => [...prev, { role: 'assistant', content: "Error: RAG backend not connected and no fallback API key is configured." }]);
        return;
    }

    const system_prompt = "You are a helpful assistant for the 'Physical AI & Humanoid Robotics' book. Answer the following question based on your general knowledge. If you don't know the answer, simply say 'I don't know.'";
    const user_prompt = `Question: ${messages[messages.length - 1].content}`;

    try {
        const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_MODEL_NAME}:generateContent?key=${GEMINI_API_KEY}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                contents: [{ parts: [{ text: `${system_prompt}\n\n${user_prompt}` }] }]
            }),
        });

        if (!response.ok) throw new Error(`Google API error! status: ${response.status}`);
        const data = await response.json();
        const fallbackContent = data.candidates[0]?.content?.parts[0]?.text || "I don't know the answer to that.";
        setMessages(prev => [...prev, { role: 'assistant', content: fallbackContent }]);
    } catch (fallbackError) {
        console.error("Fallback LLM call failed:", fallbackError);
        setMessages(prev => [...prev, { role: 'assistant', content: "I'm having trouble connecting to all my systems. Please try again later." }]);
    }
  };

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
                  setMessages(prev => [...prev.slice(0, -1), { role: 'assistant', content: assistantResponse }]);
                } else if (parsedData.type === 'citations') {
                  setMessages(prev => {
                      const lastMessage = { ...prev[prev.length - 1] };
                      lastMessage.content += `\n\n**Citations:**\n${parsedData.value.map((c: any) => `- [${c.chapter}](${c.url})`).join('\n')}`;
                      return [...prev.slice(0, -1), lastMessage];
                  });
                }
            } catch (e) { console.error("SSE parse error:", e, line); }
        }
      }
    } catch (error) {
      await handleBackendError(error.message);
    } finally {
      setIsLoading(false);
      setSelectedText('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !isLoading) sendMessage(input);
  };
  
  const handleAskSelectedText = () => {
    if (selectedText && !isLoading) sendMessage(input || `Explain this selection`, true);
  };

  return (
    <div className={styles.chatbotContainer}>
      <button className={styles.toggleButton} onClick={() => setIsOpen(!isOpen)}>
        {isOpen ? 'Close' : 'Ask AI Assistant'}
      </button>

      {isOpen && (
        <div className={styles.chatWindow}>
          <div className={styles.messagesContainer}>
            {messages.map((msg, index) => (
              <div key={index} className={`${styles.message} ${styles[msg.role]}`}>{msg.content}</div>
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
            <input type="text" value={input} onChange={(e) => setInput(e.target.value)} onKeyPress={handleKeyPress} placeholder="Ask a question..." disabled={isLoading} />
            <button onClick={() => sendMessage(input)} disabled={isLoading}>Send</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default RAGChatbotWidget;