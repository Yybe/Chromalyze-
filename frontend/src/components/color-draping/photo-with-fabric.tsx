'use client';

import React, { useState } from 'react';
import Image from 'next/image';
import { DrapingColor } from '@/lib/color-draping-types';
import { FabricOverlay } from './fabric-overlay';
import styles from './photo-with-fabric.module.css';

interface PhotoWithFabricProps {
  userPhoto: string;
  currentColor: DrapingColor;
  isTransitioning: boolean;
  className?: string;
}

export const PhotoWithFabric: React.FC<PhotoWithFabricProps> = ({
  userPhoto,
  currentColor,
  isTransitioning,
  className = ''
}) => {
  const [imageLoaded, setImageLoaded] = useState(false);
  const [imageError, setImageError] = useState(false);

  const handleImageLoad = () => {
    setImageLoaded(true);
  };

  const handleImageError = () => {
    setImageError(true);
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
      {/* User photo */}
      <div className={`${styles.photoWrapper} ${imageLoaded ? styles.loaded : styles.loading}`}>
        <Image
          src={userPhoto}
          alt="Your photo for color analysis"
          fill
          className={styles.userPhoto}
          onLoad={handleImageLoad}
          onError={handleImageError}
          priority
          sizes="(max-width: 768px) 100vw, (max-width: 1200px) 80vw, 60vw"
        />
        
        {/* Professional photo frame */}
        <div className={styles.photoFrame} />
      </div>
      
      {/* Fabric overlay positioned under chin */}
      <FabricOverlay 
        color={currentColor} 
        isTransitioning={isTransitioning}
      />
    </div>
  );
};

export default PhotoWithFabric;