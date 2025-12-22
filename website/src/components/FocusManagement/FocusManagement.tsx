import React, { useEffect, useRef } from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

interface FocusManagementProps {
  children: React.ReactNode;
  className?: string;
  autoFocus?: boolean;
  restoreFocus?: boolean;
  focusScope?: boolean;
}

// Focus trap utility for modal dialogs and similar components
const FocusTrap: React.FC<{ children: React.ReactNode, active?: boolean }> = ({ children, active = false }) => {
  const startTrapRef = useRef<HTMLSpanElement>(null);
  const endTrapRef = useRef<HTMLSpanElement>(null);

  useEffect(() => {
    if (!active) return;

    const focusableElements = document.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );

    const firstElement = focusableElements[0] as HTMLElement;
    const lastElement = focusableElements[focusableElements.length - 1] as HTMLElement;

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key !== 'Tab') return;

      if (e.shiftKey && document.activeElement === firstElement) {
        lastElement.focus();
        e.preventDefault();
      } else if (!e.shiftKey && document.activeElement === lastElement) {
        firstElement.focus();
        e.preventDefault();
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [active]);

  return (
    <>
      <span
        ref={startTrapRef}
        tabIndex={0}
        onFocus={() => {
          // Focus back to the last element when tabbing from the start
        }}
        className={styles.focusSentinel}
      />
      {children}
      <span
        ref={endTrapRef}
        tabIndex={0}
        onFocus={() => {
          // Focus back to the first element when tabbing from the end
        }}
        className={styles.focusSentinel}
      />
    </>
  );
};

// Focus management utility component
const FocusManagement: React.FC<FocusManagementProps> = ({
  children,
  className,
  autoFocus = false,
  restoreFocus = false,
  focusScope = false
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const previousActiveElementRef = useRef<HTMLElement | null>(null);

  // Handle auto-focus
  useEffect(() => {
    if (autoFocus && containerRef.current) {
      const focusableElement = containerRef.current.querySelector(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      ) as HTMLElement;

      if (focusableElement) {
        focusableElement.focus();
      }
    }
  }, [autoFocus]);

  // Handle focus restoration
  useEffect(() => {
    if (restoreFocus) {
      previousActiveElementRef.current = document.activeElement as HTMLElement;
    }

    return () => {
      if (restoreFocus && previousActiveElementRef.current) {
        previousActiveElementRef.current.focus();
      }
    };
  }, [restoreFocus]);

  // Handle focus scope (only focusable elements within this component can be focused)
  useEffect(() => {
    if (focusScope) {
      const handleFocusIn = (e: FocusEvent) => {
        if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
          // Redirect focus to the first focusable element in the scope
          const focusableElement = containerRef.current.querySelector(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
          ) as HTMLElement;

          if (focusableElement) {
            focusableElement.focus();
          }
        }
      };

      document.addEventListener('focusin', handleFocusIn);
      return () => document.removeEventListener('focusin', handleFocusIn);
    }
  }, [focusScope]);

  // Keyboard navigation utilities
  const handleKeyDown = (e: React.KeyboardEvent) => {
    // Handle common keyboard navigation patterns
    if (e.key === 'Escape') {
      // Optionally close or dismiss component when ESC is pressed
      if (restoreFocus && previousActiveElementRef.current) {
        previousActiveElementRef.current.focus();
      }
    }
  };

  return (
    <div
      ref={containerRef}
      className={clsx(
        styles.focusManagement,
        { [styles.focusScope]: focusScope },
        className
      )}
      onKeyDown={handleKeyDown}
      tabIndex={focusScope ? -1 : undefined}
      data-focus-management="true"
    >
      {focusScope ? (
        <FocusTrap active={true}>
          {children}
        </FocusTrap>
      ) : (
        children
      )}
    </div>
  );
};

// Keyboard navigation utilities for specific components
const KeyboardNavUtils = {
  // Navigate with arrow keys
  handleArrowNavigation: (
    e: React.KeyboardEvent,
    items: HTMLElement[],
    currentIndex: number,
    setCurrentIndex: (index: number) => void
  ) => {
    if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') {
      e.preventDefault();
      const newIndex = Math.max(0, currentIndex - 1);
      setCurrentIndex(newIndex);
      items[newIndex]?.focus();
    } else if (e.key === 'ArrowDown' || e.key === 'ArrowRight') {
      e.preventDefault();
      const newIndex = Math.min(items.length - 1, currentIndex + 1);
      setCurrentIndex(newIndex);
      items[newIndex]?.focus();
    }
  },

  // Handle Home/End navigation
  handleHomeEnd: (
    e: React.KeyboardEvent,
    items: HTMLElement[],
    setCurrentIndex: (index: number) => void
  ) => {
    if (e.key === 'Home') {
      e.preventDefault();
      setCurrentIndex(0);
      items[0]?.focus();
    } else if (e.key === 'End') {
      e.preventDefault();
      const lastIndex = items.length - 1;
      setCurrentIndex(lastIndex);
      items[lastIndex]?.focus();
    }
  },

  // Handle Page Up/Page Down navigation
  handlePageUpDown: (
    e: React.KeyboardEvent,
    items: HTMLElement[],
    currentIndex: number,
    setCurrentIndex: (index: number) => void,
    pageSize: number = 5
  ) => {
    if (e.key === 'PageUp') {
      e.preventDefault();
      const newIndex = Math.max(0, currentIndex - pageSize);
      setCurrentIndex(newIndex);
      items[newIndex]?.focus();
    } else if (e.key === 'PageDown') {
      e.preventDefault();
      const newIndex = Math.min(items.length - 1, currentIndex + pageSize);
      setCurrentIndex(newIndex);
      items[newIndex]?.focus();
    }
  },

  // Handle Enter/Space activation
  handleActivation: (
    e: React.KeyboardEvent,
    activate: () => void
  ) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      activate();
    }
  }
};

// Export the keyboard navigation utilities separately
export { KeyboardNavUtils };

export default FocusManagement;