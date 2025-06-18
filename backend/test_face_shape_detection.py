"""
Test cases for face shape detection accuracy.
This module provides comprehensive testing for the face shape detection system.
"""

import unittest
import os
import cv2
import numpy as np
from typing import Dict, List, Tuple
import tempfile
from pathlib import Path

# Import the modules to test
try:
    from face_shape_detector import FaceShapeDetector, classify_face_shape_advanced
    from face_shape_recommendations import FaceShapeRecommendations
    from image_analysis import classify_face_shape
    MODULES_AVAILABLE = True
except ImportError as e:
    print(f"Could not import modules for testing: {e}")
    MODULES_AVAILABLE = False

class TestFaceShapeDetection(unittest.TestCase):
    """Test cases for face shape detection accuracy."""
    
    def setUp(self):
        """Set up test fixtures."""
        if not MODULES_AVAILABLE:
            self.skipTest("Required modules not available")
        
        self.detector = FaceShapeDetector()
        self.recommendations = FaceShapeRecommendations()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Clean up temporary files
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def create_synthetic_face_image(self, face_shape: str, size: Tuple[int, int] = (400, 500)) -> str:
        """
        Create a synthetic face image for testing specific face shapes.
        
        Args:
            face_shape: The face shape to simulate
            size: Image size (width, height)
            
        Returns:
            Path to the created test image
        """
        width, height = size
        image = np.ones((height, width, 3), dtype=np.uint8) * 255  # White background
        
        # Define face parameters based on shape
        center_x, center_y = width // 2, height // 2
        
        if face_shape == "Oval":
            # Oval face: balanced proportions
            cv2.ellipse(image, (center_x, center_y), (80, 120), 0, 0, 360, (200, 200, 200), -1)
        elif face_shape == "Round":
            # Round face: similar width and height
            cv2.circle(image, (center_x, center_y), 100, (200, 200, 200), -1)
        elif face_shape == "Square":
            # Square face: angular, similar width and height
            cv2.rectangle(image, (center_x-90, center_y-90), (center_x+90, center_y+90), (200, 200, 200), -1)
        elif face_shape == "Heart":
            # Heart face: wider forehead, narrow chin
            points = np.array([
                [center_x-100, center_y-80],  # Left forehead
                [center_x+100, center_y-80],  # Right forehead
                [center_x+60, center_y+20],   # Right cheek
                [center_x, center_y+100],     # Chin point
                [center_x-60, center_y+20],   # Left cheek
            ], np.int32)
            cv2.fillPoly(image, [points], (200, 200, 200))
        elif face_shape == "Diamond":
            # Diamond face: narrow forehead and jaw, wide cheekbones
            points = np.array([
                [center_x-40, center_y-100],  # Top narrow
                [center_x+40, center_y-100],
                [center_x+100, center_y],     # Wide cheekbones
                [center_x+40, center_y+100],  # Bottom narrow
                [center_x-40, center_y+100],
                [center_x-100, center_y],     # Wide cheekbones
            ], np.int32)
            cv2.fillPoly(image, [points], (200, 200, 200))
        elif face_shape == "Oblong":
            # Oblong face: longer than wide
            cv2.ellipse(image, (center_x, center_y), (70, 140), 0, 0, 360, (200, 200, 200), -1)
        elif face_shape == "Triangle":
            # Triangle face: narrow forehead, wide jaw
            points = np.array([
                [center_x-40, center_y-100],  # Narrow forehead
                [center_x+40, center_y-100],
                [center_x+100, center_y+80],  # Wide jaw
                [center_x-100, center_y+80],
            ], np.int32)
            cv2.fillPoly(image, [points], (200, 200, 200))
        
        # Add basic facial features for better detection
        # Eyes
        cv2.circle(image, (center_x-30, center_y-20), 8, (100, 100, 100), -1)
        cv2.circle(image, (center_x+30, center_y-20), 8, (100, 100, 100), -1)
        
        # Nose
        cv2.circle(image, (center_x, center_y+10), 5, (150, 150, 150), -1)
        
        # Mouth
        cv2.ellipse(image, (center_x, center_y+40), (15, 8), 0, 0, 180, (100, 100, 100), 2)
        
        # Save the image
        filename = os.path.join(self.temp_dir, f"test_{face_shape.lower()}.jpg")
        cv2.imwrite(filename, image)
        return filename
    
    def test_face_shape_detection_accuracy(self):
        """Test the accuracy of face shape detection on synthetic images."""
        face_shapes = ["Oval", "Round", "Square", "Heart", "Diamond", "Oblong", "Triangle"]
        
        results = {}
        for shape in face_shapes:
            # Create test image
            test_image = self.create_synthetic_face_image(shape)
            
            # Test advanced detection
            detected_shape = classify_face_shape_advanced(test_image)
            results[shape] = detected_shape
            
            print(f"Expected: {shape}, Detected: {detected_shape}")
        
        # Calculate accuracy
        correct_predictions = sum(1 for expected, detected in results.items() if expected == detected)
        accuracy = correct_predictions / len(face_shapes)
        
        print(f"\nOverall Accuracy: {accuracy:.2%} ({correct_predictions}/{len(face_shapes)})")
        
        # We expect at least 60% accuracy on synthetic images
        self.assertGreaterEqual(accuracy, 0.6, f"Face shape detection accuracy too low: {accuracy:.2%}")
    
    def test_recommendations_completeness(self):
        """Test that recommendations are available for all face shapes."""
        face_shapes = ["Oval", "Round", "Square", "Heart", "Diamond", "Oblong", "Triangle"]
        
        for shape in face_shapes:
            recommendations = self.recommendations.get_recommendations(shape)
            
            # Check that all required fields are present
            self.assertIn("description", recommendations)
            self.assertIn("strengths", recommendations)
            self.assertIn("hairstyles", recommendations)
            self.assertIn("makeup", recommendations)
            self.assertIn("accessories", recommendations)
            
            # Check hairstyles section
            self.assertIn("recommended", recommendations["hairstyles"])
            self.assertIn("avoid", recommendations["hairstyles"])
            
            # Check that recommendations are not empty
            self.assertTrue(len(recommendations["hairstyles"]["recommended"]) > 0)
            self.assertTrue(len(recommendations["description"]) > 0)
    
    def test_confidence_scoring(self):
        """Test that confidence scores are reasonable."""
        # Create a clear oval face
        test_image = self.create_synthetic_face_image("Oval")
        
        detector = FaceShapeDetector()
        result = detector.detect_face_shape(test_image)
        
        # Check that confidence is returned and is reasonable
        self.assertIn("confidence", result)
        self.assertGreaterEqual(result["confidence"], 0.0)
        self.assertLessEqual(result["confidence"], 1.0)
        
        # For a clear synthetic image, confidence should be decent
        self.assertGreaterEqual(result["confidence"], 0.3)
    
    def test_error_handling(self):
        """Test error handling for invalid inputs."""
        # Test with non-existent file
        result = classify_face_shape_advanced("non_existent_file.jpg")
        self.assertEqual(result, "Unknown")
        
        # Test with invalid image
        invalid_file = os.path.join(self.temp_dir, "invalid.txt")
        with open(invalid_file, 'w') as f:
            f.write("This is not an image")
        
        result = classify_face_shape_advanced(invalid_file)
        self.assertEqual(result, "Unknown")
    
    def test_quick_tips_generation(self):
        """Test that quick tips are generated for all face shapes."""
        face_shapes = ["Oval", "Round", "Square", "Heart", "Diamond", "Oblong", "Triangle"]
        
        for shape in face_shapes:
            tips = self.recommendations.get_quick_tips(shape)
            
            # Should return a list of tips
            self.assertIsInstance(tips, list)
            self.assertGreater(len(tips), 0)
            
            # First tip should mention the face shape
            self.assertIn(shape.lower(), tips[0].lower())

def run_face_shape_tests():
    """Run all face shape detection tests."""
    if not MODULES_AVAILABLE:
        print("Required modules not available for testing")
        return False
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFaceShapeDetection)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return success status
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_face_shape_tests()
    if success:
        print("\n✅ All face shape detection tests passed!")
    else:
        print("\n❌ Some face shape detection tests failed!")
    
    exit(0 if success else 1)
