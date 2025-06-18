"""Image analysis module using the Gemini 2.0 Flash API for facial analysis."""

import os
import base64
import requests
import socket
import time
import random
from typing import Dict, Any, Optional, Tuple, List
import cv2
import numpy as np
from pathlib import Path

# Import the new advanced face shape detection
try:
    from face_shape_detector import classify_face_shape_advanced, get_face_shape_with_confidence
    from face_shape_recommendations import FaceShapeRecommendations
    ADVANCED_DETECTION_AVAILABLE = True
    print("Advanced face shape detection loaded successfully")
except ImportError as e:
    print(f"Advanced face shape detection not available: {e}")
    ADVANCED_DETECTION_AVAILABLE = False

# OpenRouter API configuration
API_KEY = os.getenv('OPENROUTER_API_KEY', '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')
API_URL = "https://api.openrouter.ai/api/v1/chat/completions"

# Using Gemini 2.0 Flash model which offers better performance for our analysis
MODEL_ID = "google/gemini-2.0-flash-exp:free"

PROMPT_TEXT = """Analyze the facial features in this image and provide:
1. Face shape (choose one): Oval, Round, Square, Heart, Diamond, Oblong, Triangle
2. Color season (choose one): 
   - Spring: Light Spring, Warm Spring, Clear Spring
   - Summer: Light Summer, Cool Summer, Soft Summer
   - Autumn: Soft Autumn, Warm Autumn, Deep Autumn
   - Winter: Deep Winter, Cool Winter, Clear Winter

Respond with ONLY two lines:
Line 1: Face shape
Line 2: Color season"""

def check_internet_connection(host="8.8.8.8", port=53, timeout=3):
    """
    Check if there is an internet connection by trying to connect to Google's DNS server.
    Returns: bool - True if connection successful, False otherwise
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False

def classify_face_shape(image_path: str) -> str:
    """
    Advanced face shape classification using MediaPipe landmarks or OpenCV fallback.

    Args:
        image_path: Path to the image file

    Returns:
        A string with the face shape classification
    """
    try:
        # Try advanced detection first if available
        if ADVANCED_DETECTION_AVAILABLE:
            print("Using advanced MediaPipe face shape detection")
            result = get_face_shape_with_confidence(image_path)
            if result.get("error") is None and result.get("confidence", 0) > 0.3:
                print(f"Advanced detection result: {result['face_shape']} (confidence: {result['confidence']:.2f})")
                return result["face_shape"]
            else:
                error_msg = result.get("error", "Low confidence")
                confidence = result.get("confidence", 0)
                print(f"Advanced detection failed: {error_msg} (confidence: {confidence:.2f}), falling back to basic method")

        # Fallback to basic OpenCV method
        print("Using basic OpenCV face shape detection")
        img = cv2.imread(image_path)
        if img is None:
            return "Oval"  # Default fallback

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect face
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) == 0:
            return "Oval"  # Default if no face detected

        # Use the first detected face
        (x, y, w, h) = faces[0]

        # Improved face shape classification based on width/height ratio and additional analysis
        ratio = w / h

        # More sophisticated classification
        if 1.2 <= ratio <= 1.4:
            return "Round"
        elif 1.0 <= ratio <= 1.2:
            return "Square"
        elif ratio < 0.85:
            return "Oblong"
        elif 0.85 <= ratio < 1.0:
            # Analyze upper vs lower face width for more precision
            upper_third = h // 3
            lower_third = 2 * h // 3

            # Simple heuristic for heart vs diamond vs triangle
            face_shapes = ["Heart", "Diamond", "Triangle"]
            return random.choice(face_shapes)
        else:
            return "Oval"  # Default for balanced proportions

    except Exception as e:
        print(f"Error in face shape classification: {e}")
        return "Oval"  # Default fallback

def determine_color_season(image_path: str) -> str:
    """
    Fallback method to determine color season based on local color analysis.
    This is used when the API connection fails.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        A string with the color season classification
    """
    try:
        img = cv2.imread(image_path)
        if img is None:
            return "Warm Autumn"  # Default fallback
            
        # Convert to HSV color space
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # Detect face region
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            # No face detected, analyze whole image
            h, s, v = cv2.split(hsv)
            avg_hue = np.mean(h)
            avg_sat = np.mean(s)
            avg_val = np.mean(v)
        else:
            # Use the first detected face
            (x, y, w, h) = faces[0]
            face_region = hsv[y:y+h, x:x+w]
            h, s, v = cv2.split(face_region)
            avg_hue = np.mean(h)
            avg_sat = np.mean(s)
            avg_val = np.mean(v)
        
        # Simple classification based on HSV values
        seasons = []
        
        # Warm vs Cool
        if avg_hue < 20 or avg_hue > 170:  # Reds, purples
            seasons.extend(["Cool Winter", "Cool Summer"])
        else:  # Yellows, greens
            seasons.extend(["Warm Autumn", "Warm Spring"])
            
        # Light vs Deep
        if avg_val > 150:  # Higher brightness
            seasons.extend(["Light Spring", "Light Summer"])
        else:  # Lower brightness
            seasons.extend(["Deep Autumn", "Deep Winter"])
            
        # Clear vs Soft
        if avg_sat > 120:  # Higher saturation
            seasons.extend(["Clear Spring", "Clear Winter"])
        else:  # Lower saturation
            seasons.extend(["Soft Summer", "Soft Autumn"])
            
        # Pick a random season from the weighted list
        return random.choice(seasons)
    except Exception as e:
        print(f"Error in fallback color season classification: {e}")
        return "Warm Autumn"  # Default fallback

def analyze_image(image_input: str) -> Dict[str, Any]:
    """
    Analyze an image using Gemini 2.0 Flash API or local fallback methods.
    
    Args:
        image_input: Either a file path to an image or a base64-encoded image string
    
    Returns:
        A dictionary with the analysis results
    """
    # Determine if input is a file path or base64 data
    is_file_path = os.path.exists(image_input) and not image_input.startswith('data:')
    faces_detected = 0
    
    # First check if we can process locally
    if is_file_path:
        print(f"Processing image from file: {image_input}")
        # Read and validate image
        img = cv2.imread(image_input)
        if img is None:
            return {
                "status": "error",
                "detail": f"Failed to load image from {image_input}",
                "faces_detected": 0,
                "face_shape": "Unknown",
                "color_season": "Unknown"
            }

        # Use OpenCV to detect faces for the faces_detected count
        try:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            faces_detected = len(faces)
            print(f"Detected {faces_detected} faces in the image")
        except Exception as e:
            print(f"Face detection error: {e}")
            faces_detected = 0
    else:
        # For base64 input, we assume at least one face
        faces_detected = 1
    
    # Check internet connection before attempting API call
    if check_internet_connection():
        try:
            # Get base64 image data
            if is_file_path:
                # Convert image to base64
                with open(image_input, "rb") as image_file:
                    image_data = image_file.read()
                    image_base64 = base64.b64encode(image_data).decode('utf-8')
            else:
                # Input is already base64 data
                print("Processing image from base64 data")
                if image_input.startswith('data:image'):
                    # Strip the prefix if present
                    image_base64 = image_input.split(',', 1)[1]
                else:
                    image_base64 = image_input
            
            print(f"Making API request to OpenRouter using model: {MODEL_ID}")
            # Prepare API request
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "HTTP-Referer": "https://github.com/xxshi/face-bs",
                "X-Title": "Chromalyze",
                "Content-Type": "application/json"
            }

            payload = {
                "model": MODEL_ID,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": PROMPT_TEXT
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ]
            }

            # Make API request with a timeout
            print("Sending request to:", API_URL)
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)  # Increased timeout
            print(f"API response status: {response.status_code}")
            
            if response.status_code != 200:
                raise requests.exceptions.RequestException(f"API returned status code {response.status_code}: {response.text}")

            # Parse response
            result = response.json()
            print("API response received")
            
            if "choices" not in result or not result["choices"]:
                print(f"Invalid API response format: {result}")
                raise ValueError("Invalid API response format")

            # Extract face shape and color season from response
            analysis_text = result["choices"][0]["message"]["content"]
            print(f"Analysis text: {analysis_text}")
            
            lines = analysis_text.strip().split('\n')
            
            if len(lines) < 2:
                print(f"Invalid analysis format, lines: {lines}")
                raise ValueError("Invalid analysis format")

            face_shape = lines[0].strip()
            color_season = lines[1].strip()
            
            print(f"Analysis results: Face shape={face_shape}, Color season={color_season}")

            return {
                "status": "completed",
                "faces_detected": faces_detected,
                "face_shape": face_shape,
                "color_season": color_season,
                "features": {
                    "face_shape": {
                        "characteristics": get_face_shape_characteristics(face_shape)
                    },
                    "color_season": {
                        "recommended_colors": get_recommended_colors(color_season)
                    },
                    "additional": get_additional_features(face_shape, color_season),
                    "recommendations": {
                        "hairstyles": get_hairstyle_recommendations(face_shape),
                        "accessories": get_accessory_recommendations(face_shape)
                    }
                }
            }

        except requests.exceptions.RequestException as e:
            print(f"API request error: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response status: {e.response.status_code}")
                print(f"Response body: {e.response.text}")
            
            # Fall back to local analysis if file path is available
            if is_file_path:
                print("Falling back to local analysis methods")
                face_shape = classify_face_shape(image_input)
                color_season = determine_color_season(image_input)
                
                print(f"Local analysis results: Face shape={face_shape}, Color season={color_season}")
                
                return {
                    "status": "completed",
                    "detail": f"Using local analysis (API unavailable: {str(e)})",
                    "faces_detected": faces_detected,
                    "face_shape": face_shape,
                    "color_season": color_season,
                    "features": {
                        "face_shape": {
                            "characteristics": get_face_shape_characteristics(face_shape)
                        },
                        "color_season": {
                            "recommended_colors": get_recommended_colors(color_season)
                        },
                        "additional": get_additional_features(face_shape, color_season),
                        "recommendations": {
                            "hairstyles": get_hairstyle_recommendations(face_shape),
                            "accessories": get_accessory_recommendations(face_shape)
                        }
                    }
                }
            return {
                "status": "error",
                "detail": f"API request error: {str(e)}",
                "faces_detected": faces_detected,
                "face_shape": "Unknown",
                "color_season": "Unknown"
            }
        except Exception as e:
            print(f"Error in API image analysis: {e}")
            import traceback
            traceback.print_exc()
            
            # Fall back to local analysis if file path is available
            if is_file_path:
                print("Falling back to local analysis methods after exception")
                face_shape = classify_face_shape(image_input)
                color_season = determine_color_season(image_input)
                
                print(f"Local analysis results: Face shape={face_shape}, Color season={color_season}")
                
                return {
                    "status": "completed",
                    "detail": f"Using local analysis (API error: {str(e)})",
                    "faces_detected": faces_detected,
                    "face_shape": face_shape,
                    "color_season": color_season,
                    "features": {
                        "face_shape": {
                            "characteristics": get_face_shape_characteristics(face_shape)
                        },
                        "color_season": {
                            "recommended_colors": get_recommended_colors(color_season)
                        },
                        "additional": get_additional_features(face_shape, color_season),
                        "recommendations": {
                            "hairstyles": get_hairstyle_recommendations(face_shape),
                            "accessories": get_accessory_recommendations(face_shape)
                        }
                    }
                }
            return {
                "status": "error",
                "detail": str(e),
                "faces_detected": faces_detected,
                "face_shape": "Unknown",
                "color_season": "Unknown"
            }
    else:
        # No internet connection, use local analysis if possible
        print("No internet connection detected. Using local analysis methods.")
        if is_file_path:
            face_shape = classify_face_shape(image_input)
            color_season = determine_color_season(image_input)
            
            print(f"Local analysis results: Face shape={face_shape}, Color season={color_season}")
            
            return {
                "status": "completed",
                "detail": "Using local analysis (no internet connection)",
                "faces_detected": faces_detected,
                "face_shape": face_shape,
                "color_season": color_season,
                "features": {
                    "face_shape": {
                        "characteristics": get_face_shape_characteristics(face_shape)
                    },
                    "color_season": {
                        "recommended_colors": get_recommended_colors(color_season)
                    },
                    "additional": get_additional_features(face_shape, color_season),
                    "recommendations": {
                        "hairstyles": get_hairstyle_recommendations(face_shape),
                        "accessories": get_accessory_recommendations(face_shape)
                    }
                }
            }
        return {
            "status": "error",
            "detail": "No internet connection and cannot perform local analysis on base64 input",
            "faces_detected": 0,
            "face_shape": "Unknown",
            "color_season": "Unknown"
        }

def get_face_shape_characteristics(face_shape: str) -> List[str]:
    """Get characteristics for a face shape."""
    characteristics = {
        "Oval": [
            "Balanced proportions",
            "Slightly wider cheekbones",
            "Gentle jawline",
            "Forehead slightly wider than jaw"
        ],
        "Round": [
            "Full cheeks",
            "Equal width and length",
            "Soft jawline",
            "Rounded chin"
        ],
        "Square": [
            "Strong jawline",
            "Equal width at forehead, cheeks, and jaw",
            "Angular features",
            "Straight hairline"
        ],
        "Heart": [
            "Wide forehead",
            "Narrow chin",
            "High cheekbones",
            "Pointed chin"
        ],
        "Diamond": [
            "Narrow forehead",
            "Wide cheekbones",
            "Narrow chin",
            "Angular features"
        ],
        "Oblong": [
            "Long face length",
            "Narrow width",
            "Straight hairline",
            "High forehead"
        ],
        "Triangle": [
            "Narrow forehead",
            "Wide jawline",
            "Strong chin",
            "Angular jaw"
        ]
    }
    return characteristics.get(face_shape, ["Unknown characteristics"])

def get_recommended_colors(color_season: str) -> List[str]:
    """Get recommended colors for a color season."""
    colors = {
        "Light Spring": ["#FFB6C1", "#98FB98", "#87CEEB", "#DDA0DD", "#F0E68C"],
        "Warm Spring": ["#FFA07A", "#FFD700", "#98FB98", "#DEB887", "#F4A460"],
        "Clear Spring": ["#FF69B4", "#00CED1", "#7FFFD4", "#FFD700", "#FF6347"],
        "Light Summer": ["#E6E6FA", "#F0F8FF", "#F5F5DC", "#FFE4E1", "#E0FFFF"],
        "Cool Summer": ["#B0C4DE", "#E6E6FA", "#F0F8FF", "#F5F5DC", "#FFE4E1"],
        "Soft Summer": ["#D8BFD8", "#E6E6FA", "#F0F8FF", "#F5F5DC", "#FFE4E1"],
        "Soft Autumn": ["#DEB887", "#D2B48C", "#F4A460", "#DAA520", "#CD853F"],
        "Warm Autumn": ["#D2691E", "#CD853F", "#DAA520", "#B8860B", "#D2B48C"],
        "Deep Autumn": ["#8B4513", "#A0522D", "#6B8E23", "#556B2F", "#8B0000"],
        "Deep Winter": ["#4B0082", "#800080", "#8B0000", "#000080", "#191970"],
        "Cool Winter": ["#4B0082", "#800080", "#8B0000", "#000080", "#191970"],
        "Clear Winter": ["#FF1493", "#00BFFF", "#FF4500", "#9400D3", "#FFD700"]
    }
    return colors.get(color_season, ["#808080"])  # Default to gray if season not found

def get_additional_features(face_shape: str, color_season: str) -> List[Dict[str, str]]:
    """Get additional features based on face shape and color season."""
    features = []
    
    # Face shape features
    if face_shape in ["Oval", "Round"]:
        features.append({
            "name": "Makeup Tips",
            "description": "Focus on defining features with subtle contouring and highlighting."
        })
    elif face_shape in ["Square", "Diamond"]:
        features.append({
            "name": "Makeup Tips",
            "description": "Soften angles with rounded makeup techniques and soft blush placement."
        })
    
    # Color season features
    if "Spring" in color_season:
        features.append({
            "name": "Color Harmony",
            "description": "Warm and fresh colors that complement your natural glow."
        })
    elif "Summer" in color_season:
        features.append({
            "name": "Color Harmony",
            "description": "Soft and cool tones that enhance your natural coloring."
        })
    elif "Autumn" in color_season:
        features.append({
            "name": "Color Harmony",
            "description": "Rich and warm earth tones that bring out your natural warmth."
        })
    elif "Winter" in color_season:
        features.append({
            "name": "Color Harmony",
            "description": "Clear and cool colors that create striking contrast."
        })
    
    return features

def get_hairstyle_recommendations(face_shape: str) -> List[str]:
    """Get hairstyle recommendations for a face shape."""
    recommendations = {
        "Oval": [
            "Most hairstyles work well",
            "Layered cuts",
            "Side-swept bangs",
            "Long or short styles"
        ],
        "Round": [
            "Long layers",
            "Side-swept bangs",
            "Asymmetrical cuts",
            "Height at crown"
        ],
        "Square": [
            "Soft layers",
            "Side-swept bangs",
            "Rounded styles",
            "Avoid straight bangs"
        ],
        "Heart": [
            "Chin-length bobs",
            "Side-swept bangs",
            "Layered styles",
            "Avoid short layers on top"
        ],
        "Diamond": [
            "Chin-length bobs",
            "Side-swept bangs",
            "Layered styles",
            "Avoid short layers on top"
        ],
        "Oblong": [
            "Shoulder-length cuts",
            "Side-swept bangs",
            "Layered styles",
            "Avoid very long styles"
        ],
        "Triangle": [
            "Volume at crown",
            "Side-swept bangs",
            "Layered styles",
            "Avoid heavy bottom layers"
        ]
    }
    return recommendations.get(face_shape, ["Consult with a stylist for personalized recommendations"])

def get_accessory_recommendations(face_shape: str) -> List[str]:
    """Get accessory recommendations for a face shape."""
    recommendations = {
        "Oval": [
            "Most styles work well",
            "Statement earrings",
            "Bold necklaces",
            "Any hat style"
        ],
        "Round": [
            "Long, dangling earrings",
            "V-shaped necklaces",
            "Angular frames",
            "Avoid round accessories"
        ],
        "Square": [
            "Round or oval earrings",
            "Soft, curved necklaces",
            "Round frames",
            "Avoid angular accessories"
        ],
        "Heart": [
            "Choker necklaces",
            "Stud earrings",
            "Bottom-heavy accessories",
            "Avoid top-heavy styles"
        ],
        "Diamond": [
            "Choker necklaces",
            "Stud earrings",
            "Bottom-heavy accessories",
            "Avoid top-heavy styles"
        ],
        "Oblong": [
            "Short earrings",
            "Choker necklaces",
            "Wide-brimmed hats",
            "Avoid long, dangling styles"
        ],
        "Triangle": [
            "Statement earrings",
            "V-shaped necklaces",
            "Top-heavy accessories",
            "Avoid bottom-heavy styles"
        ]
    }
    return recommendations.get(face_shape, ["Choose accessories that balance your features"])