"""
Deep cleaning script to remove all problematic images including truncated ones.
"""

import os
from pathlib import Path
from PIL import Image, ImageFile
import cv2

# Allow loading of truncated images for testing
ImageFile.LOAD_TRUNCATED_IMAGES = True

def is_image_completely_valid(image_path):
    """Comprehensive image validation."""
    try:
        # Test 1: PIL basic load and verify
        with Image.open(image_path) as img:
            img.load()  # Force load all data
            img.verify()
            
        # Test 2: Reload and check if we can resize (common failure point)
        with Image.open(image_path) as img:
            img.resize((224, 224))
            
        # Test 3: OpenCV load
        img_cv = cv2.imread(str(image_path))
        if img_cv is None:
            return False, "OpenCV cannot load"
            
        # Test 4: Check dimensions
        if img_cv.shape[0] < 50 or img_cv.shape[1] < 50:
            return False, "Image too small"
            
        # Test 5: Check if image has proper channels
        if len(img_cv.shape) != 3 or img_cv.shape[2] != 3:
            return False, "Invalid channels"
            
        # Test 6: Try to convert color space
        try:
            cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
        except Exception as e:
            return False, f"Color conversion failed: {e}"
            
        return True, "OK"
        
    except Exception as e:
        return False, str(e)

def deep_clean_directory(directory):
    """Deep clean a directory by testing all image operations."""
    print(f"Deep cleaning: {directory}")
    
    removed_count = 0
    total_count = 0
    
    for class_dir in directory.iterdir():
        if not class_dir.is_dir() or class_dir.name in ["desktop.ini", "__pycache__"]:
            continue
            
        print(f"  Checking class: {class_dir.name}")
        
        # Get all image files
        image_extensions = ["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.tiff", "*.gif"]
        image_files = []
        for ext in image_extensions:
            image_files.extend(class_dir.glob(ext))
            image_files.extend(class_dir.glob(ext.upper()))
        
        class_removed = 0
        
        for img_path in image_files:
            total_count += 1
            is_valid, reason = is_image_completely_valid(img_path)
            
            if not is_valid:
                print(f"    Removing {img_path.name}: {reason}")
                try:
                    img_path.unlink()
                    removed_count += 1
                    class_removed += 1
                except Exception as e:
                    print(f"    Failed to delete {img_path}: {e}")
        
        # Count remaining images
        remaining_files = []
        for ext in ["*.jpg", "*.jpeg", "*.png"]:
            remaining_files.extend(class_dir.glob(ext))
        remaining = len(remaining_files)
        
        print(f"    Removed: {class_removed}, Remaining: {remaining}")
    
    print(f"  Total processed: {total_count}")
    print(f"  Total removed: {removed_count}")
    return removed_count

def main():
    """Main deep cleaning function."""
    print("Deep Dataset Cleaning")
    print("=" * 30)
    
    dataset_root = Path("FaceShapeDS")
    
    if not dataset_root.exists():
        print(f"Error: Dataset not found at {dataset_root}")
        return
    
    total_removed = 0
    
    # Clean training set
    train_dir = dataset_root / "training_set"
    if train_dir.exists():
        print("\nDeep cleaning training set...")
        total_removed += deep_clean_directory(train_dir)
    
    # Clean test set
    test_dir = dataset_root / "testing_set"
    if test_dir.exists():
        print("\nDeep cleaning test set...")
        total_removed += deep_clean_directory(test_dir)
    
    print(f"\nDeep cleaning completed!")
    print(f"Total images removed: {total_removed}")
    
    # Final count
    print("\nFinal image counts after deep cleaning:")
    for dataset_name, dataset_dir in [("Training", train_dir), ("Test", test_dir)]:
        if dataset_dir.exists():
            print(f"\n{dataset_name} set:")
            total_images = 0
            for class_dir in sorted(dataset_dir.iterdir()):
                if class_dir.is_dir() and class_dir.name not in ["desktop.ini", "__pycache__"]:
                    count = len(list(class_dir.glob("*.jpg"))) + len(list(class_dir.glob("*.jpeg"))) + len(list(class_dir.glob("*.png")))
                    print(f"  {class_dir.name}: {count} images")
                    total_images += count
            print(f"  Total: {total_images} images")

if __name__ == "__main__":
    main()
