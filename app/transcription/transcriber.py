from typing import Optional
from transcription.whisper_loader import load_whisper_model

# Cache global
_model_cache = {}

def transcribe_audio(audio_path: str, user_id: str, model_type: str, language: Optional[str]) -> dict:
    try:
        key = f"{user_id}:{model_type}:{language or 'none'}"

        if key in _model_cache:
            model = _model_cache[key]
        else:
            model = load_whisper_model(user_id, model_type, language)
            _model_cache[key] = model

        result = model.transcribe(audio_path, fp16=False)

        return {
            "text": result["text"],
            "language": result.get("language"),
            "segments": result.get("segments", []),
        }
    except Exception as e:
        return {
            "error": f"Transcription failed: {str(e)}"
        }
