from fastapi import APIRouter

router = APIRouter(prefix="/api/system", tags=["system"])


@router.get("/status")
def system_status():
    return {
        "product": "IdX",
        "system": "decision-intelligence",
        "status": "operational",
    }
