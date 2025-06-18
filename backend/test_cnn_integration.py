"""
Test script to verify CNN model integration with face shape detection.
"""

import os
import sys
import json
from pathlib import Path
import random

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from face_shape_detector import FaceShapeDetector, get_face_shape_with_confidence
from image_analysis import analyze_image

def test_individual_images():
    """Test face shape detection on individual images from the dataset."""
    print("Testing Face Shape Detection with CNN Integration")
    print("=" * 55)
    
    # Initialize detector
    detector = FaceShapeDetector()
    
    # Test with sample images from each class
    dataset_root = Path("backend/FaceShapeDS/testing_set")
    class_names = ['Heart', 'Oblong', 'Oval', 'Round', 'Square']
    
    results = []
    
    for class_name in class_names:
        class_dir = dataset_root / class_name
        if not class_dir.exists():
            print(f"❌ Class directory not found: {class_dir}")
            continue
        
        # Get a few random images from this class
        image_files = list(class_dir.glob("*.jpg")) + list(class_dir.glob("*.jpeg")) + list(class_dir.glob("*.png"))
        
        if not image_files:
            print(f"❌ No images found in {class_dir}")
            continue
        
        # Test 3 random images from each class
        test_images = random.sample(image_files, min(3, len(image_files)))
        
        print(f"\nTesting {class_name} face shape:")
        print("-" * 30)
        
        for img_path in test_images:
            try:
                result = detector.detect_face_shape(str(img_path))
                
                predicted_shape = result.get("face_shape", "Unknown")
                confidence = result.get("confidence", 0.0)
                method = result.get("method", "Unknown")
                error = result.get("error")
                
                if error:
                    print(f"  ❌ {img_path.name}: Error - {error}")
                else:
                    # Check if prediction is correct
                    is_correct = predicted_shape == class_name
                    status = "✅" if is_correct else "❌"
                    
                    print(f"  {status} {img_path.name}: {predicted_shape} ({confidence:.3f}) [{method}]")
                    
                    results.append({
                        "image": str(img_path),
                        "true_class": class_name,
                        "predicted_class": predicted_shape,
                        "confidence": confidence,
                        "method": method,
                        "correct": is_correct
                    })
                
            except Exception as e:
                print(f"  ❌ {img_path.name}: Exception - {e}")
    
    # Calculate accuracy
    if results:
        correct_predictions = sum(1 for r in results if r["correct"])
        total_predictions = len(results)
        accuracy = correct_predictions / total_predictions
        
        print(f"\n📊 Test Results Summary:")
        print(f"   Total images tested: {total_predictions}")
        print(f"   Correct predictions: {correct_predictions}")
        print(f"   Accuracy: {accuracy:.3f} ({accuracy*100:.1f}%)")
        
        # Method breakdown
        cnn_results = [r for r in results if r["method"] == "CNN"]
        mediapipe_results = [r for r in results if r["method"] == "MediaPipe"]
        
        if cnn_results:
            cnn_accuracy = sum(1 for r in cnn_results if r["correct"]) / len(cnn_results)
            print(f"   CNN accuracy: {cnn_accuracy:.3f} ({len(cnn_results)} images)")
        
        if mediapipe_results:
            mp_accuracy = sum(1 for r in mediapipe_results if r["correct"]) / len(mediapipe_results)
            print(f"   MediaPipe accuracy: {mp_accuracy:.3f} ({len(mediapipe_results)} images)")
        
        # Save detailed results
        with open("test_results.json", "w") as f:
            json.dump(results, f, indent=2)
        print(f"\n📁 Detailed results saved to: test_results.json")
    
    return results

def test_api_integration():
    """Test integration with the main image analysis API."""
    print("\n" + "=" * 55)
    print("Testing API Integration")
    print("=" * 55)
    
    # Get a sample image
    dataset_root = Path("backend/FaceShapeDS/testing_set")
    sample_classes = ['Heart', 'Oval', 'Round']
    
    for class_name in sample_classes:
        class_dir = dataset_root / class_name
        if class_dir.exists():
            image_files = list(class_dir.glob("*.jpg"))
            if image_files:
                sample_image = image_files[0]
                
                print(f"\nTesting API with {class_name} image: {sample_image.name}")
                
                try:
                    # Test the main analyze_image function
                    result = analyze_image(str(sample_image))
                    
                    print(f"  Status: {result.get('status', 'Unknown')}")
                    print(f"  Face shape: {result.get('face_shape', 'Unknown')}")
                    print(f"  Color season: {result.get('color_season', 'Unknown')}")
                    print(f"  Faces detected: {result.get('faces_detected', 0)}")
                    
                    if result.get('detail'):
                        print(f"  Detail: {result['detail']}")
                
                except Exception as e:
                    print(f"  ❌ API test failed: {e}")
                
                break

def main():
    """Main test function."""
    # Test individual images
    results = test_individual_images()
    
    # Test API integration
    test_api_integration()
    
    print("\n🏁 Testing completed!")
    
    if results:
        accuracy = sum(1 for r in results if r["correct"]) / len(results)
        if accuracy >= 0.85:
            print(f"🎉 Great! Accuracy target achieved: {accuracy:.3f}")
        else:
            print(f"⚠️  Accuracy below target: {accuracy:.3f} (target: 0.85)")

if __name__ == "__main__":
    main()
