import React from 'react';
import { InteractiveUIProvider } from './components/InteractiveUIProvider';

export default function Root({ children }) {
  return (
    <InteractiveUIProvider>
      {children}
    </InteractiveUIProvider>
  );
}