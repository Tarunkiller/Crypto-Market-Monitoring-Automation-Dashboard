from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router as api_router
from automation.scheduler import start_scheduler
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Crypto Market Monitoring API",
    description="Backend API for the Crypto Dashboard & RAG Agent",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up FastAPI application...")
    start_scheduler()
    logger.info("Scheduler started successfully.")

@app.get("/health")
def health_check():
    return {"status": "healthy"}
