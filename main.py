from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import fitz  #PyMuPDF

app = FastAPI()

@app.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        doc = fitz.open(stream=contents, filetype="pdf")
        full_text = ""
        for page in doc:
            full_text += page.get_text()

        return {
            "status": "success",
            "text": full_text.strip()
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})
