'use client';

import React, { useState, useEffect } from 'react';
import Image from 'next/image';
import { DrapingColor } from '@/lib/color-draping-types';
import { FabricOverlay } from './fabric-overlay';
import styles from './photo-with-fabric.module.css';

interface PhotoWithFabricProps {
  userPhoto: string;
  currentColor: DrapingColor;
  isTransitioning: boolean;
  className?: string;
  showSkinEffect?: boolean;
}

export const PhotoWithFabric: React.FC<PhotoWithFabricProps> = ({
  userPhoto,
  currentColor,
  isTransitioning,
  className = '',
  showSkinEffect = true
}) => {
  const [imageLoaded, setImageLoaded] = useState(false);
  const [imageError, setImageError] = useState(false);
  const [skinEffectIntensity, setSkinEffectIntensity] = useState(0);

  const handleImageLoad = () => {
    setImageLoaded(true);
  };

  const handleImageError = () => {
    setImageError(true);
  };

  // Calculate skin effect based on color verdict
  useEffect(() => {
    if (showSkinEffect && imageLoaded) {
      const intensity = currentColor.verdict === 'best' ? 0.15 : -0.1;
      setSkinEffectIntensity(intensity);
    }
  }, [currentColor, showSkinEffect, imageLoaded]);

  // Generate enhanced skin effect filter based on color
  const getSkinEffectFilter = () => {
    if (!showSkinEffect || skinEffectIntensity === 0) return '';

    if (currentColor.verdict === 'best') {
      // Enhance skin for good colors - brighter, more vibrant, healthier glow
      return `brightness(${1 + skinEffectIntensity * 0.4}) saturate(${1 + skinEffectIntensity * 0.3}) contrast(${1 + skinEffectIntensity * 0.15}) hue-rotate(${skinEffectIntensity * 5}deg)`;
    } else {
      // Diminish skin for bad colors - duller, sallow, tired appearance
      return `brightness(${1 + skinEffectIntensity * 0.6}) saturate(${1 + skinEffectIntensity * 0.4}) contrast(${1 + skinEffectIntensity * 0.1}) hue-rotate(${skinEffectIntensity * 25}deg) sepia(${Math.abs(skinEffectIntensity) * 0.2})`;
    }
  };

  if (imageError) {
    return (
      <div className={`${styles.photoWithFabricContainer} ${className}`}>
        <div className={styles.photoPlaceholder}>
          <div className={styles.photoError}>
            <div className={styles.errorIcon}>📷</div>
            <p className={styles.errorText}>Unable to load photo</p>
            <button 
              onClick={() => {
                setImageError(false);
                setImageLoaded(false);
              }}
              className={styles.retryButton}
            >
              Try Again
            </button>
          </div>
        </div>
        <FabricOverlay 
          color={currentColor} 
          isTransitioning={isTransitioning}
        />
      </div>
    );
  }

  return (
    <div className={`${styles.photoWithFabricContainer} ${className}`}>
      {/* User photo with skin effect */}
      <div className={`${styles.photoWrapper} ${imageLoaded ? styles.loaded : styles.loading}`}>
        <div className={styles.photoContainer}>
          <Image
            src={userPhoto}
            alt="Your photo for color analysis"
            fill
            className={styles.userPhoto}
            style={{
              objectFit: 'cover',
              filter: getSkinEffectFilter(),
              transition: 'filter 0.6s ease-in-out'
            }}
            onLoad={handleImageLoad}
            onError={handleImageError}
            priority
            sizes="(max-width: 768px) 100vw, (max-width: 1200px) 80vw, 60vw"
          />
        </div>

        {/* Professional photo frame */}
        <div className={styles.photoFrame} />

        {/* Subtle positive glow for good colors */}
        {currentColor.verdict === 'best' && imageLoaded && (
          <div className={styles.positiveGlow} />
        )}
      </div>

      {/* Fabric overlay positioned under chin with realistic draping */}
      <FabricOverlay
        color={currentColor}
        isTransitioning={isTransitioning}
      />
    </div>
  );
};

export default PhotoWithFabric;