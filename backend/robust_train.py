"""
Robust training script that handles corrupted images gracefully.
"""

import os
import sys
import numpy as np
from pathlib import Path
import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import cv2
from PIL import Image, ImageFile
import random

# Allow loading of truncated images
ImageFile.LOAD_TRUNCATED_IMAGES = True

print("Starting robust face shape training...")
print("TensorFlow version:", tf.__version__)

# Configuration
IMG_SIZE = 224
BATCH_SIZE = 16
EPOCHS = 5
NUM_CLASSES = 5
LEARNING_RATE = 0.001

# Dataset paths
DATASET_ROOT = Path("FaceShapeDS")
TRAIN_DIR = DATASET_ROOT / "training_set"
TEST_DIR = DATASET_ROOT / "testing_set"

class_names = ['Heart', 'Oblong', 'Oval', 'Round', 'Square']
class_to_idx = {name: idx for idx, name in enumerate(class_names)}

def load_and_preprocess_image(image_path, target_size=(224, 224)):
    """Load and preprocess a single image with error handling."""
    try:
        # Try multiple loading methods
        img = None
        
        # Method 1: OpenCV
        try:
            img = cv2.imread(str(image_path))
            if img is not None:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = cv2.resize(img, target_size)
        except:
            pass
        
        # Method 2: PIL if OpenCV failed
        if img is None:
            try:
                with Image.open(image_path) as pil_img:
                    pil_img = pil_img.convert('RGB')
                    pil_img = pil_img.resize(target_size)
                    img = np.array(pil_img)
            except:
                pass
        
        if img is None:
            return None
            
        # Normalize
        img = img.astype(np.float32) / 255.0
        return img
        
    except Exception as e:
        print(f"Failed to load {image_path}: {e}")
        return None

def load_dataset(data_dir, max_images_per_class=None):
    """Load dataset with robust error handling."""
    print(f"Loading dataset from: {data_dir}")
    
    images = []
    labels = []
    loaded_counts = {class_name: 0 for class_name in class_names}
    
    for class_name in class_names:
        class_dir = data_dir / class_name
        if not class_dir.exists():
            print(f"Warning: Class directory not found: {class_dir}")
            continue
        
        class_idx = class_to_idx[class_name]
        
        # Get all image files
        image_files = (list(class_dir.glob("*.jpg")) + 
                      list(class_dir.glob("*.jpeg")) + 
                      list(class_dir.glob("*.png")))
        
        if max_images_per_class:
            image_files = image_files[:max_images_per_class]
        
        print(f"  Loading {class_name}: {len(image_files)} files")
        
        for img_path in image_files:
            img = load_and_preprocess_image(img_path)
            if img is not None:
                images.append(img)
                labels.append(class_idx)
                loaded_counts[class_name] += 1
            else:
                print(f"    Skipped: {img_path.name}")
    
    print("Successfully loaded images:")
    for class_name, count in loaded_counts.items():
        print(f"  {class_name}: {count}")
    
    return np.array(images), np.array(labels)

def create_model():
    """Create the CNN model."""
    print("Building model...")
    
    # Create base model
    base_model = EfficientNetB0(
        weights='imagenet',
        include_top=False,
        input_shape=(IMG_SIZE, IMG_SIZE, 3)
    )
    
    # Freeze base model
    base_model.trainable = False
    
    # Add custom head
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(128, activation='relu')(x)
    x = Dropout(0.5)(x)
    predictions = Dense(NUM_CLASSES, activation='softmax')(x)
    
    model = Model(inputs=base_model.input, outputs=predictions)
    
    # Compile model
    model.compile(
        optimizer=Adam(learning_rate=LEARNING_RATE),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def main():
    """Main training function."""
    # Check dataset
    if not TRAIN_DIR.exists():
        print(f"Error: Training directory not found: {TRAIN_DIR}")
        return
    
    # Load training data
    print("Loading training data...")
    X_train_full, y_train_full = load_dataset(TRAIN_DIR)
    
    if len(X_train_full) == 0:
        print("Error: No training images loaded!")
        return
    
    # Split into train and validation
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_full, y_train_full, 
        test_size=0.2, 
        stratify=y_train_full, 
        random_state=42
    )
    
    # Convert labels to categorical
    y_train_cat = to_categorical(y_train, NUM_CLASSES)
    y_val_cat = to_categorical(y_val, NUM_CLASSES)
    
    print(f"Training samples: {len(X_train)}")
    print(f"Validation samples: {len(X_val)}")
    
    # Load test data
    if TEST_DIR.exists():
        print("Loading test data...")
        X_test, y_test = load_dataset(TEST_DIR)
        y_test_cat = to_categorical(y_test, NUM_CLASSES)
        print(f"Test samples: {len(X_test)}")
    else:
        X_test, y_test_cat = None, None
    
    # Create model
    model = create_model()
    print(f"Model created with {model.count_params():,} parameters")
    
    # Train model
    print(f"Starting training for {EPOCHS} epochs...")
    
    history = model.fit(
        X_train, y_train_cat,
        batch_size=BATCH_SIZE,
        epochs=EPOCHS,
        validation_data=(X_val, y_val_cat),
        verbose=1
    )
    
    print("Training completed!")
    
    # Evaluate
    if X_test is not None:
        print("Evaluating on test data...")
        test_loss, test_accuracy = model.evaluate(X_test, y_test_cat, verbose=1)
        print(f"Test accuracy: {test_accuracy:.4f}")
    else:
        test_accuracy = 0
    
    # Save model
    model_dir = Path("ml_models/saved_models")
    model_dir.mkdir(parents=True, exist_ok=True)
    model_path = model_dir / "face_shape_cnn.h5"
    
    model.save(str(model_path))
    print(f"Model saved to: {model_path}")
    
    print("\nTraining Summary:")
    print(f"Final validation accuracy: {history.history['val_accuracy'][-1]:.4f}")
    if X_test is not None:
        print(f"Final test accuracy: {test_accuracy:.4f}")
    
    if test_accuracy >= 0.7:
        print("🎉 Good accuracy achieved!")
    else:
        print("⚠️ Consider training for more epochs for better accuracy")

if __name__ == "__main__":
    main()
