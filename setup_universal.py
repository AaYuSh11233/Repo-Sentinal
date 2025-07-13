#!/usr/bin/env python3
"""
Universal PR Sentinel Setup Script
Helps configure the bot for handling all repositories automatically
"""

import os
import secrets
import requests
from pathlib import Path

def generate_webhook_secret():
    """Generate a secure webhook secret"""
    return secrets.token_urlsafe(32)

def check_github_token(token):
    """Test if GitHub token has required permissions"""
    try:
        headers = {"Authorization": f"token {token}"}
        response = requests.get("https://api.github.com/user", headers=headers)
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ GitHub token valid for user: {user_data['login']}")
            
            # Check repo permissions
            repo_response = requests.get("https://api.github.com/user/repos", headers=headers)
            if repo_response.status_code == 200:
                print("✅ Token has repository access")
                return True
            else:
                print("❌ Token missing repository permissions")
                return False
        else:
            print(f"❌ Invalid GitHub token: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing GitHub token: {str(e)}")
        return False

def check_gemini_key(key):
    """Test if Gemini API key is valid"""
    try:
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        headers = {"Content-Type": "application/json", "X-goog-api-key": key}
        payload = {
            "contents": [{"parts": [{"text": "Hello"}]}]
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 200:
            print("✅ Gemini API key is valid")
            return True
        else:
            print(f"❌ Invalid Gemini API key: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing Gemini API key: {str(e)}")
        return False

def create_env_file():
    """Create .env file with required variables"""
    print("\n🔧 Setting up environment variables...")
    
    # Check if .env already exists
    if Path(".env").exists():
        print("⚠️  .env file already exists. Backing up...")
        os.rename(".env", ".env.backup")
    
    # Get GitHub token
    github_token = input("Enter your GitHub Personal Access Token: ").strip()
    if not check_github_token(github_token):
        print("❌ Please provide a valid GitHub token with repo permissions")
        return False
    
    # Get Gemini API key
    gemini_key = input("Enter your Google Gemini API key: ").strip()
    if not check_gemini_key(gemini_key):
        print("❌ Please provide a valid Gemini API key")
        return False
    
    # Generate webhook secret
    webhook_secret = generate_webhook_secret()
    print(f"🔐 Generated webhook secret: {webhook_secret}")
    
    # Create .env file
    env_content = f"""# PR Sentinel Environment Variables
GITHUB_TOKEN={github_token}
WEBHOOK_SECRET={webhook_secret}
GEMINI_API_KEY={gemini_key}
HOST=0.0.0.0
PORT=8000
RELOAD=false
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    print("✅ .env file created successfully!")
    return True

def show_deployment_steps():
    """Show deployment steps"""
    print("\n" + "="*60)
    print("🚀 UNIVERSAL DEPLOYMENT STEPS")
    print("="*60)
    
    print("\n1️⃣ **Deploy to Cloud Platform:**")
    print("   • Railway: https://railway.app")
    print("   • Render: https://render.com")
    print("   • Or your own server")
    
    print("\n2️⃣ **Set Environment Variables in Platform:**")
    print("   Copy these from your .env file:")
    with open(".env", "r") as f:
        print(f.read())
    
    print("\n3️⃣ **Get Your Webhook URL:**")
    print("   • Railway: https://your-app.railway.app/webhook")
    print("   • Render: https://your-app.onrender.com/webhook")
    print("   • Custom: https://your-domain.com/webhook")
    
    print("\n4️⃣ **Configure Universal Webhook:**")
    print("   Option A - Organization Webhook:")
    print("   • Go to: https://github.com/organizations/YOUR_ORG/settings/hooks")
    print("   • Add webhook with your URL")
    print("   • Select: Pull requests, Issues, Discussions, Security alerts")
    
    print("\n   Option B - User Webhook:")
    print("   • Go to: https://github.com/settings/hooks")
    print("   • Add webhook with your URL")
    print("   • Select same events")
    
    print("\n5️⃣ **Test the Setup:**")
    print("   • Create an issue in any of your repos")
    print("   • Create a pull request")
    print("   • Check if bot responds automatically")
    
    print("\n" + "="*60)
    print("🎯 RESULT: Bot will handle ALL your repositories automatically!")
    print("="*60)

def main():
    """Main setup function"""
    print("🤖 PR Sentinel - Universal Repository Setup")
    print("="*50)
    
    # Check if we're in the right directory
    if not Path("app").exists():
        print("❌ Please run this script from the PR Sentinel project directory")
        return
    
    # Create environment file
    if not create_env_file():
        return
    
    # Show deployment steps
    show_deployment_steps()
    
    print("\n📋 **Next Steps:**")
    print("1. Deploy to your chosen platform")
    print("2. Configure the universal webhook")
    print("3. Test with your repositories")
    print("\n📖 For detailed instructions, see: DEPLOYMENT_GUIDE.md")

if __name__ == "__main__":
    main() 