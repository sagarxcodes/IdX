from fastapi import FastAPI
from app.api.system import router as system_router
from app.api.investigations import router as investigations_router

app = FastAPI(
    title="IdX",
    description="Evidence-driven decision intelligence platform",
    version="1.0.0",
)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "product": "IdX",
        "version": "1.0.0",
    }

app.include_router(system_router)

app.include_router(investigations_router)
