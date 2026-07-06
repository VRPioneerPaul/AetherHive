from fastapi import APIRouter

router = APIRouter(prefix="/twitch", tags=["twitch"])

@router.get("/status")
async def status():
    return {"status": "offline", "version": "1.0.0"}