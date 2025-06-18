"""
Enhanced Face Shape CNN Training Script with Safety Features
Targets >85% accuracy with comprehensive dataset validation and protection.
"""

import os
import sys
import time
import json
import shutil
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np
import tensorflow as tf

# Add ml_models to path
sys.path.append(str(Path(__file__).parent / "ml_models"))

from ml_models.face_shape_cnn import FaceShapeCNN
from ml_models.data_loader import FaceShapeDataLoader
from ml_models.model_config import ModelConfig

def create_backup(dataset_path: Path, backup_path: Path):
    """Create a backup of the dataset before training."""
    print("🔒 Creating dataset backup for safety...")
    
    if backup_path.exists():
        print(f"   Backup already exists at: {backup_path}")
        return
    
    try:
        shutil.copytree(dataset_path, backup_path)
        print(f"   ✅ Dataset backed up to: {backup_path}")
    except Exception as e:
        print(f"   ❌ Failed to create backup: {e}")
        raise

def validate_dataset_safety(dataset_path: Path):
    """Validate that dataset exists and is safe to use."""
    print("🛡️  Performing safety checks...")

    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")

    # Check training and testing directories
    train_dir = dataset_path / "training_set"
    test_dir = dataset_path / "testing_set"

    if not train_dir.exists():
        raise FileNotFoundError(f"Training directory not found: {train_dir}")
    if not test_dir.exists():
        raise FileNotFoundError(f"Testing directory not found: {test_dir}")

    # Check for minimum number of images
    total_images = 0
    for data_dir in [train_dir, test_dir]:
        for class_dir in data_dir.iterdir():
            if class_dir.is_dir() and class_dir.name in ModelConfig.CLASS_NAMES:
                images = list(class_dir.glob("*.jpg")) + list(class_dir.glob("*.jpeg")) + list(class_dir.glob("*.png"))
                total_images += len(images)
                print(f"   📁 {data_dir.name}/{class_dir.name}: {len(images)} images")

    if total_images < 1000:
        raise ValueError(f"Dataset too small: {total_images} images (minimum 1000 required)")

    print(f"   ✅ Dataset validation passed: {total_images} images found")

def plot_training_history(history, save_path: Path):
    """Plot and save training history."""
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Accuracy
    axes[0, 0].plot(history['accuracy'], label='Training Accuracy')
    axes[0, 0].plot(history['val_accuracy'], label='Validation Accuracy')
    axes[0, 0].set_title('Model Accuracy')
    axes[0, 0].set_xlabel('Epoch')
    axes[0, 0].set_ylabel('Accuracy')
    axes[0, 0].legend()
    axes[0, 0].grid(True)
    
    # Loss
    axes[0, 1].plot(history['loss'], label='Training Loss')
    axes[0, 1].plot(history['val_loss'], label='Validation Loss')
    axes[0, 1].set_title('Model Loss')
    axes[0, 1].set_xlabel('Epoch')
    axes[0, 1].set_ylabel('Loss')
    axes[0, 1].legend()
    axes[0, 1].grid(True)
    
    # Precision
    axes[1, 0].plot(history['precision'], label='Training Precision')
    axes[1, 0].plot(history['val_precision'], label='Validation Precision')
    axes[1, 0].set_title('Model Precision')
    axes[1, 0].set_xlabel('Epoch')
    axes[1, 0].set_ylabel('Precision')
    axes[1, 0].legend()
    axes[1, 0].grid(True)
    
    # Recall
    axes[1, 1].plot(history['recall'], label='Training Recall')
    axes[1, 1].plot(history['val_recall'], label='Validation Recall')
    axes[1, 1].set_title('Model Recall')
    axes[1, 1].set_xlabel('Epoch')
    axes[1, 1].set_ylabel('Recall')
    axes[1, 1].legend()
    axes[1, 1].grid(True)
    
    plt.tight_layout()
    plt.savefig(save_path / "training_history.png", dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   📊 Training history saved to: {save_path / 'training_history.png'}")

def plot_confusion_matrix(y_true, y_pred, class_names, save_path: Path):
    """Plot and save confusion matrix."""
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=class_names, yticklabels=class_names)
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.tight_layout()
    plt.savefig(save_path / "confusion_matrix.png", dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   📊 Confusion matrix saved to: {save_path / 'confusion_matrix.png'}")

def main():
    """Main training function with comprehensive safety and monitoring."""
    print("🎯 Enhanced Face Shape CNN Training")
    print("=" * 60)
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Initialize configuration
    config = ModelConfig()
    
    # Create results directory
    results_dir = Path("training_results") / datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Safety checks
        dataset_path = Path("C:/Users/xxshi/Desktop/face bs/backend/FaceShapeDS")
        backup_path = Path("FaceShapeDS_backup")
        
        validate_dataset_safety(dataset_path)
        create_backup(dataset_path, backup_path)
        
        # Initialize data loader and model
        print("\n📊 Initializing data loader...")
        data_loader = FaceShapeDataLoader(config)
        
        print("🏗️  Creating data generators...")
        train_dataset, val_dataset, test_dataset = data_loader.create_data_generators()
        
        print(f"\n🧠 Building {config.BASE_MODEL} model...")
        model = FaceShapeCNN(config)
        model.build_model()
        
        # Print model summary
        print("\n📋 Model Summary:")
        print("-" * 40)
        model.model.summary()
        
        # Start training
        print(f"\n🚀 Starting training for {config.EPOCHS} epochs...")
        print(f"   Target accuracy: {config.TARGET_ACCURACY:.1%}")
        print(f"   Minimum confidence: {config.MIN_CONFIDENCE:.1%}")
        
        start_time = time.time()
        history = model.train(train_dataset, val_dataset)
        training_time = time.time() - start_time
        
        print(f"\n⏱️  Training completed in {training_time:.2f} seconds")
        
        # Evaluate model
        print("\n📈 Evaluating model on test data...")
        test_metrics = model.evaluate(test_dataset)
        
        # Generate detailed predictions for analysis
        print("\n🔍 Generating detailed predictions...")
        test_images, test_labels, _ = data_loader.load_dataset(config.TEST_DIR, use_augmentation=False)
        
        predictions = []
        true_labels = []
        
        for i in range(len(test_images)):
            image_batch = np.expand_dims(test_images[i], axis=0)
            pred = model.model.predict(image_batch, verbose=0)
            predictions.append(np.argmax(pred[0]))
            true_labels.append(test_labels[i])
        
        # Generate reports
        print("\n📊 Generating analysis reports...")
        
        # Classification report
        class_report = classification_report(true_labels, predictions, 
                                           target_names=config.CLASS_NAMES, 
                                           output_dict=True)
        
        # Save results
        results = {
            "training_config": {
                "epochs": config.EPOCHS,
                "batch_size": config.BATCH_SIZE,
                "learning_rate": config.LEARNING_RATE,
                "base_model": config.BASE_MODEL,
                "target_accuracy": config.TARGET_ACCURACY
            },
            "training_time_seconds": training_time,
            "final_metrics": test_metrics,
            "classification_report": class_report,
            "training_history": {k: [float(v) for v in history[k]] for k in history.keys()}
        }
        
        # Save results to JSON
        with open(results_dir / "training_results.json", "w") as f:
            json.dump(results, f, indent=2)
        
        # Generate plots
        plot_training_history(history, results_dir)
        plot_confusion_matrix(true_labels, predictions, config.CLASS_NAMES, results_dir)
        
        # Save model
        model.save_model()
        
        # Final summary
        final_accuracy = test_metrics.get('accuracy', 0)
        print(f"\n🎉 Training Summary:")
        print(f"   Final test accuracy: {final_accuracy:.4f} ({final_accuracy:.1%})")
        print(f"   Target achieved: {'✅ YES' if final_accuracy >= config.TARGET_ACCURACY else '❌ NO'}")
        print(f"   Model saved to: {config.get_model_path()}")
        print(f"   Results saved to: {results_dir}")
        
        if final_accuracy >= config.TARGET_ACCURACY:
            print(f"\n🏆 SUCCESS: Model achieved target accuracy of {config.TARGET_ACCURACY:.1%}!")
        else:
            print(f"\n⚠️  Model accuracy ({final_accuracy:.1%}) below target ({config.TARGET_ACCURACY:.1%})")
            print("   Consider: increasing epochs, adjusting learning rate, or data augmentation")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Training failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
