"""
Stock Saarthi - Main FastAPI Application
This is the entry point for the backend server.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Import routers
from api.routes import stocks, predictions, news, users, watchlist

# Import database
from database.models import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and shutdown events for the application.
    """
    # Startup: Create database tables
    print("🚀 Starting Stock Saarthi...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")
    yield
    # Shutdown
    print("👋 Shutting down Stock Saarthi...")


# Create FastAPI app
app = FastAPI(
    title="Stock Saarthi API",
    description="AI-Powered Stock Analysis Platform for Beginner Investors",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS (allows frontend to communicate with backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_origin_regex=r"http://localhost(:\\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(stocks.router, prefix="/api/stocks", tags=["Stocks"])
app.include_router(predictions.router, prefix="/api/predictions", tags=["Predictions"])
app.include_router(news.router, prefix="/api/news", tags=["News"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(watchlist.router, prefix="/api/watchlist", tags=["Watchlist"])


@app.get("/")
async def root():
    """
    Root endpoint - Health check
    """
    return {
        "message": "Welcome to Stock Saarthi API",
        "status": "healthy",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring
    """
    return {"status": "healthy"}


# Run with: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
