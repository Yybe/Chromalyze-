"""
K-Beauty Analysis API - A backend for analyzing facial features and providing beauty
recommendations. This module provides endpoints for image upload, analysis, and result retrieval.
"""

import asyncio
import os
import sqlite3
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional, List
import json
import base64
import requests
from concurrent.futures import ThreadPoolExecutor
import httpx
import logging
import aiofiles
import shutil
import uuid
import cv2
import numpy as np

from fastapi import FastAPI, File, UploadFile, HTTPException, status, Request, Response, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

from color_palettes import COLOR_PALETTES, get_palette

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
DATABASE = "chromalyze.db"
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True, parents=True)
RESULTS_DIR = "results"
MAX_FILE_AGE_HOURS = 24
CLEANUP_INTERVAL_HOURS = 1
ANALYSIS_TIMEOUT = 300  # 5 minutes
MAX_RETRIES = 5
RETRY_DELAY = 2

# OpenRouter API configuration
OPENROUTER_API_KEY = "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"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_ID = "google/gemini-2.0-flash-exp:free"
PROMPT_TEXT = """Analyze the facial features in this image and provide:\n1. Face shape (choose one): Oval, Round, Square, Heart, Diamond, Oblong, Triangle\n2. Color season (choose one): \n   - Spring: Light Spring, Warm Spring, Clear Spring\n   - Summer: Light Summer, Cool Summer, Soft Summer\n   - Autumn: Soft Autumn, Warm Autumn, Deep Autumn\n   - Winter: Deep Winter, Cool Winter, Clear Winter\n\nRespond with ONLY two lines:\nLine 1: Face shape\nLine 2: Color season"""

# Create a thread pool for running analysis
thread_pool = ThreadPoolExecutor(max_workers=4)

# Store analysis results
analysis_results: Dict[str, dict] = {}

# Store analysis status
analysis_status: Dict[str, dict] = {}

class AnalysisResponse(BaseModel):
    """Analysis response model."""
    analysis_id: str

class AnalysisResult(BaseModel):
    """Detailed analysis result model."""
    face_shape: str
    color_season: str
    status: str
    result: Optional[dict] = None
    error_detail: Optional[str] = None
    progress: Optional[float] = None

app = FastAPI(
    title="Chromalyze",
    description="Chromalyze API for personal color and face shape analysis based on images.",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def init_db():
    """Initialize the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS analysis_results (
            id TEXT PRIMARY KEY,
            status TEXT,
            face_shape TEXT,
            color_season TEXT,
            error_detail TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def analyze_image(file_path: str) -> dict:
    """Analyze image using OpenRouter Gemini Vision API with local fallback."""
    retries = 0
    last_error = None
    
    # First try OpenRouter API
    while retries < MAX_RETRIES:
        try:
            # Read and encode image
            with open(file_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "HTTP-Referer": "https://github.com/xxshi/face-bs",
                "X-Title": "Chromalyze"
            }

            payload = {
                "model": MODEL_ID,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": PROMPT_TEXT},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
                        ]
                    }
                ]
            }

            try:
                response = requests.post(
                    OPENROUTER_API_URL,
                    headers=headers,
                    json=payload,
                    timeout=ANALYSIS_TIMEOUT
                )

                if response.status_code == 200:
                    result = response.json()
                    if "choices" in result and result["choices"]:
                        analysis_text = result["choices"][0]["message"]["content"]
                        lines = analysis_text.strip().split('\n')
                        if len(lines) >= 2:
                            return {
                                "face_shape": lines[0].strip(),
                                "color_season": lines[1].strip()
                            }
            except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
                last_error = str(e)
                retries += 1
                if retries < MAX_RETRIES:
                    time.sleep(RETRY_DELAY * (retries + 1))
                    continue
                break

        except Exception as e:
            last_error = str(e)
            retries += 1
            if retries < MAX_RETRIES:
                time.sleep(RETRY_DELAY * (retries + 1))
                continue
            break

    # If OpenRouter fails, use local analysis
    try:
        logger.info("Falling back to local analysis")
        # Use OpenCV for basic face detection
        img = cv2.imread(file_path)
        if img is None:
            raise Exception("Failed to load image")

        # Convert to grayscale for face detection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) == 0:
            return {
                "face_shape": "Unknown",
                "color_season": "Unknown",
                "error": "No face detected in image"
            }

        # Basic face shape analysis based on face rectangle
        x, y, w, h = faces[0]
        aspect_ratio = w / float(h)
        
        # Simple face shape classification based on aspect ratio
        if aspect_ratio > 0.85:
            face_shape = "Round"
        elif aspect_ratio > 0.75:
            face_shape = "Oval"
        else:
            face_shape = "Oblong"

        # Basic color analysis
        face_roi = img[y:y+h, x:x+w]
        avg_color = np.mean(face_roi, axis=(0,1))
        
        # Simple color season classification
        if avg_color[2] > avg_color[1] and avg_color[2] > avg_color[0]:
            color_season = "Warm Autumn"
        else:
            color_season = "Cool Summer"

        return {
            "face_shape": face_shape,
            "color_season": color_season,
            "note": "Results from local analysis"
        }

    except Exception as e:
        logger.error(f"Local analysis failed: {str(e)}")
        raise Exception(f"Both API and local analysis failed. Last error: {last_error}")

def run_analysis(analysis_id: str, file_path_str: str):
    """Run analysis on the uploaded image."""
    try:
        # Initialize database connection
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Update status to processing
        cursor.execute(
            "UPDATE analysis_results SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            ("processing", analysis_id)
        )
        conn.commit()
        
        # Run analysis
        result = analyze_image(file_path_str)
        
        # Update database with results
        cursor.execute(
            """
            UPDATE analysis_results 
            SET status = ?, 
                face_shape = ?, 
                color_season = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            ("completed", result.get("face_shape"), result.get("color_season"), analysis_id)
        )
        conn.commit()
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        # Update status to error
        cursor.execute(
            "UPDATE analysis_results SET status = ?, error_detail = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            ("error", str(e), analysis_id)
        )
        conn.commit()
    finally:
        if conn:
            conn.close()

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    init_db()

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)) -> JSONResponse:
    """Upload and analyze an image file."""
    try:
        # Create a unique ID for this analysis
        analysis_id = str(uuid.uuid4())
        
        # Create uploads directory if it doesn't exist
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        
        # Save the uploaded file
        file_path = os.path.join(UPLOAD_DIR, f"{analysis_id}.jpg")
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Run analysis immediately
        result = analyze_image(file_path)
        
        # Save to database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO analysis_results (id, status, face_shape, color_season, error_detail) VALUES (?, ?, ?, ?, ?)",
            (
                analysis_id,
                "completed",
                result.get("face_shape", "Unknown"),
                result.get("color_season", "Unknown"),
                result.get("detail", None)
            )
        )
        conn.commit()
        conn.close()
        
        # Return results immediately
        return JSONResponse(content={
            "analysis_id": analysis_id,
            "status": "completed",
            "result": result
        })
        
    except Exception as e:
        logger.error(f"Error in upload: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.get("/api/results/{analysis_id}")
async def get_results(analysis_id: str) -> JSONResponse:
    """Get analysis results."""
    try:
        # Get from database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT status, face_shape, color_season, error_detail FROM analysis_results WHERE id = ?",
            (analysis_id,)
        )
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Analysis not found"
            )
            
        status_value, face_shape, color_season, error_detail = result

        # Get detailed palette data if analysis is completed
        palette_data = None
        if status_value == "completed" and color_season and color_season != "Unknown":
            try:
                normalized_season = color_season.replace('_', ' ').title()
                palette_data = get_palette(normalized_season)
            except Exception as e:
                logger.warning(f"Could not get palette for {color_season}: {e}")

        result_data = {
            "face_shape": face_shape,
            "color_season": color_season,
            "error_detail": error_detail
        }

        # Add palette data if available
        if palette_data:
            result_data["palette"] = palette_data

        return JSONResponse(content={
            "status": status_value,
            "result": result_data
        })
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting results: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.get("/api/health")
async def health_check() -> JSONResponse:
    """Health check endpoint."""
    return JSONResponse(content={"status": "healthy"})

@app.get("/api/palette/{color_season}")
async def get_color_palette(color_season: str) -> JSONResponse:
    """Get detailed color palette for a specific color season."""
    try:
        # Normalize the color season name
        normalized_season = color_season.replace('_', ' ').title()

        # Get palette from color_palettes.py
        palette = get_palette(normalized_season)

        if not palette:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Color season '{normalized_season}' not found"
            )

        return JSONResponse(content={
            "season": normalized_season,
            "palette": palette
        })

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting color palette: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

async def save_analysis_status(analysis_id: str, status: dict):
    """Save analysis status to disk"""
    status_file = os.path.join(RESULTS_DIR, f"{analysis_id}.json")
    async with aiofiles.open(status_file, 'w') as f:
        await f.write(json.dumps(status))

async def load_analysis_status(analysis_id: str) -> Optional[dict]:
    """Load analysis status from disk"""
    status_file = os.path.join(RESULTS_DIR, f"{analysis_id}.json")
    try:
        async with aiofiles.open(status_file, 'r') as f:
            return json.loads(await f.read())
    except:
        return None

async def analyze_face(file_path: str, analysis_id: str):
    """Analyze face using the API with retries and progress tracking"""
    try:
        # Initialize status
        status = {
            "status": "processing",
            "result": None,
            "error_detail": None,
            "progress": 0,
            "start_time": time.time(),
            "last_update": time.time()
        }
        analysis_status[analysis_id] = status
        await save_analysis_status(analysis_id, status)

        # Run analysis in thread pool to avoid blocking
        def run_analysis():
            try:
                result = analyze_image(file_path)
                return result
            except Exception as e:
                logger.error(f"Analysis error: {str(e)}")
                raise

        # Update progress to 30% for starting analysis
        status["progress"] = 30
        status["last_update"] = time.time()
        await save_analysis_status(analysis_id, status)

        # Run analysis with timeout
        loop = asyncio.get_event_loop()
        try:
            result = await asyncio.wait_for(
                loop.run_in_executor(thread_pool, run_analysis),
                timeout=ANALYSIS_TIMEOUT
            )
            
            # Update progress to 100% for completed analysis
            status.update({
                "status": "completed",
                "result": result,
                "progress": 100,
                "end_time": time.time()
            })
            await save_analysis_status(analysis_id, status)
            
        except asyncio.TimeoutError:
            logger.error("Analysis timed out")
            status.update({
                "status": "error",
                "error_detail": "Analysis timed out",
                "end_time": time.time()
            })
            await save_analysis_status(analysis_id, status)
            raise HTTPException(
                status_code=504,
                detail="Analysis timed out"
            )

    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        status.update({
            "status": "error",
            "error_detail": str(e),
            "end_time": time.time()
        })
        await save_analysis_status(analysis_id, status)
    finally:
        # Clean up the uploaded file
        try:
            os.remove(file_path)
        except Exception as e:
            logger.error(f"Error cleaning up file {file_path}: {str(e)}")

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    """Upload a file and start analysis"""
    try:
        # Generate a unique ID for this analysis
        analysis_id = f"{int(time.time())}_{file.filename}"
        
        # Save the file
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Start analysis in background
        if background_tasks:
            background_tasks.add_task(analyze_face, file_path, analysis_id)
        else:
            asyncio.create_task(analyze_face(file_path, analysis_id))
        
        return {"analysis_id": analysis_id, "status": "processing"}
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

async def process_image(file_path: str, analysis_id: str):
    """Process an uploaded image."""
    try:
        # Update status to processing
        status = {
            "status": "processing",
            "start_time": time.time(),
            "progress": 0
        }
        await save_analysis_status(analysis_id, status)
        
        # Run analysis
        result = analyze_image(file_path)
        
        # Update status with results
        status = {
            "status": "completed",
            "progress": 100,
            "result": result
        }
        await save_analysis_status(analysis_id, status)
        
        # Save to database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO analysis_results (id, status, face_shape, color_season, error_detail) VALUES (?, ?, ?, ?, ?)",
            (
                analysis_id,
                "completed",
                result.get("face_shape", "Unknown"),
                result.get("color_season", "Unknown"),
                result.get("detail", None)
            )
        )
        conn.commit()
        conn.close()
        
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        # Update status with error
        status = {
            "status": "error",
            "progress": 100,
            "error_detail": str(e)
        }
        await save_analysis_status(analysis_id, status)
        
        # Save error to database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO analysis_results (id, status, error_detail) VALUES (?, ?, ?)",
            (analysis_id, "error", str(e))
        )
        conn.commit()
        conn.close()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
