import React, { useState, useEffect, useRef } from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

interface InteractiveCodeBlockProps {
  code: string;
  language?: string;
  showLineNumbers?: boolean;
  title?: string;
  className?: string;
  onCopy?: (success: boolean) => void;
}

const InteractiveCodeBlock: React.FC<InteractiveCodeBlockProps> = ({
  code,
  language = 'text',
  showLineNumbers = false,
  title,
  className,
  onCopy
}) => {
  const [copied, setCopied] = useState(false);
  const [lineCount, setLineCount] = useState(0);
  const codeRef = useRef<HTMLElement>(null);

  // Calculate line count for line numbers
  useEffect(() => {
    const lines = code.split('\n');
    setLineCount(lines.length);
  }, [code]);

  // Handle copying code to clipboard
  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);

      // Reset copied state after 2 seconds
      setTimeout(() => {
        setCopied(false);
      }, 2000);

      if (onCopy) {
        onCopy(true);
      }
    } catch (err) {
      console.error('Failed to copy code:', err);
      if (onCopy) {
        onCopy(false);
      }
    }
  };

  // Generate line numbers
  const renderLineNumbers = () => {
    const lineNumbers = [];
    for (let i = 1; i <= lineCount; i++) {
      lineNumbers.push(
        <div key={i} className={styles.lineNumber}>
          {i}
        </div>
      );
    }
    return lineNumbers;
  };

  return (
    <figure
      className={clsx(
        styles.interactiveCodeBlock,
        { [styles.withTitle]: !!title },
        className
      )}
      role="region"
      aria-label={`Code block${title ? `: ${title}` : ''}`}
    >
      {title && (
        <figcaption className={styles.codeTitle}>
          {title}
        </figcaption>
      )}
      <div className={styles.codeContainer}>
        {showLineNumbers && (
          <div className={styles.lineNumbers} aria-hidden="true">
            {renderLineNumbers()}
          </div>
        )}
        <pre
          className={clsx(
            styles.codePre,
            `language-${language}`
          )}
        >
          <code
            ref={codeRef}
            className={clsx(
              styles.codeBlock,
              `language-${language}`
            )}
          >
            {code}
          </code>
        </pre>
        <button
          className={styles.copyButton}
          onClick={copyToClipboard}
          onKeyDown={(e) => {
            if (e.key === 'Enter' || e.key === ' ') {
              e.preventDefault();
              copyToClipboard();
            }
          }}
          aria-label={copied ? 'Code copied to clipboard' : 'Copy code to clipboard'}
          type="button"
          tabIndex={0}
        >
          {copied ? '✓ Copied!' : 'Copy'}
        </button>
      </div>
    </figure>
  );
};

const MemoizedInteractiveCodeBlock = React.memo(InteractiveCodeBlock);
export default MemoizedInteractiveCodeBlock;