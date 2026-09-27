from fastapi import FastAPI
from sqlalchemy import text
 
from app.db.session import engine
from app.routers import auth, trainees, jobs, applications, employment, analytics
 
app = FastAPI(title="SIH26135 Backend", version="0.1.0")
app.include_router(auth.router)
app.include_router(trainees.router)
app.include_router(jobs.router)
app.include_router(applications.router)
app.include_router(employment.router)
app.include_router(analytics.router)
 
 
@app.get("/health")
def health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db = "ok"
    except Exception as exc:  # noqa: BLE001
        db = f"error: {exc.__class__.__name__}"
    return {"status": "ok", "database": db}