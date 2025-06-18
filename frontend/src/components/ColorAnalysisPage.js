import React, { useState } from 'react';
import CameraCapture from './CameraCapture';
import ColorAnalysisResults from './ColorAnalysisResults';

const ColorAnalysisPage = () => {
    const [analysisResults, setAnalysisResults] = useState(null);
    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const [error, setError] = useState(null);

    const handleCapture = async (imageDataUrl) => {
        setIsAnalyzing(true);
        setError(null);

        try {
            // Convert base64 to blob
            const response = await fetch(imageDataUrl);
            const blob = await response.blob();

            // Create form data
            const formData = new FormData();
            formData.append('file', blob, 'capture.png');

            // Send to backend
            const result = await fetch('http://localhost:8000/analyze-image', {
                method: 'POST',
                body: formData,
            });

            if (!result.ok) {
                throw new Error('Analysis failed');
            }

            const data = await result.json();
            setAnalysisResults(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setIsAnalyzing(false);
        }
    };

    return (
        <div className="container mx-auto px-4 py-8">
            <h1 className="text-3xl font-bold mb-8">Color Analysis</h1>
            
            {error && (
                <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
                    {error}
                </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div>
                    <h2 className="text-xl font-semibold mb-4">Take Your Photo</h2>
                    <div className="bg-gray-100 p-4 rounded-lg">
                        <CameraCapture onCapture={handleCapture} />
                    </div>
                </div>

                <div>
                    <h2 className="text-xl font-semibold mb-4">Analysis Results</h2>
                    {isAnalyzing ? (
                        <div className="flex items-center justify-center h-64">
                            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
                        </div>
                    ) : analysisResults ? (
                        <ColorAnalysisResults
                            season={analysisResults.color_season}
                            palettes={analysisResults.palettes}
                        />
                    ) : (
                        <div className="bg-gray-100 p-8 rounded-lg text-center">
                            <p className="text-gray-500">Take a photo to see your color analysis results</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default ColorAnalysisPage; 