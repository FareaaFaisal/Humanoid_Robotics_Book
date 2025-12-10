import React from 'react';
import OriginalLayout from '@theme-original/Layout'; // original Docusaurus layout
import RAGChatbotWidget from '@site/src/components/RAGChatbotWidget'; // aapka chatbot component

export default function Layout(props) {
  return (
    <>
      {/* Original Layout ka content */}
      <OriginalLayout {...props} />

      {/* Chatbot widget, har page pe appear hoga */}
      <div style={{ position: 'fixed', bottom: 20, right: 20, zIndex: 9999 }}>
        <RAGChatbotWidget />
      </div>
    </>
  );
}
