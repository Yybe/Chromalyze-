"""
Quick training script to test the setup and get baseline performance.
"""

import os
import sys
from pathlib import Path
import tensorflow as tf

# Add ml_models to path
sys.path.append('ml_models')

from ml_models.face_shape_cnn import FaceShapeCNN
from ml_models.data_loader import FaceShapeDataLoader
from ml_models.model_config import ModelConfig

def main():
    """Quick training function."""
    print("Quick Face Shape CNN Training")
    print("=" * 40)
    
    # Initialize configuration with reduced epochs for quick test
    config = ModelConfig()
    config.EPOCHS = 10  # Reduced for quick test
    config.BATCH_SIZE = 16  # Smaller batch size
    
    # Check dataset paths
    print(f"Dataset root: {config.DATASET_ROOT}")
    print(f"Training directory: {config.TRAIN_DIR}")
    print(f"Test directory: {config.TEST_DIR}")
    
    if not config.TRAIN_DIR.exists():
        print(f"Error: Training directory not found: {config.TRAIN_DIR}")
        print("Current working directory:", os.getcwd())
        print("Available directories:")
        for item in Path(".").iterdir():
            if item.is_dir():
                print(f"  {item}")
        return
    
    # Initialize data loader
    print("\nInitializing data loader...")
    data_loader = FaceShapeDataLoader(config)
    
    # Create data generators
    print("Creating data generators...")
    train_dataset, val_dataset, test_dataset = data_loader.create_data_generators()
    
    # Initialize and build model
    print(f"\nBuilding {config.BASE_MODEL} model...")
    model = FaceShapeCNN(config)
    model.build_model()
    
    # Print model summary
    print("\nModel Summary:")
    print("-" * 20)
    model.model.summary()
    
    # Start training
    print(f"\nStarting quick training for {config.EPOCHS} epochs...")
    history = model.train(train_dataset, val_dataset)
    
    # Quick evaluation
    print("\nEvaluating model...")
    test_metrics = model.evaluate(test_dataset)
    
    print(f"\nQuick Training Results:")
    print(f"Test Accuracy: {test_metrics.get('accuracy', 0):.4f}")
    print(f"Target Accuracy: {config.TARGET_ACCURACY:.4f}")
    
    if test_metrics.get('accuracy', 0) >= config.TARGET_ACCURACY:
        print("🎉 Target accuracy achieved!")
    else:
        print("⚠️ Need more training to reach target accuracy")
    
    # Save model
    model.save_model()
    print("Model saved!")

if __name__ == "__main__":
    main()
