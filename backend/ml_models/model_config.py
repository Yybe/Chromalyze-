"""
Configuration settings for the face shape CNN model.
"""

import os
from pathlib import Path

class ModelConfig:
    """Configuration class for face shape classification model."""
    
    # Dataset paths
    DATASET_ROOT = Path("FaceShapeDS")
    TRAIN_DIR = DATASET_ROOT / "training_set"
    TEST_DIR = DATASET_ROOT / "testing_set"
    
    # Model parameters
    IMG_HEIGHT = 224
    IMG_WIDTH = 224
    IMG_CHANNELS = 3
    NUM_CLASSES = 5
    
    # Class names (must match directory names)
    CLASS_NAMES = ['Heart', 'Oblong', 'Oval', 'Round', 'Square']
    
    # Training parameters
    BATCH_SIZE = 16  # Reduced for better generalization
    EPOCHS = 100  # Increased epochs
    LEARNING_RATE = 0.0005  # Reduced learning rate for better convergence
    VALIDATION_SPLIT = 0.2
    
    # Model architecture
    USE_TRANSFER_LEARNING = True
    BASE_MODEL = 'EfficientNetB0'  # Using EfficientNetB0 for better accuracy
    FREEZE_BASE_LAYERS = False  # Unfreeze base layers for fine-tuning
    DROPOUT_RATE = 0.4  # Reduced dropout for better feature learning
    
    # Enhanced data augmentation
    ROTATION_RANGE = 30  # Increased rotation range
    WIDTH_SHIFT_RANGE = 0.2  # Increased shift range
    HEIGHT_SHIFT_RANGE = 0.2
    HORIZONTAL_FLIP = True
    ZOOM_RANGE = 0.2  # Increased zoom range
    BRIGHTNESS_RANGE = [0.7, 1.3]  # Increased brightness range
    CONTRAST_RANGE = [0.7, 1.3]  # Added contrast augmentation
    SHEAR_RANGE = 0.2  # Added shear augmentation
    
    # Model saving
    MODEL_DIR = Path("saved_models")
    MODEL_NAME = "face_shape_cnn.h5"
    WEIGHTS_NAME = "face_shape_weights.h5"
    
    # Performance thresholds
    MIN_CONFIDENCE = 0.75  # Increased minimum confidence threshold
    TARGET_ACCURACY = 0.85
    
    # Early stopping
    PATIENCE = 15  # Increased patience
    MONITOR = 'val_accuracy'
    
    @classmethod
    def create_directories(cls):
        """Create necessary directories if they don't exist."""
        cls.MODEL_DIR.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def get_model_path(cls):
        """Get the full path to the saved model."""
        return cls.MODEL_DIR / cls.MODEL_NAME
    
    @classmethod
    def get_weights_path(cls):
        """Get the full path to the saved weights."""
        return cls.MODEL_DIR / cls.WEIGHTS_NAME
