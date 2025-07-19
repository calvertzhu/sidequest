import React from 'react';

const Footer = () => (
  <footer className="py-8 px-4 bg-gray-950 text-gray-400 text-center mt-auto">
    <div className="flex flex-col md:flex-row justify-between items-center max-w-4xl mx-auto gap-4">
      <div className="flex gap-6 mb-2 md:mb-0">
        <a href="#about" className="hover:text-white transition">
          About
        </a>
        <a href="#contact" className="hover:text-white transition">
          Contact
        </a>
        <a href="#privacy" className="hover:text-white transition">
          Privacy
        </a>
      </div>
      <div className="flex gap-4 text-2xl">
        <a
          href="#"
          aria-label="Instagram"
          className="hover:text-pink-400 transition"
        >
          📸
        </a>
        <a
          href="#"
          aria-label="Twitter"
          className="hover:text-blue-400 transition"
        >
          🐦
        </a>
        <a
          href="#"
          aria-label="Discord"
          className="hover:text-indigo-400 transition"
        >
          💬
        </a>
      </div>
    </div>
    <div className="mt-4 text-xs text-gray-600">
      &copy; {new Date().getFullYear()} Sidequest. All rights reserved.
    </div>
  </footer>
);

export default Footer;
