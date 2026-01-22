from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import os

TESSERACT_CMD = os.getenv("TESSERACT_CMD")
if TESSERACT_CMD:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD


def ocr_extract(path: str) -> dict:
    """Extract text plus token-level confidences from a PDF or image path.

    Returns a dict with:
      - raw_text: full concatenated OCR text
      - tokens: list of {text, conf (0-1), bbox: [left,top,width,height], page}
    """
    raw_chunks = []
    tokens = []
    lower = path.lower()
    try:
        if lower.endswith(".pdf"):
            images = convert_from_path(path)
            pages = images
        else:
            pages = [Image.open(path)]

        for p_index, img in enumerate(pages, start=1):
            page_text = pytesseract.image_to_string(img)
            raw_chunks.append(page_text)

            # get detailed word-level data
            try:
                data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
                n = len(data.get("text", []))
                for i in range(n):
                    text = (data.get("text", [])[i] or "").strip()
                    if not text:
                        continue
                    conf_raw = data.get("conf", [])[i]
                    try:
                        conf = float(conf_raw)
                    except Exception:
                        conf = -1.0
                    # Normalize to 0-1, treat -1 or negative as 0.0
                    conf = max(0.0, min(1.0, conf / 100.0))
                    left = int(data.get("left", [])[i] or 0)
                    top = int(data.get("top", [])[i] or 0)
                    width = int(data.get("width", [])[i] or 0)
                    height = int(data.get("height", [])[i] or 0)
                    tokens.append({
                        "text": text,
                        "conf": conf,
                        "bbox": [left, top, width, height],
                        "page": p_index,
                    })
            except Exception:
                # best-effort: if data extraction fails, skip token details
                pass

    except Exception:
        raise

    return {"raw_text": "\n".join(raw_chunks), "tokens": tokens}
