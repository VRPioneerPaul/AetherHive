from fastapi import APIRouter

router = APIRouter(prefix="/discord", tags=["discord"])

@router.get("/status")
async def status():
    return {"status": "offline", "version": "1.0.0"}