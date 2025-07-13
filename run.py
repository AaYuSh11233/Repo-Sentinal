#!/usr/bin/env python3
"""
PR Sentinel - Startup Script
Run this to start the PR Sentinel bot
"""

import uvicorn
import os
import sys
from pathlib import Path

def main():
    """Start the PR Sentinel bot"""
    
    # Check if we're in the right directory
    if not Path("app").exists():
        print("❌ Error: Please run this script from the project root directory")
        sys.exit(1)
    
    # Check for .env file
    if not Path(".env").exists():
        print("⚠️  Warning: No .env file found. Make sure environment variables are set.")
    
    # Get configuration
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("RELOAD", "false").lower() == "true"
    
    print("🚀 Starting PR Sentinel...")
    print(f"📍 Host: {host}")
    print(f"🔌 Port: {port}")
    print(f"🔄 Reload: {reload}")
    
    # Start the server
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )

if __name__ == "__main__":
    main() 