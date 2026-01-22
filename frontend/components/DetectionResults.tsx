'use client';

import { useState } from 'react';
import { InferenceResponse } from '@/lib/api';
import BoundingBoxCanvas from './BoundingBoxCanvas';

// Color mapping for damage class badges (matches BoundingBoxCanvas)
const CLASS_COLORS: Record<string, string> = {
  'Drain hole impairment': '#FF6B6B',
  'Lightning Strike': '#FFE66D',
  'OIL LEAKAGE': '#4ECDC4',
  'PU-tape': '#A66CFF',
  'Paint': '#FF9F43',
  'Surface Crack': '#EE5A5A',
  'dirt': '#8B7355',
  'le-erosion': '#00D9FF',
};

interface DetectionResultsProps {
  results: InferenceResponse | null;
  imageUrl: string | null;
}

export default function DetectionResults({ results, imageUrl }: DetectionResultsProps) {
  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null);
  const [isRippling, setIsRippling] = useState(false);

  if (!results || !imageUrl) {
    return null;
  }

  const handleDownloadClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    // Trigger ripple effect
    setIsRippling(true);
    setTimeout(() => setIsRippling(false), 600);

    const link = document.createElement('a');
    link.href = imageUrl;
    link.download = `detection-result-${Date.now()}.jpg`;
    link.click();
  };

  return (
    <div className="w-full animate-fade-in">
      {/* Image Display with Bounding Boxes */}
      <div className="bg-white dark:bg-gray-800 rounded-xl p-3 mb-6 border-2 border-mira-blue shadow-sm transition-colors duration-300">
        <BoundingBoxCanvas
          imageUrl={imageUrl}
          detections={results.detections}
          highlightedIndex={hoveredIndex}
          enablePulse={true}
        />
      </div>

      {/* Damages Found List with Detection Details */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-heading text-gray-900 dark:text-white">
            Damages Found:
          </h3>
          {results.total_detections > 0 && (
            <span className="text-sm text-gray-500 dark:text-gray-400 tracking-wide">
              {results.total_detections} detection{results.total_detections > 1 ? 's' : ''}
            </span>
          )}
        </div>

        {results.total_detections === 0 ? (
          <div className="p-4 bg-green-50 dark:bg-green-900/30 border border-green-200 dark:border-green-800 rounded-lg animate-slide-up">
            <p className="text-green-700 dark:text-green-300">No damages detected in this image.</p>
          </div>
        ) : (
          <div className="space-y-2 max-h-72 overflow-y-auto pr-1">
            {results.detections.map((detection, index) => (
              <div
                key={index}
                className={`p-3 bg-gray-50 dark:bg-gray-800 rounded-lg border-l-4 cursor-pointer
                  transition-all duration-200 ease-out animate-slide-up
                  ${hoveredIndex === index
                    ? 'detection-item-highlight shadow-md'
                    : 'hover:bg-gray-100 dark:hover:bg-gray-700 hover:shadow-sm hover:translate-x-1'
                  }`}
                style={{
                  borderLeftColor: CLASS_COLORS[detection.class] || '#888888',
                  animationDelay: `${index * 0.05}s`,
                }}
                onMouseEnter={() => setHoveredIndex(index)}
                onMouseLeave={() => setHoveredIndex(null)}
              >
                <div className="flex justify-between items-center">
                  <div className="flex items-center space-x-2">
                    <div
                      className={`w-3 h-3 rounded-full transition-transform duration-200 ${
                        hoveredIndex === index ? 'scale-125' : ''
                      }`}
                      style={{ backgroundColor: CLASS_COLORS[detection.class] || '#888888' }}
                    />
                    <span className="font-medium text-gray-800 dark:text-gray-200 tracking-tight">
                      {detection.class}
                    </span>
                  </div>
                  <span
                    className={`font-bold px-2 py-1 rounded text-white text-xs transition-all duration-200 ${
                      hoveredIndex === index ? 'scale-110 shadow-md' : ''
                    }`}
                    style={{ backgroundColor: CLASS_COLORS[detection.class] || '#888888' }}
                  >
                    {(detection.confidence * 100).toFixed(1)}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Download Button - positioned at bottom right */}
      <div className="flex justify-end mt-6">
        <button
          className={`relative bg-mira-navy dark:bg-mira-blue text-white py-3 px-6 rounded-lg
            hover:shadow-lg hover:scale-[1.02] active:scale-[0.98]
            transition-all duration-200 font-medium tracking-wide btn-ripple overflow-hidden
            flex items-center space-x-2 group`}
          onClick={handleDownloadClick}
        >
          {/* Download icon with animation */}
          <svg
            className="w-5 h-5 transition-transform duration-200 group-hover:translate-y-0.5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
            />
          </svg>
          <span>Download Image</span>
        </button>
      </div>
    </div>
  );
}
