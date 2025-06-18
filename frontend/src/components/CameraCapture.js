import React, { useRef, useState, useEffect } from 'react';
import FaceGuideOverlay from './FaceGuideOverlay';

const CameraCapture = ({ onCapture }) => {
    const videoRef = useRef(null);
    const canvasRef = useRef(null);
    const [stream, setStream] = useState(null);
    const [isCameraOn, setIsCameraOn] = useState(false);
    const [isFaceDetected, setIsFaceDetected] = useState(false);
    const [lightingQuality, setLightingQuality] = useState('good');

    useEffect(() => {
        if (isCameraOn) {
            navigator.mediaDevices.getUserMedia({ video: true })
                .then(stream => {
                    setStream(stream);
                    if (videoRef.current) {
                        videoRef.current.srcObject = stream;
                    }
                })
                .catch(err => console.error('Error accessing camera:', err));
        } else {
            if (stream) {
                stream.getTracks().forEach(track => track.stop());
            }
        }
    }, [isCameraOn]);

    const startCamera = () => setIsCameraOn(true);
    const stopCamera = () => setIsCameraOn(false);

    const captureImage = () => {
        if (videoRef.current && canvasRef.current) {
            const context = canvasRef.current.getContext('2d');
            canvasRef.current.width = videoRef.current.videoWidth;
            canvasRef.current.height = videoRef.current.videoHeight;
            context.drawImage(videoRef.current, 0, 0);
            const imageDataUrl = canvasRef.current.toDataURL('image/png');
            onCapture(imageDataUrl);
        }
    };

    return (
        <div className="relative">
            <video ref={videoRef} autoPlay className="w-full max-w-md" />
            <canvas ref={canvasRef} style={{ display: 'none' }} />
            
            {isCameraOn && <FaceGuideOverlay />}
            
            <div className="mt-4 flex justify-center space-x-4">
                <button 
                    onClick={startCamera}
                    className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors"
                >
                    Start Camera
                </button>
                <button 
                    onClick={stopCamera}
                    className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 transition-colors"
                >
                    Stop Camera
                </button>
                <button 
                    onClick={captureImage}
                    disabled={!isFaceDetected}
                    className={`px-4 py-2 rounded transition-colors ${
                        isFaceDetected 
                            ? 'bg-green-500 text-white hover:bg-green-600' 
                            : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                    }`}
                >
                    Capture
                </button>
            </div>
            
            {isCameraOn && (
                <div className="mt-4 text-center">
                    <p className={`text-sm ${
                        isFaceDetected ? 'text-green-500' : 'text-yellow-500'
                    }`}>
                        {isFaceDetected 
                            ? 'Face detected! Ready to capture.' 
                            : 'Position your face within the guide'}
                    </p>
                    <p className="text-sm text-gray-500">
                        Lighting quality: {lightingQuality}
                    </p>
                </div>
            )}
        </div>
    );
};

export default CameraCapture; 