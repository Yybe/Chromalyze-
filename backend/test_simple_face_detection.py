"""
Simple test for face shape detection system.
"""

import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported correctly."""
    try:
        from face_shape_detector import FaceShapeDetector, classify_face_shape_advanced
        print("✅ Face shape detector imported successfully")
        
        from face_shape_recommendations import FaceShapeRecommendations
        print("✅ Face shape recommendations imported successfully")
        
        from image_analysis import classify_face_shape
        print("✅ Image analysis imported successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_recommendations():
    """Test the recommendations system."""
    try:
        from face_shape_recommendations import FaceShapeRecommendations
        
        recommendations = FaceShapeRecommendations()
        face_shapes = ["Oval", "Round", "Square", "Heart", "Diamond", "Oblong", "Triangle"]
        
        print("\n🧪 Testing recommendations for all face shapes:")
        for shape in face_shapes:
            recs = recommendations.get_recommendations(shape)
            tips = recommendations.get_quick_tips(shape)
            
            print(f"  {shape}: {len(recs)} recommendation categories, {len(tips)} quick tips")
            
            # Verify structure
            assert "description" in recs
            assert "hairstyles" in recs
            assert "makeup" in recs
            assert "accessories" in recs
            assert len(tips) > 0
        
        print("✅ All face shape recommendations working correctly")
        return True
    except Exception as e:
        print(f"❌ Recommendations test failed: {e}")
        return False

def test_detector_initialization():
    """Test that the face shape detector can be initialized."""
    try:
        from face_shape_detector import FaceShapeDetector
        
        detector = FaceShapeDetector()
        print("✅ Face shape detector initialized successfully")
        
        # Test with a non-existent file (should handle gracefully)
        result = detector.detect_face_shape("non_existent_file.jpg")
        
        assert "face_shape" in result
        assert "confidence" in result
        assert "error" in result
        
        print(f"✅ Error handling works: {result}")
        return True
    except Exception as e:
        print(f"❌ Detector initialization test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting face shape detection system tests...\n")
    
    tests = [
        ("Import Test", test_imports),
        ("Recommendations Test", test_recommendations),
        ("Detector Initialization Test", test_detector_initialization),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Face shape detection system is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
