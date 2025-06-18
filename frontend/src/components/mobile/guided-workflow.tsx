'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { 
  ChevronRight, 
  ChevronLeft, 
  Camera, 
  Upload, 
  Zap, 
  CheckCircle,
  AlertCircle,
  Info,
  Smartphone,
  Monitor,
  Tablet
} from 'lucide-react';
import { Alert, AlertDescription } from '@/components/ui/alert';

// Workflow step interface
interface WorkflowStep {
  id: string;
  title: string;
  description: string;
  icon: React.ReactNode;
  component: React.ReactNode;
  isComplete: boolean;
  isOptional?: boolean;
  mobileOptimized: boolean;
}

// Device type detection
type DeviceType = 'mobile' | 'tablet' | 'desktop';

interface GuidedWorkflowProps {
  onComplete?: (results: any) => void;
  children?: React.ReactNode;
}

const GuidedWorkflow: React.FC<GuidedWorkflowProps> = ({ onComplete, children }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [deviceType, setDeviceType] = useState<DeviceType>('desktop');
  const [isPortrait, setIsPortrait] = useState(true);
  const [workflowData, setWorkflowData] = useState<any>({});

  // Detect device type and orientation
  useEffect(() => {
    const detectDevice = () => {
      const width = window.innerWidth;
      const height = window.innerHeight;
      
      if (width < 768) {
        setDeviceType('mobile');
      } else if (width < 1024) {
        setDeviceType('tablet');
      } else {
        setDeviceType('desktop');
      }
      
      setIsPortrait(height > width);
    };

    detectDevice();
    window.addEventListener('resize', detectDevice);
    window.addEventListener('orientationchange', detectDevice);

    return () => {
      window.removeEventListener('resize', detectDevice);
      window.removeEventListener('orientationchange', detectDevice);
    };
  }, []);

  // Workflow steps
  const steps: WorkflowStep[] = [
    {
      id: 'welcome',
      title: 'Welcome to Chromalyze',
      description: 'Get personalized style recommendations based on your face shape and color season',
      icon: <Zap className="h-6 w-6" />,
      component: <WelcomeStep deviceType={deviceType} />,
      isComplete: false,
      mobileOptimized: true
    },
    {
      id: 'photo-capture',
      title: 'Take or Upload Photo',
      description: 'Capture a clear photo of your face for analysis',
      icon: <Camera className="h-6 w-6" />,
      component: <PhotoCaptureStep 
        deviceType={deviceType} 
        onPhotoSelected={(photo) => updateWorkflowData('photo', photo)}
      />,
      isComplete: false,
      mobileOptimized: true
    },
    {
      id: 'analysis',
      title: 'AI Analysis',
      description: 'Our AI analyzes your face shape and color season',
      icon: <Zap className="h-6 w-6" />,
      component: <AnalysisStep 
        photo={workflowData.photo}
        onAnalysisComplete={(results) => updateWorkflowData('results', results)}
      />,
      isComplete: false,
      mobileOptimized: true
    },
    {
      id: 'results',
      title: 'Your Results',
      description: 'View your personalized style recommendations',
      icon: <CheckCircle className="h-6 w-6" />,
      component: <ResultsStep results={workflowData.results} />,
      isComplete: false,
      mobileOptimized: true
    }
  ];

  const updateWorkflowData = (key: string, value: any) => {
    setWorkflowData(prev => ({ ...prev, [key]: value }));
    
    // Mark current step as complete
    const updatedSteps = [...steps];
    updatedSteps[currentStep].isComplete = true;
  };

  const nextStep = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      onComplete?.(workflowData);
    }
  };

  const prevStep = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const goToStep = (stepIndex: number) => {
    setCurrentStep(stepIndex);
  };

  const getDeviceIcon = () => {
    switch (deviceType) {
      case 'mobile':
        return <Smartphone className="h-4 w-4" />;
      case 'tablet':
        return <Tablet className="h-4 w-4" />;
      default:
        return <Monitor className="h-4 w-4" />;
    }
  };

  const currentStepData = steps[currentStep];
  const progress = ((currentStep + 1) / steps.length) * 100;

  return (
    <div className={`min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 ${
      deviceType === 'mobile' ? 'px-4 py-2' : 'px-6 py-4'
    }`}>
      {/* Header */}
      <div className={`mb-6 ${deviceType === 'mobile' ? 'text-center' : ''}`}>
        <div className="flex items-center justify-between mb-4">
          <h1 className={`font-bold bg-gradient-to-r from-pink-500 to-violet-500 bg-clip-text text-transparent ${
            deviceType === 'mobile' ? 'text-2xl' : 'text-3xl'
          }`}>
            Chromalyze
          </h1>
          <div className="flex items-center gap-2 text-sm text-gray-600">
            {getDeviceIcon()}
            <span className="capitalize">{deviceType}</span>
            {deviceType === 'mobile' && (
              <Badge variant="secondary" className="text-xs">
                {isPortrait ? 'Portrait' : 'Landscape'}
              </Badge>
            )}
          </div>
        </div>

        {/* Progress Bar */}
        <div className="space-y-2">
          <div className="flex justify-between text-sm">
            <span>Step {currentStep + 1} of {steps.length}</span>
            <span>{Math.round(progress)}% Complete</span>
          </div>
          <Progress value={progress} className="h-2" />
        </div>

        {/* Step Navigation (Mobile-optimized) */}
        {deviceType !== 'mobile' && (
          <div className="flex justify-center mt-4">
            <div className="flex space-x-2">
              {steps.map((step, index) => (
                <button
                  key={step.id}
                  onClick={() => goToStep(index)}
                  className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-medium transition-all ${
                    index === currentStep
                      ? 'bg-blue-500 text-white'
                      : index < currentStep
                      ? 'bg-green-500 text-white'
                      : 'bg-gray-200 text-gray-600 hover:bg-gray-300'
                  }`}
                >
                  {index < currentStep ? (
                    <CheckCircle className="h-4 w-4" />
                  ) : (
                    index + 1
                  )}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Mobile Orientation Warning */}
      {deviceType === 'mobile' && !isPortrait && (
        <Alert className="mb-4 border-yellow-500 bg-yellow-50">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>
            For the best experience, please rotate your device to portrait mode.
          </AlertDescription>
        </Alert>
      )}

      {/* Main Content */}
      <Card className={`mx-auto ${
        deviceType === 'mobile' 
          ? 'max-w-full' 
          : deviceType === 'tablet' 
          ? 'max-w-2xl' 
          : 'max-w-4xl'
      }`}>
        <CardHeader className={deviceType === 'mobile' ? 'pb-4' : 'pb-6'}>
          <CardTitle className={`flex items-center gap-3 ${
            deviceType === 'mobile' ? 'text-lg' : 'text-xl'
          }`}>
            {currentStepData.icon}
            <div>
              <h2>{currentStepData.title}</h2>
              <p className={`font-normal text-gray-600 ${
                deviceType === 'mobile' ? 'text-sm' : 'text-base'
              }`}>
                {currentStepData.description}
              </p>
            </div>
          </CardTitle>
        </CardHeader>
        
        <CardContent className={deviceType === 'mobile' ? 'px-4 pb-4' : 'px-6 pb-6'}>
          {/* Step Content */}
          <div className="mb-6">
            {currentStepData.component}
          </div>

          {/* Navigation Buttons */}
          <div className={`flex gap-3 ${
            deviceType === 'mobile' 
              ? 'flex-col' 
              : 'justify-between'
          }`}>
            <Button
              variant="outline"
              onClick={prevStep}
              disabled={currentStep === 0}
              className={deviceType === 'mobile' ? 'w-full order-2' : ''}
            >
              <ChevronLeft className="h-4 w-4 mr-2" />
              Previous
            </Button>

            <Button
              onClick={nextStep}
              className={`${
                deviceType === 'mobile' ? 'w-full order-1' : ''
              } bg-gradient-to-r from-pink-500 to-violet-500 hover:from-pink-600 hover:to-violet-600`}
            >
              {currentStep === steps.length - 1 ? 'Complete' : 'Next'}
              <ChevronRight className="h-4 w-4 ml-2" />
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Mobile Step Indicator */}
      {deviceType === 'mobile' && (
        <div className="fixed bottom-4 left-1/2 transform -translate-x-1/2">
          <div className="flex space-x-2 bg-white rounded-full px-4 py-2 shadow-lg">
            {steps.map((_, index) => (
              <div
                key={index}
                className={`w-2 h-2 rounded-full transition-all ${
                  index === currentStep
                    ? 'bg-blue-500'
                    : index < currentStep
                    ? 'bg-green-500'
                    : 'bg-gray-300'
                }`}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

// Individual step components
const WelcomeStep: React.FC<{ deviceType: DeviceType }> = ({ deviceType }) => (
  <div className={`text-center space-y-4 ${deviceType === 'mobile' ? 'py-4' : 'py-8'}`}>
    <div className="mx-auto w-24 h-24 bg-gradient-to-r from-pink-500 to-violet-500 rounded-full flex items-center justify-center">
      <Zap className="h-12 w-12 text-white" />
    </div>
    <div className="space-y-2">
      <h3 className={deviceType === 'mobile' ? 'text-lg font-semibold' : 'text-xl font-semibold'}>
        Discover Your Perfect Style
      </h3>
      <p className={`text-gray-600 max-w-md mx-auto ${deviceType === 'mobile' ? 'text-sm' : 'text-base'}`}>
        Our AI-powered analysis will determine your face shape and color season to provide 
        personalized style recommendations that enhance your natural beauty.
      </p>
    </div>
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
      <div className="text-center">
        <Camera className="h-8 w-8 mx-auto mb-2 text-blue-500" />
        <h4 className="font-medium">Face Analysis</h4>
        <p className="text-sm text-gray-600">AI-powered face shape detection</p>
      </div>
      <div className="text-center">
        <Zap className="h-8 w-8 mx-auto mb-2 text-purple-500" />
        <h4 className="font-medium">Color Season</h4>
        <p className="text-sm text-gray-600">Personalized color palette</p>
      </div>
      <div className="text-center">
        <CheckCircle className="h-8 w-8 mx-auto mb-2 text-green-500" />
        <h4 className="font-medium">Style Guide</h4>
        <p className="text-sm text-gray-600">Tailored recommendations</p>
      </div>
    </div>
  </div>
);

const PhotoCaptureStep: React.FC<{ 
  deviceType: DeviceType; 
  onPhotoSelected: (photo: File) => void;
}> = ({ deviceType, onPhotoSelected }) => (
  <div className="space-y-4">
    <Alert>
      <Info className="h-4 w-4" />
      <AlertDescription>
        For best results, ensure good lighting and look directly at the camera.
      </AlertDescription>
    </Alert>
    {/* Photo capture component would go here */}
    <div className="text-center py-8 border-2 border-dashed border-gray-300 rounded-lg">
      <Camera className="h-12 w-12 mx-auto mb-4 text-gray-400" />
      <p className="text-gray-600">Photo capture component will be integrated here</p>
    </div>
  </div>
);

const AnalysisStep: React.FC<{ 
  photo?: File; 
  onAnalysisComplete: (results: any) => void;
}> = ({ photo, onAnalysisComplete }) => (
  <div className="text-center space-y-4">
    <div className="mx-auto w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center">
      <Zap className="h-8 w-8 text-blue-500 animate-pulse" />
    </div>
    <div>
      <h3 className="text-lg font-semibold">Analyzing Your Photo</h3>
      <p className="text-gray-600">Our AI is processing your image...</p>
    </div>
    <Progress value={75} className="max-w-xs mx-auto" />
  </div>
);

const ResultsStep: React.FC<{ results?: any }> = ({ results }) => (
  <div className="text-center space-y-4">
    <div className="mx-auto w-16 h-16 bg-green-100 rounded-full flex items-center justify-center">
      <CheckCircle className="h-8 w-8 text-green-500" />
    </div>
    <div>
      <h3 className="text-lg font-semibold">Analysis Complete!</h3>
      <p className="text-gray-600">Your personalized style guide is ready.</p>
    </div>
  </div>
);

export default GuidedWorkflow;
