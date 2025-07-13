#!/usr/bin/env python3
"""
Test script for PR Sentinel
Simulates GitHub webhook events for testing
"""

import requests
import json
import hmac
import hashlib
import os
from datetime import datetime

# Configuration
WEBHOOK_URL = "http://localhost:8000/webhook"
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "test_secret")

def create_signature(body, secret):
    """Create HMAC signature for webhook verification"""
    return "sha256=" + hmac.new(
        secret.encode(), body, hashlib.sha256
    ).hexdigest()

def send_test_webhook(event_type, payload):
    """Send a test webhook to the bot"""
    body = json.dumps(payload).encode()
    signature = create_signature(body, WEBHOOK_SECRET)
    
    headers = {
        "Content-Type": "application/json",
        "X-GitHub-Event": event_type,
        "X-Hub-Signature-256": signature
    }
    
    try:
        response = requests.post(WEBHOOK_URL, data=body, headers=headers)
        print(f"✅ {event_type} webhook sent - Status: {response.status_code}")
        if response.status_code != 200:
            print(f"Response: {response.text}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print(f"❌ Failed to connect to {WEBHOOK_URL}")
        print("Make sure the bot is running with: python run.py")
        return False

def test_issue_webhook():
    """Test issue creation webhook"""
    payload = {
        "action": "opened",
        "issue": {
            "number": 123,
            "title": "Test Issue - Please help with feature",
            "body": "I'm trying to implement a new feature but I'm having trouble with the authentication flow. Can someone help me understand how to properly handle user sessions?",
            "user": {"login": "testuser"},
            "labels": []
        },
        "repository": {
            "full_name": "your-username/your-repo",
            "name": "your-repo"
        }
    }
    return send_test_webhook("issues", payload)

def test_pr_webhook():
    """Test pull request webhook"""
    payload = {
        "action": "opened",
        "pull_request": {
            "number": 456,
            "title": "Add new authentication feature",
            "body": "This PR adds a new authentication system with JWT tokens and proper session management.",
            "user": {"login": "testuser"},
            "head": {
                "ref": "feature/auth",
                "repo": {
                    "clone_url": "https://github.com/your-username/your-repo.git"
                }
            },
            "diff_url": "https://api.github.com/repos/your-username/your-repo/pulls/456.diff"
        },
        "repository": {
            "full_name": "your-username/your-repo",
            "name": "your-repo"
        }
    }
    return send_test_webhook("pull_request", payload)

def test_discussion_webhook():
    """Test discussion webhook"""
    payload = {
        "action": "created",
        "discussion": {
            "number": 789,
            "title": "Best practices for API design",
            "body": "What are the best practices for designing REST APIs? I'm working on a new project and want to make sure I follow industry standards.",
            "user": {"login": "testuser"}
        },
        "repository": {
            "full_name": "your-username/your-repo",
            "name": "your-repo"
        }
    }
    return send_test_webhook("discussion", payload)

def test_security_alert_webhook():
    """Test security alert webhook"""
    payload = {
        "action": "created",
        "alert": {
            "number": 1,
            "severity": "high",
            "state": "open",
            "created_at": datetime.now().isoformat()
        },
        "repository": {
            "full_name": "your-username/your-repo",
            "name": "your-repo"
        }
    }
    return send_test_webhook("code_scanning_alert", payload)

def main():
    """Run all tests"""
    print("🧪 Testing PR Sentinel Bot")
    print("=" * 40)
    
    # Test health endpoint first
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ Bot is running and healthy")
        else:
            print("❌ Bot health check failed")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Bot is not running. Start it with: python run.py")
        return
    
    print("\n📝 Testing Issue Webhook...")
    test_issue_webhook()
    
    print("\n🔀 Testing Pull Request Webhook...")
    test_pr_webhook()
    
    print("\n💬 Testing Discussion Webhook...")
    test_discussion_webhook()
    
    print("\n🚨 Testing Security Alert Webhook...")
    test_security_alert_webhook()
    
    print("\n✅ All tests completed!")
    print("\n📋 Next steps:")
    print("1. Check your GitHub repository for new issues/comments")
    print("2. Verify that the bot responded appropriately")
    print("3. Check the bot logs for any errors")

if __name__ == "__main__":
    main() 