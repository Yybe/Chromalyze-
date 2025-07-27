'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { ComprehensiveAnalysisResult } from '@/lib/analysis-service';
import ColorDrapingWalkthrough from '@/components/color-draping/color-draping-walkthrough';

interface WalkthroughPageProps {
  params: {
    id: string;
  };
}

export default function WalkthroughPage({ params }: WalkthroughPageProps) {
  const router = useRouter();
  const [analysisResult, setAnalysisResult] = useState<ComprehensiveAnalysisResult | null>(null);
  const [userPhotoUrl, setUserPhotoUrl] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [originalAnalysisId, setOriginalAnalysisId] = useState<string | null>(null);

  useEffect(() => {
    const loadAnalysisData = async () => {
      try {
        setLoading(true);
        setError(null);

        // Check if the data exists in sessionStorage
        const storedResult = sessionStorage.getItem(`analysis_${params.id}`);
        const storedPhoto = sessionStorage.getItem(`photo_${params.id}`);
        const storedOriginalId = sessionStorage.getItem(`original_id_${params.id}`);

        if (!storedResult || !storedPhoto) {
          throw new Error('Analysis data not found');
        }

        const result: ComprehensiveAnalysisResult = JSON.parse(storedResult);
        setAnalysisResult(result);
        setUserPhotoUrl(storedPhoto);
        setOriginalAnalysisId(storedOriginalId);
      } catch (err) {
        console.error('Failed to load analysis data:', err);
        setError('Analysis data not found. Please start a new analysis.');
      } finally {
        setLoading(false);
      }
    };

    if (params.id) {
      loadAnalysisData();
    }
  }, [params.id]);

  const handleViewFullAnalysis = () => {
    // Set flag to skip entry screen and go directly to full analysis
    sessionStorage.setItem('fromWalkthrough', 'true');
    // Always redirect to the full analysis results page for this analysis ID
    router.push(`/analyze/${params.id}`);
  };

  if (loading) {
    return (
      <div className="walkthrough-page-loading">
        <div className="loading-content">
          <div className="loading-spinner">
            <div className="spinner" />
          </div>
          <h2>Loading Your Analysis...</h2>
          <p>Preparing your color walkthrough experience</p>
        </div>
      </div>
    );
  }

  if (error || !analysisResult) {
    return (
      <div className="walkthrough-page-error">
        <div className="error-content">
          <h2>Analysis Not Found</h2>
          <p>{error || 'We couldn\'t find your analysis data.'}</p>
          <div className="error-actions">
            <button 
              onClick={() => router.push('/analyze')}
              className="error-button primary"
            >
              Start New Analysis
            </button>
            <button 
              onClick={() => router.back()}
              className="error-button secondary"
            >
              Go Back
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="walkthrough-page">
      <ColorDrapingWalkthrough
        analysisResult={analysisResult}
        userPhotoUrl={userPhotoUrl}
        analysisId={params.id}
        onViewFullAnalysis={handleViewFullAnalysis}
      />
    </div>
  );
}