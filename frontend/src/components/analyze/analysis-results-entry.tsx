'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { ComprehensiveAnalysisResult } from '@/lib/analysis-service';
import { transformToColorDrapingData, transformBasicAnalysisToColorDrapingData } from '@/lib/color-draping-utils';
import EntryScreen from '@/components/color-draping/entry-screen';
import ResultsDisplay from '@/app/analyze/[id]/results-display';

interface AnalysisResult {
  face_shape: string;
  color_season: string;
  faces_detected?: number;
  palette?: {
    description: string;
    recommended: { name: string; hex: string; }[];
    avoid: { name: string; hex: string; }[];
  };
  face_shape_recommendations?: any;
}

interface AnalysisResultsEntryProps {
  results: AnalysisResult;
  analysisId: string;
  userPhotoUrl?: string;
}

export const AnalysisResultsEntry: React.FC<AnalysisResultsEntryProps> = ({
  results,
  analysisId,
  userPhotoUrl
}) => {
  const router = useRouter();
  const [showChoice, setShowChoice] = useState(true);
  const [hasWalkthroughData, setHasWalkthroughData] = useState(false);

  useEffect(() => {
    // Check if we have the necessary data for walkthrough
    const checkWalkthroughData = () => {
      const hasColorData = results.palette && 
        results.palette.recommended && 
        results.palette.recommended.length > 0;
      
      const hasPhoto = Boolean(userPhotoUrl && userPhotoUrl.length > 0);
      
      setHasWalkthroughData(Boolean(hasColorData && hasPhoto));
    };

    checkWalkthroughData();
  }, [results, userPhotoUrl]);

  const handleViewFullAnalysis = () => {
    setShowChoice(false);
  };

  const handleStartWalkthrough = () => {
    // Store the analysis data for the walkthrough page
    if (userPhotoUrl) {
      // Use the basic analysis transformation to get accurate color data
      const drapingData = transformBasicAnalysisToColorDrapingData(
        results,
        userPhotoUrl,
        analysisId
      );

      // Convert to ComprehensiveAnalysisResult format for compatibility
      const comprehensiveResult: ComprehensiveAnalysisResult = {
        faceShape: {
          faceShape: results.face_shape as any,
          confidence: 0.8,
          landmarks: [],
          measurements: {
            faceWidth: 100,
            faceHeight: 120,
            jawWidth: 80,
            foreheadWidth: 90,
            cheekboneWidth: 95,
            faceRatio: 1.2,
            jawlineAngle: 45
          }
        },
        colorSeason: {
          season: results.color_season as any,
          undertone: 'neutral' as any,
          confidence: 0.8,
          dominantColors: [{ L: 50, a: 0, b: 0 }],
          skinTone: { L: 50, a: 0, b: 0 },
          contrast: 0.5,
          chroma: 20,
          lightness: 50,
          recommendations: {
            bestColors: results.palette?.recommended.map(c => c.name) || [],
            avoidColors: results.palette?.avoid.map(c => c.name) || [],
            neutrals: ['Gray', 'Beige', 'Navy'],
            metals: ['Silver', 'Gold']
          }
        },
        recommendations: {
          hairstyles: [],
          colors: {
            primary: results.palette?.recommended.slice(0, 4).map(c => c.hex) || [],
            secondary: results.palette?.recommended.slice(4, 8).map(c => c.hex) || [],
            accent: results.palette?.recommended.slice(8, 12).map(c => c.hex) || [],
            neutrals: ['#808080', '#F5F5DC', '#000080'],
            metals: ['Silver', 'Gold'],
            avoid: results.palette?.avoid.map(c => c.hex) || []
          },
          accessories: [],
          makeup: {
            foundation: [],
            lipColors: [],
            eyeColors: [],
            blush: [],
            techniques: []
          },
          styling: {
            clothing: [],
            patterns: [],
            necklines: [],
            general: []
          }
        },
        confidence: 0.8,
        processingTime: 1000
      };

      // Store both the comprehensive result and the draping data
      sessionStorage.setItem(`analysis_${analysisId}`, JSON.stringify(comprehensiveResult));
      sessionStorage.setItem(`draping_${analysisId}`, JSON.stringify(drapingData));
      sessionStorage.setItem(`photo_${analysisId}`, userPhotoUrl);
      // Store the original analysis ID for navigation back to full analysis
      sessionStorage.setItem(`original_id_${analysisId}`, analysisId);
    }

    router.push(`/analyze/${analysisId}/walkthrough`);
  };

  if (!showChoice || !hasWalkthroughData) {
    return <ResultsDisplay results={results} userPhotoUrl={userPhotoUrl} />;
  }

  return (
    <EntryScreen
      onViewFullAnalysis={handleViewFullAnalysis}
      onStartWalkthrough={handleStartWalkthrough}
      analysisComplete={true}
    />
  );
};

export default AnalysisResultsEntry;