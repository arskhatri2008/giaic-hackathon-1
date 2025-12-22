import React, { useState, useEffect } from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';
import type { NavigationState, BreadcrumbItem, ExpandableSectionState } from '../../types';
import { useInteractiveContext, useInteractiveActions } from '../InteractiveComponents/Context';

interface InteractiveSidebarProps {
  items: Array<{
    title: string;
    path: string;
    children?: Array<{
      title: string;
      path: string;
    }>;
  }>;
  currentPath: string;
  isCollapsed?: boolean;
  className?: string;
}

const InteractiveSidebar: React.FC<InteractiveSidebarProps> = ({
  items,
  currentPath,
  isCollapsed = false,
  className
}) => {
  const { navigationState, uiState } = useInteractiveContext();
  const { toggleSection, setCurrentPath } = useInteractiveActions();
  const [keyboardNav, setKeyboardNav] = useState<boolean>(false);

  // Update active item when currentPath changes
  useEffect(() => {
    setCurrentPath(currentPath);
  }, [currentPath, setCurrentPath]);

  // Handle keyboard navigation detection
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Tab' || e.key === 'ArrowDown' || e.key === 'ArrowUp' || e.key === 'Enter' || e.key === ' ') {
        setKeyboardNav(true);
      }
    };

    const handleMouseDown = () => {
      setKeyboardNav(false);
    };

    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('mousedown', handleMouseDown);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('mousedown', handleMouseDown);
    };
  }, []);

  // Check if a section is expanded using context state
  const isSectionExpanded = (sectionId: string): boolean => {
    return navigationState.expandedSections.includes(sectionId);
  };

  // Check if an item is active (current page) using context state
  const isActiveItem = (path: string): boolean => {
    return navigationState.currentPath === path;
  };

  // Render sidebar items recursively
  const renderItems = (items: InteractiveSidebarProps['items'], level: number = 0) => {
    return items.map((item, index) => {
      const hasChildren = item.children && item.children.length > 0;
      const sectionId = `${level}-${index}`;
      const isExpanded = isSectionExpanded(sectionId);
      const isActive = isActiveItem(item.path);

      return (
        <li
          key={item.path}
          className={clsx(
            styles.sidebarItem,
            { [styles.level2]: level === 1, [styles.level3]: level >= 2 }
          )}
        >
          <div className={styles.sidebarItemContainer}>
            {hasChildren ? (
              <>
                <button
                  className={clsx(
                    styles.sidebarLink,
                    styles.expandableHeader,
                    { [styles.active]: isActive },
                    { [styles.expanded]: isExpanded }
                  )}
                  onClick={() => toggleSection(sectionId)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                      e.preventDefault();
                      toggleSection(sectionId);
                    } else if (e.key === 'ArrowRight' && !isExpanded) {
                      toggleSection(sectionId);
                    } else if (e.key === 'ArrowLeft' && isExpanded) {
                      toggleSection(sectionId);
                    }
                  }}
                  aria-expanded={isExpanded}
                  aria-controls={`section-${sectionId}`}
                  aria-label={`${isExpanded ? 'Collapse' : 'Expand'} section ${item.title}`}
                  tabIndex={0}
                >
                  <span className={styles.itemText}>{item.title}</span>
                  <span className={clsx(styles.collapseIcon, { [styles.expanded]: isExpanded })}>▼</span>
                </button>
                <ul
                  id={`section-${sectionId}`}
                  className={clsx(
                    styles.sidebarSubmenu,
                    { [styles.expanded]: isExpanded }
                  )}
                  style={{ display: isExpanded ? 'block' : 'none' }}
                >
                  {renderItems(item.children!, level + 1)}
                </ul>
              </>
            ) : (
              <a
                href={item.path}
                className={clsx(
                  styles.sidebarLink,
                  { [styles.active]: isActive }
                )}
                aria-current={isActive ? 'page' : undefined}
                tabIndex={0}
              >
                {item.title}
              </a>
            )}
          </div>
        </li>
      );
    });
  };

  return (
    <nav
      className={clsx(
        styles.interactiveSidebar,
        { [styles.collapsed]: isCollapsed },
        { [styles.keyboardNav]: keyboardNav },
        className
      )}
      aria-label="Table of Contents"
      role="navigation"
    >
      <ul className={styles.sidebarList} role="list">
        {renderItems(items)}
      </ul>
    </nav>
  );
};

const MemoizedInteractiveSidebar = React.memo(InteractiveSidebar);
export default MemoizedInteractiveSidebar;