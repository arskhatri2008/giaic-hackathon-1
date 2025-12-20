import React from 'react';
import clsx from 'clsx';
import styles from './IsaacConceptExplainer.module.css';

// Simple educational component to explain Isaac concepts
const IsaacConceptExplainer = ({ title, description, children }) => {
  return (
    <div className={clsx('margin--lg', styles.isaacConceptExplainer)}>
      <div className={styles.header}>
        <h3>{title}</h3>
      </div>
      <div className={styles.content}>
        <p>{description}</p>
        <div className={styles.interactiveContent}>
          {children}
        </div>
      </div>
    </div>
  );
};

export default IsaacConceptExplainer;