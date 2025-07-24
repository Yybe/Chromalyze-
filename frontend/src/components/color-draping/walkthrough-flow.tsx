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

  if (!currentColor) {
    return (
      <div className={styles.walkthroughError}>
        <p>No color data available</p>
        <button onClick={onBack}>Go Back</button>
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