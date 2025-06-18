'use client';

import React, { useRef, useState, useCallback, useEffect } from 'react';
import { Camera, CameraOff, RotateCcw, Check, AlertCircle, Zap } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';

interface CameraCaptureProps {
  onCapture: (imageSrc: string) => void;
  onClose: () => void;
}

interface FaceGuide {
  message: string;
  type: 'info' | 'warning' | 'success' | 'error';
  icon: React.ReactNode;
}

const CameraCapture: React.FC<CameraCaptureProps> = ({ onCapture, onClose }) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const streamRef = useRef<MediaStream | null>(null);

  const [isCapturing, setIsCapturing] = useState(false);
  const [capturedImage, setCapturedImage] = useState<string | null>(null);
  const [currentGuide, setCurrentGuide] = useState<FaceGuide>({
    message: "Initializing camera...",
    type: 'info',
    icon: <Camera className="h-4 w-4" />
  });
  const [countdown, setCountdown] = useState<number | null>(null);
  const [facingMode, setFacingMode] = useState<'user' | 'environment'>('user');
  const [cameraReady, setCameraReady] = useState(false);
  const [faceDetected, setFaceDetected] = useState(false);
  const [lightingQuality, setLightingQuality] = useState<'poor' | 'good' | 'excellent'>('poor');

  // Dynamic guides based on real-time analysis
  const getDynamicGuide = (): FaceGuide => {
    if (!cameraReady) {
      return {
        message: "Initializing camera...",
        type: 'info',
        icon: <Camera className="h-4 w-4" />
      };
    }

    if (!faceDetected) {
      return {
        message: "Please position your face in the center of the frame",
        type: 'warning',
        icon: <AlertCircle className="h-4 w-4" />
      };
    }

    if (lightingQuality === 'poor') {
      return {
        message: "Move to better lighting - face a window or bright light",
        type: 'warning',
        icon: <Zap className="h-4 w-4" />
      };
    }

    if (lightingQuality === 'good') {
      return {
        message: "Good! Keep your face straight and look at the camera",
        type: 'info',
        icon: <Check className="h-4 w-4" />
      };
    }

    return {
      message: "Perfect! Ready to capture your photo",
      type: 'success',
      icon: <Check className="h-4 w-4" />
    };
  };

  // Initialize camera on mount
  useEffect(() => {
    initializeCamera();
    return () => {
      stopCamera();
    };
  }, [facingMode]);

  // Real-time analysis
  useEffect(() => {
    if (cameraReady && videoRef.current) {
      const interval = setInterval(() => {
        analyzeFrame();
        setCurrentGuide(getDynamicGuide());
      }, 500); // Analyze every 500ms

      return () => clearInterval(interval);
    }
  }, [cameraReady, faceDetected, lightingQuality]);

  const initializeCamera = async () => {
    try {
      const constraints = {
        video: {
          facingMode: facingMode,
          width: { ideal: 1280 },
          height: { ideal: 720 }
        }
      };

      const stream = await navigator.mediaDevices.getUserMedia(constraints);
      streamRef.current = stream;

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.onloadedmetadata = () => {
          setCameraReady(true);
          setCurrentGuide({
            message: "Camera ready! Position your face in the frame",
            type: 'success',
            icon: <Check className="h-4 w-4" />
          });
        };
      }
    } catch (error) {
      console.error('Camera initialization failed:', error);
      setCurrentGuide({
        message: "Camera access denied. Please allow camera permissions.",
        type: 'error',
        icon: <CameraOff className="h-4 w-4" />
      });
    }
  };

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    setCameraReady(false);
  };

  const analyzeFrame = () => {
    if (!videoRef.current || !canvasRef.current) return;

    const video = videoRef.current;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');

    if (!ctx) return;

    // Set canvas size to match video
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Draw current frame
    ctx.drawImage(video, 0, 0);

    // Analyze lighting quality
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const brightness = calculateBrightness(imageData);

    if (brightness < 80) {
      setLightingQuality('poor');
    } else if (brightness < 120) {
      setLightingQuality('good');
    } else {
      setLightingQuality('excellent');
    }

    // Simple face detection (check for skin-like colors in center region)
    const centerRegion = ctx.getImageData(
      canvas.width * 0.3,
      canvas.height * 0.3,
      canvas.width * 0.4,
      canvas.height * 0.4
    );

    setFaceDetected(detectFaceInRegion(centerRegion));
  };

  const calculateBrightness = (imageData: ImageData): number => {
    const data = imageData.data;
    let totalBrightness = 0;

    for (let i = 0; i < data.length; i += 4) {
      const r = data[i];
      const g = data[i + 1];
      const b = data[i + 2];
      totalBrightness += (r + g + b) / 3;
    }

    return totalBrightness / (data.length / 4);
  };

  const detectFaceInRegion = (imageData: ImageData): boolean => {
    const data = imageData.data;
    let skinPixels = 0;
    let totalPixels = data.length / 4;

    for (let i = 0; i < data.length; i += 4) {
      const r = data[i];
      const g = data[i + 1];
      const b = data[i + 2];

      // Simple skin color detection
      if (r > 95 && g > 40 && b > 20 && r > g && r > b) {
        skinPixels++;
      }
    }

    return (skinPixels / totalPixels) > 0.1; // At least 10% skin-like pixels
  };

  const startCountdown = useCallback(() => {
    setCountdown(3);
    const countdownInterval = setInterval(() => {
      setCountdown((prev) => {
        if (prev === 1) {
          clearInterval(countdownInterval);
          capturePhoto();
          return null;
        }
        return prev ? prev - 1 : null;
      });
    }, 1000);
  }, []);

  const capturePhoto = useCallback(() => {
    if (!videoRef.current || !canvasRef.current) return;

    const video = videoRef.current;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');

    if (!ctx) return;

    // Set canvas to high quality for final capture
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Draw the current frame
    ctx.drawImage(video, 0, 0);

    // Convert to high-quality JPEG
    const imageSrc = canvas.toDataURL('image/jpeg', 0.95);
    setCapturedImage(imageSrc);
    setIsCapturing(false);
  }, []);

  const handleCapture = useCallback(() => {
    setIsCapturing(true);
    startCountdown();
  }, [startCountdown]);

  const handleRetake = useCallback(() => {
    setCapturedImage(null);
    setCountdown(null);
  }, []);

  const handleConfirm = useCallback(() => {
    if (capturedImage) {
      onCapture(capturedImage);
    }
  }, [capturedImage, onCapture]);

  const toggleCamera = useCallback(() => {
    stopCamera();
    setFacingMode(prev => prev === 'user' ? 'environment' : 'user');
    setCameraReady(false);
    setFaceDetected(false);
    setLightingQuality('poor');
  }, []);

  return (
    <div className="fixed inset-0 bg-black bg-opacity-90 z-50 flex items-center justify-center">
      <div className="bg-white rounded-lg p-6 max-w-4xl w-full mx-4 max-h-[90vh] overflow-auto">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-bold text-gray-900">Take Your Photo</h2>
          <Button variant="outline" onClick={onClose}>
            Close
          </Button>
        </div>

        {/* Guide Alert with Real-time Status */}
        <Alert className={`mb-4 transition-all duration-300 ${
          currentGuide.type === 'success' ? 'border-green-500 bg-green-50 text-green-800' :
          currentGuide.type === 'warning' ? 'border-yellow-500 bg-yellow-50 text-yellow-800' :
          currentGuide.type === 'error' ? 'border-red-500 bg-red-50 text-red-800' :
          'border-blue-500 bg-blue-50 text-blue-800'
        }`}>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              {currentGuide.icon}
              <AlertDescription className="font-medium">
                {currentGuide.message}
              </AlertDescription>
            </div>
            <div className="flex items-center gap-2 text-sm">
              <div className={`w-2 h-2 rounded-full ${faceDetected ? 'bg-green-500' : 'bg-red-500'}`}></div>
              <span>Face: {faceDetected ? 'Detected' : 'Not Found'}</span>
              <div className={`w-2 h-2 rounded-full ml-2 ${
                lightingQuality === 'excellent' ? 'bg-green-500' :
                lightingQuality === 'good' ? 'bg-yellow-500' : 'bg-red-500'
              }`}></div>
              <span>Light: {lightingQuality}</span>
            </div>
          </div>
        </Alert>

        <div className="relative">
          {/* Camera View */}
          <div className="relative bg-black rounded-lg overflow-hidden">
            {capturedImage ? (
              <img
                src={capturedImage}
                alt="Captured"
                className="w-full h-auto max-h-96 object-cover"
              />
            ) : (
              <div className="relative">
                <video
                  ref={videoRef}
                  autoPlay
                  playsInline
                  muted
                  className="w-full h-auto max-h-96 object-cover"
                />

                {/* Hidden canvas for analysis */}
                <canvas
                  ref={canvasRef}
                  className="hidden"
                />

                {/* Face Guide Overlay with Dynamic Feedback */}
                <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                  <div className={`border-2 border-dashed rounded-full w-64 h-80 transition-all duration-300 ${
                    faceDetected ? 'border-green-400 opacity-80' : 'border-white opacity-50'
                  }`}>
                    {/* Face detection indicator */}
                    {faceDetected && (
                      <div className="absolute top-2 right-2 bg-green-500 text-white px-2 py-1 rounded text-xs">
                        Face Detected ✓
                      </div>
                    )}
                  </div>
                </div>

                {/* Lighting Quality Indicator */}
                <div className="absolute top-4 left-4 bg-black bg-opacity-50 text-white px-3 py-2 rounded-lg">
                  <div className="flex items-center gap-2">
                    <Zap className="h-4 w-4" />
                    <span className="text-sm">
                      Lighting: <span className={`font-semibold ${
                        lightingQuality === 'excellent' ? 'text-green-400' :
                        lightingQuality === 'good' ? 'text-yellow-400' : 'text-red-400'
                      }`}>
                        {lightingQuality}
                      </span>
                    </span>
                  </div>
                </div>

                {/* Countdown Overlay */}
                {countdown && (
                  <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50">
                    <div className="text-white text-6xl font-bold animate-pulse">
                      {countdown}
                    </div>
                  </div>
                )}

                {/* Camera not ready overlay */}
                {!cameraReady && (
                  <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-75">
                    <div className="text-white text-center">
                      <Camera className="h-12 w-12 mx-auto mb-4 animate-pulse" />
                      <p>Initializing camera...</p>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Smart Controls */}
          <div className="flex justify-center gap-4 mt-4">
            {capturedImage ? (
              <>
                <Button variant="outline" onClick={handleRetake}>
                  <RotateCcw className="h-4 w-4 mr-2" />
                  Retake
                </Button>
                <Button onClick={handleConfirm} className="bg-green-600 hover:bg-green-700">
                  <Check className="h-4 w-4 mr-2" />
                  Use This Photo
                </Button>
              </>
            ) : (
              <>
                <Button variant="outline" onClick={toggleCamera} disabled={!cameraReady}>
                  <RotateCcw className="h-4 w-4 mr-2" />
                  Flip Camera
                </Button>
                <Button
                  onClick={handleCapture}
                  disabled={isCapturing || !cameraReady || !faceDetected || lightingQuality === 'poor'}
                  className={`transition-all duration-300 ${
                    faceDetected && lightingQuality !== 'poor'
                      ? 'bg-green-600 hover:bg-green-700 animate-pulse'
                      : 'bg-blue-600 hover:bg-blue-700'
                  }`}
                >
                  {isCapturing ? (
                    <CameraOff className="h-4 w-4 mr-2" />
                  ) : (
                    <Camera className="h-4 w-4 mr-2" />
                  )}
                  {isCapturing ? 'Capturing...' :
                   !cameraReady ? 'Camera Loading...' :
                   !faceDetected ? 'Position Face' :
                   lightingQuality === 'poor' ? 'Improve Lighting' :
                   'Take Photo'}
                </Button>
              </>
            )}
          </div>
        </div>

        {/* Smart Tips */}
        <div className="mt-6 p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg border">
          <h3 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
            <Zap className="h-4 w-4 text-blue-500" />
            Smart Photo Tips
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h4 className="font-medium text-gray-800 mb-2">For Best Analysis:</h4>
              <ul className="text-sm text-gray-600 space-y-1">
                <li className={`flex items-center gap-2 ${faceDetected ? 'text-green-600' : ''}`}>
                  <div className={`w-2 h-2 rounded-full ${faceDetected ? 'bg-green-500' : 'bg-gray-400'}`}></div>
                  Face centered in frame
                </li>
                <li className={`flex items-center gap-2 ${lightingQuality !== 'poor' ? 'text-green-600' : ''}`}>
                  <div className={`w-2 h-2 rounded-full ${lightingQuality !== 'poor' ? 'bg-green-500' : 'bg-gray-400'}`}></div>
                  Good lighting (natural preferred)
                </li>
                <li className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-gray-400"></div>
                  Remove glasses and accessories
                </li>
                <li className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-gray-400"></div>
                  Hair pulled away from face
                </li>
              </ul>
            </div>
            <div>
              <h4 className="font-medium text-gray-800 mb-2">Current Status:</h4>
              <div className="space-y-2 text-sm">
                <div className="flex items-center justify-between">
                  <span>Camera:</span>
                  <span className={`font-medium ${cameraReady ? 'text-green-600' : 'text-red-600'}`}>
                    {cameraReady ? 'Ready' : 'Loading...'}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span>Face Detection:</span>
                  <span className={`font-medium ${faceDetected ? 'text-green-600' : 'text-red-600'}`}>
                    {faceDetected ? 'Detected' : 'Not Found'}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span>Lighting:</span>
                  <span className={`font-medium ${
                    lightingQuality === 'excellent' ? 'text-green-600' :
                    lightingQuality === 'good' ? 'text-yellow-600' : 'text-red-600'
                  }`}>
                    {lightingQuality.charAt(0).toUpperCase() + lightingQuality.slice(1)}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span>Ready to Capture:</span>
                  <span className={`font-medium ${
                    cameraReady && faceDetected && lightingQuality !== 'poor' ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {cameraReady && faceDetected && lightingQuality !== 'poor' ? 'Yes' : 'No'}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CameraCapture;
