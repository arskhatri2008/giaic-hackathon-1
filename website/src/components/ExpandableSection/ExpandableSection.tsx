import React, { useState, useEffect, useRef, useMemo } from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';
import { useInteractiveContext, useInteractiveActions } from '../InteractiveComponents/Context';

interface ExpandableSectionProps {
  title: string;
  children: React.ReactNode;
  defaultExpanded?: boolean;
  className?: string;
  onToggle?: (isExpanded: boolean) => void;
}

const ExpandableSection: React.FC<ExpandableSectionProps> = ({
  title,
  children,
  defaultExpanded = false,
  className,
  onToggle
}) => {
  const { navigationState } = useInteractiveContext();
  const { toggleSection, expandSection, collapseSection } = useInteractiveActions();
  const [height, setHeight] = useState<number | 'auto'>('0px');
  const contentRef = useRef<HTMLDivElement>(null);

  // Generate a unique ID for this expandable section
  const sectionId = useMemo(() => {
    return `expandable-section-${title.replace(/\s+/g, '-').toLowerCase()}`;
  }, [title]);

  // Check if this section is expanded based on context state
  const isExpanded = useMemo(() => {
    return navigationState.expandedSections.includes(sectionId);
  }, [navigationState.expandedSections, sectionId]);

  // Handle expansion/collapse with animation
  useEffect(() => {
    if (contentRef.current) {
      if (isExpanded) {
        setHeight(contentRef.current.scrollHeight);
      } else {
        setHeight(0);
      }
    }
  }, [isExpanded]);

  // Call onToggle callback when state changes
  useEffect(() => {
    if (onToggle) {
      onToggle(isExpanded);
    }
  }, [isExpanded, onToggle]);

  const toggleExpanded = () => {
    toggleSection(sectionId);
  };

  return (
    <div
      className={clsx(
        styles.expandableSection,
        { [styles.expanded]: isExpanded },
        className
      )}
      role="region"
      aria-labelledby="expandable-section-title"
    >
      <button
        className={clsx(
          styles.expandableHeader,
          { [styles.expanded]: isExpanded }
        )}
        onClick={toggleExpanded}
        onKeyDown={(e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            toggleExpanded();
          }
        }}
        aria-expanded={isExpanded}
        aria-controls="expandable-section-content"
        id="expandable-section-title"
        type="button"
      >
        <span className={styles.sectionTitle}>{title}</span>
        <span
          className={clsx(
            styles.expandIcon,
            { [styles.rotated]: isExpanded }
          )}
          aria-hidden="true"
        >
          ▼
        </span>
      </button>
      <div
        id="expandable-section-content"
        className={styles.expandableContent}
        ref={contentRef}
        style={{ height }}
        aria-hidden={!isExpanded}
      >
        <div className={styles.contentInner}>
          {children}
        </div>
      </div>
    </div>
  );
};

const MemoizedExpandableSection = React.memo(ExpandableSection);
export default MemoizedExpandableSection;