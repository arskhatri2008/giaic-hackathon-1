import React, { useState, useEffect, useRef } from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

interface PerformanceMetrics {
  componentLoadTime: number;
  renderTime: number;
  memoryUsage?: number;
  domSize?: number;
  firstContentfulPaint?: number;
  largestContentfulPaint?: number;
}

interface PerformanceMonitorProps {
  children: React.ReactNode;
  componentName?: string;
  onMetrics?: (metrics: PerformanceMetrics) => void;
  className?: string;
  enabled?: boolean; // Whether to actively monitor performance
}

const PerformanceMonitor: React.FC<PerformanceMonitorProps> = ({
  children,
  componentName = 'UnknownComponent',
  onMetrics,
  className,
  enabled = true
}) => {
  const [metrics, setMetrics] = useState<PerformanceMetrics | null>(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const componentRef = useRef<HTMLDivElement>(null);
  const startTimeRef = useRef<number>(0);

  // Measure component performance
  useEffect(() => {
    if (!enabled) return;

    // Record start time
    startTimeRef.current = performance.now();

    // Monitor memory usage if available
    const getMemoryUsage = () => {
      // @ts-ignore - memory property is not always available
      if (performance.memory) {
        // @ts-ignore
        return performance.memory.usedJSHeapSize;
      }
      return undefined;
    };

    // Monitor DOM size
    const getDOMSize = () => {
      if (componentRef.current) {
        return componentRef.current.querySelectorAll('*').length;
      }
      return undefined;
    };

    // Capture initial metrics after component mounts
    const initialMemory = getMemoryUsage();
    const initialDOMSize = getDOMSize();

    // Wait for next tick to measure render time
    const renderTimer = setTimeout(() => {
      const renderTime = performance.now() - startTimeRef.current;
      const finalMemory = getMemoryUsage();
      const finalDOMSize = getDOMSize();

      const componentMetrics: PerformanceMetrics = {
        componentLoadTime: renderTime,
        renderTime,
        memoryUsage: finalMemory ? finalMemory - (initialMemory || 0) : undefined,
        domSize: finalDOMSize,
        firstContentfulPaint: undefined, // Would need PerformanceObserver to measure this
        largestContentfulPaint: undefined // Would need PerformanceObserver to measure this
      };

      setMetrics(componentMetrics);
      setIsLoaded(true);

      // Report metrics if callback is provided
      if (onMetrics) {
        onMetrics(componentMetrics);
      }

      // Log performance metrics to console in development
      if (process.env.NODE_ENV === 'development') {
        console.group(`Performance Metrics: ${componentName}`);
        console.log(`Load Time: ${renderTime.toFixed(2)}ms`);
        if (finalMemory && initialMemory) {
          console.log(`Memory Change: ${(finalMemory - initialMemory) / 1024 / 1024} MB`);
        }
        if (finalDOMSize) {
          console.log(`DOM Elements: ${finalDOMSize}`);
        }
        console.groupEnd();
      }
    }, 0);

    return () => {
      clearTimeout(renderTimer);
    };
  }, [enabled, componentName, onMetrics]);

  // Monitor for performance observer events (if supported)
  useEffect(() => {
    if (!enabled || !window.PerformanceObserver) return;

    const observer = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        if (entry.entryType === 'paint' && componentRef.current) {
          const element = componentRef.current;

          // Update metrics with paint timing if this component caused the paint
          if (metrics && element.contains(document.elementFromPoint(100, 100))) {
            setMetrics(prev => ({
              ...prev!,
              ...(entry.name === 'first-contentful-paint' && { firstContentfulPaint: entry.startTime }),
              ...(entry.name === 'largest-contentful-paint' && { largestContentfulPaint: entry.startTime })
            }));
          }
        }
      }
    });

    try {
      observer.observe({ entryTypes: ['paint', 'largest-contentful-paint'] });
    } catch (e) {
      // Some browsers may not support certain entry types
      observer.observe({ entryTypes: ['paint'] });
    }

    return () => {
      observer.disconnect();
    };
  }, [enabled, metrics]);

  return (
    <div
      ref={componentRef}
      className={clsx(
        styles.performanceMonitor,
        { [styles.loaded]: isLoaded },
        className
      )}
      data-component={componentName}
      data-performance-measured={enabled}
    >
      {children}

      {enabled && process.env.NODE_ENV === 'development' && metrics && (
        <div className={styles.performanceMetricsOverlay}>
          <div className={styles.metricItem}>
            <span className={styles.metricLabel}>Load Time:</span>
            <span className={styles.metricValue}>{metrics.renderTime.toFixed(2)}ms</span>
          </div>
          {metrics.memoryUsage && (
            <div className={styles.metricItem}>
              <span className={styles.metricLabel}>Memory Change:</span>
              <span className={styles.metricValue}>{(metrics.memoryUsage / 1024 / 1024).toFixed(2)}MB</span>
            </div>
          )}
          {metrics.domSize && (
            <div className={styles.metricItem}>
              <span className={styles.metricLabel}>DOM Elements:</span>
              <span className={styles.metricValue}>{metrics.domSize}</span>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default PerformanceMonitor;