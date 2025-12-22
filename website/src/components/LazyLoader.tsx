import React, { lazy, Suspense } from 'react';

// Lazy load interactive components with fallback
export const LazyInteractiveSidebar = lazy(() => import('./InteractiveSidebar/InteractiveSidebar'));
export const LazyResponsiveNavbar = lazy(() => import('./ResponsiveNavbar/ResponsiveNavbar'));
export const LazyBreadcrumb = lazy(() => import('./Breadcrumb/Breadcrumb'));
export const LazyExpandableSection = lazy(() => import('./ExpandableSection/ExpandableSection'));
export const LazyInteractiveCodeBlock = lazy(() => import('./InteractiveCodeBlock/InteractiveCodeBlock'));
export const LazyKnowledgeCheck = lazy(() => import('./KnowledgeCheck/KnowledgeCheck'));
export const LazyTabbedInterface = lazy(() => import('./TabbedInterface/TabbedInterface'));

// Wrapper components with suspense fallback
interface LazyComponentWrapperProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

export const InteractiveComponentSuspense: React.FC<LazyComponentWrapperProps> = ({
  children,
  fallback = <div className="loading-placeholder">Loading...</div>
}) => {
  return (
    <Suspense fallback={fallback}>
      {children}
    </Suspense>
  );
};