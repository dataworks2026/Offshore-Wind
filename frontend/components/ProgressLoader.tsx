'use client';

import { useEffect, useState } from 'react';

interface ProgressLoaderProps {
  isLoading: boolean;
}

export default function ProgressLoader({ isLoading }: ProgressLoaderProps) {
  const [progress, setProgress] = useState(0);
  const [stage, setStage] = useState(0);

  const stages = [
    'Uploading image...',
    'Processing image...',
    'Running AI detection...',
    'Analyzing damage patterns...',
    'Generating results...',
  ];

  useEffect(() => {
    if (!isLoading) {
      setProgress(0);
      setStage(0);
      return;
    }

    // Simulate progress
    const progressInterval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 90) return prev; // Cap at 90% until complete
        const increment = Math.random() * 15 + 5;
        return Math.min(prev + increment, 90);
      });
    }, 500);

    // Cycle through stages
    const stageInterval = setInterval(() => {
      setStage((prev) => (prev + 1) % stages.length);
    }, 2000);

    return () => {
      clearInterval(progressInterval);
      clearInterval(stageInterval);
    };
  }, [isLoading]);

  if (!isLoading) return null;

  return (
    <div className="flex-1 flex flex-col items-center justify-center p-6 animate-fade-in">
      {/* Animated wind turbine icon */}
      <div className="relative mb-6">
        <svg
          className="w-20 h-20 text-mira-blue animate-spin"
          style={{ animationDuration: '3s' }}
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
        >
          {/* Turbine blades */}
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={1.5}
            d="M12 12L12 2M12 12L19.794 17M12 12L4.206 17"
          />
          {/* Center hub */}
          <circle cx="12" cy="12" r="2" fill="currentColor" />
        </svg>
        {/* Glow effect */}
        <div className="absolute inset-0 rounded-full bg-mira-blue/20 blur-xl animate-pulse" />
      </div>

      {/* Progress bar container */}
      <div className="w-full max-w-xs mb-4">
        <div className="h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
          <div
            className="h-full progress-bar rounded-full transition-all duration-500 ease-out"
            style={{ width: `${progress}%` }}
          />
        </div>
        <div className="flex justify-between mt-2 text-xs text-gray-500 dark:text-gray-400">
          <span>{Math.round(progress)}%</span>
          <span>Processing</span>
        </div>
      </div>

      {/* Current stage text */}
      <p className="text-gray-600 dark:text-gray-300 text-sm font-medium animate-pulse">
        {stages[stage]}
      </p>

      {/* Skeleton preview of results */}
      <div className="mt-8 w-full max-w-sm space-y-3">
        <div className="text-xs text-gray-400 dark:text-gray-500 text-center mb-2 tracking-wide uppercase">
          Preparing results...
        </div>

        {/* Skeleton items */}
        {[...Array(3)].map((_, i) => (
          <div
            key={i}
            className="flex items-center space-x-3 p-3 bg-gray-100 dark:bg-gray-800 rounded-lg animate-slide-up"
            style={{ animationDelay: `${i * 0.1}s` }}
          >
            <div className="w-3 h-3 rounded-full skeleton" />
            <div className="flex-1 space-y-2">
              <div className="h-3 w-24 rounded skeleton" />
              <div className="h-2 w-16 rounded skeleton" />
            </div>
            <div className="h-6 w-12 rounded skeleton" />
          </div>
        ))}
      </div>
    </div>
  );
}
