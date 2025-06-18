"""
Data loading and preprocessing for face shape classification.
"""

import os
import numpy as np
import cv2
from pathlib import Path
from typing import Tuple, Generator, List
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import albumentations as A
from .model_config import ModelConfig

class FaceShapeDataLoader:
    """Data loader for face shape classification with augmentation."""
    
    def __init__(self, config: ModelConfig = None):
        self.config = config or ModelConfig()
        self.class_to_idx = {name: idx for idx, name in enumerate(self.config.CLASS_NAMES)}
        self.idx_to_class = {idx: name for name, idx in self.class_to_idx.items()}
        
        # Enhanced augmentation pipeline
        self.train_transform = A.Compose([
            A.Resize(self.config.IMG_HEIGHT, self.config.IMG_WIDTH),
            A.HorizontalFlip(p=0.5),
            A.Rotate(limit=self.config.ROTATION_RANGE, p=0.7),
            A.RandomBrightnessContrast(
                brightness_limit=self.config.BRIGHTNESS_RANGE,
                contrast_limit=self.config.CONTRAST_RANGE,
                p=0.7
            ),
            A.ShiftScaleRotate(
                shift_limit=self.config.WIDTH_SHIFT_RANGE,
                scale_limit=self.config.ZOOM_RANGE,
                rotate_limit=self.config.ROTATION_RANGE,
                p=0.7
            ),
            A.GaussNoise(var_limit=(10.0, 50.0), p=0.3),
            A.GaussianBlur(blur_limit=(3, 7), p=0.3),
            A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        # Validation transform with minimal augmentation
        self.val_transform = A.Compose([
            A.Resize(self.config.IMG_HEIGHT, self.config.IMG_WIDTH),
            A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    
    def preprocess_image(self, image: np.ndarray, is_training: bool = True) -> np.ndarray:
        """Enhanced image preprocessing with face detection and alignment."""
        # Convert to RGB if needed
        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        elif image.shape[2] == 4:
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
        
        # Apply face detection and alignment
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) > 0:
            # Get the largest face
            face = max(faces, key=lambda x: x[2] * x[3])
            x, y, w, h = face
            
            # Add margin around face
            margin = int(max(w, h) * 0.2)
            x1 = max(0, x - margin)
            y1 = max(0, y - margin)
            x2 = min(image.shape[1], x + w + margin)
            y2 = min(image.shape[0], y + h + margin)
            
            # Crop and resize
            face_img = image[y1:y2, x1:x2]
            face_img = cv2.resize(face_img, (self.config.IMG_WIDTH, self.config.IMG_HEIGHT))
        else:
            # If no face detected, resize the whole image
            face_img = cv2.resize(image, (self.config.IMG_WIDTH, self.config.IMG_HEIGHT))
        
        # Apply transformations
        transform = self.train_transform if is_training else self.val_transform
        transformed = transform(image=face_img)
        return transformed['image']
    
    def load_image(self, image_path: str, is_training: bool = True) -> np.ndarray:
        """Load and preprocess a single image with enhanced error handling."""
        try:
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not load image: {image_path}")
            
            # Convert BGR to RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Apply preprocessing
            return self.preprocess_image(image, is_training)
        except Exception as e:
            print(f"Error processing image {image_path}: {str(e)}")
            # Return a blank image as fallback
            return np.zeros((self.config.IMG_HEIGHT, self.config.IMG_WIDTH, 3))
    
    def load_dataset(self, data_dir: Path, use_augmentation: bool = True) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """Load dataset with enhanced error handling and augmentation."""
        images = []
        labels = []
        image_paths = []
        
        for class_name in self.config.CLASS_NAMES:
            class_dir = data_dir / class_name
            if not class_dir.exists():
                print(f"Warning: Class directory not found: {class_dir}")
                continue
            
            class_idx = self.class_to_idx[class_name]
            for img_path in class_dir.glob('*'):
                if img_path.suffix.lower() not in ['.jpg', '.jpeg', '.png']:
                    continue
                
                try:
                    image = self.load_image(str(img_path), is_training=use_augmentation)
                    if image is not None and not np.all(image == 0):
                        images.append(image)
                        labels.append(class_idx)
                        image_paths.append(str(img_path))
                except Exception as e:
                    print(f"Error loading {img_path}: {str(e)}")
                    continue
        
        if not images:
            raise ValueError(f"No valid images found in {data_dir}")
        
        return np.array(images), np.array(labels), image_paths
    
    def create_data_generators(self) -> Tuple[tf.data.Dataset, tf.data.Dataset, tf.data.Dataset]:
        """Create training, validation, and test data generators with enhanced preprocessing."""
        
        # Load training data
        train_images, train_labels, _ = self.load_dataset(
            Path("C:/Users/xxshi/Desktop/face bs/backend/FaceShapeDS/training_set"),
            use_augmentation=True
        )
        
        # Split training data into train and validation
        X_train, X_val, y_train, y_val = train_test_split(
            train_images, train_labels,
            test_size=self.config.VALIDATION_SPLIT,
            stratify=train_labels,
            random_state=42
        )
        
        # Load test data
        test_images, test_labels, _ = self.load_dataset(
            Path("C:/Users/xxshi/Desktop/face bs/backend/FaceShapeDS/testing_set"),
            use_augmentation=False
        )
        
        # Convert labels to categorical
        y_train_cat = to_categorical(y_train, num_classes=self.config.NUM_CLASSES)
        y_val_cat = to_categorical(y_val, num_classes=self.config.NUM_CLASSES)
        y_test_cat = to_categorical(test_labels, num_classes=self.config.NUM_CLASSES)
        
        # Create TensorFlow datasets with enhanced preprocessing
        train_dataset = tf.data.Dataset.from_tensor_slices((X_train, y_train_cat))
        train_dataset = train_dataset.shuffle(buffer_size=len(X_train))
        train_dataset = train_dataset.batch(self.config.BATCH_SIZE)
        train_dataset = train_dataset.prefetch(tf.data.AUTOTUNE)
        
        val_dataset = tf.data.Dataset.from_tensor_slices((X_val, y_val_cat))
        val_dataset = val_dataset.batch(self.config.BATCH_SIZE)
        val_dataset = val_dataset.prefetch(tf.data.AUTOTUNE)
        
        test_dataset = tf.data.Dataset.from_tensor_slices((test_images, y_test_cat))
        test_dataset = test_dataset.batch(self.config.BATCH_SIZE)
        test_dataset = test_dataset.prefetch(tf.data.AUTOTUNE)
        
        print(f"Training samples: {len(X_train)}")
        print(f"Validation samples: {len(X_val)}")
        print(f"Test samples: {len(test_images)}")
        
        return train_dataset, val_dataset, test_dataset
