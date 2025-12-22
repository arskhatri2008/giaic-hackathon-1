import React, { useState } from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

interface TabItem {
  label: string;
  content: React.ReactNode;
  language?: string;
}

interface TabbedInterfaceProps {
  tabs: TabItem[];
  defaultActiveTab?: number;
  className?: string;
}

const TabbedInterface: React.FC<TabbedInterfaceProps> = ({
  tabs,
  defaultActiveTab = 0,
  className
}) => {
  const [activeTab, setActiveTab] = useState(defaultActiveTab);

  const handleTabChange = (index: number) => {
    setActiveTab(index);
  };

  return (
    <div
      className={clsx(
        styles.tabbedInterface,
        className
      )}
      role="tabpanel"
      aria-label="Multi-language code examples"
    >
      <div className={styles.tabsContainer}>
        <ul className={styles.tabsList} role="tablist">
          {tabs.map((tab, index) => (
            <li key={index} className={styles.tabItem}>
              <button
                className={clsx(
                  styles.tabButton,
                  { [styles.active]: index === activeTab }
                )}
                onClick={() => handleTabChange(index)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    handleTabChange(index);
                  }
                }}
                role="tab"
                aria-selected={index === activeTab}
                aria-controls={`tab-panel-${index}`}
                id={`tab-${index}`}
                type="button"
              >
                {tab.label}
              </button>
            </li>
          ))}
        </ul>
      </div>
      <div
        className={styles.tabPanelsContainer}
        role="tabpanel"
        id={`tab-panel-${activeTab}`}
        aria-labelledby={`tab-${activeTab}`}
        tabIndex={0}
      >
        {tabs[activeTab].content}
      </div>
    </div>
  );
};

const MemoizedTabbedInterface = React.memo(TabbedInterface);
export default MemoizedTabbedInterface;