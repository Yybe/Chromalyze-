"""
Clean the dataset by removing corrupted images.
"""

import os
from pathlib import Path
from PIL import Image
import cv2

def check_image(image_path):
    """Check if an image is valid and can be loaded."""
    try:
        # Try with PIL
        with Image.open(image_path) as img:
            img.verify()
        
        # Try with OpenCV
        img = cv2.imread(str(image_path))
        if img is None:
            return False
            
        return True
    except Exception as e:
        print(f"Corrupted image: {image_path} - {e}")
        return False

def clean_dataset_directory(directory):
    """Clean a dataset directory by removing corrupted images."""
    print(f"Cleaning directory: {directory}")
    
    corrupted_files = []
    total_files = 0
    
    for class_dir in directory.iterdir():
        if not class_dir.is_dir():
            continue
            
        print(f"  Checking class: {class_dir.name}")
        
        image_files = list(class_dir.glob("*.jpg")) + list(class_dir.glob("*.jpeg")) + list(class_dir.glob("*.png"))
        
        for img_path in image_files:
            total_files += 1
            if not check_image(img_path):
                corrupted_files.append(img_path)
                print(f"    Removing: {img_path.name}")
                try:
                    img_path.unlink()  # Delete the file
                except Exception as e:
                    print(f"    Failed to delete {img_path}: {e}")
    
    print(f"  Total files checked: {total_files}")
    print(f"  Corrupted files removed: {len(corrupted_files)}")
    return len(corrupted_files)

def main():
    """Main function to clean the dataset."""
    print("Dataset Cleaning Tool")
    print("=" * 30)
    
    dataset_root = Path("FaceShapeDS")
    train_dir = dataset_root / "training_set"
    test_dir = dataset_root / "testing_set"
    
    if not dataset_root.exists():
        print(f"Error: Dataset not found at {dataset_root}")
        return
    
    total_corrupted = 0
    
    # Clean training set
    if train_dir.exists():
        print("\nCleaning training set...")
        total_corrupted += clean_dataset_directory(train_dir)
    
    # Clean test set
    if test_dir.exists():
        print("\nCleaning test set...")
        total_corrupted += clean_dataset_directory(test_dir)
    
    print(f"\nDataset cleaning completed!")
    print(f"Total corrupted images removed: {total_corrupted}")
    
    # Count remaining images
    print("\nRemaining images per class:")
    for dataset_name, dataset_dir in [("Training", train_dir), ("Test", test_dir)]:
        if dataset_dir.exists():
            print(f"\n{dataset_name} set:")
            for class_dir in sorted(dataset_dir.iterdir()):
                if class_dir.is_dir() and class_dir.name != "desktop.ini":
                    image_count = len(list(class_dir.glob("*.jpg")) + list(class_dir.glob("*.jpeg")) + list(class_dir.glob("*.png")))
                    print(f"  {class_dir.name}: {image_count} images")

if __name__ == "__main__":
    main()
