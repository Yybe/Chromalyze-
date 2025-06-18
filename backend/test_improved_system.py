"""
Comprehensive test for the improved K-Beauty Analysis system.
Tests face shape detection accuracy and recommendations system.
"""

import sys
import os
import json
import tempfile
import cv2
import numpy as np
from typing import Dict, Any

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_realistic_test_image(face_shape: str, filename: str) -> str:
    """
    Create a more realistic test image for face shape detection.
    
    Args:
        face_shape: The face shape to simulate
        filename: Output filename
        
    Returns:
        Path to the created image
    """
    # Create a larger, more realistic image
    width, height = 600, 800
    image = np.ones((height, width, 3), dtype=np.uint8) * 240  # Light gray background
    
    center_x, center_y = width // 2, height // 2 + 50
    
    # Create more realistic face shapes with better proportions
    if face_shape == "Oval":
        # Oval: balanced, slightly longer than wide
        cv2.ellipse(image, (center_x, center_y), (120, 160), 0, 0, 360, (220, 200, 180), -1)
        # Add facial features
        add_facial_features(image, center_x, center_y, "oval")
        
    elif face_shape == "Round":
        # Round: similar width and height
        cv2.circle(image, (center_x, center_y), 140, (220, 200, 180), -1)
        add_facial_features(image, center_x, center_y, "round")
        
    elif face_shape == "Square":
        # Square: angular, strong jawline
        cv2.rectangle(image, (center_x-130, center_y-130), (center_x+130, center_y+130), (220, 200, 180), -1)
        # Soften corners slightly
        cv2.circle(image, (center_x-130, center_y-130), 20, (240, 240, 240), -1)
        cv2.circle(image, (center_x+130, center_y-130), 20, (240, 240, 240), -1)
        cv2.circle(image, (center_x-130, center_y+130), 20, (240, 240, 240), -1)
        cv2.circle(image, (center_x+130, center_y+130), 20, (240, 240, 240), -1)
        add_facial_features(image, center_x, center_y, "square")
        
    elif face_shape == "Heart":
        # Heart: wider forehead, narrow chin
        points = np.array([
            [center_x-140, center_y-120],  # Left forehead
            [center_x+140, center_y-120],  # Right forehead
            [center_x+100, center_y],      # Right cheek
            [center_x+40, center_y+80],    # Right jaw
            [center_x, center_y+140],      # Chin point
            [center_x-40, center_y+80],    # Left jaw
            [center_x-100, center_y],      # Left cheek
        ], np.int32)
        cv2.fillPoly(image, [points], (220, 200, 180))
        add_facial_features(image, center_x, center_y, "heart")
        
    elif face_shape == "Diamond":
        # Diamond: narrow forehead and jaw, wide cheekbones
        points = np.array([
            [center_x-60, center_y-140],   # Top narrow
            [center_x+60, center_y-140],
            [center_x+80, center_y-80],    # Upper cheek
            [center_x+140, center_y],      # Wide cheekbones
            [center_x+80, center_y+80],    # Lower cheek
            [center_x+60, center_y+140],   # Bottom narrow
            [center_x-60, center_y+140],
            [center_x-80, center_y+80],    # Lower cheek
            [center_x-140, center_y],      # Wide cheekbones
            [center_x-80, center_y-80],    # Upper cheek
        ], np.int32)
        cv2.fillPoly(image, [points], (220, 200, 180))
        add_facial_features(image, center_x, center_y, "diamond")
        
    elif face_shape == "Oblong":
        # Oblong: longer than wide
        cv2.ellipse(image, (center_x, center_y), (100, 180), 0, 0, 360, (220, 200, 180), -1)
        add_facial_features(image, center_x, center_y, "oblong")
        
    elif face_shape == "Triangle":
        # Triangle: narrow forehead, wide jaw
        points = np.array([
            [center_x-60, center_y-140],   # Narrow forehead
            [center_x+60, center_y-140],
            [center_x+80, center_y-40],    # Cheek
            [center_x+140, center_y+100],  # Wide jaw
            [center_x-140, center_y+100],
            [center_x-80, center_y-40],    # Cheek
        ], np.int32)
        cv2.fillPoly(image, [points], (220, 200, 180))
        add_facial_features(image, center_x, center_y, "triangle")
    
    # Save the image
    cv2.imwrite(filename, image)
    return filename

def add_facial_features(image, center_x, center_y, face_type):
    """Add realistic facial features to the test image."""
    # Eyes
    eye_y = center_y - 40
    cv2.ellipse(image, (center_x-40, eye_y), (12, 8), 0, 0, 360, (100, 80, 60), -1)
    cv2.ellipse(image, (center_x+40, eye_y), (12, 8), 0, 0, 360, (100, 80, 60), -1)
    
    # Pupils
    cv2.circle(image, (center_x-40, eye_y), 4, (0, 0, 0), -1)
    cv2.circle(image, (center_x+40, eye_y), 4, (0, 0, 0), -1)
    
    # Eyebrows
    cv2.ellipse(image, (center_x-40, eye_y-15), (15, 4), 0, 0, 180, (80, 60, 40), -1)
    cv2.ellipse(image, (center_x+40, eye_y-15), (15, 4), 0, 0, 180, (80, 60, 40), -1)
    
    # Nose
    nose_y = center_y + 10
    cv2.ellipse(image, (center_x, nose_y), (8, 15), 0, 0, 360, (200, 180, 160), -1)
    cv2.circle(image, (center_x-4, nose_y+8), 2, (180, 160, 140), -1)
    cv2.circle(image, (center_x+4, nose_y+8), 2, (180, 160, 140), -1)
    
    # Mouth
    mouth_y = center_y + 50
    cv2.ellipse(image, (center_x, mouth_y), (20, 8), 0, 0, 180, (160, 100, 100), -1)
    
    # Add some texture/shading for realism
    # Cheekbones
    if face_type in ["diamond", "square"]:
        cv2.ellipse(image, (center_x-80, center_y-10), (15, 25), 0, 0, 360, (210, 190, 170), -1)
        cv2.ellipse(image, (center_x+80, center_y-10), (15, 25), 0, 0, 360, (210, 190, 170), -1)

def test_face_shape_accuracy():
    """Test the accuracy of the improved face shape detection."""
    print("🧪 Testing Face Shape Detection Accuracy...")
    
    try:
        from face_shape_detector import classify_face_shape_advanced, get_face_shape_with_confidence
        from image_analysis import classify_face_shape
        
        face_shapes = ["Oval", "Round", "Square", "Heart", "Diamond", "Oblong", "Triangle"]
        results = {}
        detailed_results = {}
        
        temp_dir = tempfile.mkdtemp()
        
        for shape in face_shapes:
            # Create test image
            test_image = os.path.join(temp_dir, f"test_{shape.lower()}.jpg")
            create_realistic_test_image(shape, test_image)
            
            # Test advanced detection
            detected_shape = classify_face_shape_advanced(test_image)
            detailed_result = get_face_shape_with_confidence(test_image)
            
            results[shape] = detected_shape
            detailed_results[shape] = detailed_result
            
            print(f"  Expected: {shape:8} | Detected: {detected_shape:8} | Confidence: {detailed_result.get('confidence', 0):.2f}")
        
        # Calculate accuracy
        correct_predictions = sum(1 for expected, detected in results.items() if expected == detected)
        accuracy = correct_predictions / len(face_shapes)
        
        print(f"\n📊 Overall Accuracy: {accuracy:.1%} ({correct_predictions}/{len(face_shapes)})")
        
        # Clean up
        import shutil
        shutil.rmtree(temp_dir)
        
        return accuracy >= 0.5  # At least 50% accuracy expected
        
    except Exception as e:
        print(f"❌ Face shape accuracy test failed: {e}")
        return False

def test_recommendations_system():
    """Test the recommendations system comprehensively."""
    print("\n🎨 Testing Recommendations System...")
    
    try:
        from face_shape_recommendations import FaceShapeRecommendations
        
        recommendations = FaceShapeRecommendations()
        face_shapes = ["Oval", "Round", "Square", "Heart", "Diamond", "Oblong", "Triangle"]
        
        for shape in face_shapes:
            recs = recommendations.get_recommendations(shape)
            tips = recommendations.get_quick_tips(shape)
            
            # Verify structure
            assert "description" in recs, f"Missing description for {shape}"
            assert "strengths" in recs, f"Missing strengths for {shape}"
            assert "hairstyles" in recs, f"Missing hairstyles for {shape}"
            assert "makeup" in recs, f"Missing makeup for {shape}"
            assert "accessories" in recs, f"Missing accessories for {shape}"
            
            # Verify content quality
            assert len(recs["description"]) > 50, f"Description too short for {shape}"
            assert len(recs["strengths"]) >= 3, f"Not enough strengths for {shape}"
            assert len(recs["hairstyles"]["recommended"]) >= 4, f"Not enough hairstyle recommendations for {shape}"
            assert len(tips) >= 3, f"Not enough quick tips for {shape}"
            
            print(f"  ✅ {shape}: Complete recommendations with {len(recs['hairstyles']['recommended'])} hairstyles, {len(recs['strengths'])} strengths")
        
        print("✅ All recommendations are complete and detailed")
        return True
        
    except Exception as e:
        print(f"❌ Recommendations test failed: {e}")
        return False

def test_api_integration():
    """Test that the API properly returns enhanced recommendations."""
    print("\n🔗 Testing API Integration...")
    
    try:
        # Test imports
        from main import face_shape_recommendations, FACE_RECOMMENDATIONS_AVAILABLE
        
        if not FACE_RECOMMENDATIONS_AVAILABLE:
            print("❌ Face shape recommendations not available in API")
            return False
        
        # Test that recommendations can be retrieved
        test_shape = "Oval"
        recs = face_shape_recommendations.get_recommendations(test_shape)
        
        assert isinstance(recs, dict), "Recommendations should be a dictionary"
        assert "description" in recs, "API recommendations missing description"
        
        print("✅ API integration working correctly")
        return True
        
    except Exception as e:
        print(f"❌ API integration test failed: {e}")
        return False

def main():
    """Run all improvement tests."""
    print("🚀 Testing K-Beauty Analysis System Improvements\n")
    
    tests = [
        ("Face Shape Detection Accuracy", test_face_shape_accuracy),
        ("Recommendations System", test_recommendations_system),
        ("API Integration", test_api_integration),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED\n")
            else:
                print(f"❌ {test_name} FAILED\n")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}\n")
    
    print(f"📊 Final Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All improvement tests passed! System is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
