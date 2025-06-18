"""
Setup script to install dependencies and train the face shape CNN model.
"""

import subprocess
import sys
import os
from pathlib import Path

def install_dependencies():
    """Install required ML dependencies."""
    print("Installing ML dependencies...")
    
    dependencies = [
        "tensorflow==2.15.0",
        "keras==2.15.0", 
        "albumentations==1.3.1",
        "tqdm==4.66.1"
    ]
    
    for dep in dependencies:
        print(f"Installing {dep}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✅ {dep} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {dep}: {e}")
            return False
    
    return True

def check_dataset():
    """Check if the dataset is available."""
    dataset_root = Path("backend/FaceShapeDS")
    train_dir = dataset_root / "training_set"
    test_dir = dataset_root / "testing_set"
    
    if not dataset_root.exists():
        print(f"❌ Dataset not found at: {dataset_root}")
        return False
    
    if not train_dir.exists():
        print(f"❌ Training directory not found: {train_dir}")
        return False
    
    if not test_dir.exists():
        print(f"❌ Test directory not found: {test_dir}")
        return False
    
    # Check class directories
    class_names = ['Heart', 'Oblong', 'Oval', 'Round', 'Square']
    
    for class_name in class_names:
        train_class_dir = train_dir / class_name
        test_class_dir = test_dir / class_name
        
        if not train_class_dir.exists():
            print(f"❌ Training class directory not found: {train_class_dir}")
            return False
        
        if not test_class_dir.exists():
            print(f"❌ Test class directory not found: {test_class_dir}")
            return False
        
        # Count images
        train_images = len(list(train_class_dir.glob("*.jpg")) + list(train_class_dir.glob("*.jpeg")) + list(train_class_dir.glob("*.png")))
        test_images = len(list(test_class_dir.glob("*.jpg")) + list(test_class_dir.glob("*.jpeg")) + list(test_class_dir.glob("*.png")))
        
        print(f"✅ {class_name}: {train_images} training, {test_images} test images")
    
    return True

def train_model():
    """Train the face shape CNN model."""
    print("\nStarting model training...")
    
    try:
        # Change to backend directory
        os.chdir("backend")
        
        # Run quick training
        result = subprocess.run([sys.executable, "ml_models/quick_train.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Model training completed successfully!")
            print(result.stdout)
            return True
        else:
            print("❌ Model training failed!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error during training: {e}")
        return False
    finally:
        # Change back to original directory
        os.chdir("..")

def main():
    """Main setup function."""
    print("Face Shape CNN Model Setup")
    print("=" * 40)
    
    # Step 1: Check dataset
    print("\n1. Checking dataset...")
    if not check_dataset():
        print("❌ Dataset check failed. Please ensure the dataset is properly organized.")
        return
    
    # Step 2: Install dependencies
    print("\n2. Installing dependencies...")
    if not install_dependencies():
        print("❌ Dependency installation failed.")
        return
    
    # Step 3: Train model
    print("\n3. Training model...")
    if not train_model():
        print("❌ Model training failed.")
        return
    
    print("\n🎉 Setup completed successfully!")
    print("\nThe CNN model is now ready to use for face shape detection.")
    print("The model will be automatically used in the face shape detector with MediaPipe as fallback.")

if __name__ == "__main__":
    main()
