"""
Simple test script to analyze a face image using our image_analysis module.
"""

import os
import sys
from pathlib import Path
import requests
import json

# Import our image analysis function
from image_analysis import analyze_image

def download_test_image(url, output_path):
    """Download a test image if none exists"""
    try:
        if os.path.exists(output_path):
            print(f"Using existing test image: {output_path}")
            return True
            
        print(f"Downloading test image from {url} to {output_path}")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        print(f"Test image downloaded successfully")
        return True
    except Exception as e:
        print(f"Error downloading test image: {e}")
        return False

def main():
    """Run a test analysis on a face image"""
    # Default test image URL and path
    test_image_url = "https://thispersondoesnotexist.com"
    test_image_path = "test_image.jpg"
    
    # Check if an image path is provided
    if len(sys.argv) > 1:
        test_image_path = sys.argv[1]
        print(f"Using provided image path: {test_image_path}")
    else:
        # Download test image if it doesn't exist
        if not os.path.exists(test_image_path):
            success = download_test_image(test_image_url, test_image_path)
            if not success:
                print("Failed to download test image. Please provide an image path.")
                return
    
    # Check if the image exists
    if not os.path.exists(test_image_path):
        print(f"Error: Image not found at {test_image_path}")
        return
        
    print(f"Analyzing image: {test_image_path}")
    
    # Run the analysis
    result = analyze_image(test_image_path)
    
    # Display the result
    print("\n--- Analysis Results ---")
    print(f"Status: {result['status']}")
    
    if result['status'] == 'completed':
        print(f"Faces detected: {result['faces_detected']}")
        print(f"Face shape: {result['face_shape']}")
        print(f"Color season: {result['color_season']}")
    else:
        print(f"Error: {result.get('detail', 'Unknown error')}")
    
    # Save the result to a JSON file
    output_file = "analysis_result.json"
    with open(output_file, "w") as f:
        json.dump(result, f, indent=2)
    
    print(f"\nResults saved to: {output_file}")

if __name__ == "__main__":
    main() 