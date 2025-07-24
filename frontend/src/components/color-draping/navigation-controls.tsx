'use client';

import React, { useEffect } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface NavigationControlsProps {
  currentIndex: number;
  totalColors: number;
  onPrevious: () => void;
  onNext: () => void;
  canGoPrevious: boolean;
  canGoNext: boolean;
  className?: string;
}

export const NavigationControls: React.FC<NavigationControlsProps> = ({
  currentIndex,
  totalColors,
  onPrevious,
  onNext,
  canGoPrevious,
  canGoNext,
  className = ''
}) => {
  // Keyboard navigation
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      switch (event.key) {
        case 'ArrowLeft':
          if (canGoPrevious) {
            event.preventDefault();
            onPrevious();
          }
          break;
        case 'ArrowRight':
        case ' ':
        case 'Enter':
          if (canGoNext) {
            event.preventDefault();
            onNext();
          }
          break;
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [canGoPrevious, canGoNext, onPrevious, onNext]);

  return (
    <div className={`p-8 flex flex-col items-center gap-6 max-w-2xl mx-auto ${className}`}>
      {/* Progress Indicator */}
      <div className="flex flex-col items-center gap-3 w-full">
        <div className="text-sm font-semibold text-gray-600 uppercase tracking-wide">
          {currentIndex + 1} of {totalColors}
        </div>
        <div className="w-full max-w-sm h-1 bg-gray-200 rounded-full overflow-hidden">
          <div 
            className="h-full bg-gradient-to-r from-blue-500 to-blue-600 rounded-full transition-all duration-500 ease-out"
            style={{ width: `${((currentIndex + 1) / totalColors) * 100}%` }}
          />
        </div>
      </div>

      {/* Navigation Buttons */}
      <div className="flex gap-4 items-center">
        <Button
          variant="outline"
          size="lg"
          onClick={onPrevious}
          disabled={!canGoPrevious}
          className="flex items-center gap-2 px-6 py-3 font-semibold rounded-full min-w-[120px] justify-center transition-all duration-200"
          aria-label="Previous color"
        >
          <ChevronLeft size={20} />
          <span className="hidden sm:inline">Back</span>
        </Button>

        <Button
          size="lg"
          onClick={onNext}
          disabled={!canGoNext}
          className="flex items-center gap-2 px-6 py-3 font-semibold rounded-full min-w-[120px] justify-center bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white border-none transition-all duration-200 hover:-translate-y-0.5 hover:shadow-lg"
          aria-label={canGoNext ? "Next color" : "Go to summary"}
        >
          <span className="hidden sm:inline">
            {currentIndex === totalColors - 1 ? 'Summary' : 'Next'}
          </span>
          <ChevronRight size={20} />
        </Button>
      </div>

      {/* Touch/Swipe Instructions */}
      <div className="mt-2 hidden sm:block">
        <span className="text-xs text-gray-500 italic">
          Swipe or use arrow keys to navigate
        </span>
      </div>
    </div>
  );
};

export default NavigationControls;