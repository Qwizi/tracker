import json
import httpx
from pathlib import Path
from fastapi import Depends, FastAPI, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel


app = FastAPI()


class TrackQuery(BaseModel):
    topic: str | None = Query(description="Channel", default="task3-dsw")
    message: str | None = Query(description="Data", default="Ktoś otworzył dokument!")


async def notify(topic: str, message: str):
    url = "https://ntfy.sh"
    async with httpx.AsyncClient() as client:
        r = await client.post(url, data=json.dumps({"topic": topic, "message": message}))
        data = r.json()
        print(data)
        return r


@app.get("/image.png")
async def track(query: TrackQuery = Depends()):
    image_path = Path("image.png")
    print(image_path)
    if not image_path.exists():
        return {"message": "No tracking available"}
    response = await notify(query.topic, query.message)
    print(response)
    return FileResponse(image_path)
