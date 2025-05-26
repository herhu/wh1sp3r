"""
Whisper loader module that supports loading base or fine-tuned models.
Used by transcriber for modular model loading.
"""

import os
from typing import Optional
import whisper
from pathlib import Path
from utils.logger import get_logger

logger = get_logger(__name__)

_loaded_models = {}

def load_whisper_model(user_id: str, model_type: str, language: Optional[str]) -> whisper.Whisper:
    model_path = None
    cache_key = None

    if model_type == "private":
        model_path = f"data/users/{user_id}/model"
        cache_key = f"private:{user_id}"

    elif model_type == "internal":
        if not language:
            raise ValueError("Language is required for internal model")
        model_path = f"data/internal/{language}/model"
        cache_key = f"internal:{language}"

    else:
        # Unknown or default fallback
        model_name = "small.en" if language == "en" else "small"
        logger.info(f"🌐 Using default Whisper model: '{model_name}'")
        return _load_cached_or_new_model(model_name, f"default:{model_name}")

    if not os.path.exists(model_path):
        logger.warning(f"❌ Model path not found: {model_path}")

        # Fallback only applies to internal/private
        fallback_model = "small.en" if language == "en" else "small"
        fallback_key = f"fallback:{fallback_model}"
        logger.info(f"☁️ Fallback to Whisper built-in: {fallback_model}")
        return _load_cached_or_new_model(fallback_model, fallback_key)

    logger.info(f"✅ Loaded model from: {model_path}")
    return _load_cached_or_new_model(model_path, cache_key)


def _load_cached_or_new_model(model_path_or_name: str, cache_key: str) -> whisper.Whisper:
    if cache_key in _loaded_models:
        logger.debug(f"🔁 Using cached model: {cache_key}")
        return _loaded_models[cache_key]

    model = whisper.load_model(model_path_or_name)
    _loaded_models[cache_key] = model
    return model

