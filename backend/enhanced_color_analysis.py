"""
Enhanced Color Season Detection with MediaPipe Face Mesh and Lab Color Space Analysis
Implements 12-season color analysis with precise skin tone extraction and undertone detection.
"""

import cv2
import numpy as np
import mediapipe as mp
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import json
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
import joblib

class EnhancedColorAnalyzer:
    """Enhanced color analysis using MediaPipe Face Mesh and Lab color space."""
    
    def __init__(self):
        # Initialize MediaPipe Face Mesh
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5
        )
        
        # Define skin region landmarks (cheeks, forehead, nose)
        self.skin_landmarks = {
            'left_cheek': [116, 117, 118, 119, 120, 121, 126, 142, 36, 205, 206, 207, 213, 192, 147, 187, 207, 213, 192, 147],
            'right_cheek': [345, 346, 347, 348, 349, 350, 355, 371, 266, 425, 426, 427, 436, 416, 376, 411, 427, 436, 416, 376],
            'forehead': [10, 151, 9, 8, 107, 55, 8, 9, 10, 151, 337, 299, 333, 298, 301],
            'nose_bridge': [6, 19, 20, 94, 125, 141, 235, 236, 3, 51, 48, 115, 131, 134, 102, 49, 220, 305, 290, 328, 460, 461, 462]
        }
        
        # 12 Color Seasons with characteristics
        self.color_seasons = {
            'Deep Winter': {'undertone': 'cool', 'contrast': 'high', 'saturation': 'high'},
            'Cool Winter': {'undertone': 'cool', 'contrast': 'high', 'saturation': 'medium'},
            'Clear Winter': {'undertone': 'cool', 'contrast': 'high', 'saturation': 'high'},
            'Deep Autumn': {'undertone': 'warm', 'contrast': 'high', 'saturation': 'high'},
            'Warm Autumn': {'undertone': 'warm', 'contrast': 'medium', 'saturation': 'medium'},
            'Soft Autumn': {'undertone': 'warm', 'contrast': 'low', 'saturation': 'low'},
            'Light Spring': {'undertone': 'warm', 'contrast': 'low', 'saturation': 'medium'},
            'Warm Spring': {'undertone': 'warm', 'contrast': 'medium', 'saturation': 'high'},
            'Clear Spring': {'undertone': 'warm', 'contrast': 'high', 'saturation': 'high'},
            'Light Summer': {'undertone': 'cool', 'contrast': 'low', 'saturation': 'low'},
            'Cool Summer': {'undertone': 'cool', 'contrast': 'medium', 'saturation': 'medium'},
            'Soft Summer': {'undertone': 'cool', 'contrast': 'low', 'saturation': 'low'}
        }
        
        # Load or initialize ML model for season classification
        self.season_model = None
        self.load_season_model()
    
    def load_season_model(self):
        """Load pre-trained season classification model if available."""
        model_path = Path("saved_models/color_season_model.pkl")
        if model_path.exists():
            try:
                self.season_model = joblib.load(model_path)
                print("✅ Loaded pre-trained color season model")
            except Exception as e:
                print(f"⚠️  Could not load season model: {e}")
    
    def normalize_lighting(self, image: np.ndarray) -> np.ndarray:
        """Normalize lighting using Gray World algorithm."""
        try:
            # Convert to float for calculations
            img_float = image.astype(np.float32)
            
            # Calculate mean for each channel
            b_mean = np.mean(img_float[:, :, 0])
            g_mean = np.mean(img_float[:, :, 1])
            r_mean = np.mean(img_float[:, :, 2])
            
            # Calculate gray world scale
            gray_world = (b_mean + g_mean + r_mean) / 3
            
            # Apply correction
            if b_mean > 0:
                img_float[:, :, 0] *= (gray_world / b_mean)
            if g_mean > 0:
                img_float[:, :, 1] *= (gray_world / g_mean)
            if r_mean > 0:
                img_float[:, :, 2] *= (gray_world / r_mean)
            
            # Clip and convert back
            normalized = np.clip(img_float, 0, 255).astype(np.uint8)
            return normalized
            
        except Exception as e:
            print(f"Lighting normalization failed: {e}")
            return image
    
    def extract_skin_regions(self, image: np.ndarray, landmarks) -> Dict[str, np.ndarray]:
        """Extract skin regions using MediaPipe landmarks."""
        h, w = image.shape[:2]
        skin_regions = {}
        
        for region_name, landmark_indices in self.skin_landmarks.items():
            try:
                # Get landmark coordinates
                points = []
                for idx in landmark_indices:
                    if idx < len(landmarks.landmark):
                        x = int(landmarks.landmark[idx].x * w)
                        y = int(landmarks.landmark[idx].y * h)
                        points.append([x, y])
                
                if len(points) < 3:
                    continue
                
                # Create mask for the region
                mask = np.zeros((h, w), dtype=np.uint8)
                points_array = np.array(points, dtype=np.int32)
                cv2.fillPoly(mask, [points_array], 255)
                
                # Extract skin pixels
                skin_pixels = image[mask == 255]
                if len(skin_pixels) > 0:
                    skin_regions[region_name] = skin_pixels
                    
            except Exception as e:
                print(f"Error extracting {region_name}: {e}")
                continue
        
        return skin_regions
    
    def analyze_skin_tone_lab(self, skin_pixels: np.ndarray) -> Dict[str, float]:
        """Analyze skin tone in Lab color space."""
        if len(skin_pixels) == 0:
            return {'L': 0, 'a': 0, 'b': 0, 'chroma': 0}
        
        # Convert to Lab color space
        lab = cv2.cvtColor(skin_pixels.reshape(-1, 1, 3), cv2.COLOR_BGR2Lab)
        lab = lab.reshape(-1, 3)
        
        # Calculate mean values
        L_mean = np.mean(lab[:, 0])  # Lightness
        a_mean = np.mean(lab[:, 1])  # Green-Red axis
        b_mean = np.mean(lab[:, 2])  # Blue-Yellow axis
        
        # Calculate chroma (color intensity)
        chroma = np.sqrt(a_mean**2 + b_mean**2)
        
        return {
            'L': float(L_mean),
            'a': float(a_mean),
            'b': float(b_mean),
            'chroma': float(chroma)
        }
    
    def determine_undertone(self, lab_values: Dict[str, float]) -> str:
        """Determine undertone from Lab values."""
        a_val = lab_values['a']
        b_val = lab_values['b']
        
        # Undertone classification based on a and b channels
        if b_val > a_val + 2:  # More yellow
            return 'warm'
        elif a_val > b_val + 2:  # More red/pink
            return 'cool'
        else:
            return 'neutral'
    
    def calculate_contrast_level(self, image: np.ndarray, landmarks) -> float:
        """Calculate contrast level between skin, hair, and eyes."""
        try:
            h, w = image.shape[:2]
            
            # Extract skin tone (average from multiple regions)
            skin_regions = self.extract_skin_regions(image, landmarks)
            if not skin_regions:
                return 0.5  # Default medium contrast
            
            all_skin_pixels = np.vstack(list(skin_regions.values()))
            skin_lab = self.analyze_skin_tone_lab(all_skin_pixels)
            skin_lightness = skin_lab['L']
            
            # Estimate hair region (top of image)
            hair_region = image[:h//4, :]
            hair_lab = cv2.cvtColor(hair_region, cv2.COLOR_BGR2Lab)
            hair_lightness = np.mean(hair_lab[:, :, 0])
            
            # Calculate contrast
            contrast = abs(skin_lightness - hair_lightness) / 100.0
            return min(contrast, 1.0)  # Normalize to 0-1
            
        except Exception as e:
            print(f"Contrast calculation failed: {e}")
            return 0.5
    
    def classify_color_season(self, features: Dict[str, float]) -> Tuple[str, float]:
        """Classify color season based on extracted features."""
        
        if self.season_model:
            try:
                # Use ML model if available
                feature_vector = [
                    features['L'], features['a'], features['b'], 
                    features['chroma'], features['contrast'],
                    1 if features['undertone'] == 'warm' else 0
                ]
                
                probabilities = self.season_model.predict_proba([feature_vector])[0]
                predicted_idx = np.argmax(probabilities)
                season_names = list(self.color_seasons.keys())
                
                return season_names[predicted_idx], float(probabilities[predicted_idx])
                
            except Exception as e:
                print(f"ML classification failed: {e}")
        
        # Fallback to rule-based classification
        undertone = features['undertone']
        contrast = features['contrast']
        chroma = features['chroma']
        lightness = features['L']
        
        # Rule-based season determination
        if undertone == 'cool':
            if contrast > 0.6:  # High contrast
                if chroma > 15:
                    return 'Clear Winter', 0.8
                else:
                    return 'Cool Winter', 0.7
            elif lightness > 60:  # Light
                return 'Light Summer', 0.7
            else:  # Soft
                return 'Soft Summer', 0.7
        
        elif undertone == 'warm':
            if contrast > 0.6:  # High contrast
                if chroma > 15:
                    return 'Clear Spring', 0.8
                else:
                    return 'Deep Autumn', 0.7
            elif lightness > 60:  # Light
                return 'Light Spring', 0.7
            else:  # Soft
                return 'Soft Autumn', 0.7
        
        else:  # Neutral
            if contrast > 0.6:
                return 'Deep Winter', 0.6
            else:
                return 'Cool Summer', 0.6
    
    def analyze_image(self, image_path: str) -> Dict:
        """Perform comprehensive color analysis on an image."""
        try:
            # Load and preprocess image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not load image: {image_path}")
            
            # Normalize lighting
            normalized_image = self.normalize_lighting(image)
            
            # Convert to RGB for MediaPipe
            rgb_image = cv2.cvtColor(normalized_image, cv2.COLOR_BGR2RGB)
            
            # Process with MediaPipe
            results = self.face_mesh.process(rgb_image)
            
            if not results.multi_face_landmarks:
                return {
                    'error': 'No face detected',
                    'color_season': 'Unknown',
                    'confidence': 0.0
                }
            
            landmarks = results.multi_face_landmarks[0]
            
            # Extract skin regions
            skin_regions = self.extract_skin_regions(normalized_image, landmarks)
            
            if not skin_regions:
                return {
                    'error': 'Could not extract skin regions',
                    'color_season': 'Unknown',
                    'confidence': 0.0
                }
            
            # Combine all skin pixels for analysis
            all_skin_pixels = np.vstack(list(skin_regions.values()))
            
            # Analyze skin tone in Lab space
            lab_analysis = self.analyze_skin_tone_lab(all_skin_pixels)
            
            # Determine undertone
            undertone = self.determine_undertone(lab_analysis)
            
            # Calculate contrast
            contrast = self.calculate_contrast_level(normalized_image, landmarks)
            
            # Prepare features for classification
            features = {
                'L': lab_analysis['L'],
                'a': lab_analysis['a'],
                'b': lab_analysis['b'],
                'chroma': lab_analysis['chroma'],
                'undertone': undertone,
                'contrast': contrast
            }
            
            # Classify color season
            color_season, confidence = self.classify_color_season(features)
            
            return {
                'color_season': color_season,
                'confidence': confidence,
                'undertone': undertone,
                'skin_tone_lab': lab_analysis,
                'contrast_level': contrast,
                'features': features,
                'skin_regions_detected': list(skin_regions.keys()),
                'error': None
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'color_season': 'Unknown',
                'confidence': 0.0
            }

def analyze_color_season(image: np.ndarray) -> Tuple[str, float]:
    """Analyze color season from an image."""
    try:
        # Initialize analyzer
        analyzer = EnhancedColorAnalyzer()
        
        # Convert to RGB for MediaPipe
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Process with MediaPipe
        results = analyzer.face_mesh.process(image_rgb)
        if not results.multi_face_landmarks:
            return "No face detected", 0.0
            
        # Get landmarks
        landmarks = results.multi_face_landmarks[0]
        
        # Extract skin regions
        skin_regions = analyzer.extract_skin_regions(image, landmarks)
        if not skin_regions:
            return "Could not detect skin regions", 0.0
            
        # Analyze skin tone
        all_skin_pixels = np.vstack(list(skin_regions.values()))
        lab_values = analyzer.analyze_skin_tone_lab(all_skin_pixels)
        
        # Get additional features
        undertone = analyzer.determine_undertone(lab_values)
        contrast = analyzer.calculate_contrast_level(image, landmarks)
        
        # Combine features
        features = {
            'L': lab_values['L'],
            'a': lab_values['a'],
            'b': lab_values['b'],
            'chroma': lab_values['chroma'],
            'contrast': contrast,
            'undertone': undertone
        }
        
        # Classify season
        season, confidence = analyzer.classify_color_season(features)
        return season, confidence
        
    except Exception as e:
        return f"Error: {str(e)}", 0.0

# Example usage and testing
if __name__ == "__main__":
    analyzer = EnhancedColorAnalyzer()
    
    # Test with a sample image
    test_image = "test_image.jpg"  # Replace with actual test image
    if Path(test_image).exists():
        result = analyzer.analyze_image(test_image)
        print("Enhanced Color Analysis Result:")
        print(json.dumps(result, indent=2))
    else:
        print("No test image found. Place a test image as 'test_image.jpg' to test.")
