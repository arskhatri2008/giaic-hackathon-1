import React, { useState } from 'react';
import './ChatInput.css';

const ChatInput = ({ onSendMessage, isLoading }) => {
  const [inputText, setInputText] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputText.trim() && !isLoading) {
      onSendMessage(inputText);
      setInputText('');
    }
  };

  return (
    <form className="chat-input-form" onSubmit={handleSubmit}>
      <input
        type="text"
        className="chat-input"
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
        placeholder={isLoading ? "Processing..." : "Type your message here..."}
        disabled={isLoading}
      />
      <button
        type="submit"
        className="chat-send-button"
        disabled={isLoading || !inputText.trim()}
      >
        Send
      </button>
    </form>
  );
};

export default ChatInput;