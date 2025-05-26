import sys
import os
import tempfile
import traceback
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form
from mangum import Mangum

# 🧠 Configure cache and home to /tmp to avoid read-only filesystem issues
os.environ["XDG_CACHE_HOME"] = "/tmp"
os.environ["TRANSFORMERS_CACHE"] = "/tmp"
os.environ["HF_HOME"] = "/tmp"
os.environ["TORCH_HOME"] = "/tmp"

# 🔍 Debug system paths and directory structure
APP_PATH = os.path.join(os.path.dirname(__file__), "app")
print(f"🔍 Adding to sys.path: {APP_PATH}")
sys.path.insert(0, APP_PATH)

print(f"🔍 sys.path = {sys.path}")
print(f"📂 Current working directory: {os.getcwd()}")
print(f"📁 CWD contents: {os.listdir('.')}")
print(f"📁 /var/task contents: {os.listdir('/var/task')}")
print(f"📁 /tmp contents: {os.listdir('/tmp')}")
print(f"📁 App folder: {os.listdir('./app') if os.path.exists('./app') else '❌ Missing /app'}")

# 🧠 Import model logic
try:
    from transcription.transcriber import transcribe_audio
    print("✅ transcribe_audio imported successfully")
except Exception as e:
    print(f"❌ Failed to import transcribe_audio:\n{traceback.format_exc()}")

app = FastAPI()

@app.post("/transcribe")
async def transcribe(
    user_id: Optional[str] = Form(None),
    model_type: Optional[str] = Form(None),
    language: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    ping: Optional[bool] = Form(False)
):
    print(f"📩 Request received: ping={ping}, user_id={user_id}, model_type={model_type}, language={language}")
    
    if ping:
        return {"status": "🔥 Lambda is warm and ready!"}

    if not user_id or not model_type or not file:
        print("⚠️ Missing required fields")
        return {"error": "Missing required fields: user_id, model_type, or file"}

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
            print(f"📁 Saved uploaded file to: {tmp_path} ({len(content)} bytes)")

        print(f"🎙️ Calling transcribe_audio on: {tmp_path}")
        result = transcribe_audio(tmp_path, user_id, model_type, language)
        print(f"✅ Transcription output: {result}")

        if "error" in result:
            raise Exception(result["error"])

        return {
            "text": result["text"],
            "language": result.get("language", "und"),
            "slang_tokens": result.get("slang_tokens", []),
            "predicted_label": result.get("predicted_label", None)
        }

    except Exception as e:
        print(f"❌ Exception during transcription:\n{traceback.format_exc()}")
        return {"error": str(e)}

handler = Mangum(app)
print("🚀 Lambda handler initialized.")
