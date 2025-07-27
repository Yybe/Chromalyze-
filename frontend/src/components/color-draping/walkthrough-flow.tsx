'use client';

import React, { useState, useCallback } from 'react';
import { ColorDrapingData } from '@/lib/color-draping-types';
import { useSwipeGesture } from '@/hooks/use-swipe-gesture';
import PhotoWithFabric from './photo-with-fabric';
import ColorDetails from './color-details';
import NavigationControls from './navigation-controls';
import styles from './walkthrough-flow.module.css';

interface WalkthroughFlowProps {
  drapingData: ColorDrapingData;
  onComplete: () => void;
  onBack: () => void;
  className?: string;
}

export const WalkthroughFlow: React.FC<WalkthroughFlowProps> = ({
  drapingData,
  onComplete,
  onBack,
  className = ''
}) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isTransitioning, setIsTransitioning] = useState(false);

  const currentColor = drapingData.colors[currentIndex];
  const totalColors = drapingData.colors.length;

  const handleNext = useCallback(() => {
    if (currentIndex === totalColors - 1) {
      // Last color, go to summary
      onComplete();
      return;
    }

    setIsTransitioning(true);
    setTimeout(() => {
      setCurrentIndex(prev => prev + 1);
      setIsTransitioning(false);
    }, 200);
  }, [currentIndex, totalColors, onComplete]);

  const handlePrevious = useCallback(() => {
    if (currentIndex === 0) {
      onBack();
      return;
    }

    setIsTransitioning(true);
    setTimeout(() => {
      setCurrentIndex(prev => prev - 1);
      setIsTransitioning(false);
    }, 200);
  }, [currentIndex, onBack]);

  // Swipe gesture support
  useSwipeGesture({
    onSwipeLeft: handleNext,
    onSwipeRight: handlePrevious,
    threshold: 50,
    preventScroll: true
  });

  const canGoPrevious = currentIndex > 0;
  const canGoNext = true; // Always can go next (either to next color or summary)

  // Check if we have valid color data
  if (!drapingData.colors || drapingData.colors.length === 0 || !currentColor) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center p-4">
        <div className="max-w-md w-full text-center space-y-6">
          <div className="w-16 h-16 mx-auto bg-destructive/10 rounded-full flex items-center justify-center">
            <span className="text-2xl">🎨</span>
          </div>
          <div className="space-y-2">
            <h2 className="text-2xl font-bold text-foreground font-[Inter]">No Color Data Available</h2>
            <p className="text-muted-foreground font-[Inter]">
              We couldn't find any color recommendations for your walkthrough. This might be due to an issue with your analysis data.
            </p>
          </div>
          <div className="flex flex-col gap-3">
            <button
              onClick={onBack}
              className="px-6 py-3 bg-primary hover:bg-primary/90 text-primary-foreground rounded-md font-medium transition-colors"
            >
              Go Back
            </button>
            <button
              onClick={() => window.location.href = '/analyze'}
              className="px-6 py-3 border border-border hover:bg-secondary/50 text-foreground rounded-md font-medium transition-colors"
            >
              Start New Analysis
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`${styles.walkthroughFlow} ${className}`}>
      {/* Photo with fabric overlay */}
      <div className={styles.photoSection}>
        <PhotoWithFabric
          userPhoto={drapingData.userPhoto}
          currentColor={currentColor}
          isTransitioning={isTransitioning}
          showSkinEffect={true}
        />
      </div>

      {/* Color information */}
      <div className={styles.detailsSection}>
        <ColorDetails
          color={currentColor}
          isVisible={!isTransitioning}
        />
      </div>

      {/* Navigation controls */}
      <div className={styles.navigationSection}>
        <NavigationControls
          currentIndex={currentIndex}
          totalColors={totalColors}
          onPrevious={handlePrevious}
          onNext={handleNext}
          canGoPrevious={canGoPrevious}
          canGoNext={canGoNext}
        />
      </div>
    </div>
  );
};

export default WalkthroughFlow;