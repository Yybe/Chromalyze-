import React from 'react';

const FaceGuideOverlay = () => {
    return (
        <div className="absolute inset-0 pointer-events-none">
            {/* Face outline guide */}
            <div className="absolute top-1/4 left-1/2 transform -translate-x-1/2 w-64 h-80 border-2 border-blue-500 rounded-full opacity-50">
                {/* Eye guides */}
                <div className="absolute top-1/3 left-1/4 w-8 h-4 border-2 border-blue-500 rounded-full opacity-50"></div>
                <div className="absolute top-1/3 right-1/4 w-8 h-4 border-2 border-blue-500 rounded-full opacity-50"></div>
                
                {/* Mouth guide */}
                <div className="absolute bottom-1/4 left-1/2 transform -translate-x-1/2 w-16 h-8 border-2 border-blue-500 rounded-full opacity-50"></div>
            </div>
            
            {/* Instructions */}
            <div className="absolute bottom-4 left-0 right-0 text-center text-white bg-black bg-opacity-50 p-2">
                <p className="text-sm">Position your face within the oval guide</p>
                <p className="text-sm">Ensure good lighting and remove glasses</p>
            </div>
            
            {/* Lighting indicator */}
            <div className="absolute top-4 right-4 bg-black bg-opacity-50 p-2 rounded">
                <div className="flex items-center space-x-2">
                    <div className="w-3 h-3 rounded-full bg-green-500"></div>
                    <span className="text-white text-sm">Good lighting</span>
                </div>
            </div>
        </div>
    );
};

export default FaceGuideOverlay; 