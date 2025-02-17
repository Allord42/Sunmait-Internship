from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

# Load the summarization model
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-6-6")


class TextRequest(BaseModel):
    text: str


@app.get("/ping")
async def ping():
    return {"message": "200 OK"}


@app.post("/predict")
async def predict(request: TextRequest):
    try:
        summary = summarizer(
            request.text, max_length=130, min_length=30, do_sample=False
        )
        return {"summary": summary[0]["summary_text"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
