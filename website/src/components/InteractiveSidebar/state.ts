import { useState, useEffect } from 'react';
import type { NavigationState, BreadcrumbItem } from '../../types';

// Custom hook for managing navigation state
export const useNavigationState = (initialPath: string = ''): NavigationState => {
  // Initialize state from localStorage if available, otherwise use defaults
  const getInitialState = (): NavigationState => {
    if (typeof window !== 'undefined') {
      const savedState = localStorage.getItem('navigationState');
      if (savedState) {
        try {
          const parsed = JSON.parse(savedState);
          return {
            currentPath: parsed.currentPath || initialPath,
            expandedSections: new Set(parsed.expandedSections || []),
            breadcrumbTrail: parsed.breadcrumbTrail || [],
          };
        } catch (error) {
          console.warn('Failed to parse navigation state from localStorage:', error);
        }
      }
    }

    return {
      currentPath: initialPath,
      expandedSections: new Set<string>(),
      breadcrumbTrail: [],
    };
  };

  const [state, setState] = useState<NavigationState>(getInitialState);

  // Persist state to localStorage whenever it changes
  useEffect(() => {
    if (typeof window !== 'undefined') {
      try {
        const serializableState = {
          currentPath: state.currentPath,
          expandedSections: Array.from(state.expandedSections),
          breadcrumbTrail: state.breadcrumbTrail,
        };
        localStorage.setItem('navigationState', JSON.stringify(serializableState));
      } catch (error) {
        console.warn('Failed to save navigation state to localStorage:', error);
      }
    }
  }, [state]);

  return state;
};

// Hook for updating navigation state
export const useNavigationActions = (setNavigationState: React.Dispatch<React.SetStateAction<NavigationState>>) => {
  return {
    setCurrentPath: (path: string) => {
      setNavigationState(prev => ({
        ...prev,
        currentPath: path,
      }));
    },

    toggleSection: (sectionId: string) => {
      setNavigationState(prev => {
        const newExpandedSections = new Set(prev.expandedSections);
        if (newExpandedSections.has(sectionId)) {
          newExpandedSections.delete(sectionId);
        } else {
          newExpandedSections.add(sectionId);
        }
        return {
          ...prev,
          expandedSections: newExpandedSections,
        };
      });
    },

    expandSection: (sectionId: string) => {
      setNavigationState(prev => {
        const newExpandedSections = new Set(prev.expandedSections);
        newExpandedSections.add(sectionId);
        return {
          ...prev,
          expandedSections: newExpandedSections,
        };
      });
    },

    collapseSection: (sectionId: string) => {
      setNavigationState(prev => {
        const newExpandedSections = new Set(prev.expandedSections);
        newExpandedSections.delete(sectionId);
        return {
          ...prev,
          expandedSections: newExpandedSections,
        };
      });
    },

    setBreadcrumbTrail: (trail: BreadcrumbItem[]) => {
      setNavigationState(prev => ({
        ...prev,
        breadcrumbTrail: trail,
      }));
    },

    addToBreadcrumb: (item: BreadcrumbItem) => {
      setNavigationState(prev => {
        // Remove any existing items that are deeper than the current one
        const filteredTrail = prev.breadcrumbTrail.filter(
          existingItem => existingItem.path !== item.path
        );

        return {
          ...prev,
          breadcrumbTrail: [...filteredTrail, item],
        };
      });
    },

    clearNavigationState: () => {
      setNavigationState({
        currentPath: '',
        expandedSections: new Set(),
        breadcrumbTrail: [],
      });
    },
  };
};

// Helper function to get current path from URL
export const getCurrentPath = (): string => {
  if (typeof window !== 'undefined') {
    return window.location.pathname;
  }
  return '';
};

// Helper function to generate breadcrumbs from path
export const generateBreadcrumbs = (currentPath: string, pathLabels: Record<string, string> = {}): BreadcrumbItem[] => {
  if (!currentPath || currentPath === '/') {
    return [];
  }

  const paths = currentPath.split('/').filter(path => path);
  const breadcrumbs: BreadcrumbItem[] = [];

  for (let i = 0; i < paths.length; i++) {
    const pathSegment = paths.slice(0, i + 1).join('/');
    const fullPath = `/${pathSegment}`;
    const label = pathLabels[fullPath] || paths[i];

    breadcrumbs.push({
      title: label,
      path: fullPath,
      isCurrent: i === paths.length - 1,
    });
  }

  return breadcrumbs;
};

// Helper function to check if a path is active
export const isActivePath = (currentPath: string, targetPath: string): boolean => {
  // Exact match
  if (currentPath === targetPath) {
    return true;
  }

  // Check if current path starts with target path (for nested routes)
  if (currentPath.startsWith(targetPath)) {
    // Ensure it's not a partial match (e.g., /docs/path should not match /docs/pathname)
    const nextChar = currentPath.substring(targetPath.length, targetPath.length + 1);
    if (nextChar === '/' || nextChar === undefined) {
      return true;
    }
  }

  return false;
};

// Context provider for navigation state (if needed for larger applications)
export type NavigationContextType = {
  navigationState: NavigationState;
  actions: ReturnType<typeof useNavigationActions>;
};

// Helper to initialize navigation state from initial props
export const initializeNavigationState = (initialPath: string, initialExpanded: string[] = []): NavigationState => {
  return {
    currentPath: initialPath,
    expandedSections: new Set(initialExpanded),
    breadcrumbTrail: generateBreadcrumbs(initialPath),
  };
};