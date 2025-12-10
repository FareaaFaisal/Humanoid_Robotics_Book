import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'Unlock the future of intelligent machines: Master Humanoid Robotics, Physical AI, Simulation, and Next-Gen Autonomous Systems for a world where robots think, move, and act like us',
  favicon: 'img/favicon.ico',

   clientModules: [require.resolve('./src/components/RAGChatbotWidget/index.tsx')],

  // Production URL and base URL for GitHub Pages
  url: 'https://fareaafaisal.github.io',
  baseUrl: '/hackathon-1/',

  // GitHub pages deployment config
  organizationName: 'FareaaFaisal', // GitHub username
  projectName: 'hackathon-1',       // Repo name

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Internationalization
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  // Presets
  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          // Link to edit pages on GitHub
          editUrl: 'https://github.com/FareaaFaisal/hackathon-1/edit/main/',
        },
        blog: {
          showReadingTime: true,
          editUrl: 'https://github.com/FareaaFaisal/hackathon-1/edit/main/',
          feedOptions: {
            type: ['rss', 'atom'],
            xslt: true,
          },
          onInlineTags: 'warn',
          onInlineAuthors: 'warn',
          onUntruncatedBlogPosts: 'warn',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  // Theme configuration
  themeConfig: {
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      defaultMode: 'light',
      respectPrefersColorScheme: false,
    },
    navbar: {
      hideOnScroll: false,
      title: 'Humanoid Robotics',
      logo: {
        alt: 'Humanoid Robotics Book Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'TextBook',
        },
        {to: '/blog', label: 'Blog', position: 'left'},
        {
          href: 'https://github.com/FareaaFaisal/hackathon-1',
          label: 'GitHub Repo',
          position: 'right',
        },
      ],
    },
    footer: {
  style: 'dark',
  logo: {
    alt: 'Humanoid Robotics Logo',
    src: 'img/logo.svg',
    href: '/',
  },
  links: [
    {
      title: 'Explore',
      items: [
        { label: 'Modules', to: '/docs/robotic-nervous-system/intro-physical-ai' },
        { label: 'Blog', to: '/blog' },
        { label: 'GitHub Repo', href: 'https://github.com/FareaaFaisal/hackathon-1' },
      ],
    },
    {
      title: 'Community',
      items: [
        { label: 'Stack Overflow', href: 'https://stackoverflow.com/questions/tagged/docusaurus' },
        { label: 'Discord', href: 'https://discord.com/invite/docusaurus' },
        { label: 'Twitter', href: 'https://x.com/docusaurus' },
      ],
    },
    {
      title: 'Connect',
      items: [
        { label: 'GitHub', href: 'https://github.com/FareaaFaisal' },
        { label: 'LinkedIn', href: 'https://www.linkedin.com/in/fareaa-faisal-31569a2ba/' },
      ],
    },
    {
      title: 'Resources',
      items: [
        { label: 'Docusaurus Docs', href: 'https://docusaurus.io/docs' },
        { label: 'NVIDIA Isaac Sim', href: 'https://developer.nvidia.com/isaac-sim' },
        { label: 'Physical AI Research', href: 'https://arxiv.org/search/?query=physical+AI&searchtype=all' },
      ],
    },
  ],
  copyright: `© ${new Date().getFullYear()} Physical AI & Humanoid Robotics | Designed & Developed by Fareaa Faisal`,

},

  
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
    algolia: {
      appId: 'YOUR_APP_ID',           // Optional, set if you have Algolia search
      apiKey: 'YOUR_SEARCH_API_KEY',
      indexName: 'YOUR_INDEX_NAME',
      contextualSearch: true,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
