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
    <div className={`flex items-center justify-between w-full max-w-6xl mx-auto ${className}`}>
      {/* Progress Indicator - Left Side */}
      <div className="flex items-center gap-4 flex-1">
        <div className="text-sm font-semibold text-muted-foreground font-[Inter] whitespace-nowrap">
          {currentIndex + 1} of {totalColors}
        </div>
        <div className="flex-1 max-w-xs h-2 bg-secondary rounded-full overflow-hidden">
          <div
            className="h-full bg-primary rounded-full transition-all duration-500 ease-out"
            style={{ width: `${((currentIndex + 1) / totalColors) * 100}%` }}
          />
        </div>
      </div>

      {/* Navigation Buttons - Center */}
      <div className="flex gap-4 items-center">
        <Button
          variant="outline"
          size="default"
          onClick={onPrevious}
          disabled={!canGoPrevious}
          className="flex items-center gap-2 px-6 py-3 font-semibold transition-all duration-200 hover:bg-secondary/50 disabled:opacity-50 disabled:cursor-not-allowed min-h-[44px] min-w-[44px]"
          aria-label="Previous color"
        >
          <ChevronLeft size={18} />
          <span className="hidden sm:inline">Back</span>
        </Button>

        <Button
          size="default"
          onClick={onNext}
          disabled={!canGoNext}
          className="flex items-center gap-2 px-6 py-3 font-semibold bg-primary hover:bg-primary/90 text-primary-foreground transition-all duration-200 hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed min-h-[44px] min-w-[44px]"
          aria-label={canGoNext ? "Next color" : "Go to summary"}
        >
          <span className="hidden sm:inline">
            {currentIndex === totalColors - 1 ? 'Summary' : 'Next'}
          </span>
          <ChevronRight size={18} />
        </Button>
      </div>

      {/* Touch/Swipe Instructions - Right Side */}
      <div className="hidden lg:flex flex-1 justify-end">
        <span className="text-xs text-muted-foreground italic font-[Inter]">
          Swipe or use arrow keys to navigate
        </span>
      </div>
    </div>
  );
};

export default NavigationControls;