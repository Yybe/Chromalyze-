"""
Thorough dataset cleaning - removes all problematic images.
"""

import os
from pathlib import Path
from PIL import Image, ImageFile
import cv2

# Allow loading of truncated images for checking
ImageFile.LOAD_TRUNCATED_IMAGES = True

def is_image_valid(image_path):
    """Check if an image is valid and can be loaded properly."""
    try:
        # Test 1: PIL basic load
        with Image.open(image_path) as img:
            img.load()  # Force load the image data
            
        # Test 2: PIL verify
        with Image.open(image_path) as img:
            img.verify()
            
        # Test 3: OpenCV load
        img = cv2.imread(str(image_path))
        if img is None:
            return False, "OpenCV cannot load"
            
        # Test 4: Check if image has proper dimensions
        if img.shape[0] < 50 or img.shape[1] < 50:
            return False, "Image too small"
            
        # Test 5: Try to resize (this often fails on corrupted images)
        try:
            with Image.open(image_path) as img:
                img.resize((224, 224))
        except Exception as e:
            return False, f"Resize failed: {e}"
            
        return True, "OK"
        
    except Exception as e:
        return False, str(e)

def clean_directory_thoroughly(directory):
    """Thoroughly clean a directory by testing all images."""
    print(f"Thoroughly cleaning: {directory}")
    
    removed_count = 0
    total_count = 0
    
    for class_dir in directory.iterdir():
        if not class_dir.is_dir() or class_dir.name == "desktop.ini":
            continue
            
        print(f"  Checking class: {class_dir.name}")
        
        # Get all image files
        image_extensions = ["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.tiff"]
        image_files = []
        for ext in image_extensions:
            image_files.extend(class_dir.glob(ext))
            image_files.extend(class_dir.glob(ext.upper()))
        
        class_removed = 0
        
        for img_path in image_files:
            total_count += 1
            is_valid, reason = is_image_valid(img_path)
            
            if not is_valid:
                print(f"    Removing {img_path.name}: {reason}")
                try:
                    img_path.unlink()
                    removed_count += 1
                    class_removed += 1
                except Exception as e:
                    print(f"    Failed to delete {img_path}: {e}")
        
        remaining = len(list(class_dir.glob("*.jpg"))) + len(list(class_dir.glob("*.jpeg"))) + len(list(class_dir.glob("*.png")))
        print(f"    Removed: {class_removed}, Remaining: {remaining}")
    
    print(f"  Total processed: {total_count}")
    print(f"  Total removed: {removed_count}")
    return removed_count

def main():
    """Main cleaning function."""
    print("Thorough Dataset Cleaning")
    print("=" * 30)
    
    dataset_root = Path("FaceShapeDS")
    
    if not dataset_root.exists():
        print(f"Error: Dataset not found at {dataset_root}")
        return
    
    total_removed = 0
    
    # Clean training set
    train_dir = dataset_root / "training_set"
    if train_dir.exists():
        print("\nCleaning training set...")
        total_removed += clean_directory_thoroughly(train_dir)
    
    # Clean test set
    test_dir = dataset_root / "testing_set"
    if test_dir.exists():
        print("\nCleaning test set...")
        total_removed += clean_directory_thoroughly(test_dir)
    
    print(f"\nThorough cleaning completed!")
    print(f"Total images removed: {total_removed}")
    
    # Final count
    print("\nFinal image counts:")
    for dataset_name, dataset_dir in [("Training", train_dir), ("Test", test_dir)]:
        if dataset_dir.exists():
            print(f"\n{dataset_name} set:")
            total_images = 0
            for class_dir in sorted(dataset_dir.iterdir()):
                if class_dir.is_dir() and class_dir.name != "desktop.ini":
                    count = len(list(class_dir.glob("*.jpg"))) + len(list(class_dir.glob("*.jpeg"))) + len(list(class_dir.glob("*.png")))
                    print(f"  {class_dir.name}: {count} images")
                    total_images += count
            print(f"  Total: {total_images} images")

if __name__ == "__main__":
    main()
