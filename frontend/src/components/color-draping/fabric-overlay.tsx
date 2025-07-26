'use client';

import React from 'react';
import { DrapingColor } from '@/lib/color-draping-types';
import { getFabricTexture } from '@/lib/color-draping-utils';
import styles from './fabric-overlay.module.css';

interface FabricOverlayProps {
  color: DrapingColor;
  isTransitioning: boolean;
  className?: string;
}

export const FabricOverlay: React.FC<FabricOverlayProps> = ({
  color,
  isTransitioning,
  className = ''
}) => {
  const fabricType = getFabricTexture(color);

  return (
    <div className={`${styles.fabricOverlayContainer} ${className}`}>
      {/* Main fabric swatch with realistic draping */}
      <div
        className={`${styles.fabricSwatch} ${styles[`fabric${fabricType.charAt(0).toUpperCase() + fabricType.slice(1)}`]} ${isTransitioning ? styles.transitioning : ''}`}
        style={{
          '--fabric-color': color.hex,
          backgroundColor: color.hex
        } as React.CSSProperties}
        data-fabric-type={fabricType}
        data-color={color.hex}
      >
        {/* Fabric texture overlay */}
        <div className={styles.fabricTexture} />

        {/* Subtle fabric weave pattern */}
        <div className={styles.fabricWeave} />

        {/* Soft highlight for realism */}
        <div className={styles.fabricHighlight} />

        {/* Fabric shadow for depth */}
        <div className={styles.fabricShadow} />

        {/* Draping fold effect */}
        <div className={styles.fabricFold} />
      </div>
    </div>
  );
};

export default FabricOverlay;