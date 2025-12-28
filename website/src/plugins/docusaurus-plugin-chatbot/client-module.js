import React, { useState, useEffect } from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import { useLocation } from '@docusaurus/router';
import Chatbot from '@site/src/components/Chatbot/Chatbot';

const ChatbotInjector = () => {
  const [isVisible, setIsVisible] = useState(false);
  const location = useLocation();

  // Toggle chatbot visibility
  const toggleChatbot = () => {
    setIsVisible(!isVisible);
  };

  // Close chatbot when navigating to a new page
  useEffect(() => {
    setIsVisible(false);
  }, [location.pathname]);

  // Create the chatbot button after component mounts
  useEffect(() => {
    if (typeof document !== 'undefined' && typeof window !== 'undefined') {
      // Create the toggle button
      const toggleButton = document.createElement('button');
      toggleButton.id = 'chatbot-toggle-btn';
      toggleButton.innerHTML = '🤖';
      toggleButton.style.position = 'fixed';
      toggleButton.style.bottom = '20px';
      toggleButton.style.right = '20px';
      toggleButton.style.width = '60px';
      toggleButton.style.height = '60px';
      toggleButton.style.borderRadius = '50%';
      toggleButton.style.backgroundColor = '#4f46e5';
      toggleButton.style.color = 'white';
      toggleButton.style.fontSize = '24px';
      toggleButton.style.border = 'none';
      toggleButton.style.cursor = 'pointer';
      toggleButton.style.zIndex = '1000';
      toggleButton.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
      toggleButton.style.display = 'flex';
      toggleButton.style.alignItems = 'center';
      toggleButton.style.justifyContent = 'center';
      toggleButton.onclick = toggleChatbot;

      // Add button to DOM
      document.body.appendChild(toggleButton);

      // Cleanup function to remove elements when component unmounts
      return () => {
        if (toggleButton.parentNode) {
          toggleButton.parentNode.removeChild(toggleButton);
        }
      };
    }
  }, []);

  return isVisible ? (
    <BrowserOnly fallback={<div style={{ display: 'none' }} />}>
      {() => {
        try {
          const ChatbotComponent = require('@site/src/components/Chatbot/Chatbot').default;
          return (
            <div style={{
              position: 'fixed',
              bottom: '90px',
              right: '20px',
              width: '400px',
              height: '500px',
              zIndex: '1000',
              boxShadow: '0 10px 25px rgba(0,0,0,0.2)',
              borderRadius: '12px',
              backgroundColor: 'white',
              display: 'flex',
              flexDirection: 'column'
            }}>
              <div style={{
                padding: '12px',
                backgroundColor: '#4f46e5',
                color: 'white',
                borderTopLeftRadius: '12px',
                borderTopRightRadius: '12px',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
              }}>
                <h3 style={{ margin: 0, fontSize: '16px' }}>RAG Assistant</h3>
                <button
                  onClick={() => setIsVisible(false)}
                  style={{
                    background: 'none',
                    border: 'none',
                    color: 'white',
                    fontSize: '20px',
                    cursor: 'pointer',
                    padding: '0',
                    width: '24px',
                    height: '24px'
                  }}
                  aria-label="Close chatbot"
                >
                  ×
                </button>
              </div>
              <div style={{ flex: 1, overflow: 'hidden' }}>
                <ChatbotComponent />
              </div>
            </div>
          );
        } catch (error) {
          console.error('Error loading Chatbot component:', error);
          return null;
        }
      }}
    </BrowserOnly>
  ) : null;
};

export default ChatbotInjector;