'use client';

import Link from 'next/link';
import { useTheme } from './ThemeProvider';

export default function Navbar() {
  const { theme, toggleTheme, mounted } = useTheme();

  return (
    <nav className="bg-mira-navy dark:bg-gray-900 text-white px-4 sm:px-6 flex justify-between items-center h-[60px] transition-colors duration-300">
      <div className="flex items-center h-full py-2">
        <img
          src="/img/logo.png"
          alt="Mira Intel Logo"
          className="object-contain h-[40px] w-auto"
        />
      </div>

      <div className="flex items-center space-x-6 sm:space-x-12">
        <div className="flex space-x-6 sm:space-x-12 text-sm sm:text-base font-medium tracking-wide">
          <Link
            href="/"
            className="hover:text-mira-blue transition-all duration-200 hover:scale-105"
          >
            Home
          </Link>
          <Link
            href="/history"
            className="hover:text-mira-blue transition-all duration-200 hover:scale-105"
          >
            Case History
          </Link>
        </div>

        {/* Dark Mode Toggle */}
        <button
          onClick={toggleTheme}
          className="p-2 rounded-lg bg-white/10 hover:bg-white/20 transition-all duration-200 hover:scale-110 active:scale-95 btn-ripple"
          aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
        >
          {!mounted ? (
            // Placeholder while loading
            <div className="w-5 h-5" />
          ) : theme === 'light' ? (
            // Moon icon for dark mode
            <svg
              className="w-5 h-5 text-yellow-300 icon-hover"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
              />
            </svg>
          ) : (
            // Sun icon for light mode
            <svg
              className="w-5 h-5 text-yellow-300 icon-hover"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"
              />
            </svg>
          )}
        </button>
      </div>
    </nav>
  );
}

