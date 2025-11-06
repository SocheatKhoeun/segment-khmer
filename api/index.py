from fastapi import FastAPI
from pydantic import BaseModel
from khmernltk import word_tokenize
import re


app = FastAPI()

class TextRequest(BaseModel):
    text: str

@app.post("/segment")
def segment_text(request: TextRequest):
    text = request.text.strip()
    
    # Detect Khmer text by Unicode range
    is_khmer = any('\u1780' <= ch <= '\u17FF' for ch in text)
    
    if is_khmer:
        tokens = word_tokenize(text, return_tokens=True)
    else:
        # Split English text on spaces, remove punctuation
        tokens = re.findall(r"\b\w+\b", text)
    
    tokens = [t for t in tokens if t.strip()]
    total_words = len(tokens)
    return {
        # "total_words": total_words,
        "tokens": tokens
    }
