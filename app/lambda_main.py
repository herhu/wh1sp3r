from fastapi import FastAPI, File, UploadFile, Form
from mangum import Mangum
import tempfile
from transcription.transcriber import transcribe_audio

app = FastAPI()

@app.post("/transcribe")
async def transcribe(
    user_id: str = Form(...),
    model_type: str = Form(...),
    language: str = Form(None),
    file: UploadFile = File(...)
):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        result = transcribe_audio(tmp_path, user_id, model_type, language)

        return {
            "text": result["text"],
            "language": result["language"],
            "slang_tokens": result.get("slang_tokens", []),
            "predicted_label": result.get("predicted_label", None)
        }

    except Exception as e:
        return {"error": str(e)}

handler = Mangum(app)