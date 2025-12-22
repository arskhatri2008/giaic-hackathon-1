// Common TypeScript interfaces for UI state management

// Navigation state interfaces
export interface NavigationState {
  currentPath: string;
  expandedSections: string[];
  breadcrumbTrail: BreadcrumbItem[];
}

export interface BreadcrumbItem {
  title: string;
  path: string;
  isCurrent?: boolean;
}

// UI state interfaces
export interface UIState {
  sidebarCollapsed: boolean;
  theme: 'light' | 'dark' | 'auto';
  mobileMenuOpen: boolean;
  currentBreakpoint: 'mobile' | 'tablet' | 'desktop';
  language: string;
  accessibilityMode: boolean;
}

// Interactive component state interfaces
export interface ExpandableSectionState {
  id: string;
  isExpanded: boolean;
  defaultExpanded?: boolean;
}

export interface KnowledgeCheckState {
  questionId: string;
  selectedOption: number | null;
  submitted: boolean;
  correctAnswer: number;
}

export interface InteractiveCodeBlockState {
  code: string;
  language: string;
  showLineNumbers: boolean;
  copied: boolean;
  copiedTimeout: number | null;
}

// Component configuration interfaces
export interface ComponentConfig {
  id: string;
  className?: string;
  style?: React.CSSProperties;
  ariaLabel?: string;
  tabIndex?: number;
}

export interface InteractiveComponentConfig extends ComponentConfig {
  enabled: boolean;
  disabledMessage?: string;
}

// Theme and styling interfaces
export interface ThemeContextType {
  theme: 'light' | 'dark' | 'auto';
  toggleTheme: () => void;
  setTheme: (theme: 'light' | 'dark' | 'auto') => void;
}

export interface ResponsiveConfig {
  mobileBreakpoint: number;
  tabletBreakpoint: number;
  desktopBreakpoint: number;
}

// Accessibility interfaces
export interface AccessibilityConfig {
  highContrast: boolean;
  reducedMotion: boolean;
  screenReaderMode: boolean;
  keyboardOnly: boolean;
}

export interface FocusManagement {
  focusElement: (elementId: string) => void;
  focusFirstChild: (parentId: string) => void;
  trapFocus: (containerId: string, returnFocus?: boolean) => void;
}

// Generic state management interface
export interface StateManager<T> {
  state: T;
  setState: (newState: T | ((prevState: T) => T)) => void;
  resetState: () => void;
  updateState: (partialState: Partial<T>) => void;
}

// Event handler interfaces
export interface NavigationEventHandlers {
  onNavigate: (path: string) => void;
  onExpandSection: (sectionId: string) => void;
  onCollapseSection: (sectionId: string) => void;
  onBreadcrumbClick: (item: BreadcrumbItem) => void;
}

export interface InteractiveEventHandlers {
  onClick?: (event: React.MouseEvent) => void;
  onKeyDown?: (event: React.KeyboardEvent) => void;
  onFocus?: (event: React.FocusEvent) => void;
  onBlur?: (event: React.FocusEvent) => void;
  onTouchStart?: (event: React.TouchEvent) => void;
  onTouchEnd?: (event: React.TouchEvent) => void;
}

// Component lifecycle interfaces
export interface ComponentLifecycle {
  onMount?: () => void;
  onUnmount?: () => void;
  onUpdate?: (prevProps: any, prevState: any) => void;
}

// Error boundary interfaces
export interface ErrorBoundaryState {
  hasError: boolean;
  error?: Error;
  errorInfo?: React.ErrorInfo;
}

// Loading state interfaces
export interface LoadingState {
  isLoading: boolean;
  loadingProgress?: number;
  loadingMessage?: string;
}

// Modal/dialog interfaces
export interface ModalState {
  isOpen: boolean;
  content: React.ReactNode;
  title?: string;
  ariaLabel?: string;
  onClose: () => void;
}

// Form-related interfaces
export interface FormState<T> {
  values: T;
  errors: Partial<Record<keyof T, string>>;
  touched: Partial<Record<keyof T, boolean>>;
  isValid: boolean;
  isSubmitting: boolean;
}

// Animation interfaces
export interface AnimationState {
  isVisible: boolean;
  animationClass: string;
  onAnimationStart?: () => void;
  onAnimationEnd?: () => void;
}

// Responsive state interfaces
export interface ResponsiveState {
  isMobile: boolean;
  isTablet: boolean;
  isDesktop: boolean;
  currentBreakpoint: 'mobile' | 'tablet' | 'desktop';
}

// Accessibility state interfaces
export interface AccessibilityState {
  prefersReducedMotion: boolean;
  prefersHighContrast: boolean;
  screenReaderDetected: boolean;
  highContrastMode: boolean;
}