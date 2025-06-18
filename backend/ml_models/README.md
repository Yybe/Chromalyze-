# Face Shape CNN Model

This directory contains the machine learning implementation for accurate face shape classification using a custom CNN model.

## 🎯 Overview

The face shape classification system uses a Convolutional Neural Network (CNN) with transfer learning to achieve high accuracy (target: >85%) in classifying faces into 5 categories:

- **Heart**: Wider forehead, narrow chin
- **Oblong**: Longer than wide, balanced proportions
- **Oval**: Balanced proportions, slightly longer than wide
- **Round**: Similar width and height, soft curves
- **Square**: Angular features, similar width and height

## 🏗️ Architecture

### Model Design
- **Base Model**: EfficientNetB0 (pre-trained on ImageNet)
- **Transfer Learning**: Frozen base layers with custom classification head
- **Input Size**: 224x224x3 RGB images
- **Output**: 5-class softmax classification

### Key Features
- **Data Augmentation**: Rotation, brightness, contrast, horizontal flip
- **Regularization**: Dropout layers and batch normalization
- **Early Stopping**: Prevents overfitting with patience-based stopping
- **Model Checkpointing**: Saves best model during training

## 📁 File Structure

```
ml_models/
├── __init__.py              # Package initialization
├── model_config.py          # Configuration settings
├── data_loader.py           # Data loading and preprocessing
├── face_shape_cnn.py        # CNN model implementation
├── train_model.py           # Full training script
├── quick_train.py           # Quick training (reduced epochs)
├── saved_models/            # Trained model storage
└── README.md               # This file
```

## 🚀 Quick Start

### 1. Setup and Training

Run the PowerShell setup script from the project root:

```powershell
.\setup_face_shape_ml.ps1
```

Or manually:

```bash
# Install dependencies
pip install tensorflow==2.15.0 keras==2.15.0 albumentations==1.3.1 tqdm==4.66.1

# Train the model (quick version)
cd backend
python ml_models/quick_train.py
```

### 2. Full Training (Optional)

For better accuracy with more epochs:

```bash
cd backend
python ml_models/train_model.py
```

### 3. Test Integration

```bash
cd backend
python test_cnn_integration.py
```

## 🔧 Configuration

Edit `model_config.py` to customize:

```python
# Training parameters
EPOCHS = 50              # Number of training epochs
BATCH_SIZE = 32          # Batch size for training
LEARNING_RATE = 0.001    # Learning rate

# Model architecture
BASE_MODEL = 'EfficientNetB0'  # Base model choice
DROPOUT_RATE = 0.5            # Dropout rate

# Performance
MIN_CONFIDENCE = 0.7     # Minimum confidence threshold
TARGET_ACCURACY = 0.85   # Target accuracy
```

## 📊 Performance

### Expected Results
- **Target Accuracy**: >85%
- **Training Time**: ~10-30 minutes (depending on hardware)
- **Inference Time**: <100ms per image

### Evaluation Metrics
- Accuracy, Precision, Recall, F1-Score
- Per-class accuracy breakdown
- Confusion matrix visualization

## 🔄 Integration

The CNN model is automatically integrated into the existing face shape detection system:

1. **Primary Method**: CNN model prediction
2. **Fallback**: MediaPipe facial landmark analysis
3. **Confidence Threshold**: Switches to fallback if CNN confidence < 0.7

### Usage in Code

```python
from face_shape_detector import FaceShapeDetector

detector = FaceShapeDetector()
result = detector.detect_face_shape("path/to/image.jpg")

print(f"Face shape: {result['face_shape']}")
print(f"Confidence: {result['confidence']}")
print(f"Method: {result['method']}")  # 'CNN' or 'MediaPipe'
```

## 📈 Training Process

### Data Pipeline
1. **Loading**: Images loaded from organized directory structure
2. **Preprocessing**: Resize to 224x224, normalize pixel values
3. **Augmentation**: Random transformations for training data
4. **Splitting**: 80% train, 20% validation from training set

### Training Steps
1. **Model Building**: Create CNN with transfer learning
2. **Compilation**: Adam optimizer, categorical crossentropy loss
3. **Training**: Fit model with callbacks (early stopping, checkpointing)
4. **Evaluation**: Test on separate test set
5. **Saving**: Save best model for deployment

## 🛠️ Troubleshooting

### Common Issues

**1. Dataset Not Found**
```
Error: Training directory not found
```
- Ensure `backend/FaceShapeDS/` exists with proper structure
- Check that training_set and testing_set folders contain class subdirectories

**2. Memory Issues**
```
ResourceExhaustedError: OOM when allocating tensor
```
- Reduce `BATCH_SIZE` in `model_config.py`
- Use `quick_train.py` instead of full training

**3. Low Accuracy**
```
Target accuracy not reached
```
- Increase `EPOCHS` in configuration
- Check data quality and balance
- Try different `BASE_MODEL` options

**4. Import Errors**
```
ModuleNotFoundError: No module named 'tensorflow'
```
- Install dependencies: `pip install -r requirements.txt`
- Ensure virtual environment is activated

### Performance Optimization

**For Faster Training:**
- Use `quick_train.py` (10 epochs)
- Reduce image resolution in config
- Use smaller batch size

**For Better Accuracy:**
- Increase epochs to 50-100
- Use data augmentation
- Try ensemble methods

## 📝 Model Details

### Architecture Summary
```
Input (224x224x3)
    ↓
EfficientNetB0 (frozen)
    ↓
GlobalAveragePooling2D
    ↓
BatchNormalization
    ↓
Dense(512, relu) + Dropout(0.5)
    ↓
Dense(256, relu) + Dropout(0.5)
    ↓
Dense(5, softmax)
```

### Training Configuration
- **Optimizer**: Adam (lr=0.001)
- **Loss**: Categorical Crossentropy
- **Metrics**: Accuracy, Precision, Recall
- **Callbacks**: EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

## 🔮 Future Improvements

1. **Model Ensemble**: Combine multiple models for better accuracy
2. **Real-time Optimization**: Model quantization for faster inference
3. **Data Augmentation**: Advanced augmentation techniques
4. **Active Learning**: Improve model with user feedback
5. **Multi-task Learning**: Combine with other facial analysis tasks
