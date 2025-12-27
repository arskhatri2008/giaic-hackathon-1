// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config

import { themes as prismThemes } from "prism-react-renderer";

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: "Physical AI & Humanoid Robotics",
  tagline:
    "Module 1: The Robotic Nervous System (ROS 2) & Module 2: The Digital Twin (Gazebo & Unity) - Learn ROS 2 fundamentals, physics simulation, and perception systems for humanoid robots",
  favicon: "img/favicon.ico",

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Updated deprecated option (will show warning but works)
  onBrokenMarkdownLinks: 'warn',
  markdown: {
    mermaid: true,
  },

  // Set the production url of your site here
  url: "https://giaic-hackathon-1-ten.vercel.app/",
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: "/",

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: "your-username", // Usually your GitHub org/user name.
  projectName: "physical-ai-robotics", // Usually your repo name.

  onBrokenLinks: "throw",
  onBrokenMarkdownLinks: "warn",

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: "en",
    locales: ["en", "ur"], // Adding Urdu for future translation support
  },

  presets: [
    [
      "classic",
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: "./sidebars.js",
          // Remove this to remove the "edit this page" links.
          editUrl:
            "https://github.com/arskhatri2008/giaic-hackathon-1/tree/main/website/",
        },
        blog: {
          showReadingTime: true,
          feedOptions: {
            type: ["rss", "atom"],
            xslt: true,
          },
          // Remove this to remove the "edit this page" links.
          editUrl:
            "https://github.com/arskhatri2008/giaic-hackathon-1/tree/main/website/",
          // Useful options to enforce blogging best practices
          onInlineTags: "warn",
          onInlineAuthors: "warn",
          onUntruncatedBlogPosts: "warn",
        },
        theme: {
          customCss: "./src/css/custom.css",
        },
      }),
    ],
  ],

  plugins: [
    // Chatbot is implemented as a theme component in src/theme/Layout.js
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: "img/docusaurus-social-card.jpg",
      metadata: [
        {
          name: "keywords",
          content:
            "ROS 2, robotics, humanoid robots, AI, Physical AI, robot operating system, robot development, robotics education, AI integration, ROS architecture, robot communication, URDF, robot modeling",
        },
        { name: "author", content: "Physical AI & Humanoid Robotics Course" },
        { name: "robots", content: "index, follow" },
        { name: "og:type", content: "website" },
        {
          name: "og:title",
          content:
            "Physical AI & Humanoid Robotics - Module 1: The Robotic Nervous System (ROS 2)",
        },
        {
          name: "og:description",
          content:
            "Learn ROS 2 fundamentals, communication primitives, and robot modeling with URDF for humanoid robotics and AI integration.",
        },
        {
          name: "og:url",
          content: "https://your-username.github.io/physical-ai-robotics/",
        },
        { name: "twitter:card", content: "summary_large_image" },
        {
          name: "twitter:title",
          content:
            "Physical AI & Humanoid Robotics - Module 1: The Robotic Nervous System (ROS 2)",
        },
        {
          name: "twitter:description",
          content:
            "Learn ROS 2 fundamentals, communication primitives, and robot modeling with URDF for humanoid robotics and AI integration.",
        },
      ],
      colorMode: {
        respectPrefersColorScheme: true,
      },
      navbar: {
        title: "Physical AI & Humanoid Robotics",
        logo: {
          alt: "Physical AI & Humanoid Robotics Logo",
          src: "img/logo.svg",
        },
        items: [
          {
            type: "docSidebar",
            sidebarId: "tutorialSidebar",
            position: "left",
            label: "Book",
          },
          { to: "/blog", label: "Blog", position: "left" },
          {
            href: "https://github.com/arskhatri2008/giaic-hackathon-1",
            label: "GitHub",
            position: "right",
          },
        ],
      },
      footer: {
        style: "dark",
        links: [
          {
            title: "Docs",
            items: [
              {
                label: "Module 1: ROS 2",
                to: "/docs/module-1/intro",
              },
              {
                label: "Module 2: Digital Twin",
                to: "/docs/modules/digital-twin-simulation/intro",
              },
            ],
          },
          {
            title: "Community",
            items: [
              {
                label: "ROS Answers",
                href: "https://answers.ros.org/",
              },
              {
                label: "Robotics Stack Exchange",
                href: "https://robotics.stackexchange.com/",
              },
              {
                label: "ROS Discourse",
                href: "https://discourse.ros.org/",
              },
            ],
          },
          {
            title: "More",
            items: [
              {
                label: "Blog",
                to: "/blog",
              },
              {
                label: "GitHub",
                href: "https://github.com/arskhatri2008/giaic-hackathon-1",
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
};

export default config;
