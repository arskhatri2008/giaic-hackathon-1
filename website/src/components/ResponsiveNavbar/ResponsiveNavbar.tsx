import React, { useState, useEffect } from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';
import type { NavigationState } from '../../types';
import { useInteractiveContext, useInteractiveActions } from '../InteractiveComponents/Context';

interface NavItem {
  label: string;
  href?: string;
  to?: string;
  activeBaseRegex?: string;
}

interface ResponsiveNavbarProps {
  logo?: {
    alt: string;
    src: string;
    href?: string;
  };
  title?: string;
  items: NavItem[];
  className?: string;
}

const ResponsiveNavbar: React.FC<ResponsiveNavbarProps> = ({
  logo,
  title,
  items,
  className
}) => {
  const { uiState } = useInteractiveContext();
  const { toggleMobileMenu, setCurrentBreakpoint } = useInteractiveActions();
  const [isScrolled, setIsScrolled] = useState(false);

  // Handle scroll effect for navbar
  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Update breakpoint based on window size
  useEffect(() => {
    const handleResize = () => {
      const width = window.innerWidth;
      if (width < 768) {
        setCurrentBreakpoint('mobile');
      } else if (width < 996) {
        setCurrentBreakpoint('tablet');
      } else {
        setCurrentBreakpoint('desktop');
      }
    };

    // Initial check
    handleResize();

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [setCurrentBreakpoint]);

  // Close mobile menu when clicking a link
  const handleLinkClick = () => {
    // Only close menu if it's currently open
    if (uiState.mobileMenuOpen) {
      toggleMobileMenu();
    }
  };

  return (
    <header
      className={clsx(
        styles.navbar,
        { [styles.navbarScrolled]: isScrolled },
        { [styles.navbarMobileOpen]: uiState.mobileMenuOpen },
        className
      )}
      role="banner"
    >
      <div className={styles.navbarRow}>
        <div className={styles.navbarLeft}>
          {/* Logo and title */}
          <div className={styles.navbarLogo}>
            {logo && (
              <a
                href={logo.href || '/'}
                className={styles.navbarLogoLink}
                aria-label={logo.alt}
              >
                <img
                  src={logo.src}
                  alt={logo.alt}
                  className={styles.navbarLogoImg}
                />
              </a>
            )}
            {title && (
              <a
                href="/"
                className={styles.navbarTitle}
                aria-current="page"
              >
                {title}
              </a>
            )}
          </div>
        </div>

        {/* Desktop Navigation Items */}
        <div className={styles.navbarCenter}>
          <ul className={styles.navbarItems}>
            {items.map((item, index) => (
              <li key={index} className={styles.navbarItem}>
                {item.to ? (
                  <a
                    href={item.to}
                    className={clsx(styles.navbarLink, styles.navbarLinkDesktop)}
                    onClick={handleLinkClick}
                  >
                    {item.label}
                  </a>
                ) : item.href ? (
                  <a
                    href={item.href}
                    className={clsx(styles.navbarLink, styles.navbarLinkDesktop)}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    {item.label}
                  </a>
                ) : (
                  <span className={clsx(styles.navbarLink, styles.navbarLinkDesktop)}>
                    {item.label}
                  </span>
                )}
              </li>
            ))}
          </ul>
        </div>

        {/* Mobile Menu Button */}
        <div className={styles.navbarRight}>
          <button
            className={clsx(
              styles.mobileMenuButton,
              { [styles.mobileMenuButtonOpen]: uiState.mobileMenuOpen }
            )}
            type="button"
            aria-label={uiState.mobileMenuOpen ? 'Close navigation menu' : 'Open navigation menu'}
            aria-expanded={uiState.mobileMenuOpen}
            onClick={toggleMobileMenu}
          >
            <span className={styles.mobileMenuBar}></span>
            <span className={styles.mobileMenuBar}></span>
            <span className={styles.mobileMenuBar}></span>
          </button>
        </div>
      </div>

      {/* Mobile Navigation Menu */}
      <div
        className={clsx(
          styles.mobileMenu,
          { [styles.mobileMenuOpen]: uiState.mobileMenuOpen }
        )}
        role="navigation"
        aria-label="Mobile navigation"
      >
        <ul className={styles.mobileMenuItems}>
          {items.map((item, index) => (
            <li key={index} className={styles.mobileMenuItem}>
              {item.to ? (
                <a
                  href={item.to}
                  className={styles.mobileMenuLink}
                  onClick={handleLinkClick}
                >
                  {item.label}
                </a>
              ) : item.href ? (
                <a
                  href={item.href}
                  className={styles.mobileMenuLink}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {item.label}
                </a>
              ) : (
                <span className={styles.mobileMenuLink}>
                  {item.label}
                </span>
              )}
            </li>
          ))}
        </ul>
      </div>
    </header>
  );
};

const MemoizedResponsiveNavbar = React.memo(ResponsiveNavbar);
export default MemoizedResponsiveNavbar;