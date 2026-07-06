from fastapi import FastAPI

from .routes import twitch, discord

app = FastAPI()

app.include_router(twitch.router)
app.include_router(discord.router)

@app.get("/health")
async def health():
    return {
        "discord_status": await discord.status(),
        "twitch_status": await twitch.status(),
        "overall_status": "healthy"
        }