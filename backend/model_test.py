"""
Test file to compare OpenRouter models for face analysis.
This script tests both Gemini 2.0 Flash Experimental and Qwen2.5 VL 3B Instruct 
to determine which performs better for our facial analysis task.
"""

import os
import sys
import base64
import time
import json
from pathlib import Path
import requests

# Set your API key here (or use environment variable)
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "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")

# Test prompt
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

def encode_image(image_path):
    """Encode an image to base64."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def test_model(model_id, image_path, prompt):
    """Test a specific model with the given image and prompt."""
    base64_image = encode_image(image_path)
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/xxshi/face-bs",
        "X-Title": "Chromalyze"
    }
    
    payload = {
        "model": model_id,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
    }
    
    start_time = time.time()
    try:
        response = requests.post(
            "https://api.openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        result = response.json()
        
        end_time = time.time()
        duration = end_time - start_time
        
        analysis_text = result["choices"][0]["message"]["content"]
        
        return {
            "model": model_id,
            "duration": duration,
            "response_text": analysis_text,
            "full_response": result
        }
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        return {
            "model": model_id,
            "duration": duration,
            "error": str(e),
            "response_text": "ERROR"
        }

def main():
    """Main test function comparing models."""
    # Check if an image path is provided
    if len(sys.argv) < 2:
        print("Usage: python model_test.py <path_to_image>")
        print("Using default test image...")
        # Use a default test image if none provided
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, "test_image.jpg")
        if not os.path.exists(image_path):
            print(f"Default test image not found: {image_path}")
            print("Please provide an image path")
            return
    else:
        image_path = sys.argv[1]
    
    if not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        return
    
    print(f"Testing with image: {image_path}")
    
    # Models to test
    models = [
        "google/gemini-2.0-flash-exp:free",
        "qwen/qwen2.5-vl-3b-instruct:free"
    ]
    
    results = {}
    
    # Test each model
    for model in models:
        print(f"\nTesting model: {model}")
        result = test_model(model, image_path, PROMPT_TEXT)
        results[model] = result
        
        print(f"Response time: {result['duration']:.2f} seconds")
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            print(f"Response:\n{result['response_text']}")
        
        # Wait a bit between API calls
        time.sleep(2)
    
    # Compare and recommend
    recommend_model = None
    
    # Both succeeded
    if "error" not in results[models[0]] and "error" not in results[models[1]]:
        # Choose based on response quality and time
        # For now, prioritize Gemini if both work
        recommend_model = models[0]
        
        # Check if Qwen is significantly faster (30% or more)
        if results[models[1]]["duration"] < 0.7 * results[models[0]]["duration"]:
            recommend_model = models[1]
    
    # One succeeded, one failed
    elif "error" not in results[models[0]]:
        recommend_model = models[0]
    elif "error" not in results[models[1]]:
        recommend_model = models[1]
    
    print("\n----- SUMMARY -----")
    for model in models:
        status = "✅ SUCCESS" if "error" not in results[model] else "❌ FAILED"
        time_info = f"{results[model]['duration']:.2f}s" if "error" not in results[model] else "N/A"
        print(f"{model}: {status} ({time_info})")
    
    if recommend_model:
        print(f"\nRECOMMENDED MODEL: {recommend_model}")
    else:
        print("\nBoth models failed. Please check your API key or try again later.")
    
    # Save results to a JSON file
    output_file = "model_test_results.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDetailed results saved to: {output_file}")

if __name__ == "__main__":
    main() 