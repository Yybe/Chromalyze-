"""
Advanced Face Shape Detection using CNN and MediaPipe Facial Landmarks
This module provides accurate face shape classification using a trained CNN model with MediaPipe fallback.
"""

import cv2
import numpy as np
import mediapipe as mp
from typing import Dict, List, Tuple, Optional
import math
import os
from pathlib import Path

# Try to import CNN model
try:
    from ml_models.face_shape_cnn import load_trained_model
    from ml_models.model_config import ModelConfig
    CNN_MODEL_AVAILABLE = True
    print("CNN model imports successful")
except ImportError as e:
    print(f"CNN model not available: {e}")
    CNN_MODEL_AVAILABLE = False

class FaceShapeDetector:
    """
    Advanced face shape detector using CNN model with MediaPipe fallback.
    Analyzes facial geometry to accurately classify face shapes.
    """

    def __init__(self):
        """Initialize CNN model and MediaPipe face mesh detector."""
        # Try to load CNN model first
        self.cnn_model = None
        if CNN_MODEL_AVAILABLE:
            try:
                config = ModelConfig()
                if config.get_model_path().exists():
                    self.cnn_model = load_trained_model()
                    print("CNN model loaded successfully")
                else:
                    print(f"CNN model file not found: {config.get_model_path()}")
            except Exception as e:
                print(f"Failed to load CNN model: {e}")

        # Initialize MediaPipe as fallback
        self.mp_face_mesh = mp.solutions.face_mesh.FaceMesh(
            max_num_faces=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Key facial landmark indices for face shape analysis
        self.FACE_OVAL = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288,
                         397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136,
                         172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109]

        # More comprehensive landmark points for better measurements
        self.FOREHEAD_TOP = 10
        self.FOREHEAD_LEFT = 21
        self.FOREHEAD_RIGHT = 251
        self.CHIN_BOTTOM = 152
        self.CHIN_LEFT = 172
        self.CHIN_RIGHT = 397
        self.LEFT_CHEEK = 234
        self.RIGHT_CHEEK = 454
        self.JAW_LEFT = 172
        self.JAW_RIGHT = 397
        self.TEMPLE_LEFT = 21
        self.TEMPLE_RIGHT = 251

        # Additional points for better analysis
        self.NOSE_TIP = 1
        self.LEFT_EYE_OUTER = 33
        self.RIGHT_EYE_OUTER = 362
        self.MOUTH_LEFT = 61
        self.MOUTH_RIGHT = 291

    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Enhanced image preprocessing for better face detection."""
        # Convert to RGB if needed
        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        elif image.shape[2] == 4:
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
        
        # Apply face detection and alignment
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # Enhance image for better detection
        gray = cv2.equalizeHist(gray)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) > 0:
            # Get the largest face
            face = max(faces, key=lambda x: x[2] * x[3])
            x, y, w, h = face
            
            # Add margin around face
            margin = int(max(w, h) * 0.2)
            x1 = max(0, x - margin)
            y1 = max(0, y - margin)
            x2 = min(image.shape[1], x + w + margin)
            y2 = min(image.shape[0], y + h + margin)
            
            # Crop and resize
            face_img = image[y1:y2, x1:x2]
            face_img = cv2.resize(face_img, (224, 224))
            
            # Apply additional preprocessing
            face_img = cv2.fastNlMeansDenoisingColored(face_img, None, 10, 10, 7, 21)
            face_img = cv2.detailEnhance(face_img, sigma_s=10, sigma_r=0.15)
            
            return face_img
        else:
            # If no face detected, resize the whole image
            return cv2.resize(image, (224, 224))

    def detect_face_shape(self, image: np.ndarray) -> Tuple[str, float, Dict[str, float]]:
        """Detect face shape using CNN model with enhanced confidence scoring."""
        # Preprocess image
        processed_image = self.preprocess_image(image)
        
        if self.cnn_model is not None:
            try:
                # Add batch dimension and normalize
                input_image = np.expand_dims(processed_image, axis=0)
                input_image = input_image.astype(np.float32) / 255.0
                
                # Get predictions
                predictions = self.cnn_model.model.predict(input_image, verbose=0)
                predicted_probs = predictions[0]
                
                # Get predicted class and confidence
                predicted_idx = np.argmax(predicted_probs)
                confidence = float(predicted_probs[predicted_idx])
                
                # Create probability dictionary
                class_probabilities = {}
                for idx, prob in enumerate(predicted_probs):
                    class_name = self.cnn_model.data_loader.idx_to_class[idx]
                    class_probabilities[class_name] = float(prob)
                
                # If confidence is too low, use MediaPipe fallback
                if confidence < 0.75:
                    print("Low CNN confidence, using MediaPipe fallback...")
                    return self._detect_with_mediapipe(image)
                
                return self.cnn_model.data_loader.idx_to_class[predicted_idx], confidence, class_probabilities
                
            except Exception as e:
                print(f"CNN prediction failed: {e}")
                return self._detect_with_mediapipe(image)
        else:
            return self._detect_with_mediapipe(image)

    def _detect_with_mediapipe(self, image: np.ndarray) -> Tuple[str, float, Dict[str, float]]:
        """Fallback detection using MediaPipe facial landmarks."""
        # Convert to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Get face mesh
        results = self.mp_face_mesh.process(image_rgb)
        
        if not results.multi_face_landmarks:
            return "Unknown", 0.0, {}
        
        # Get landmarks
        landmarks = results.multi_face_landmarks[0].landmark
        
        # Calculate face measurements
        face_width = self._calculate_distance(landmarks[self.TEMPLE_LEFT], landmarks[self.TEMPLE_RIGHT])
        face_height = self._calculate_distance(landmarks[self.FOREHEAD_TOP], landmarks[self.CHIN_BOTTOM])
        jaw_width = self._calculate_distance(landmarks[self.JAW_LEFT], landmarks[self.JAW_RIGHT])
        forehead_width = self._calculate_distance(landmarks[self.FOREHEAD_LEFT], landmarks[self.FOREHEAD_RIGHT])
        
        # Calculate ratios
        face_ratio = face_height / face_width
        jaw_ratio = jaw_width / forehead_width
        
        # Determine face shape
        if jaw_ratio < 0.8:
            shape = "Heart"
            confidence = 0.85
        elif face_ratio > 1.5:
            shape = "Oblong"
            confidence = 0.85
        elif 1.3 <= face_ratio <= 1.5 and 0.8 <= jaw_ratio <= 1.1:
            shape = "Oval"
            confidence = 0.85
        elif face_ratio < 1.3 and jaw_ratio > 1.1:
            shape = "Round"
            confidence = 0.85
        else:
            shape = "Square"
            confidence = 0.85
        
        # Create probability dictionary
        class_probabilities = {
            "Heart": 0.0, "Oblong": 0.0, "Oval": 0.0, "Round": 0.0, "Square": 0.0
        }
        class_probabilities[shape] = confidence
        
        return shape, confidence, class_probabilities

    def _calculate_distance(self, point1, point2) -> float:
        """Calculate Euclidean distance between two points."""
        return math.sqrt(
            (point1.x - point2.x) ** 2 +
            (point1.y - point2.y) ** 2
        )

    def _get_key_points(self, landmarks, image_shape) -> Dict[str, Tuple[float, float]]:
        """Extract key facial landmarks and convert to pixel coordinates."""
        h, w = image_shape[:2]
        return {
            "forehead": (landmarks[10].x * w, landmarks[10].y * h),  # Top of forehead
            "chin": (landmarks[152].x * w, landmarks[152].y * h),     # Bottom of chin
            "left_cheek": (landmarks[234].x * w, landmarks[234].y * h),  # Left cheekbone
            "right_cheek": (landmarks[454].x * w, landmarks[454].y * h), # Right cheekbone
            "left_jaw": (landmarks[93].x * w, landmarks[93].y * h),   # Left jaw
            "right_jaw": (landmarks[323].x * w, landmarks[323].y * h) # Right jaw
        }

    def _compute_measurements(self, key_points: Dict[str, Tuple[float, float]]) -> Dict[str, float]:
        """Compute facial measurements from key points."""
        length = abs(key_points["forehead"][1] - key_points["chin"][1])
        width = abs(key_points["left_cheek"][0] - key_points["right_cheek"][0])
        jaw_width = abs(key_points["left_jaw"][0] - key_points["right_jaw"][0])
        forehead_width = abs(key_points["left_cheek"][0] - key_points["right_cheek"][0])  # Using cheek width as approximation
        
        length_width_ratio = length / width if width > 0 else 1.0
        jaw_forehead_ratio = jaw_width / forehead_width if forehead_width > 0 else 1.0
        
        # Calculate jawline angle
        jawline_angle = np.arctan2(
            key_points["chin"][1] - key_points["left_jaw"][1],
            key_points["chin"][0] - key_points["left_jaw"][0]
        ) * 180 / np.pi
        
        return {
            "length_width_ratio": length_width_ratio,
            "jaw_forehead_ratio": jaw_forehead_ratio,
            "jawline_angle": jawline_angle
        }

    def _classify_face_shape(self, measurements: Dict[str, float]) -> Tuple[str, float]:
        """Classify face shape based on measurements using rule-based approach."""
        shapes = ["Oval", "Round", "Square", "Heart", "Diamond", "Oblong", "Triangle"]
        scores = [0.0] * 7
        
        lw_ratio = measurements["length_width_ratio"]
        jf_ratio = measurements["jaw_forehead_ratio"]
        jaw_angle = measurements["jawline_angle"]
        
        # Oval: Length ~1.5x width, jaw ≈ forehead
        if 1.3 <= lw_ratio <= 1.6 and abs(jf_ratio - 1.0) < 0.1:
            scores[0] = 0.9
            
        # Round: Length ≈ width, rounded jaw
        if 0.9 <= lw_ratio <= 1.1 and jaw_angle < 30:
            scores[1] = 0.85
            
        # Square: Length ≈ width, wide jaw
        if 0.9 <= lw_ratio <= 1.1 and jf_ratio > 1.1:
            scores[2] = 0.85
            
        # Heart: Wider cheekbones, pointed chin
        if jf_ratio < 0.8 and lw_ratio > 1.2:
            scores[3] = 0.9
            
        # Diamond: Wider cheekbones, narrower forehead/chin
        if jf_ratio < 0.9 and lw_ratio > 1.4:
            scores[4] = 0.85
            
        # Oblong: Length > 1.6x width
        if lw_ratio > 1.6:
            scores[5] = 0.9
            
        # Triangle: Wider jaw, narrower forehead
        if jf_ratio > 1.2 and lw_ratio < 1.3:
            scores[6] = 0.85
            
        # Normalize scores
        total_score = sum(scores)
        if total_score == 0:
            return "Uncertain", 0.0
            
        scores = [s / total_score for s in scores]
        max_idx = np.argmax(scores)
        return shapes[max_idx], float(scores[max_idx])

    def detect_face_shape(self, image: np.ndarray) -> Tuple[str, float]:
        """Detect face shape from an image."""
        try:
            # Convert to RGB for MediaPipe
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Process with MediaPipe
            results = self.mp_face_mesh.process(image_rgb)
            if not results.multi_face_landmarks:
                return "No face detected", 0.0
                
            # Get landmarks and compute measurements
            landmarks = results.multi_face_landmarks[0].landmark
            key_points = self._get_key_points(landmarks, image.shape)
            measurements = self._compute_measurements(key_points)
            
            # Classify face shape
            shape, confidence = self._classify_face_shape(measurements)
            return shape, confidence
            
        except Exception as e:
            return f"Error: {str(e)}", 0.0

def classify_face_shape_advanced(image_path: str) -> str:
    """
    Advanced face shape classification function for backward compatibility.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Face shape classification as string
    """
    detector = FaceShapeDetector()
    result = detector.detect_face_shape(cv2.imread(image_path))
    return result[0]

def get_face_shape_with_confidence(image_path: str) -> Dict[str, any]:
    """
    Get face shape classification with confidence score and detailed measurements.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Dictionary with face shape, confidence, and measurements
    """
    detector = FaceShapeDetector()
    return detector.detect_face_shape(cv2.imread(image_path))
