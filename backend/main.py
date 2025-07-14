"""
Chromalyze Face Analysis API - A backend for analyzing facial features and providing personalized
recommendations. This module provides endpoints for image upload, analysis, and result retrieval.
"""

import asyncio
import os
import sqlite3
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Tuple, Any, Optional, List, Union, TypeVar, cast, Callable, Literal, Type, Protocol, Sequence, overload
from collections import OrderedDict, defaultdict
import cv2
import numpy as np
import sys

# Add the current directory to the path to ensure imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, File, UploadFile, HTTPException, status, Request, Response, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.models import OpenAPI
from fastapi.openapi.utils import get_openapi as get_fastapi_openapi
from contextlib import asynccontextmanager
import base64
from pydantic import BaseModel, Field, ConfigDict

# Import analysis function
from image_analysis import analyze_image

# Import palettes if the file exists
try:
    from color_palettes import get_palette
except ImportError:
    # Define a fallback palette function if import fails
    print("Warning: color_palettes module not found. Using fallback palettes.")
    def get_palette(season: str) -> Optional[Dict[str, Any]]:
        """Fallback palette function."""
        return {
            "description": f"Color palette for {season}",
            "recommended": ["Default recommended colors"],
            "avoid": ["Default colors to avoid"]
        }

# Import face shape recommendations
try:
    from face_shape_recommendations import FaceShapeRecommendations
    face_shape_recommendations = FaceShapeRecommendations()
    FACE_RECOMMENDATIONS_AVAILABLE = True
    print("Face shape recommendations loaded successfully")
except ImportError as e:
    print(f"Face shape recommendations not available: {e}")
    FACE_RECOMMENDATIONS_AVAILABLE = False
    face_shape_recommendations = None

# --- Constants (Consider moving to a config file) ---
MAX_CACHE_SIZE = 100
CACHE_TTL_MINUTES = 60
RATE_LIMIT_REQUESTS = 10
RATE_LIMIT_WINDOW = 60 # seconds
MAX_FILE_AGE_HOURS = 24
CLEANUP_INTERVAL_HOURS = 1
# --- End Constants ---

class RateLimiter:
    def __init__(self, requests: int, window: int) -> None:
        self.requests = requests
        self.window = window
        self.clients: Dict[str, List[float]] = defaultdict(list)

    def is_allowed(self, client_id: str) -> bool:
        now = time.time()
        client_requests = self.clients[client_id]
        
        # Remove old timestamps
        while client_requests and now - client_requests[0] > self.window:
            client_requests.pop(0)
        
        # Check if allowed
        if len(client_requests) < self.requests:
            client_requests.append(now)
            return True
        return False

    async def cleanup(self) -> None:
        """Remove expired client records."""
        now = time.time()
        expired = [
            client_id
            for client_id, timestamps in self.clients.items()
            if not timestamps or now - timestamps[-1] > self.window
        ]
        for client_id in expired:
            del self.clients[client_id]

class CustomBaseModel(BaseModel):
    """Base model with common configuration."""
    model_config = ConfigDict(from_attributes=True)

class AnalysisRequest(CustomBaseModel):
    """Analysis request model."""
    file: UploadFile

class AnalysisResponse(CustomBaseModel):
    """Analysis response model."""
    analysis_id: str

class AnalysisResult(CustomBaseModel):
    """Detailed analysis result model including palette."""
    face_shape: str
    color_season: str
    palette: Optional[Dict[str, Any]] = None # To hold description, recommended, avoid

class AnalysisStatus(CustomBaseModel):
    """Analysis status model."""
    status: Literal["pending", "processing", "completed", "error"] # Added 'processing'
    results: Optional[AnalysisResult] = None
    error_detail: Optional[str] = None # Added for error reporting

class UploadResponse(CustomBaseModel):
    """API response model for file uploads."""
    analysis_id: str = Field(
        description="Unique identifier for the uploaded image analysis",
        examples=["a1b2c3d4e5f6", "b2c3d4e5f6g7"]
    )

class ErrorResponse(CustomBaseModel):
    """API error response model."""
    detail: str = Field(
        description="Detailed error message",
        examples=["File must be an image", "Analysis not found", "Rate limit exceeded"]
    )

class CacheEntry:
    def __init__(self, value: Any) -> None:
        self.value = value
        self.timestamp = datetime.now()

class Cache:
    def __init__(self, max_size: int = MAX_CACHE_SIZE, ttl_minutes: int = CACHE_TTL_MINUTES) -> None:
        self.max_size = max_size
        self.ttl = timedelta(minutes=ttl_minutes)
        self.cache: OrderedDict[str, CacheEntry] = OrderedDict()

    def get(self, key: str) -> Optional[Any]:
        if key not in self.cache:
            return None
        entry = self.cache[key]
        if datetime.now() - entry.timestamp > self.ttl:
            del self.cache[key]
            return None
        self.cache.move_to_end(key)
        return entry.value

    def set(self, key: str, value: Any) -> None:
        if key in self.cache:
            del self.cache[key]
        elif len(self.cache) >= self.max_size:
            self.cache.popitem(last=False)
        self.cache[key] = CacheEntry(value)

    async def cleanup(self) -> None:
        """Remove expired entries."""
        now = datetime.now()
        expired = [k for k, v in self.cache.items() if now - v.timestamp > self.ttl]
        for key in expired:
            del self.cache[key]

@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Initialize database and start cleanup tasks on startup."""
    init_db()  # Initialize SQLite database
    UPLOAD_DIR.mkdir(exist_ok=True)  # Ensure upload directory exists
    cleanup_task = asyncio.create_task(start_cleanup_scheduler())
    yield
    cleanup_task.cancel()

app = FastAPI(
    title="Chromalyze",
    description="Chromalyze API for advanced face analysis and personalized recommendations based on images.",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)

DATABASE = "chromalyze.db"

def custom_openapi() -> Dict[str, Any]:
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_fastapi_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return openapi_schema

# Set the custom OpenAPI schema
setattr(app, 'openapi', custom_openapi)
results_cache = Cache()
rate_limiter = RateLimiter(RATE_LIMIT_REQUESTS, RATE_LIMIT_WINDOW)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"],  # Expose all headers
    max_age=3600  # Cache CORS preflight response for 1 hour
)

# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True, parents=True)

async def cleanup_old_files() -> None:
    """Remove files older than MAX_FILE_AGE_HOURS."""
    try:
        current_time = datetime.now()
        for file_path in UPLOAD_DIR.glob("*.jpg"):
            file_age = current_time - datetime.fromtimestamp(file_path.stat().st_mtime)
            if file_age > timedelta(hours=MAX_FILE_AGE_HOURS):
                try:
                    file_path.unlink()
                except OSError as e:
                    print(f"Error deleting {file_path}: {e}")
    except Exception as e:
        print(f"Error during cleanup: {e}")

async def start_cleanup_scheduler() -> None:
    """Start the periodic cleanup task."""
    while True:
        await cleanup_old_files()
        await asyncio.sleep(CLEANUP_INTERVAL_HOURS * 3600)  # Convert hours to seconds

async def cache_cleanup_scheduler() -> None:
    """Periodically clean up expired cache entries."""
    while True:
        await results_cache.cleanup()
        await asyncio.sleep(300)  # Clean up every 5 minutes

async def rate_limit_cleanup_scheduler() -> None:
    """Periodically clean up expired rate limit records."""
    while True:
        await rate_limiter.cleanup()
        await asyncio.sleep(60)  # Clean up every minute

async def cleanup_file(upload_id: str) -> None:
    """Clean up a specific file after analysis."""
    try:
        await asyncio.sleep(300)  # Wait 5 minutes before cleanup
        file_path = UPLOAD_DIR / f"{upload_id}.jpg"
        if file_path.exists():
            file_path.unlink()
    except Exception as e:
        print(f"Error cleaning up file {upload_id}: {e}")

def init_db() -> None:
    """Initialize the SQLite database with required tables."""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS analysis_results
        (id TEXT PRIMARY KEY,
         status TEXT NOT NULL, 
         faces_detected INTEGER,
         skin_tone TEXT,
         face_shape TEXT, 
         color_season TEXT,
         error_detail TEXT,
         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)
    ''')
    # Add indexes for faster lookups
    c.execute('CREATE INDEX IF NOT EXISTS idx_analysis_status ON analysis_results (status)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_analysis_created_at ON analysis_results (created_at)')
    
    # Check if we need to add the error_detail column
    c.execute("PRAGMA table_info(analysis_results)")
    columns = [column[1] for column in c.fetchall()]
    
    if 'error_detail' not in columns:
        print("Adding missing error_detail column to analysis_results table")
        c.execute("ALTER TABLE analysis_results ADD COLUMN error_detail TEXT")
        
    conn.commit()
    conn.close()

async def check_rate_limit(request: Request) -> None:
    """Check if the request is within rate limits."""
    client_id = request.client.host if request.client else "unknown"
    if not rate_limiter.is_allowed(client_id):
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please try again later."
        )


@app.post("/api/upload")
async def upload_file(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None
) -> JSONResponse:
    """
    Upload an image to Chromalyze for analysis
    """
    try:
        # Validate file type
        if not file.filename:
            return JSONResponse(
                {"status": "error", "detail": "No file name provided"},
                status_code=400
            )

        # Check file extension
        file_ext = file.filename.lower().split('.')[-1] if file.filename else ''

        if file_ext not in ['jpg', 'jpeg', 'png', 'bmp']:
            return JSONResponse(
                {"status": "error", "detail": "Invalid file type. Only image files are allowed"},
                status_code=400
            )

        # Generate a unique ID for this analysis
        analysis_id = str(int(time.time() * 1000))
        
        # Create the uploads directory if it doesn't exist
        UPLOAD_DIR.mkdir(exist_ok=True, parents=True)
        
        # Save the uploaded file
        file_path = UPLOAD_DIR / f"{analysis_id}.{file_ext}"
        
        # Ensure file size is not too large (e.g., 10MB max)
        file.file.seek(0, 2)  # Go to end of file
        file_size = file.file.tell()
        file.file.seek(0)  # Reset file pointer
        
        if file_size > 10 * 1024 * 1024:  # 10MB
            return JSONResponse(
                {"status": "error", "detail": "File too large. Maximum size is 10MB"},
                status_code=400
            )
        
        # Write file contents
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Initialize analysis record in database
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute(
            "INSERT INTO analysis_results (id, status, created_at) VALUES (?, ?, ?)",
            (analysis_id, "pending", datetime.now().isoformat())
        )
        conn.commit()
        conn.close()

        if background_tasks:
            background_tasks.add_task(run_analysis, analysis_id, str(file_path))
        
        return JSONResponse({
            "status": "success",
            "analysis_id": analysis_id
        })
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Upload error: {e}")
        
        try:
            # Clean up any database entry
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute("DELETE FROM analysis_results WHERE id = ?", (analysis_id,))
            conn.commit()
            conn.close()
        except Exception as db_clean_err:
            print(f"Failed to cleanup DB entry for failed upload {analysis_id}: {db_clean_err}")
            
        return JSONResponse(
            {"status": "error", "detail": f"Failed to upload image: {str(e)}"},
            status_code=500
        )

async def run_analysis(analysis_id: str, file_path_str: str):
    """Background task to perform image analysis."""
    conn = None
    file_path = Path(file_path_str)
    error_detail = None
    season = None
    shape = None
    faces_detected = 0
    status_to_set = "error" # Default to error

    try:
        # Update status to processing
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("UPDATE analysis_results SET status = ? WHERE id = ?", ("processing", analysis_id))
        conn.commit()
        conn.close()
        conn = None # Reset connection variable

        if not file_path.exists():
            raise FileNotFoundError(f"Analysis file not found: {file_path_str}")

        # Call the image analysis function with the file path
        # This now uses the Gemini 2.0 Flash model for better performance
        result = analyze_image(str(file_path))
        
        if result["status"] == "completed":
            season = result["color_season"]
            shape = result["face_shape"]
            faces_detected = result.get("faces_detected", 0)
            status_to_set = "completed"
        else:
            error_detail = result.get("detail", "Image analysis failed")
            status_to_set = "error"

    except FileNotFoundError as fnf_err:
        print(f"Analysis error for {analysis_id}: {fnf_err}")
        error_detail = str(fnf_err)
    except Exception as e:
        print(f"Unexpected analysis error for {analysis_id}: {e}")
        import traceback
        traceback.print_exc()
        error_detail = f"An unexpected error occurred during analysis: {str(e)}"
    finally:
        # Update database with final status, results, or error
        try:
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute(
                """UPDATE analysis_results 
                   SET status = ?, color_season = ?, face_shape = ?, faces_detected = ?, error_detail = ?
                   WHERE id = ?""",
                (status_to_set, season, shape, faces_detected, error_detail, analysis_id)
            )
            conn.commit()
        except sqlite3.Error as db_error:
            print(f"Failed to update final analysis status for {analysis_id}: {db_error}")
        finally:
            if conn:
                conn.close()


@app.get("/api/results/{analysis_id}")
async def get_results(analysis_id: str) -> JSONResponse:
    """Retrieve analysis status and results with caching and rate limiting."""
    # No rate limit check here for status polling, apply on upload if needed
    
    # Try to get completed result from cache first
    cached_response = results_cache.get(analysis_id)
    if cached_response and cached_response.get("status") == "completed":
        return JSONResponse(cached_response)

    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
        # Use row factory for dictionary access
        conn.row_factory = sqlite3.Row 
        c = conn.cursor()
        c.execute(
            """SELECT id, status, face_shape, color_season, faces_detected, error_detail, created_at 
               FROM analysis_results WHERE id = ?""",
            (analysis_id,)
        )
        result_row = c.fetchone()
        
        if not result_row:
            return JSONResponse(
                {"status": "error", "detail": "Analysis not found"}, 
                status_code=404
            )

        # Convert row to dictionary
        result_data = dict(result_row)
        status = result_data["status"]
        
        response_data: Dict[str, Any] = {"status": status}

        if status == "completed":
            season = result_data.get("color_season")
            shape = result_data.get("face_shape")
            faces_detected = result_data.get("faces_detected", 0)
            palette = None
            if season:
                palette = get_palette(season) # Fetch palette details
            
            response_data["results"] = {
                "face_shape": shape,
                "color_season": season,
                "faces_detected": faces_detected,
                "palette": palette # Include full palette details
            }
            # Cache the completed response
            results_cache.set(analysis_id, response_data)
        elif status == "error":
            response_data["error_detail"] = result_data.get("error_detail", "An unknown error occurred.")
        # For "pending" or "processing", just return the status

        return JSONResponse(response_data)

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error retrieving results for {analysis_id}: {e}")
        return JSONResponse(
            {"status": "error", "detail": f"Failed to retrieve results: {str(e)}"}, 
            status_code=500
        )
    finally:
        if conn:
            conn.close()


@app.get("/")
async def root() -> JSONResponse:
    """Root endpoint that provides API information."""
    return JSONResponse({
        "name": "Chromalyze API",
        "version": app.version,
        "description": "Chromalyze API for advanced face analysis and personalized recommendations based on images.",
        "docs_url": "/api/docs",
        "redoc_url": "/api/redoc"
    })

@app.get("/api/health")
async def health_check() -> JSONResponse:
    """Health check endpoint."""
    return JSONResponse(content={"status": "ok"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
