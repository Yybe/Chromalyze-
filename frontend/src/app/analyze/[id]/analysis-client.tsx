"use client"

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import ResultsDisplay from './results-display'

interface ColorObject {
  name: string;
  hex: string;
}

interface Palette {
  description: string;
  recommended: ColorObject[];
  avoid: ColorObject[];
}

interface FaceShapeRecommendations {
  description: string;
  strengths: string[];
  hairstyles: {
    recommended: string[];
    avoid: string[];
  };
  makeup: {
    contouring: string;
    eyebrows: string;
    eyes: string;
    lips: string;
  };
  accessories: {
    earrings: string;
    glasses: string;
    hats: string;
  };
}

interface AnalysisResult {
  face_shape: string;
  color_season: string;
  faces_detected?: number;
  palette?: Palette;
  face_shape_recommendations?: FaceShapeRecommendations;
}

export default function AnalysisClient({ id }: { id: string }) {
  const router = useRouter()
  const [status, setStatus] = useState<'pending' | 'processing' | 'completed' | 'error'>('pending')
  const [results, setResults] = useState<AnalysisResult | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [progress, setProgress] = useState(0)
  const [pollCount, setPollCount] = useState(0)
  const [isLocalAnalysis, setIsLocalAnalysis] = useState(false)
  const [analysisDetail, setAnalysisDetail] = useState<string | null>(null)

  useEffect(() => {
    // Debug log for ID
    console.log('AnalysisClient mounted with ID:', id);
    
    if (!id) {
      console.error('Missing analysis ID in URL params');
      setError('Missing analysis ID. Please try again with a valid analysis.');
      return; // Don't proceed with polling if no ID
    }
    
    // Define the fetch function inside the useEffect to properly capture the id
    const fetchResults = async () => {
      try {
        console.log(`Fetching results for analysis ID: ${id}`);
        const response = await fetch(`http://localhost:8000/api/results/${id}`, {
          headers: {
            'Accept': 'application/json'
          }
        });
        
        if (!response.ok) {
          const errorData = await response.text();
          console.error(`Error fetching results: Status ${response.status}`, errorData);
          throw new Error(`Failed to fetch results: ${response.statusText}`);
        }
        
        const data = await response.json();
        console.log('Results data:', data);
        
        setStatus(data.status);
        
        // Check if this was a local analysis
        if (data.detail && data.detail.includes('local analysis')) {
          setIsLocalAnalysis(true);
          setAnalysisDetail(data.detail);
          console.log('Using local analysis results:', data.detail);
        }
        
        if (data.status === 'completed' && data.results) {
          setResults(data.results);
          setProgress(100);
        } else if (data.status === 'error') {
          setError(data.error_detail || 'Analysis failed');
          setProgress(0);
        } else {
          // Calculate progress based on poll count for pending/processing
          if (data.status === 'pending') {
            setProgress(Math.min(40, 10 + (pollCount * 2)));
          } else if (data.status === 'processing') {
            setProgress(Math.min(90, 40 + (pollCount * 5)));
          }
        }
        
        return data.status;
      } catch (err) {
        console.error('Error fetching analysis results:', err);
        setError(err instanceof Error ? err.message : 'Failed to fetch analysis results');
        return 'error';
      }
    };

    let pollTimer: NodeJS.Timeout | null = null;
    let attempts = 0;
    const maxAttempts = 30;
    
    const pollResults = async () => {
      attempts++;
      setPollCount(attempts);
      console.log(`Polling results attempt ${attempts}/${maxAttempts} for ID: ${id}`);
      
      const currentStatus = await fetchResults();
      
      if (currentStatus === 'completed' || currentStatus === 'error') {
        if (pollTimer) clearTimeout(pollTimer);
      } else if (attempts < maxAttempts) {
        // Continue polling if we haven't reached max attempts
        pollTimer = setTimeout(pollResults, 2000);
      } else {
        // Hit max attempts without completion
        setError('Analysis timed out. Please try again.');
        if (pollTimer) clearTimeout(pollTimer);
      }
    };
    
    // Start polling
    pollResults();
    
    // Cleanup
    return () => {
      if (pollTimer) clearTimeout(pollTimer);
    };
  }, [id, pollCount]);

  const handleRetry = () => {
    router.push('/analyze')
  }

  if (error) {
    return (
      <div className="container flex-1 py-6 md:py-12">
        <div className="mx-auto flex max-w-[800px] flex-col items-center space-y-4">
          <h1 className="text-3xl font-bold tracking-tight text-destructive">Analysis Failed</h1>
          <p className="text-center text-muted-foreground">{error}</p>
          <Button onClick={handleRetry}>Retry Analysis</Button>
        </div>
      </div>
    )
  }

  if (status === "completed" && results) {
    return (
      <>
        <ResultsDisplay results={results} />
        {isLocalAnalysis && (
          <div className="container mx-auto max-w-[800px] mt-4 mb-8">
            <div className="bg-amber-50 border border-amber-200 rounded-md p-4">
              <h3 className="text-amber-800 font-semibold mb-1">Local Analysis Mode</h3>
              <p className="text-amber-700 text-sm">
                {analysisDetail || 'Your results were generated using our backup local analysis system due to connectivity issues with our advanced AI service.'}
              </p>
            </div>
          </div>
        )}
      </>
    )
  }

  return (
    <div className="container flex-1 py-6 md:py-12">
      <div className="mx-auto flex max-w-[800px] flex-col items-center space-y-8">
        <h1 className="text-3xl font-bold tracking-tight">
          {status === "processing" ? "Processing Image" : "Analyzing Features"}
        </h1>
        
        <div className="w-full space-y-4">
          <Progress value={progress} className="w-full" />
          <p className="text-center text-sm text-muted-foreground">
            {status === "pending" 
              ? "Preparing analysis. Please wait..." 
              : "Analyzing image features. This may take up to a minute..."}
          </p>
        </div>
      </div>
    </div>
  )
}
