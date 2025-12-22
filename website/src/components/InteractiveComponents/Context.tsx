import React, { createContext, useContext, useReducer, ReactNode } from 'react';
import { UIState, NavigationState, BreadcrumbItem } from '../../types';

// Define the context state type
interface InteractiveContextType {
  uiState: UIState;
  navigationState: NavigationState;
  dispatch: React.Dispatch<InteractiveContextAction>;
}

// Define action types for state management
type InteractiveContextAction =
  | { type: 'SET_SIDEBAR_COLLAPSED'; payload: boolean }
  | { type: 'SET_THEME'; payload: 'light' | 'dark' | 'auto' }
  | { type: 'SET_MOBILE_MENU_OPEN'; payload: boolean }
  | { type: 'SET_CURRENT_BREAKPOINT'; payload: 'mobile' | 'tablet' | 'desktop' }
  | { type: 'SET_CURRENT_PATH'; payload: string }
  | { type: 'TOGGLE_SECTION'; payload: string }
  | { type: 'EXPAND_SECTION'; payload: string }
  | { type: 'COLLAPSE_SECTION'; payload: string }
  | { type: 'SET_BREADCRUMB_TRAIL'; payload: BreadcrumbItem[] }
  | { type: 'ADD_TO_BREADCRUMB'; payload: BreadcrumbItem }
  | { type: 'CLEAR_NAVIGATION_STATE' }
  | { type: 'SET_LANGUAGE'; payload: string }
  | { type: 'SET_ACCESSIBILITY_MODE'; payload: boolean };

// Initial state
const initialState: {
  uiState: UIState;
  navigationState: NavigationState;
} = {
  uiState: {
    sidebarCollapsed: false,
    theme: 'auto',
    mobileMenuOpen: false,
    currentBreakpoint: 'desktop',
    language: 'en',
    accessibilityMode: false,
  },
  navigationState: {
    currentPath: '',
    expandedSections: [],
    breadcrumbTrail: [],
  },
};

// Reducer function to handle state updates
const interactiveContextReducer = (
  state: typeof initialState,
  action: InteractiveContextAction
): typeof initialState => {
  switch (action.type) {
    case 'SET_SIDEBAR_COLLAPSED':
      return {
        ...state,
        uiState: {
          ...state.uiState,
          sidebarCollapsed: action.payload,
        },
      };

    case 'SET_THEME':
      return {
        ...state,
        uiState: {
          ...state.uiState,
          theme: action.payload,
        },
      };

    case 'SET_MOBILE_MENU_OPEN':
      return {
        ...state,
        uiState: {
          ...state.uiState,
          mobileMenuOpen: action.payload,
        },
      };

    case 'SET_CURRENT_BREAKPOINT':
      return {
        ...state,
        uiState: {
          ...state.uiState,
          currentBreakpoint: action.payload,
        },
      };

    case 'SET_CURRENT_PATH':
      return {
        ...state,
        navigationState: {
          ...state.navigationState,
          currentPath: action.payload,
        },
      };

    case 'TOGGLE_SECTION':
      const sectionId = action.payload;
      const isCurrentlyExpanded = state.navigationState.expandedSections.includes(sectionId);
      const newExpandedSections = isCurrentlyExpanded
        ? state.navigationState.expandedSections.filter(id => id !== sectionId)
        : [...state.navigationState.expandedSections, sectionId];

      return {
        ...state,
        navigationState: {
          ...state.navigationState,
          expandedSections: newExpandedSections,
        },
      };

    case 'EXPAND_SECTION':
      if (!state.navigationState.expandedSections.includes(action.payload)) {
        return {
          ...state,
          navigationState: {
            ...state.navigationState,
            expandedSections: [...state.navigationState.expandedSections, action.payload],
          },
        };
      }
      return state;

    case 'COLLAPSE_SECTION':
      return {
        ...state,
        navigationState: {
          ...state.navigationState,
          expandedSections: state.navigationState.expandedSections.filter(id => id !== action.payload),
        },
      };

    case 'SET_BREADCRUMB_TRAIL':
      return {
        ...state,
        navigationState: {
          ...state.navigationState,
          breadcrumbTrail: action.payload,
        },
      };

    case 'ADD_TO_BREADCRUMB':
      const existingIndex = state.navigationState.breadcrumbTrail.findIndex(
        item => item.path === action.payload.path
      );

      if (existingIndex >= 0) {
        // Update existing breadcrumb
        const updatedTrail = [...state.navigationState.breadcrumbTrail];
        updatedTrail[existingIndex] = action.payload;
        return {
          ...state,
          navigationState: {
            ...state.navigationState,
            breadcrumbTrail: updatedTrail,
          },
        };
      } else {
        // Add new breadcrumb
        return {
          ...state,
          navigationState: {
            ...state.navigationState,
            breadcrumbTrail: [...state.navigationState.breadcrumbTrail, action.payload],
          },
        };
      }

    case 'CLEAR_NAVIGATION_STATE':
      return {
        ...state,
        navigationState: {
          currentPath: '',
          expandedSections: [],
          breadcrumbTrail: [],
        },
      };

    case 'SET_LANGUAGE':
      return {
        ...state,
        uiState: {
          ...state.uiState,
          language: action.payload,
        },
      };

    case 'SET_ACCESSIBILITY_MODE':
      return {
        ...state,
        uiState: {
          ...state.uiState,
          accessibilityMode: action.payload,
        },
      };

    default:
      return state;
  }
};

// Create the context
const InteractiveContext = createContext<InteractiveContextType | undefined>(undefined);

// Provider component
interface InteractiveContextProviderProps {
  children: ReactNode;
  initialUiState?: Partial<UIState>;
  initialNavigationState?: Partial<NavigationState>;
}

export const InteractiveContextProvider: React.FC<InteractiveContextProviderProps> = ({
  children,
  initialUiState = {},
  initialNavigationState = {},
}) => {
  const [state, dispatch] = useReducer(interactiveContextReducer, {
    uiState: { ...initialState.uiState, ...initialUiState },
    navigationState: { ...initialState.navigationState, ...initialNavigationState },
  });

  const contextValue = {
    uiState: state.uiState,
    navigationState: state.navigationState,
    dispatch,
  };

  return (
    <InteractiveContext.Provider value={contextValue}>
      {children}
    </InteractiveContext.Provider>
  );
};

// Custom hook to use the context
export const useInteractiveContext = (): InteractiveContextType => {
  const context = useContext(InteractiveContext);
  if (context === undefined) {
    throw new Error('useInteractiveContext must be used within an InteractiveContextProvider');
  }
  return context;
};

// Helper functions for common actions
export const useInteractiveActions = () => {
  const { dispatch } = useInteractiveContext();

  return {
    toggleSidebar: () => dispatch({ type: 'SET_SIDEBAR_COLLAPSED', payload: !useInteractiveContext().uiState.sidebarCollapsed }),
    setTheme: (theme: 'light' | 'dark' | 'auto') => dispatch({ type: 'SET_THEME', payload: theme }),
    toggleMobileMenu: () => dispatch({ type: 'SET_MOBILE_MENU_OPEN', payload: !useInteractiveContext().uiState.mobileMenuOpen }),
    setCurrentBreakpoint: (breakpoint: 'mobile' | 'tablet' | 'desktop') => dispatch({ type: 'SET_CURRENT_BREAKPOINT', payload: breakpoint }),
    setCurrentPath: (path: string) => dispatch({ type: 'SET_CURRENT_PATH', payload: path }),
    toggleSection: (sectionId: string) => dispatch({ type: 'TOGGLE_SECTION', payload: sectionId }),
    expandSection: (sectionId: string) => dispatch({ type: 'EXPAND_SECTION', payload: sectionId }),
    collapseSection: (sectionId: string) => dispatch({ type: 'COLLAPSE_SECTION', payload: sectionId }),
    setBreadcrumbTrail: (trail: BreadcrumbItem[]) => dispatch({ type: 'SET_BREADCRUMB_TRAIL', payload: trail }),
    addToBreadcrumb: (item: BreadcrumbItem) => dispatch({ type: 'ADD_TO_BREADCRUMB', payload: item }),
    clearNavigationState: () => dispatch({ type: 'CLEAR_NAVIGATION_STATE' }),
    setLanguage: (language: string) => dispatch({ type: 'SET_LANGUAGE', payload: language }),
    setAccessibilityMode: (mode: boolean) => dispatch({ type: 'SET_ACCESSIBILITY_MODE', payload: mode }),
  };
};