from fastapi import FastAPI
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

app = FastAPI()

@app.get("/")
def root():
    return {
        "message": "API is live. Use /get-transcript?youtube_url=..."
    }

@app.get("/get-transcript")
def get_transcript(youtube_url: str):
    try:
        video_id = parse_qs(urlparse(youtube_url).query).get("v")
        if not video_id:
            return {"error": "Invalid YouTube URL"}
        transcript_raw = YouTubeTranscriptApi.get_transcript(video_id[0])
        full_text = " ".join([entry["text"].strip() for entry in transcript_raw])
        cleaned = full_text.replace("\n", " ").replace("  ", " ").strip()
        return {"transcript": cleaned}
    except Exception as e:
        return {"error": str(e)}
import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
