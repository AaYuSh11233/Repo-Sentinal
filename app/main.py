from fastapi import FastAPI, Request, Header, HTTPException
from app.config import WEBHOOK_SECRET
from app.utils import verify_signature
from app.github import handle_event
import logging
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI(title="PR Sentinel", description="Repository Assistant Manager Bot")

@app.on_event("startup")
async def startup_event():
    """Validate configuration on startup"""
    try:
        from app.config import GITHUB_TOKEN, WEBHOOK_SECRET, GEMINI_API_KEY
        logger.info("✅ Configuration validated successfully")
        logger.info("🚀 PR Sentinel is ready to receive webhooks!")
    except ValueError as e:
        logger.error(f"❌ Configuration error: {e}")
        sys.exit(1)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "PR Sentinel"}

@app.get("/")
async def root():
    """Root endpoint with basic info"""
    return {
        "service": "PR Sentinel",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "webhook": "/webhook"
        }
    }

@app.post("/webhook")
async def webhook(request: Request, x_hub_signature_256: str = Header(None)):
    try:
        body = await request.body()
        
        # Validate signature
        if not x_hub_signature_256:
            logger.warning("Missing signature header")
            raise HTTPException(status_code=401, detail="Missing signature")
            
        if not verify_signature(WEBHOOK_SECRET, body, x_hub_signature_256):
            logger.warning("Invalid signature")
            raise HTTPException(status_code=401, detail="Invalid signature")

        payload = await request.json()
        event = request.headers.get("x-github-event")
        
        if not event:
            logger.warning("Missing GitHub event header")
            raise HTTPException(status_code=400, detail="Missing GitHub event")

        logger.info(f"Processing {event} event")
        await handle_event(event, payload)

        return {"status": "ok"}
        
    except Exception as e:
        logger.error(f"Webhook processing error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
