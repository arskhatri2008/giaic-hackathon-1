import React from 'react';
import './ChatMessage.css';

const ChatMessage = ({ message, isTyping = false }) => {
  const isUser = message.sender === 'user';

  return (
    <div className={`message-container ${isUser ? 'user-message' : 'bot-message'}`}>
      <div className={`message ${isUser ? 'user' : 'bot'}`}>
        <div className="message-content">
          {isTyping ? (
            <div className="typing-indicator">
              <div className="typing-dot"></div>
              <div className="typing-dot"></div>
              <div className="typing-dot"></div>
            </div>
          ) : (
            <>
              <p>{message.text}</p>
              {message.sources && message.sources.length > 0 && (
                <div className="sources">
                  <h4>Sources:</h4>
                  <ul>
                    {message.sources.map((source, index) => (
                      <li key={index}>
                        <a href={source.url} target="_blank" rel="noopener noreferrer">
                          {source.title}
                        </a>
                        <span className="relevance">({(source.relevance_score * 100).toFixed(1)}%)</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChatMessage;