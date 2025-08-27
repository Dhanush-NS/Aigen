# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from backend.routers import image, dashboard, search, auth
from backend.mcp_clients import init_mcp_clients, cleanup_mcp_clients
from backend.database import engine, Base

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    # Startup
    logger.info("Starting up AI-Gen application...")
    
    # Create database tables
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created/verified")
    except Exception as e:
        logger.error(f"Database setup failed: {e}")
    
    # Initialize MCP clients
    try:
        mcp_success = await init_mcp_clients()
        if mcp_success:
            logger.info("MCP clients initialized successfully")
        else:
            logger.warning("Some MCP clients failed to initialize, fallback methods will be used")
    except Exception as e:
        logger.error(f"MCP client initialization failed: {e}")
    
    logger.info("Application startup complete")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    try:
        await cleanup_mcp_clients()
        logger.info("MCP clients cleaned up")
    except Exception as e:
        logger.error(f"MCP cleanup failed: {e}")
    
    logger.info("Application shutdown complete")

# Create FastAPI app with lifespan management
app = FastAPI(
    title="AI-Gen API",
    description="AI-powered content and image explorer with MCP integration",
    version="1.0.0",
    lifespan=lifespan
)

# CORS setup
origins = [
    "http://localhost:5173",  # Vite dev server
    "http://localhost:3000",  # Alternative React dev server
    "https://your-domain.com",  # Production domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/", tags=["health"])
async def root():
    return {
        "message": "AI-Gen API is running",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint for monitoring"""
    from backend.mcp_clients import search_client, image_client
    
    return {
        "status": "healthy",
        "services": {
            "database": "connected",  # Could add actual DB health check
            "mcp_search": "connected" if search_client.session else "disconnected",
            "mcp_image": "connected" if image_client.session else "disconnected",
        }
    }

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(search.router, prefix="/search", tags=["Search"])
app.include_router(image.router, prefix="/image", tags=["Image Generation"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)