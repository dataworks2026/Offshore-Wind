'use client';

import { useState } from 'react';
import { toast } from 'sonner';
import Navbar from '@/components/Navbar';
import ImageUpload from '@/components/ImageUpload';
import DetectionResults from '@/components/DetectionResults';
import ProgressLoader from '@/components/ProgressLoader';
import { predictDamage, InferenceResponse } from '@/lib/api';

export default function Home() {
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState<InferenceResponse | null>(null);
  const [imageUrl, setImageUrl] = useState<string | null>(null);

  const handleFileSelect = async (file: File) => {
    setIsLoading(true);
    setResults(null);

    // Show upload started toast
    toast.loading('Processing image...', { id: 'processing' });

    try {
      // Create preview URL
      const url = URL.createObjectURL(file);
      setImageUrl(url);

      // Call API
      const response = await predictDamage(file);
      setResults(response);

      // Dismiss loading toast and show success
      toast.dismiss('processing');

      if (response.total_detections === 0) {
        toast.success('Analysis complete!', {
          description: 'No damages detected in this image.',
          duration: 5000,
        });
      } else {
        toast.success('Analysis complete!', {
          description: `Found ${response.total_detections} damage${response.total_detections > 1 ? 's' : ''}: ${response.damages_found.join(', ')}`,
          duration: 5000,
        });
      }
    } catch (err: any) {
      console.error('Error during inference:', err);

      // Dismiss loading toast and show error
      toast.dismiss('processing');

      const errorMessage =
        err.response?.data?.message ||
        err.message ||
        'Failed to process image. Please try again.';

      toast.error('Detection failed', {
        description: errorMessage,
        duration: 6000,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleClear = () => {
    setResults(null);
    setImageUrl(null);
    toast.info('Cleared', {
      description: 'Ready for a new upload.',
      duration: 2000,
    });
  };

  return (
    <div className="min-h-screen bg-gray-200 dark:bg-gray-900 transition-colors duration-300">
      <Navbar />

      <main className="px-4 sm:px-6 lg:px-8 py-4 sm:py-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6 max-w-[1400px] mx-auto">
          {/* Left Column - Upload */}
          <div className="panel-gradient rounded-2xl p-4 sm:p-6 shadow-sm border border-gray-200 dark:border-gray-700 min-h-[400px] sm:min-h-[500px] lg:min-h-[calc(100vh-120px)] transition-all duration-300">
            <ImageUpload onFileSelect={handleFileSelect} isLoading={isLoading} previewUrl={imageUrl} />

            {imageUrl && !isLoading && (
              <button
                onClick={handleClear}
                className="mt-4 w-full bg-mira-navy dark:bg-mira-blue text-white py-2.5 sm:py-3 px-4 rounded-lg
                  hover:bg-opacity-90 hover:shadow-lg hover:scale-[1.01] active:scale-[0.99]
                  transition-all duration-200 font-medium text-sm sm:text-base tracking-wide
                  btn-ripple flex items-center justify-center space-x-2 group"
              >
                {/* Refresh icon */}
                <svg
                  className="w-4 h-4 transition-transform duration-300 group-hover:rotate-180"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                  />
                </svg>
                <span>Clear and Upload New Image</span>
              </button>
            )}
          </div>

          {/* Right Column - Results */}
          <div className="panel-gradient rounded-2xl p-4 sm:p-6 shadow-sm border border-gray-200 dark:border-gray-700 min-h-[400px] sm:min-h-[500px] lg:min-h-[calc(100vh-120px)] flex flex-col transition-all duration-300">
            {/* Center-aligned title - always visible */}
            <h2 className="text-xl sm:text-2xl font-semibold text-center text-gray-900 dark:text-white mb-4 sm:mb-6 tracking-tight text-display">
              Detected Damages
            </h2>

            {!results && !isLoading && (
              <div className="flex-1 flex flex-col animate-fade-in">
                {/* Placeholder image box */}
                <div className="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-xl bg-gray-50 dark:bg-gray-800 flex-1 min-h-[200px] sm:min-h-[300px] flex items-center justify-center mb-4 sm:mb-6 transition-colors duration-300">
                  <div className="text-center p-4 sm:p-8">
                    <svg
                      className="w-12 h-12 sm:w-16 sm:h-16 mx-auto mb-3 sm:mb-4 text-gray-300 dark:text-gray-600"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={1.5}
                        d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                      />
                    </svg>
                    <p className="text-gray-400 dark:text-gray-500 text-xs sm:text-sm tracking-wide">
                      Detection results will appear here
                    </p>
                  </div>
                </div>

                {/* Placeholder damages list */}
                <div className="space-y-2 sm:space-y-3">
                  <h3 className="text-base sm:text-lg font-semibold text-gray-400 dark:text-gray-500 text-heading">
                    Damages Found:
                  </h3>
                  <div className="p-3 sm:p-4 bg-gray-50 dark:bg-gray-800 border border-dashed border-gray-300 dark:border-gray-600 rounded-lg transition-colors duration-300">
                    <p className="text-gray-400 dark:text-gray-500 text-xs sm:text-sm text-center tracking-wide">
                      Upload an image to see detection results
                    </p>
                  </div>
                </div>
              </div>
            )}

            {isLoading && <ProgressLoader isLoading={isLoading} />}

            {results && <DetectionResults results={results} imageUrl={imageUrl} />}
          </div>
        </div>
      </main>
    </div>
  );
}
