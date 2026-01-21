'use client';

import { useState, useCallback, useEffect, useRef } from 'react';
import { toast } from 'sonner';

interface ImageUploadProps {
  onFileSelect: (file: File) => void;
  isLoading: boolean;
  previewUrl?: string | null;
}

export default function ImageUpload({ onFileSelect, isLoading, previewUrl }: ImageUploadProps) {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFileName, setSelectedFileName] = useState<string>('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Reset file input when previewUrl is cleared
  useEffect(() => {
    if (!previewUrl) {
      setSelectedFileName('');
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  }, [previewUrl]);

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      if (file.type.startsWith('image/')) {
        setSelectedFileName(file.name);
        onFileSelect(file);
      } else {
        toast.error('Invalid file type', {
          description: 'Please upload an image file (jpeg, jpg, png)',
        });
      }
    }
  }, [onFileSelect]);

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      if (file.type.startsWith('image/')) {
        setSelectedFileName(file.name);
        onFileSelect(file);
      } else {
        toast.error('Invalid file type', {
          description: 'Please upload an image file (jpeg, jpg, png)',
        });
      }
    }
  }, [onFileSelect]);

  return (
    <div className="w-full">
      {/* Center-aligned title */}
      <h2 className="text-2xl font-semibold text-center text-gray-900 dark:text-white mb-6 tracking-tight text-display">
        Upload Blade Turbine Image
      </h2>

      <p className="text-sm text-gray-600 dark:text-gray-400 mb-2 tracking-wide">
        Upload and attach images
      </p>
      <p className="text-xs text-gray-500 dark:text-gray-500 mb-4 uppercase tracking-wider font-medium">
        Supported formats: jpeg, jpg, png
      </p>

      <div
        className={`border-2 border-dashed rounded-xl overflow-hidden transition-all duration-300 ease-out
          ${previewUrl && !isLoading
            ? 'bg-white dark:bg-gray-800 p-4 border-mira-blue'
            : 'py-12 px-8 text-center bg-white dark:bg-gray-800 border-mira-blue hover:border-solid hover:border-[#2563eb] hover:shadow-[0_0_20px_rgba(74,144,226,0.3)] hover:bg-gradient-to-br hover:from-blue-50 hover:to-white dark:hover:from-gray-700 dark:hover:to-gray-800'
          }
          ${isLoading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
          ${dragActive ? 'border-solid border-[#2563eb] bg-gradient-to-br from-blue-50 to-white dark:from-gray-700 dark:to-gray-800 shadow-[0_0_25px_rgba(74,144,226,0.4)] scale-[1.01]' : ''}
        `}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={() => !isLoading && !previewUrl && document.getElementById('fileInput')?.click()}
      >
        <input
          ref={fileInputRef}
          id="fileInput"
          type="file"
          className="hidden"
          accept="image/jpeg,image/jpg,image/png"
          onChange={handleChange}
          disabled={isLoading}
        />

        {/* Show upload prompt when no image */}
        {!previewUrl && !isLoading && (
          <div className="flex flex-col items-center animate-fade-in">
            <div className={`text-mira-blue mb-4 transition-transform duration-300 ${dragActive ? 'scale-110 -translate-y-1' : ''}`}>
              <svg
                className={`w-10 h-10 mx-auto icon-hover ${dragActive ? 'animate-bounce' : ''}`}
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                strokeWidth={1.5}
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5"
                />
              </svg>
            </div>
            <p className="text-gray-700 dark:text-gray-300 font-medium mb-1 tracking-tight">
              Click to upload or drag and drop
            </p>
            <p className="text-sm text-gray-500 dark:text-gray-400">Maximum file size 50 MB.</p>
          </div>
        )}

        {/* Show image preview inside the dotted area */}
        {previewUrl && !isLoading && (
          <div className="flex items-center justify-center animate-fade-in">
            <img
              src={previewUrl}
              alt="Preview"
              className="max-w-full h-auto max-h-96 object-contain rounded-lg shadow-sm transition-transform duration-300 hover:scale-[1.02]"
            />
          </div>
        )}

        {/* Loading state */}
        {isLoading && (
          <div className="p-12 flex flex-col items-center">
            <div className="inline-block animate-spin rounded-full h-10 w-10 border-b-2 border-mira-blue mb-3"></div>
            <p className="text-gray-600 dark:text-gray-400">Analyzing image...</p>
          </div>
        )}
      </div>

      {selectedFileName && !isLoading && (
        <div className="mt-3 flex items-center space-x-2 text-sm text-green-600 dark:text-green-400 animate-slide-up">
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path
              fillRule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
              clipRule="evenodd"
            />
          </svg>
          <span className="font-medium">Selected: {selectedFileName}</span>
        </div>
      )}
    </div>
  );
}
