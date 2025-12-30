import React, { useState, useEffect } from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import { useLocation } from '@docusaurus/router';
import Chatbot from '@site/src/components/Chatbot/Chatbot';
import OriginalLayout from '@theme-original/Layout';

const LayoutWrapper = (props) => {
  const [isVisible, setIsVisible] = useState(false);
  const [isClient, setIsClient] = useState(false);
  const location = useLocation();

  // Toggle chatbot visibility
  const toggleChatbot = () => {
    setIsVisible(!isVisible);
  };

  // Close chatbot when navigating to a new page
  useEffect(() => {
    setIsVisible(false);
  }, [location.pathname]);

  // Mark as client-side after mount
  useEffect(() => {
    setIsClient(true);
  }, []);

  // Create the chatbot button after component mounts
  useEffect(() => {
    if (typeof document !== 'undefined' && typeof window !== 'undefined' && isClient) {
      // Check if button already exists to avoid duplicates
      let toggleButton = document.getElementById('chatbot-toggle-btn');
      if (!toggleButton) {
        // Create the toggle button
        toggleButton = document.createElement('button');
        toggleButton.id = 'chatbot-toggle-btn';
        toggleButton.innerHTML = '🤖';
        toggleButton.style.position = 'fixed';
        toggleButton.style.bottom = '20px';
        toggleButton.style.right = '20px';
        toggleButton.style.width = '60px';
        toggleButton.style.height = '60px';
        toggleButton.style.borderRadius = '50%';
        toggleButton.style.backgroundColor = '#2e8555'; /* Primary theme color */
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

        // Add responsive styles via CSS rules
        const style = document.createElement('style');
        style.textContent = `
          @media (max-width: 768px) {
            #chatbot-toggle-btn {
              bottom: 15px !important;
              right: 15px !important;
              width: 50px !important;
              height: 50px !important;
              font-size: 20px !important;
            }
          }
          @media (max-width: 480px) {
            #chatbot-toggle-btn {
              bottom: 10px !important;
              right: 10px !important;
              width: 45px !important;
              height: 45px !important;
              font-size: 18px !important;
            }
          }
        `;
        document.head.appendChild(style);
      }

      // Cleanup function to remove elements when component unmounts
      return () => {
        const existingButton = document.getElementById('chatbot-toggle-btn');
        if (existingButton && existingButton.parentNode) {
          existingButton.parentNode.removeChild(existingButton);
        }
        // Remove the added styles
        const styles = document.querySelectorAll('style');
        styles.forEach(s => {
          if (s.textContent && s.textContent.includes('#chatbot-toggle-btn')) {
            s.remove();
          }
        });
      };
    }
  }, [isClient]);

  return (
    <>
      <OriginalLayout {...props} />
      {isClient && isVisible && (
        <BrowserOnly fallback={<div style={{ display: 'none' }} />}>
          {() => (
            <div style={{
              position: 'fixed',
              bottom: '90px',
              right: '20px',
              width: 'min(90%, 400px)', // Responsive width - up to 90% of screen or max 400px
              height: 'min(60vh, 500px)', // Responsive height - up to 60% of viewport or max 500px
              zIndex: '1000',
              boxShadow: '0 10px 25px rgba(0,0,0,0.2)',
              borderRadius: '12px',
              backgroundColor: 'white',
              display: 'flex',
              flexDirection: 'column'
            }}>
              <div style={{
                padding: '12px',
                backgroundColor: '#2e8555', /* Primary theme color */
                color: 'white',
                borderTopLeftRadius: '12px',
                borderTopRightRadius: '12px',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
              }}>
                <h3 style={{ margin: 0, fontSize: '16px', color: 'white' }}>RAG Assistant</h3>
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
                <Chatbot />
              </div>
            </div>
          )}
        </BrowserOnly>
      )}
    </>
  );
};

export default LayoutWrapper;