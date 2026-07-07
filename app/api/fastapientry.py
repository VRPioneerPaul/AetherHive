from fastapi import FastAPI

from app.api.state import state 

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health():
    return {
        "discord_status": state.discord_online,
        "twitch_status": state.twitch_online,
        "overall_status": state.overall_online
        }