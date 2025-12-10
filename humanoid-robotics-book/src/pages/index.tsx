import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import RAGChatbotWidget from '@site/src/components/RAGChatbotWidget';


import styles from './index.module.css';

export default function Home() {
  const { siteConfig } = useDocusaurusContext();

  return (
    <Layout
      title={siteConfig.title}
      description={siteConfig.tagline}
    >

      {/* HERO SECTION */}
      <header className={styles.heroBanner}>
        <div className="container">
          <h1 className={styles.heroTitle}>{siteConfig.title}</h1>
          <p className={styles.heroSubtitle}>{siteConfig.tagline}</p>

          <Link className="button button--secondary button--lg " to="/docs/robotic-nervous-system/intro-physical-ai">
            Start Reading →
          </Link>
        </div>
      </header>

      {/* WHAT THIS COVERS */}
      <section className={styles.sectionDark}>
        <div className="container">
          <h2 className={styles.sectionTitle}>What This Textbook Covers</h2>
          <p className={styles.sectionDesc}>
           This textbook is a complete blueprint for mastering next-generation robotic intelligence. It unifies the core pillars of physical AI, humanoid robot design, embodied reasoning, ROS 2 control architectures, digital-twin simulation workflows, and Vision-Language-Action (VLA) systems. Through a carefully sequenced structure, it transforms complex robotics concepts into an intuitive, hands-on learning experience, guiding you from foundational principles to advanced system integration with the clarity and depth required for real-world engineering.
          </p>
        </div>
      </section>

      {/* MODULE CARDS */}
      <section className={styles.modulesSection}>
        <div className="container">
          <h2 className={styles.sectionTitle1}>Explore All Modules</h2>

          <div className={styles.modulesGrid}>

            <div className={styles.moduleCard}>
              <h3>Module 1: The Robotic Nervous System</h3>
              <p>A deep dive into ROS 2 as the communication backbone that powers humanoid robot control, modeling, and real-time coordination.</p>
              <Link className="button button--secondary button--md" to="/docs/robotic-nervous-system/ros-architecture" style={{ color: '#fff' }}>Open Module →</Link>
            </div>

            <div className={styles.moduleCard}>
              <h3>Module 2: The Digital Twin</h3>
              <p>Learn to build and simulate realistic robotic worlds using physics-accurate environments, sensors, and high-fidelity digital twins.</p>
              <Link className="button button--secondary button--md" to="/docs/digital-twin/simulation-theory" style={{ color: '#fff' }}>Open Module →</Link>
            </div>

            <div className={styles.moduleCard}>
              <h3>Module 3: The AI-Robot Brain</h3>
              <p>Master advanced perception, navigation, and AI-accelerated robotics through NVIDIA Isaac Sim, Isaac ROS, and real-world-ready planning pipelines.</p>
              <Link className="button button--secondary button--md" to="/docs/ai-robot-brain/isaac-ecosystem" style={{ color: '#fff' }}>Open Module →</Link>
            </div>

            <div className={styles.moduleCard}>
              <h3>Module 4: Vision-Language-Action</h3>
              <p>Explore how LLMs, voice commands, and cognitive planners enable robots to understand language and execute complex tasks.</p>
              <Link className="button button--secondary button--md" to="/docs/vision-language-action/vla-intro" style={{ color: '#fff' }}>Open Module →</Link>
            </div>

          </div>
        </div>
      </section>


      {/* ========================= */}
      {/* ADD THE CHATBOT HERE */}
      <RAGChatbotWidget /> 
      {/* ========================= */}

    </Layout>
  );
}
