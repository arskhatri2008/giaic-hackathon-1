import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';
import type { BreadcrumbItem } from '../../types';
import { useInteractiveContext } from '../InteractiveComponents/Context';

interface BreadcrumbProps {
  items: BreadcrumbItem[];
  className?: string;
  homeLabel?: string;
  separator?: string;
}

const Breadcrumb: React.FC<BreadcrumbProps> = ({
  items,
  className = '',
  homeLabel = 'Home',
  separator = '/'
}) => {
  const { navigationState } = useInteractiveContext();

  // Use the breadcrumb trail from context if no items are provided
  const breadcrumbItems = items && items.length > 0 ? items : navigationState.breadcrumbTrail;

  if (!breadcrumbItems || breadcrumbItems.length === 0) {
    return null;
  }

  // Add home item if it doesn't exist at the beginning
  const finalBreadcrumbItems = breadcrumbItems.length > 0 && breadcrumbItems[0].path !== '/'
    ? [{ title: homeLabel, path: '/', isCurrent: false }, ...breadcrumbItems]
    : breadcrumbItems;

  return (
    <nav
      className={clsx(styles.breadcrumbNav, className)}
      aria-label="Breadcrumb"
    >
      <ol className={styles.breadcrumbList}>
        {finalBreadcrumbItems.map((item, index) => {
          const isLast = index === finalBreadcrumbItems.length - 1;
          const isHome = index === 0 && item.path === '/';

          return (
            <li
              key={item.path}
              className={clsx(
                styles.breadcrumbItem,
                { [styles.breadcrumbItemActive]: isLast },
                { [styles.breadcrumbItemHome]: isHome }
              )}
            >
              {isLast ? (
                <span
                  className={clsx(
                    styles.breadcrumbLink,
                    styles.breadcrumbLinkActive
                  )}
                  aria-current="page"
                >
                  {item.title}
                </span>
              ) : (
                <a
                  href={item.path}
                  className={clsx(
                    styles.breadcrumbLink,
                    styles.breadcrumbLinkInactive
                  )}
                  aria-label={`Go to ${item.title}`}
                >
                  {isHome ? homeLabel : item.title}
                </a>
              )}

              {!isLast && (
                <span
                  className={styles.breadcrumbSeparator}
                  aria-hidden="true"
                >
                  {separator}
                </span>
              )}
            </li>
          );
        })}
      </ol>
    </nav>
  );
};

const MemoizedBreadcrumb = React.memo(Breadcrumb);
export default MemoizedBreadcrumb;