import React from 'react';
import { InteractiveContextProvider } from './InteractiveComponents/Context';

interface InteractiveUIProviderProps {
  children: React.ReactNode;
}

const InteractiveUIProvider: React.FC<InteractiveUIProviderProps> = ({ children }) => {
  return (
    <InteractiveContextProvider>
      {children}
    </InteractiveContextProvider>
  );
};

const MemoizedInteractiveUIProvider = React.memo(InteractiveUIProvider);
export default MemoizedInteractiveUIProvider;