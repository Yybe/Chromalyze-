'use client';

import React from 'react';
import { Palette, Eye, ArrowRight } from 'lucide-react';
import styles from './entry-screen.module.css';

interface EntryScreenProps {
  onViewFullAnalysis: () => void;
  onStartWalkthrough: () => void;
  analysisComplete: boolean;
  className?: string;
}

export const EntryScreen: React.FC<EntryScreenProps> = ({
  onViewFullAnalysis,
  onStartWalkthrough,
  analysisComplete,
  className = ''
}) => {
  if (!analysisComplete) {
    return (
      <div className={`${styles.entryScreen} ${className}`}>
        <div className={styles.entryContent}>
          <h1 className={styles.entryTitle}>Analyzing Your Colors...</h1>
          <p className={styles.entrySubtitle}>
            Please wait while we process your photo and determine your perfect color palette.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className={`${styles.entryScreen} ${className}`}>
      <div className={styles.entryContent}>
        {/* Welcome Message */}
        <div className={styles.welcomeSection}>
          <div className={styles.successIcon}>
            <Palette size={48} />
          </div>
          <h1 className={styles.entryTitle}>
            Your Color Analysis is Ready!
          </h1>
          <p className={styles.entrySubtitle}>
            Discover your perfect colors through an immersive draping experience, 
            or view your complete analysis results.
          </p>
        </div>

        {/* Action Buttons */}
        <div className={styles.actionButtons}>
          <button
            onClick={onStartWalkthrough}
            className={styles.primaryAction}
          >
            <Palette className={styles.buttonIcon} size={20} />
            <span>Walk Through Your Palette</span>
            <ArrowRight className={styles.buttonIcon} size={20} />
          </button>

          <button
            onClick={onViewFullAnalysis}
            className={styles.secondaryAction}
          >
            <Eye className={styles.buttonIcon} size={20} />
            <span>View Full Analysis</span>
          </button>
        </div>

        {/* Feature Highlights */}
        <div className={styles.featureHighlights}>
          <div className={styles.feature}>
            <div className={styles.featureIcon}>🎨</div>
            <div className={styles.featureText}>
              <h3>Interactive Draping</h3>
              <p>See each color against your photo like a real styling session</p>
            </div>
          </div>
          <div className={styles.feature}>
            <div className={styles.featureIcon}>✨</div>
            <div className={styles.featureText}>
              <h3>Personalized Feedback</h3>
              <p>Learn why each color works or doesn't work for you</p>
            </div>
          </div>
          <div className={styles.feature}>
            <div className={styles.featureIcon}>📱</div>
            <div className={styles.featureText}>
              <h3>Swipe to Navigate</h3>
              <p>Easy touch controls for a smooth experience</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EntryScreen;