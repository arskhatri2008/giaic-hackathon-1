import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

interface ScreenReaderOnlyProps {
  children: React.ReactNode;
  className?: string;
}

interface AriaLiveRegionProps {
  children: React.ReactNode;
  politeness?: 'polite' | 'assertive';
  className?: string;
}

interface SkipLinkProps {
  targetId: string;
  children: React.ReactNode;
  className?: string;
}

interface FocusIndicatorProps {
  children: React.ReactNode;
  className?: string;
}

interface AccessibilityContainerProps {
  children: React.ReactNode;
  skipLinkId?: string;
  skipLinkLabel?: string;
  liveAnnouncement?: string;
  className?: string;
}

// Component to hide content visually but keep it accessible to screen readers
const ScreenReaderOnly: React.FC<ScreenReaderOnlyProps> = ({
  children,
  className
}) => {
  return (
    <span
      className={clsx(
        styles.screenReaderOnly,
        className
      )}
    >
      {children}
    </span>
  );
};

// ARIA live region for announcing dynamic content changes
const AriaLiveRegion: React.FC<AriaLiveRegionProps> = ({
  children,
  politeness = 'polite',
  className
}) => {
  return (
    <div
      className={clsx(
        styles.ariaLiveRegion,
        className
      )}
      aria-live={politeness}
      aria-atomic="true"
    >
      {children}
    </div>
  );
};

// Skip link for keyboard users to bypass navigation
const SkipLink: React.FC<SkipLinkProps> = ({
  targetId,
  children,
  className
}) => {
  const handleClick = (e: React.MouseEvent) => {
    e.preventDefault();
    const targetElement = document.getElementById(targetId);
    if (targetElement) {
      targetElement.focus();
      targetElement.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      const targetElement = document.getElementById(targetId);
      if (targetElement) {
        targetElement.focus();
        targetElement.scrollIntoView({ behavior: 'smooth' });
      }
    }
  };

  return (
    <a
      href={`#${targetId}`}
      onClick={handleClick}
      onKeyDown={handleKeyDown}
      className={clsx(
        styles.skipLink,
        className
      )}
      aria-label="Skip to main content"
    >
      {children}
    </a>
  );
};

// Component to enhance focus indicators for better visibility
const FocusIndicator: React.FC<FocusIndicatorProps> = ({
  children,
  className
}) => {
  return (
    <div
      className={clsx(
        styles.focusIndicatorWrapper,
        className
      )}
    >
      {children}
    </div>
  );
};

// Utility component that combines multiple accessibility features
const AccessibilityContainer: React.FC<AccessibilityContainerProps> = ({
  children,
  skipLinkId,
  skipLinkLabel = 'Skip to main content',
  liveAnnouncement,
  className
}) => {
  return (
    <div className={clsx(styles.accessibilityContainer, className)}>
      {skipLinkId && (
        <SkipLink
          targetId={skipLinkId}
          className={styles.skipLink}
        >
          {skipLinkLabel}
        </SkipLink>
      )}

      {liveAnnouncement && (
        <AriaLiveRegion politeness="polite">
          {liveAnnouncement}
        </AriaLiveRegion>
      )}

      <div className={styles.contentArea}>
        {children}
      </div>
    </div>
  );
};

// Export individual components and the container
export {
  ScreenReaderOnly,
  AriaLiveRegion,
  SkipLink,
  FocusIndicator
};

export default AccessibilityContainer;