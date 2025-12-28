import React, { useState, useEffect, useRef } from 'react';
import ErrorBoundary from './ErrorBoundary';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import { queryAPI, healthAPI } from '../../services/api';
import './Chatbot.css';

const Chatbot = () => {
  const [messages, setMessages] = useState([
    { id: 1, text: "Hello! I'm your RAG assistant. How can I help you today?", sender: 'bot' }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (text) => {
    if (!text.trim() || isLoading) return;

    // Add user message
    const userMessage = {
      id: Date.now(),
      text: text,
      sender: 'user'
    };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // Call the backend API
      const response = await queryAPI({ query: text });

      // Add bot response
      const botMessage = {
        id: Date.now() + 1,
        text: response.response,
        sender: 'bot',
        sources: response.sources || []
      };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      // Add error message
      const errorMessage = {
        id: Date.now() + 1,
        text: "Sorry, I encountered an error processing your request. Please try again.",
        sender: 'bot'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <ErrorBoundary>
      <div className="chatbot-container">
        <div className="chatbot-header">
          <h3>RAG Assistant</h3>
        </div>
        <div className="chatbot-messages">
          {messages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))}
          {isLoading && <ChatMessage message={{ id: 'loading', text: 'Thinking...', sender: 'bot' }} isTyping={true} />}
          <div ref={messagesEndRef} />
        </div>
        <div className="chatbot-input">
          <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
        </div>
      </div>
    </ErrorBoundary>
  );
};

export default Chatbot;