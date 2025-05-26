"""
Transcriber: runs Whisper on preprocessed audio
"""

import os
from typing import Optional
import whisper
from config import USE_API, DEFAULT_MODEL_PATH
from utils.logger import get_logger
from fine_tuning.model_router import get_user_model_path  # Removed
from transcription.whisper_loader import load_whisper_model

logger = get_logger(__name__)

# Load the model once per session
_model = None

def load_model(user_id: str):
    global _model
    if _model is None:
        logger.info("Loading Whisper model...")

        # Use model_loader to choose model path
        model = load_whisper_model(user_id)
        _model = model

    return _model

def transcribe_audio(audio_path: str, user_id: str, model_type: str, language: Optional[str]) -> dict:
    if USE_API:
        raise NotImplementedError("OpenAI API mode not implemented yet.")

    try:
        logger.info(f"Transcribing: {audio_path} for user_id: {user_id}, model_type: {model_type}")
        model = load_whisper_model(user_id, model_type, language)

    except Exception as e:
        logger.warning(f"⚠️ Model loading failed: {e}")
        fallback_model = "small.en" if language == "en" else "small"
        logger.info(f"🔁 Using fallback model: {fallback_model}")
        model = whisper.load_model(fallback_model)

    result = model.transcribe(audio_path)
    text = result.get("text", "").strip()

    if not text:
        logger.error("❌ Transcription result is empty.")
        raise RuntimeError("Empty transcription.")

    logger.info("✅ Transcription complete.")
    return {
        "text": text
    }
