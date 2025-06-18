"""
Training script for the face shape CNN model.
"""

import os
import sys
import time
import json
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from ml_models.face_shape_cnn import FaceShapeCNN
from ml_models.data_loader import FaceShapeDataLoader
from ml_models.model_config import ModelConfig

def plot_training_history(history, save_path: str):
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
    if 'precision' in history:
        axes[1, 0].plot(history['precision'], label='Training Precision')
        axes[1, 0].plot(history['val_precision'], label='Validation Precision')
        axes[1, 0].set_title('Model Precision')
        axes[1, 0].set_xlabel('Epoch')
        axes[1, 0].set_ylabel('Precision')
        axes[1, 0].legend()
        axes[1, 0].grid(True)
    
    # Recall
    if 'recall' in history:
        axes[1, 1].plot(history['recall'], label='Training Recall')
        axes[1, 1].plot(history['val_recall'], label='Validation Recall')
        axes[1, 1].set_title('Model Recall')
        axes[1, 1].set_xlabel('Epoch')
        axes[1, 1].set_ylabel('Recall')
        axes[1, 1].legend()
        axes[1, 1].grid(True)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Training history plot saved to: {save_path}")

def evaluate_model_detailed(model: FaceShapeCNN, test_dataset, config: ModelConfig):
    """Perform detailed model evaluation."""
    print("\n" + "="*50)
    print("DETAILED MODEL EVALUATION")
    print("="*50)
    
    # Basic evaluation
    test_metrics = model.evaluate(test_dataset)
    
    # Get predictions for confusion matrix
    y_true = []
    y_pred = []
    
    for batch_x, batch_y in test_dataset:
        predictions = model.model.predict(batch_x, verbose=0)
        y_true.extend(np.argmax(batch_y.numpy(), axis=1))
        y_pred.extend(np.argmax(predictions, axis=1))
    
    # Classification report
    print("\nClassification Report:")
    print("-" * 30)
    report = classification_report(
        y_true, y_pred, 
        target_names=config.CLASS_NAMES,
        digits=4
    )
    print(report)
    
    # Confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    
    # Plot confusion matrix
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        cm, 
        annot=True, 
        fmt='d', 
        cmap='Blues',
        xticklabels=config.CLASS_NAMES,
        yticklabels=config.CLASS_NAMES
    )
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    
    cm_path = config.MODEL_DIR / "confusion_matrix.png"
    plt.savefig(cm_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Confusion matrix saved to: {cm_path}")
    
    # Calculate per-class accuracy
    per_class_accuracy = cm.diagonal() / cm.sum(axis=1)
    print("\nPer-class Accuracy:")
    print("-" * 20)
    for i, class_name in enumerate(config.CLASS_NAMES):
        print(f"{class_name}: {per_class_accuracy[i]:.4f}")
    
    return test_metrics, report, cm

def main():
    """Main training function."""
    print("Starting Face Shape CNN Training")
    print("=" * 40)
    
    # Initialize configuration
    config = ModelConfig()
    
    # Check if dataset exists
    if not config.TRAIN_DIR.exists():
        print(f"Error: Training directory not found: {config.TRAIN_DIR}")
        return
    
    if not config.TEST_DIR.exists():
        print(f"Error: Test directory not found: {config.TEST_DIR}")
        return
    
    print(f"Dataset root: {config.DATASET_ROOT}")
    print(f"Training directory: {config.TRAIN_DIR}")
    print(f"Test directory: {config.TEST_DIR}")
    print(f"Model will be saved to: {config.get_model_path()}")
    
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
    print(f"\nStarting training...")
    start_time = time.time()
    
    history = model.train(train_dataset, val_dataset)
    
    training_time = time.time() - start_time
    print(f"\nTraining completed in {training_time:.2f} seconds ({training_time/60:.2f} minutes)")
    
    # Save training history plot
    history_plot_path = config.MODEL_DIR / "training_history.png"
    plot_training_history(history, str(history_plot_path))
    
    # Detailed evaluation
    test_metrics, report, cm = evaluate_model_detailed(model, test_dataset, config)
    
    # Save evaluation results
    results = {
        'training_time_seconds': training_time,
        'test_metrics': test_metrics,
        'final_val_accuracy': history['val_accuracy'][-1],
        'best_val_accuracy': max(history['val_accuracy']),
        'config': {
            'base_model': config.BASE_MODEL,
            'epochs': config.EPOCHS,
            'batch_size': config.BATCH_SIZE,
            'learning_rate': config.LEARNING_RATE,
            'target_accuracy': config.TARGET_ACCURACY
        }
    }
    
    results_path = config.MODEL_DIR / "training_results.json"
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nTraining results saved to: {results_path}")
    
    # Check if target accuracy was achieved
    final_accuracy = test_metrics.get('accuracy', 0)
    if final_accuracy >= config.TARGET_ACCURACY:
        print(f"\n🎉 SUCCESS! Target accuracy of {config.TARGET_ACCURACY:.1%} achieved!")
        print(f"Final test accuracy: {final_accuracy:.4f}")
    else:
        print(f"\n⚠️  Target accuracy not reached. Final test accuracy: {final_accuracy:.4f}")
        print(f"Target was: {config.TARGET_ACCURACY:.4f}")
    
    print("\nTraining complete!")

if __name__ == "__main__":
    main()
