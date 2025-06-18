"""
Quick training script with reduced epochs for fast testing.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from ml_models.face_shape_cnn import FaceShapeCNN
from ml_models.data_loader import FaceShapeDataLoader
from ml_models.model_config import ModelConfig

def quick_train():
    """Quick training with reduced epochs for testing."""
    print("Quick Face Shape CNN Training (Reduced Epochs)")
    print("=" * 50)
    
    # Initialize configuration with reduced epochs
    config = ModelConfig()
    config.EPOCHS = 10  # Reduced for quick training
    config.BATCH_SIZE = 16  # Smaller batch size for faster training
    config.PATIENCE = 5  # Reduced patience
    
    print(f"Quick training mode: {config.EPOCHS} epochs")
    
    # Check if dataset exists
    if not config.TRAIN_DIR.exists():
        print(f"Error: Training directory not found: {config.TRAIN_DIR}")
        return
    
    # Initialize data loader
    print("Loading data...")
    data_loader = FaceShapeDataLoader(config)
    
    # Create data generators
    train_dataset, val_dataset, test_dataset = data_loader.create_data_generators()
    
    # Initialize and build model
    print("Building model...")
    model = FaceShapeCNN(config)
    model.build_model()
    
    # Start training
    print("Starting quick training...")
    history = model.train(train_dataset, val_dataset)
    
    # Quick evaluation
    print("Evaluating model...")
    test_metrics = model.evaluate(test_dataset)
    
    print(f"\nQuick Training Results:")
    print(f"Final validation accuracy: {history['val_accuracy'][-1]:.4f}")
    print(f"Test accuracy: {test_metrics.get('accuracy', 0):.4f}")
    
    # Save model
    model.save_model()
    print(f"Model saved to: {config.get_model_path()}")
    
    return model

if __name__ == "__main__":
    quick_train()
