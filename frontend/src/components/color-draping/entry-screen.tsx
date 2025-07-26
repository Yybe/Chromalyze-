'use client';

import React from 'react';
import { Palette, Eye, ArrowRight, CheckCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
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
        <Card className="max-w-2xl w-full shadow-lg">
          <CardContent className="p-8 text-center">
            <div className="animate-spin w-12 h-12 border-4 border-primary/20 border-t-primary rounded-full mx-auto mb-6"></div>
            <h1 className={styles.entryTitle}>Analyzing Your Colors...</h1>
            <p className={styles.entrySubtitle}>
              Please wait while we process your photo and determine your perfect color palette.
            </p>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className={`${styles.entryScreen} ${className}`}>
      <Card className="max-w-2xl w-full shadow-lg">
        <CardContent className="p-8 text-center">
          {/* Welcome Message */}
          <div className={styles.welcomeSection}>
            <div className={styles.successIcon}>
              <CheckCircle size={48} />
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
          <div className="flex flex-col gap-4 mt-8 mb-8">
            <Button
              onClick={onStartWalkthrough}
              size="lg"
              className="h-14 text-lg font-semibold bg-gradient-to-r from-primary to-primary/90 hover:from-primary/90 hover:to-primary text-primary-foreground shadow-lg hover:shadow-xl transition-all duration-200"
            >
              <Palette className="mr-3 h-5 w-5" />
              Walk Through Your Palette
              <ArrowRight className="ml-3 h-5 w-5" />
            </Button>

            <Button
              onClick={onViewFullAnalysis}
              variant="outline"
              size="lg"
              className="h-12 text-base font-medium border-2 hover:bg-secondary/50 transition-all duration-200"
            >
              <Eye className="mr-2 h-4 w-4" />
              View Full Analysis
            </Button>
          </div>

          {/* Feature Highlights */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-muted-foreground">
            <div className="flex flex-col items-center gap-2 p-4 rounded-lg bg-secondary/20">
              <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
                <Palette className="h-4 w-4 text-primary" />
              </div>
              <div className="text-center">
                <h3 className="font-medium text-foreground mb-1">Interactive Draping</h3>
                <p className="text-xs">See each color against your photo like a real styling session</p>
              </div>
            </div>
            <div className="flex flex-col items-center gap-2 p-4 rounded-lg bg-secondary/20">
              <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
                <CheckCircle className="h-4 w-4 text-primary" />
              </div>
              <div className="text-center">
                <h3 className="font-medium text-foreground mb-1">Personalized Feedback</h3>
                <p className="text-xs">Learn why each color works or doesn't work for you</p>
              </div>
            </div>
            <div className="flex flex-col items-center gap-2 p-4 rounded-lg bg-secondary/20">
              <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
                <ArrowRight className="h-4 w-4 text-primary" />
              </div>
              <div className="text-center">
                <h3 className="font-medium text-foreground mb-1">Easy Navigation</h3>
                <p className="text-xs">Swipe or click to navigate through your colors</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default EntryScreen;