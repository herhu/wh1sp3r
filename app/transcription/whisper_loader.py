import os
from typing import Optional
import whisper

def load_whisper_model(user_id: str, model_type: str, language: Optional[str]):
    # Decide path
    if model_type == "private":
        model_path = f"data/users/{user_id}/model"
    elif model_type == "internal":
        if not language:
            raise ValueError("Language is required for internal model")
        model_path = f"data/internal/{language}/model"
    else:
        return whisper.load_model("small")

    # Fallback si no existe
    if not os.path.exists(model_path):
        print(f"[WARN] Model path not found: {model_path}. Using default 'small'.")
        return whisper.load_model("small")

    print(f"[INFO] Loaded Whisper model from: {model_path}")
    return whisper.load_model(model_path)
