import React from 'react';
import ErrorBoundary from './ErrorBoundary';

// Higher-order component to wrap interactive components with error boundaries
export const withErrorBoundary = (
  Component: React.ComponentType<any>,
  fallback?: React.ReactNode,
  onError?: (error: Error, errorInfo: React.ErrorInfo) => void
) => {
  return (props: any) => (
    <ErrorBoundary fallback={fallback} onError={onError}>
      <Component {...props} />
    </ErrorBoundary>
  );
};

// Wrapper for interactive components with default error handling
export const InteractiveComponentWithErrorBoundary: React.FC<{
  children: React.ReactNode;
  fallback?: React.ReactNode;
}> = ({ children, fallback }) => {
  return (
    <ErrorBoundary
      fallback={fallback || (
        <div className="error-boundary" role="alert">
          <h3>Interactive component failed to load</h3>
          <p>This interactive element could not be displayed. Please refresh the page.</p>
        </div>
      )}
    >
      {children}
    </ErrorBoundary>
  );
};