from fastapi import FastAPI

from .routes import twitch, discord

app = FastAPI()

app.include_router(twitch.router)
app.include_router(discord.router)

@app.get("/health")
async def health():
    return {'status': 'running', 'version': '1.0.0'}

health = {health() + discord.status() + twitch.status()}