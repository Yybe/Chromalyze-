'use client';

import React, { useState, useEffect } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { ComprehensiveAnalysisResult } from '@/lib/analysis-service';
import { transformToColorDrapingData, transformBasicAnalysisToColorDrapingData } from '@/lib/color-draping-utils';
import EntryScreen from '@/components/color-draping/entry-screen';

interface BasicAnalysisResult {
  face_shape: string;
  color_season: string;
  note?: string;
}

export default function AnalysisEntryPage() {
  const router = useRouter();
  const params = useParams();
  const id = params.id as string;
  
  const [analysisResults, setAnalysisResults] = useState<ComprehensiveAnalysisResult | BasicAnalysisResult | null>(null);
  const [userPhotoUrl, setUserPhotoUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Load analysis results from session storage
    const analysisData = sessionStorage.getItem(`analysis_${id}`);
    const photoData = sessionStorage.getItem(`photo_${id}`);
    
    if (analysisData) {
      try {
        const parsedData = JSON.parse(analysisData);
        setAnalysisResults(parsedData);
      } catch (error) {
        console.error('Failed to parse analysis data:', error);
        router.push('/analyze');
        return;
      }
    } else {
      // No analysis data found, redirect to upload
      router.push('/analyze');
      return;
    }
    
    if (photoData) {
      setUserPhotoUrl(photoData);
    }
    
    setLoading(false);
  }, [id, router]);

  const handleViewFullAnalysis = () => {
    // Navigate to the full analysis results page
    router.push(`/analyze/${id}`);
  };

  const handleStartWalkthrough = () => {
    // Navigate to the walkthrough page
    router.push(`/analyze/${id}/walkthrough`);
  };

  if (loading) {
    return (
      <div className="container flex-1 py-6 md:py-12">
        <div className="mx-auto flex max-w-[800px] flex-col items-center space-y-4">
          <div className="animate-spin w-12 h-12 border-4 border-primary/20 border-t-primary rounded-full"></div>
          <p className="text-muted-foreground">Loading your analysis...</p>
        </div>
      </div>
    );
  }

  if (!analysisResults) {
    return (
      <div className="container flex-1 py-6 md:py-12">
        <div className="mx-auto flex max-w-[800px] flex-col items-center space-y-4">
          <h1 className="text-3xl font-bold tracking-tight text-destructive">Analysis Not Found</h1>
          <p className="text-center text-muted-foreground">
            We couldn't find your analysis results. Please try uploading your image again.
          </p>
          <button 
            onClick={() => router.push('/analyze')}
            className="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90"
          >
            Start New Analysis
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container flex-1 py-6 md:py-12">
      <div className="mx-auto flex max-w-[800px] flex-col items-center">
        <EntryScreen
          onViewFullAnalysis={handleViewFullAnalysis}
          onStartWalkthrough={handleStartWalkthrough}
          analysisComplete={true}
        />
      </div>
    </div>
  );
}
