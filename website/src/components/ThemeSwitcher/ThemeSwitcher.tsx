import React, { useState, useEffect } from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

interface ThemeSwitcherProps {
  className?: string;
}

const ThemeSwitcher: React.FC<ThemeSwitcherProps> = ({ className }) => {
  const [theme, setTheme] = useState<'light' | 'dark' | 'auto'>('auto');

  // Initialize theme from system preference or saved preference
  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') as 'light' | 'dark' | 'auto' | null;
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    if (savedTheme) {
      setTheme(savedTheme);
      applyTheme(savedTheme, systemPrefersDark);
    } else {
      const initialTheme = systemPrefersDark ? 'dark' : 'light';
      setTheme(initialTheme);
      applyTheme(initialTheme, systemPrefersDark);
    }
  }, []);

  // Apply theme to document
  const applyTheme = (selectedTheme: 'light' | 'dark' | 'auto', systemPrefersDark: boolean) => {
    let themeToApply: 'light' | 'dark';

    if (selectedTheme === 'auto') {
      themeToApply = systemPrefersDark ? 'dark' : 'light';
    } else {
      themeToApply = selectedTheme;
    }

    document.documentElement.setAttribute('data-theme', themeToApply);
    localStorage.setItem('theme', selectedTheme);
  };

  // Handle theme change
  const changeTheme = (newTheme: 'light' | 'dark' | 'auto') => {
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    setTheme(newTheme);
    applyTheme(newTheme, systemPrefersDark);
  };

  // Listen for system theme changes
  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const handleChange = () => {
      if (theme === 'auto') {
        const systemPrefersDark = mediaQuery.matches;
        const newTheme = systemPrefersDark ? 'dark' : 'light';
        applyTheme('auto', systemPrefersDark);
      }
    };

    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, [theme]);

  return (
    <div className={clsx(styles.themeSwitcher, className)} role="toolbar" aria-label="Theme selector">
      <button
        className={clsx(
          styles.themeButton,
          { [styles.active]: theme === 'light' }
        )}
        onClick={() => changeTheme('light')}
        aria-pressed={theme === 'light'}
        aria-label="Switch to light theme"
        type="button"
      >
        <span className={styles.themeIcon} aria-hidden="true">☀️</span>
        <span className={styles.themeLabel}>Light</span>
      </button>
      <button
        className={clsx(
          styles.themeButton,
          { [styles.active]: theme === 'dark' }
        )}
        onClick={() => changeTheme('dark')}
        aria-pressed={theme === 'dark'}
        aria-label="Switch to dark theme"
        type="button"
      >
        <span className={styles.themeIcon} aria-hidden="true">🌙</span>
        <span className={styles.themeLabel}>Dark</span>
      </button>
      <button
        className={clsx(
          styles.themeButton,
          { [styles.active]: theme === 'auto' }
        )}
        onClick={() => changeTheme('auto')}
        aria-pressed={theme === 'auto'}
        aria-label="Use system theme preference"
        type="button"
      >
        <span className={styles.themeIcon} aria-hidden="true">💻</span>
        <span className={styles.themeLabel}>Auto</span>
      </button>
    </div>
  );
};

export default ThemeSwitcher;