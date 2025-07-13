from dotenv import load_dotenv
import os
import logging

load_dotenv()

logger = logging.getLogger(__name__)

# Required environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Validate required environment variables
if not GITHUB_TOKEN:
    logger.error("GITHUB_TOKEN environment variable is required")
    raise ValueError("GITHUB_TOKEN environment variable is required")

if not WEBHOOK_SECRET:
    logger.error("WEBHOOK_SECRET environment variable is required")
    raise ValueError("WEBHOOK_SECRET environment variable is required")

if not GEMINI_API_KEY:
    logger.error("GEMINI_API_KEY environment variable is required")
    raise ValueError("GEMINI_API_KEY environment variable is required")

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
)
