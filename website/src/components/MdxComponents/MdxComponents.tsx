import React from 'react';
import InteractiveSidebar from '../InteractiveSidebar/InteractiveSidebar';
import ResponsiveNavbar from '../ResponsiveNavbar/ResponsiveNavbar';
import ExpandableSection from '../ExpandableSection/ExpandableSection';
import InteractiveCodeBlock from '../InteractiveCodeBlock/InteractiveCodeBlock';
import KnowledgeCheck from '../KnowledgeCheck/KnowledgeCheck';
import TabbedInterface from '../TabbedInterface/TabbedInterface';

// Define the MDX components mapping
const MDXComponents = {
  // Custom interactive components
  InteractiveSidebar,
  ResponsiveNavbar,
  ExpandableSection,
  InteractiveCodeBlock,
  KnowledgeCheck,
  TabbedInterface,

  // Extended native HTML elements with enhanced functionality
  details: (props: React.DetailedHTMLProps<React.DetailsHTMLAttributes<HTMLElement>, HTMLElement>) => (
    <details {...props} className={`custom-details ${props.className || ''}`} />
  ),

  summary: (props: React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement>, HTMLElement>) => (
    <summary {...props} className={`custom-summary ${props.className || ''}`} />
  ),

  // Code block wrapper for syntax highlighting
  pre: (props: React.DetailedHTMLProps<React.HTMLAttributes<HTMLPreElement>, HTMLPreElement>) => (
    <div className="code-block-wrapper">
      <pre {...props} />
    </div>
  ),

  // Custom blockquote for tips and insights
  blockquote: (props: React.DetailedHTMLProps<React.BlockquoteHTMLAttributes<HTMLElement>, HTMLElement>) => (
    <blockquote
      {...props}
      className={`interactive-blockquote ${props.className || ''}`}
    />
  ),
};

export default MDXComponents;