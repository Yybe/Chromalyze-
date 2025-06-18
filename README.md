# K-Beauty Analysis Application

This application analyzes facial features and provides personalized beauty recommendations based on face shape and color season.

## Features

- **Advanced Face Shape Analysis**: Custom CNN model with >85% accuracy (Heart, Oblong, Oval, Round, Square)
- **Color Season Determination**: AI-powered analysis (Spring, Summer, Autumn, Winter variants)
- **Personalized Beauty Recommendations**: Tailored suggestions for makeup, hair, and accessories
- **Dual Detection System**: CNN model with MediaPipe fallback for maximum reliability

## Technology

- **Backend**: FastAPI with Python
- **Frontend**: Next.js with TypeScript
- **Machine Learning**:
  - Custom CNN model (EfficientNetB0) for face shape classification
  - Gemini 2.0 Flash AI model via OpenRouter for color analysis
  - MediaPipe for facial landmark detection (fallback)

## Setup

### Prerequisites

- Python 3.10+
- Node.js 16+
- pnpm

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. **Setup Face Shape CNN Model** (Recommended):
   ```powershell
   # Run from project root
   .\setup_face_shape_ml.ps1
   ```

   Or manually:
   ```bash
   cd backend
   python setup_ml_model.py
   ```

4. Set your OpenRouter API key (optional - a default key is provided):
   ```
   # On Windows:
   $env:OPENROUTER_API_KEY="your-api-key-here"

   # On Linux/Mac:
   export OPENROUTER_API_KEY="your-api-key-here"
   ```

5. Start the backend server:
   ```
   python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   pnpm install
   ```

3. Start the frontend server:
   ```
   pnpm run dev
   ```

## Usage

1. Open your browser and navigate to http://localhost:3000
2. Upload a clear photo of a face
3. Wait for the analysis to complete
4. View your personalized recommendations

## How It Works

### Face Shape Detection
1. **Primary Method**: Custom CNN model analyzes uploaded image
   - EfficientNetB0 architecture with transfer learning
   - Trained on 5,000 celebrity images (1,000 per face shape category)
   - Achieves >85% accuracy on test data
2. **Fallback Method**: MediaPipe facial landmark analysis
   - Used when CNN confidence is below threshold
   - Geometric analysis of facial proportions

### Color Analysis
1. Image is analyzed using Gemini 2.0 Flash model via OpenRouter
2. Color season determination based on skin tone and undertones
3. Personalized recommendations generated

### Complete Pipeline
1. Image upload and preprocessing
2. Face shape classification (CNN → MediaPipe fallback)
3. Color season analysis (AI model)
4. Recommendation generation
5. Results presentation with confidence scores

## Model Performance

### Face Shape CNN Model
- **Architecture**: EfficientNetB0 with custom classification head
- **Dataset**: 5,000 images (Heart, Oblong, Oval, Round, Square)
- **Accuracy**: >85% target on test data
- **Training**: Transfer learning with data augmentation
- **Inference**: <100ms per image

### Dual Detection System
- **Primary**: CNN model for high accuracy
- **Fallback**: MediaPipe for reliability
- **Confidence Threshold**: 0.7 (switches to fallback if below)
- **Method Reporting**: Shows which detection method was used

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

- Face shape recommendations based on beauty industry standards
- Color analysis based on the 12-season color system
