from fastapi import FastAPI
from pydantic import BaseModel
from khmernltk import word_tokenize
import re

app = FastAPI()

class TextRequest(BaseModel):
    text: str

@app.post("/segment")
def segment_text(request: TextRequest):
    text = request.text

    # Detect if the text contains Khmer
    is_khmer = any('\u1780' <= ch <= '\u17FF' for ch in text)

    if is_khmer:
        # Khmer segmentation first
        words = word_tokenize(text, return_tokens=True)

        tokens = []
        for w in words:
            # Support Khmer letters, English letters, digits, punctuation, spaces
            sub_tokens = re.findall(
                r"[\u1780-\u17FF]+|[A-Za-z]+|\d+|[។៕៚.,!?;:]| +",
                w
            )
            tokens.extend(sub_tokens)
    else:
        # Pure English fallback
        tokens = re.findall(
            r"[A-Za-z]+|\d+|[.,!?;:]| +",
            text
        )

    return {"tokens": tokens}
