from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
import pdfplumber
from pypdf import PdfReader, PdfWriter
import io
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="PDF Page Extractor API")

TARGET_TITLES = [
    "POWER OF ATTORNEY",
    "TITLE AND REGISTRATION APPLICATION",
    "ODOMETER DISCLOSURE"
]

@app.get("/")
def root():
    return {"status": "running", "message": "PDF Extractor API is live!"}

@app.post("/extract-pages")
async def extract_pages(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    # Read uploaded PDF into memory
    pdf_bytes = await file.read()
    input_stream = io.BytesIO(pdf_bytes)

    matching_pages = []

    # Scan each page for target titles
    with pdfplumber.open(input_stream) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            lines = [line.strip() for line in text.strip().split("\n") if line.strip()]
            title_area = " ".join(lines[:5]).upper()

            for title in TARGET_TITLES:
                if title in title_area:
                    matching_pages.append(i)
                    logger.info(f"Page {i+1} matched: '{title}'")
                    break

    if not matching_pages:
        raise HTTPException(status_code=404, detail="No matching pages found for the given titles.")

    # Extract matched pages preserving exact format
    input_stream.seek(0)
    reader = PdfReader(input_stream)
    writer = PdfWriter()

    for page_num in matching_pages:
        writer.add_page(reader.pages[page_num])

    # Write output to memory
    output_stream = io.BytesIO()
    writer.write(output_stream)
    output_stream.seek(0)

    logger.info(f"Extracted {len(matching_pages)} pages: {[p+1 for p in matching_pages]}")

    return StreamingResponse(
        output_stream,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=extracted_pages.pdf",
            "X-Matched-Pages": str([p+1 for p in matching_pages])
        }
    )
