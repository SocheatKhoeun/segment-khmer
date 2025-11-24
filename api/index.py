from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import re

app = FastAPI()

class TextRequest(BaseModel):
    text: str

# CRITICAL FIX: Never import khmernltk at the top!
# Only import inside the function when needed
def get_khmer_tokens(text: str):
    try:
        from khmernltk import word_tokenize
        words = word_tokenize(text, return_tokens=True)
        tokens = []
        for w in words:
            subs = re.findall(r"[\u1780-\u17FF]+|[A-Za-z]+|\d+|[។៕៚.,!?;:]|[ \n\t]+", w)
            tokens.extend([t for t in subs if t])
        return tokens
    except:
        pass  # fall back to regex
    return re.findall(r"[\u1780-\u17FF]+|[A-Za-z]+|\d+|[។៕៚.,!?;:]|[ \n\t]+", text)

@app.post("/segment")
async def segment_text(request: TextRequest):
    text = request.text
    
    if not text:
        return {"tokens": []}

    # Detect Khmer
    has_khmer = any('\u1780' <= c <= '\u17FF' for c in text)
    
    if has_khmer:
        tokens = get_khmer_tokens(text)
    else:
        tokens = re.findall(r"[A-Za-z]+|\d+|[.,!?;:]|[ \n\t]+", text)

    # Keep spaces, newlines, everything
    tokens = [t for t in tokens if t != ""]
    
    return {"tokens": tokens}

@app.get("/")
def health():
    return {"status": "Khmer segmentation API ready", "time": "2025"}