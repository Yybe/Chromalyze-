"""
Simple training script for face shape CNN - easier to debug.
"""

import os
import sys
import numpy as np
from pathlib import Path
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

print("Starting simple face shape training...")
print("TensorFlow version:", tf.__version__)

# Configuration
IMG_SIZE = 224
BATCH_SIZE = 16  # Smaller batch size
EPOCHS = 5       # Very few epochs for quick test
NUM_CLASSES = 5
LEARNING_RATE = 0.001

# Dataset paths
DATASET_ROOT = Path("FaceShapeDS")
TRAIN_DIR = DATASET_ROOT / "training_set"
TEST_DIR = DATASET_ROOT / "testing_set"

print(f"Train directory: {TRAIN_DIR}")
print(f"Test directory: {TEST_DIR}")

# Check if directories exist
if not TRAIN_DIR.exists():
    print(f"Error: Training directory not found: {TRAIN_DIR}")
    sys.exit(1)

if not TEST_DIR.exists():
    print(f"Error: Test directory not found: {TEST_DIR}")
    sys.exit(1)

print("Dataset directories found!")

# Create data generators
print("Creating data generators...")

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True,
    validation_split=0.2
)

test_datagen = ImageDataGenerator(rescale=1./255)

# Load training data
print("Loading training data...")
train_generator = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training'
)

validation_generator = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation'
)

# Load test data
print("Loading test data...")
test_generator = test_datagen.flow_from_directory(
    TEST_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=False
)

print(f"Training samples: {train_generator.samples}")
print(f"Validation samples: {validation_generator.samples}")
print(f"Test samples: {test_generator.samples}")
print(f"Classes: {train_generator.class_indices}")

# Build model
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

print("Model compiled successfully!")
print(f"Total parameters: {model.count_params():,}")

# Train model
print(f"Starting training for {EPOCHS} epochs...")

history = model.fit(
    train_generator,
    epochs=EPOCHS,
    validation_data=validation_generator,
    verbose=1
)

print("Training completed!")

# Evaluate on test data
print("Evaluating on test data...")
test_loss, test_accuracy = model.evaluate(test_generator, verbose=1)

print(f"Test accuracy: {test_accuracy:.4f}")

# Save model
model_dir = Path("ml_models/saved_models")
model_dir.mkdir(parents=True, exist_ok=True)
model_path = model_dir / "face_shape_cnn.h5"

model.save(str(model_path))
print(f"Model saved to: {model_path}")

print("Simple training completed successfully!")
print(f"Final test accuracy: {test_accuracy:.4f}")

if test_accuracy >= 0.7:
    print("🎉 Good accuracy achieved!")
else:
    print("⚠️ Low accuracy - may need more training epochs")
