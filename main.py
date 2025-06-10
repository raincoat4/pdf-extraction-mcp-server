from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import tempfile
import fitz  # PyMuPDF

app = FastAPI()

@app.post("/extract")
async def extract_pdf(
    file: UploadFile = File(...),
    pages: str = Form(None)  # Optional string form input
):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        doc = fitz.open(tmp_path)

        # Parse page string like "1,2,-1"
        if pages:
            try:
                page_numbers = []
                for p in pages.split(','):
                    p = p.strip()
                    if p.startswith('-'):
                        page_numbers.append(len(doc) + int(p))
                    else:
                        page_numbers.append(int(p) - 1)
            except Exception:
                return JSONResponse(status_code=400, content={"error": "Invalid page numbers"})
        else:
            page_numbers = list(range(len(doc)))

        text = ""
        for i in page_numbers:
            if 0 <= i < len(doc):
                text += f"\n--- Page {i+1} ---\n"
                text += doc[i].get_text()

        return {"text": text.strip()}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
