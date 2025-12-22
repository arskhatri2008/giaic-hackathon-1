import React, { useState, useEffect } from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

interface HighContrastModeProps {
  children: React.ReactNode;
  className?: string;
}

const HighContrastMode: React.FC<HighContrastModeProps> = ({
  children,
  className
}) => {
  const [isHighContrast, setIsHighContrast] = useState(false);

  // Detect high contrast mode preference
  useEffect(() => {
    // Check for high contrast using CSS custom media query
    const highContrastMedia = window.matchMedia('(prefers-contrast: high)');

    // For browsers that don't support prefers-contrast, use alternative detection
    const checkHighContrast = () => {
      // Create a temporary element to test for high contrast mode
      const testElement = document.createElement('div');
      testElement.style.border = '1px solid buttonborder';
      testElement.style.color = 'buttonface';
      testElement.style.fontSize = '0px';
      testElement.style.height = '0px';
      testElement.style.width = '0px';
      testElement.style.position = 'absolute';
      testElement.style.left = '-999px';
      testElement.style.top = '-999px';
      document.body.appendChild(testElement);

      // If the computed styles are different from what we set, we're in high contrast mode
      const computedStyle = window.getComputedStyle(testElement);
      const isHighContrastMode =
        computedStyle.borderTopColor !== computedStyle.borderRightColor ||
        computedStyle.color === computedStyle.backgroundColor ||
        computedStyle.fontSize !== '0px';

      document.body.removeChild(testElement);
      setIsHighContrast(isHighContrastMode);
    };

    // Initial check
    checkHighContrast();

    // Listen for changes in high contrast preference
    const handleChange = (e: MediaQueryListEvent) => {
      setIsHighContrast(e.matches);
    };

    highContrastMedia.addEventListener('change', handleChange);

    // Also check for Windows high contrast mode (fallback)
    const intervalId = setInterval(checkHighContrast, 1000);

    return () => {
      highContrastMedia.removeEventListener('change', handleChange);
      clearInterval(intervalId);
    };
  }, []);

  // Add/remove high contrast class to body element
  useEffect(() => {
    if (isHighContrast) {
      document.body.classList.add(styles.highContrastMode);
    } else {
      document.body.classList.remove(styles.highContrastMode);
    }

    return () => {
      document.body.classList.remove(styles.highContrastMode);
    };
  }, [isHighContrast]);

  return (
    <div
      className={clsx(
        { [styles.highContrastMode]: isHighContrast },
        className
      )}
      data-high-contrast={isHighContrast}
    >
      {children}
    </div>
  );
};

export default HighContrastMode;