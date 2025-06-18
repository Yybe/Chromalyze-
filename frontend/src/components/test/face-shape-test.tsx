'use client';

import React, { useState } from 'react';
import { analysisService } from '@/lib/analysis-service';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Upload, TestTube, CheckCircle, AlertCircle } from 'lucide-react';

// Test images with known face shapes for validation
const TEST_IMAGES = [
  {
    name: 'Round Face Test',
    expectedShape: 'round',
    description: 'Should detect round face shape'
  },
  {
    name: 'Oval Face Test', 
    expectedShape: 'oval',
    description: 'Should detect oval face shape'
  },
  {
    name: 'Square Face Test',
    expectedShape: 'square', 
    description: 'Should detect square face shape'
  },
  {
    name: 'Heart Face Test',
    expectedShape: 'heart',
    description: 'Should detect heart face shape'
  },
  {
    name: 'Oblong Face Test',
    expectedShape: 'oblong',
    description: 'Should detect oblong face shape'
  }
];

interface TestResult {
  imageName: string;
  expectedShape: string;
  detectedShape: string;
  confidence: number;
  isCorrect: boolean;
  measurements: any;
  processingTime: number;
}

const FaceShapeTest: React.FC = () => {
  const [testResults, setTestResults] = useState<TestResult[]>([]);
  const [isRunning, setIsRunning] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [singleTestResult, setSingleTestResult] = useState<any>(null);

  const runAllTests = async () => {
    setIsRunning(true);
    setTestResults([]);
    
    // For now, we'll test with user-uploaded images
    // In a real implementation, you'd load the test images from the dataset
    console.log('Test framework ready - upload images to test face shape detection');
    setIsRunning(false);
  };

  const testSingleImage = async () => {
    if (!selectedFile) return;

    setIsRunning(true);
    setSingleTestResult(null);

    try {
      // Create image element from file
      const imageElement = await createImageElement(selectedFile);
      
      // Run analysis
      const result = await analysisService.analyzeImage(imageElement, false);
      
      setSingleTestResult({
        fileName: selectedFile.name,
        detectedShape: result.faceShape.faceShape,
        confidence: result.faceShape.confidence,
        measurements: result.faceShape.measurements,
        processingTime: result.processingTime,
        colorSeason: result.colorSeason.season
      });

    } catch (error) {
      console.error('Test failed:', error);
    } finally {
      setIsRunning(false);
    }
  };

  const createImageElement = (file: File): Promise<HTMLImageElement> => {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.onload = () => resolve(img);
      img.onerror = reject;
      img.src = URL.createObjectURL(file);
    });
  };

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      setSingleTestResult(null);
    }
  };

  const getAccuracy = () => {
    if (testResults.length === 0) return 0;
    const correct = testResults.filter(r => r.isCorrect).length;
    return (correct / testResults.length) * 100;
  };

  return (
    <div className="container mx-auto px-4 py-8 space-y-6">
      <div className="text-center">
        <h1 className="text-3xl font-bold mb-2 flex items-center justify-center gap-2">
          <TestTube className="h-8 w-8 text-blue-500" />
          Face Shape Detection Test
        </h1>
        <p className="text-gray-600">
          Test the accuracy of our face shape detection algorithm
        </p>
      </div>

      {/* Single Image Test */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Upload className="h-5 w-5" />
            Test Single Image
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <input
              type="file"
              accept="image/*"
              onChange={handleFileSelect}
              className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
            />
          </div>
          
          {selectedFile && (
            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-600">
                Selected: {selectedFile.name}
              </span>
              <Button 
                onClick={testSingleImage} 
                disabled={isRunning}
                size="sm"
              >
                {isRunning ? 'Analyzing...' : 'Test Image'}
              </Button>
            </div>
          )}

          {singleTestResult && (
            <div className="mt-4 p-4 bg-gray-50 rounded-lg">
              <h4 className="font-semibold mb-3">Analysis Results:</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <p><strong>File:</strong> {singleTestResult.fileName}</p>
                  <p><strong>Detected Shape:</strong> 
                    <Badge variant="secondary" className="ml-2 capitalize">
                      {singleTestResult.detectedShape}
                    </Badge>
                  </p>
                  <p><strong>Confidence:</strong> {Math.round(singleTestResult.confidence * 100)}%</p>
                  <p><strong>Processing Time:</strong> {Math.round(singleTestResult.processingTime)}ms</p>
                  <p><strong>Color Season:</strong> 
                    <Badge variant="outline" className="ml-2 capitalize">
                      {singleTestResult.colorSeason.replace('_', ' ')}
                    </Badge>
                  </p>
                </div>
                <div>
                  <h5 className="font-medium mb-2">Face Measurements:</h5>
                  <div className="text-sm space-y-1">
                    <p>Face Ratio: {singleTestResult.measurements.faceRatio.toFixed(2)}</p>
                    <p>Face Width: {Math.round(singleTestResult.measurements.faceWidth)}px</p>
                    <p>Face Height: {Math.round(singleTestResult.measurements.faceHeight)}px</p>
                    <p>Jaw Width: {Math.round(singleTestResult.measurements.jawWidth)}px</p>
                    <p>Forehead Width: {Math.round(singleTestResult.measurements.foreheadWidth)}px</p>
                    <p>Cheekbone Width: {Math.round(singleTestResult.measurements.cheekboneWidth)}px</p>
                    <p>Jawline Angle: {Math.round(singleTestResult.measurements.jawlineAngle)}°</p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Batch Test Results */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <span className="flex items-center gap-2">
              <TestTube className="h-5 w-5" />
              Batch Test Results
            </span>
            <Button onClick={runAllTests} disabled={isRunning}>
              {isRunning ? 'Running Tests...' : 'Run All Tests'}
            </Button>
          </CardTitle>
        </CardHeader>
        <CardContent>
          {testResults.length > 0 && (
            <div className="mb-4">
              <div className="flex items-center gap-4">
                <span className="text-lg font-semibold">
                  Accuracy: {getAccuracy().toFixed(1)}%
                </span>
                <span className="text-sm text-gray-600">
                  ({testResults.filter(r => r.isCorrect).length}/{testResults.length} correct)
                </span>
              </div>
            </div>
          )}

          {testResults.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <TestTube className="h-12 w-12 mx-auto mb-4 opacity-50" />
              <p>No test results yet. Upload images to test the face shape detection.</p>
              <p className="text-sm mt-2">
                For best results, use clear photos with good lighting and the face centered.
              </p>
            </div>
          ) : (
            <div className="space-y-3">
              {testResults.map((result, index) => (
                <div 
                  key={index}
                  className={`p-3 rounded-lg border ${
                    result.isCorrect 
                      ? 'border-green-200 bg-green-50' 
                      : 'border-red-200 bg-red-50'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      {result.isCorrect ? (
                        <CheckCircle className="h-5 w-5 text-green-500" />
                      ) : (
                        <AlertCircle className="h-5 w-5 text-red-500" />
                      )}
                      <div>
                        <p className="font-medium">{result.imageName}</p>
                        <p className="text-sm text-gray-600">
                          Expected: {result.expectedShape} | 
                          Detected: {result.detectedShape} | 
                          Confidence: {Math.round(result.confidence * 100)}%
                        </p>
                      </div>
                    </div>
                    <Badge variant={result.isCorrect ? "default" : "destructive"}>
                      {result.isCorrect ? 'Correct' : 'Incorrect'}
                    </Badge>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Test Instructions */}
      <Card>
        <CardHeader>
          <CardTitle>Testing Instructions</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3 text-sm">
            <p><strong>For accurate testing:</strong></p>
            <ul className="list-disc list-inside space-y-1 text-gray-600">
              <li>Use clear, well-lit photos</li>
              <li>Ensure the face is centered and looking forward</li>
              <li>Remove glasses and pull hair away from face</li>
              <li>Use photos from the training dataset for validation</li>
              <li>Test with different face shapes to verify accuracy</li>
            </ul>
            <p className="mt-4 text-gray-600">
              <strong>Note:</strong> The current implementation uses enhanced geometric analysis. 
              For production use, integrate with MediaPipe Face Mesh for higher accuracy.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default FaceShapeTest;
