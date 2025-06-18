"""
CNN model for face shape classification using transfer learning.
"""

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, BatchNormalization
from tensorflow.keras.applications import EfficientNetB0, ResNet50, MobileNetV2
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.metrics import Precision, Recall
from pathlib import Path
from typing import Tuple, Dict, Any, Optional
import joblib

from .model_config import ModelConfig
from .data_loader import FaceShapeDataLoader

class FaceShapeCNN:
    """CNN model for face shape classification."""
    
    def __init__(self, config: ModelConfig = None):
        self.config = config or ModelConfig()
        self.model = None
        self.history = None
        self.data_loader = FaceShapeDataLoader(self.config)
        
        # Ensure model directory exists
        self.config.create_directories()
    
    def build_model(self) -> Model:
        """Build the CNN model with transfer learning."""
        
        # Choose base model
        if self.config.BASE_MODEL == 'EfficientNetB0':
            base_model = EfficientNetB0(
                weights='imagenet',
                include_top=False,
                input_shape=(self.config.IMG_HEIGHT, self.config.IMG_WIDTH, self.config.IMG_CHANNELS)
            )
        elif self.config.BASE_MODEL == 'ResNet50':
            base_model = ResNet50(
                weights='imagenet',
                include_top=False,
                input_shape=(self.config.IMG_HEIGHT, self.config.IMG_WIDTH, self.config.IMG_CHANNELS)
            )
        elif self.config.BASE_MODEL == 'MobileNetV2':
            base_model = MobileNetV2(
                weights='imagenet',
                include_top=False,
                input_shape=(self.config.IMG_HEIGHT, self.config.IMG_WIDTH, self.config.IMG_CHANNELS)
            )
        else:
            raise ValueError(f"Unsupported base model: {self.config.BASE_MODEL}")
        
        # Freeze base model layers if specified
        if self.config.FREEZE_BASE_LAYERS:
            base_model.trainable = False
        
        # Add custom classification head
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = BatchNormalization()(x)
        x = Dense(512, activation='relu')(x)
        x = Dropout(self.config.DROPOUT_RATE)(x)
        x = Dense(256, activation='relu')(x)
        x = Dropout(self.config.DROPOUT_RATE)(x)
        predictions = Dense(self.config.NUM_CLASSES, activation='softmax', name='predictions')(x)
        
        # Create the model
        model = Model(inputs=base_model.input, outputs=predictions)
        
        # Compile the model
        model.compile(
            optimizer=Adam(learning_rate=self.config.LEARNING_RATE),
            loss='categorical_crossentropy',
            metrics=['accuracy', Precision(name='precision'), Recall(name='recall')]
        )
        
        self.model = model
        return model
    
    def train(self, train_dataset, val_dataset) -> Dict[str, Any]:
        """Train the model."""
        
        if self.model is None:
            self.build_model()
        
        # Define callbacks
        callbacks = [
            EarlyStopping(
                monitor=self.config.MONITOR,
                patience=self.config.PATIENCE,
                restore_best_weights=True,
                verbose=1
            ),
            ModelCheckpoint(
                filepath=str(self.config.get_model_path()),
                monitor=self.config.MONITOR,
                save_best_only=True,
                verbose=1
            ),
            ReduceLROnPlateau(
                monitor=self.config.MONITOR,
                factor=0.5,
                patience=5,
                min_lr=1e-7,
                verbose=1
            )
        ]
        
        print(f"Starting training for {self.config.EPOCHS} epochs...")
        print(f"Model architecture: {self.config.BASE_MODEL}")
        print(f"Target accuracy: {self.config.TARGET_ACCURACY}")
        
        # Train the model
        self.history = self.model.fit(
            train_dataset,
            epochs=self.config.EPOCHS,
            validation_data=val_dataset,
            callbacks=callbacks,
            verbose=1
        )
        
        return self.history.history
    
    def evaluate(self, test_dataset) -> Dict[str, float]:
        """Evaluate the model on test data."""
        if self.model is None:
            raise ValueError("Model not trained or loaded")
        
        print("Evaluating model on test data...")
        results = self.model.evaluate(test_dataset, verbose=1)
        
        # Create results dictionary
        metrics = {}
        for i, metric_name in enumerate(self.model.metrics_names):
            metrics[metric_name] = results[i]
        
        print(f"Test Results:")
        for metric, value in metrics.items():
            print(f"  {metric}: {value:.4f}")
        
        return metrics
    
    def predict(self, image_path: str) -> Tuple[str, float, Dict[str, float]]:
        """Predict face shape for a single image."""
        if self.model is None:
            raise ValueError("Model not trained or loaded")
        
        # Preprocess image
        processed_image = self.data_loader.preprocess_single_image(image_path)
        
        # Make prediction
        predictions = self.model.predict(processed_image, verbose=0)
        predicted_probs = predictions[0]
        
        # Get predicted class
        predicted_idx = np.argmax(predicted_probs)
        predicted_class = self.data_loader.idx_to_class[predicted_idx]
        confidence = float(predicted_probs[predicted_idx])
        
        # Create probability dictionary
        class_probabilities = {}
        for idx, prob in enumerate(predicted_probs):
            class_name = self.data_loader.idx_to_class[idx]
            class_probabilities[class_name] = float(prob)
        
        return predicted_class, confidence, class_probabilities
    
    def save_model(self, filepath: Optional[str] = None):
        """Save the trained model."""
        if self.model is None:
            raise ValueError("No model to save")
        
        if filepath is None:
            filepath = str(self.config.get_model_path())
        
        self.model.save(filepath)
        print(f"Model saved to: {filepath}")
    
    def load_model(self, filepath: Optional[str] = None):
        """Load a trained model."""
        if filepath is None:
            filepath = str(self.config.get_model_path())
        
        if not Path(filepath).exists():
            raise FileNotFoundError(f"Model file not found: {filepath}")
        
        self.model = load_model(filepath)
        print(f"Model loaded from: {filepath}")

def load_trained_model(model_path: Optional[str] = None) -> FaceShapeCNN:
    """Load a pre-trained face shape CNN model."""
    config = ModelConfig()
    model = FaceShapeCNN(config)
    
    if model_path is None:
        model_path = str(config.get_model_path())
    
    model.load_model(model_path)
    return model
