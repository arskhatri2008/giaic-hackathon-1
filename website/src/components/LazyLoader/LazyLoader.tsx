import React, { useState, useEffect, useRef } from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

interface LazyLoaderProps {
  children: React.ReactNode;
  className?: string;
  fallback?: React.ReactNode;
  threshold?: number;
  rootMargin?: string;
  delay?: number; // Delay in milliseconds before showing content after intersection
}

const LazyLoader: React.FC<LazyLoaderProps> = ({
  children,
  className,
  fallback = <div className={styles.lazyLoaderFallback}>Loading...</div>,
  threshold = 0.1,
  rootMargin = '0px',
  delay = 0
}) => {
  const [isVisible, setIsVisible] = useState(false);
  const [showContent, setShowContent] = useState(false);
  const elementRef = useRef<HTMLDivElement>(null);
  const observerRef = useRef<IntersectionObserver | null>(null);
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    const element = elementRef.current;
    if (!element) return;

    // If Intersection Observer is not supported, show content immediately
    if (!window.IntersectionObserver) {
      setIsVisible(true);
      setShowContent(true);
      return;
    }

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);

          // If there's a delay, wait before showing the content
          if (delay > 0) {
            timeoutRef.current = setTimeout(() => {
              setShowContent(true);
            }, delay);
          } else {
            setShowContent(true);
          }

          // Disconnect after first intersection
          observer.unobserve(element);
          observer.disconnect();
        }
      },
      {
        threshold,
        rootMargin
      }
    );

    observerRef.current = observer;
    observer.observe(element);

    return () => {
      if (observerRef.current) {
        observerRef.current.disconnect();
      }
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, [threshold, rootMargin, delay]);

  return (
    <div
      ref={elementRef}
      className={clsx(
        styles.lazyLoader,
        { [styles.visible]: showContent },
        className
      )}
      data-is-visible={showContent}
    >
      {showContent ? children : fallback}
    </div>
  );
};

export default LazyLoader;