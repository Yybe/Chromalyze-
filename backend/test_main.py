import os
import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import cv2
import numpy as np
import shutil
from main import app, Image, detect_skin_tone, detect_face_shape, determine_color_season, init_db

client = TestClient(app)

# Test data setup
TEST_IMAGE_DIR = Path(__file__).parent / "test_data"
TEST_DB = "test_chromalyze.db"

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Set up test environment with directory and database."""
    # Create test directory
    TEST_IMAGE_DIR.mkdir(exist_ok=True)
    
    # Initialize test database
    init_db()
    
    yield
    
    # Cleanup
    try:
        shutil.rmtree(TEST_IMAGE_DIR, ignore_errors=True)
    except Exception:
        pass
    
    try:
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
    except Exception:
        pass

def create_test_face_image(size: tuple[int, int] = (200, 300)) -> tuple[str, Image]:
    """Create a test face image with known properties."""
    # Create a simple face-like image for testing
    img = np.ones((size[1], size[0], 3), dtype=np.uint8) * 200  # Light skin tone
    
    # Create face-like features
    center_x = size[0] // 2
    center_y = size[1] // 2
    
    # Draw eyes
    cv2.circle(img, (center_x - 30, center_y - 30), 10, (0, 0, 0), -1)
    cv2.circle(img, (center_x + 30, center_y - 30), 10, (0, 0, 0), -1)
    
    # Draw mouth
    cv2.ellipse(img, (center_x, center_y + 30), (30, 10), 0, 0, 180, (0, 0, 0), 2)
    
    img_path = str(TEST_IMAGE_DIR / "test_face.jpg")
    cv2.imwrite(img_path, img)
    return img_path, img

def test_upload_endpoint():
    """Test the file upload endpoint."""
    img_path, _ = create_test_face_image()
    
    with open(img_path, "rb") as f:
        response = client.post(
            "/api/upload",
            files={"file": ("test_face.jpg", f, "image/jpeg")}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert "analysis_id" in data
    return data["analysis_id"]

def test_upload_invalid_file():
    """Test uploading an invalid file type."""
    response = client.post(
        "/api/upload",
        files={"file": ("test.txt", b"not an image", "text/plain")}
    )
    
    assert response.status_code == 400
    assert "File must be an image" in response.json()["detail"]

def test_analyze_endpoint():
    """Test the analysis endpoint."""
    analysis_id = test_upload_endpoint()
    
    response = client.post(f"/api/analyze/{analysis_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    assert data["status"] in ["pending", "completed"]

def test_get_results():
    """Test retrieving analysis results."""
    analysis_id = test_upload_endpoint()
    
    # First analyze the image
    client.post(f"/api/analyze/{analysis_id}")
    
    # Then get results
    response = client.get(f"/api/results/{analysis_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    if data["status"] == "completed":
        assert "results" in data
        results = data["results"]
        assert "faces_detected" in results
        assert "skin_tone" in results
        assert "face_shape" in results
        assert "color_season" in results

def test_skin_tone_detection():
    """Test skin tone detection function."""
    _, test_img = create_test_face_image()
    skin_tone = detect_skin_tone(test_img)
    assert isinstance(skin_tone, str)
    assert skin_tone in ["Very Light", "Light", "Medium", "Medium Dark", "Dark"]

def test_face_shape_detection():
    """Test face shape detection function."""
    _, test_img = create_test_face_image()
    face_coords = (50, 50, 100, 150)  # Simulated face coordinates
    face_shape = detect_face_shape(test_img, face_coords)
    assert isinstance(face_shape, str)
    assert face_shape in ["Oval", "Round", "Square", "Oblong"]

def test_color_season_determination():
    """Test color season determination function."""
    test_skin_tones = ["Very Light", "Light", "Medium", "Medium Dark", "Dark"]
    
    for tone in test_skin_tones:
        season = determine_color_season(tone)
        assert isinstance(season, str)
        assert season in ["Spring", "Summer", "Autumn", "Winter"]

def test_rate_limiting():
    """Test rate limiting functionality."""
    img_path, _ = create_test_face_image()
    
    # Make multiple requests quickly
    responses = []
    for _ in range(12):  # More than our limit
        with open(img_path, "rb") as f:
            response = client.post(
                "/api/upload",
                files={"file": ("test_face.jpg", f, "image/jpeg")}
            )
            responses.append(response.status_code)
    
    # Should see some 429 responses
    assert 429 in responses

def test_error_handling():
    """Test error handling for various scenarios."""
    # Test non-existent analysis
    response = client.get("/api/results/nonexistent")
    assert response.status_code == 404
    
    # Test invalid analysis ID
    response = client.post("/api/analyze/invalid")
    assert response.status_code == 404 