'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { ComprehensiveAnalysisResult } from '@/lib/analysis-service';
import EntryScreen from '@/components/color-draping/entry-screen';
import EnhancedResults from './enhanced-results';

interface EnhancedResultsEntryProps {
  results: ComprehensiveAnalysisResult;
  userPhotoUrl?: string;
}

export const EnhancedResultsEntry: React.FC<EnhancedResultsEntryProps> = ({
  results,
  userPhotoUrl
}) => {
  const router = useRouter();
  const [showChoice, setShowChoice] = useState(true);

  const handleViewFullAnalysis = () => {
    setShowChoice(false);
  };

  const handleStartWalkthrough = () => {
    if (userPhotoUrl) {
      // Generate a unique ID for this analysis
      const analysisId = `enhanced_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

      // Store data for walkthrough page
      sessionStorage.setItem(`analysis_${analysisId}`, JSON.stringify(results));
      sessionStorage.setItem(`photo_${analysisId}`, userPhotoUrl);
      // Mark this as an enhanced analysis (no original backend ID)
      sessionStorage.setItem(`original_id_${analysisId}`, 'enhanced');

      // Navigate to walkthrough
      router.push(`/analyze/${analysisId}/walkthrough`);
    }
  };

  // Check if we have the necessary data for walkthrough
  const hasWalkthroughData = userPhotoUrl && 
    results.recommendations.colors.primary.length > 0;

  if (!showChoice || !hasWalkthroughData) {
    return <EnhancedResults results={results} />;
  }

  return (
    <EntryScreen
      onViewFullAnalysis={handleViewFullAnalysis}
      onStartWalkthrough={handleStartWalkthrough}
      analysisComplete={true}
    />
  );
};

export default EnhancedResultsEntry;