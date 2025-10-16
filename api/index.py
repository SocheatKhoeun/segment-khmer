from fastapi import FastAPI
from pydantic import BaseModel
from khmernltk import word_tokenize

app = FastAPI()

# Request model
class TextRequest(BaseModel):
    text: str

# Endpoint for Khmer word segmentation
@app.post("/segment")
def segment_text(request: TextRequest):
    tokens = word_tokenize(request.text, return_tokens=True)
    total_words = len(tokens)
    return {
        "total_words": total_words,
        "tokens": tokens
    }
