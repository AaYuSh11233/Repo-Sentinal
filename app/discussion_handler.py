from github import Github
from app.config import GITHUB_TOKEN
from app.gemini import ai_reply
import logging
import requests

logger = logging.getLogger(__name__)
gh = Github(GITHUB_TOKEN)

async def handle_discussion(payload):
    try:
        discussion_data = payload["discussion"]
        action = payload.get("action", "created")
        repo_name = payload["repository"]["full_name"]
        
        # Only process newly created discussions
        if action != "created":
            logger.info(f"Skipping discussion #{discussion_data['number']} - action: {action}")
            return
        
        logger.info(f"Processing discussion #{discussion_data['number']} in {repo_name}")
        
        discussion_title = discussion_data.get("title", "No title")
        discussion_body = discussion_data.get("body", "")
        
        # Check if discussion should be closed (spam, unnecessary, etc.)
        if should_close_discussion(discussion_title, discussion_body):
            logger.info(f"Discussion #{discussion_data['number']} identified as spam - will be handled by repo admin")
            return
        
        # Combine title and body for AI analysis
        content = f"{discussion_title}\n\n{discussion_body}" if discussion_body else discussion_title
        
        logger.info("Generating AI reply")
        reply = ai_reply(content)

        # Comment on the discussion using GitHub API
        try:
            comment_url = f"https://api.github.com/repos/{repo_name}/discussions/{discussion_data['number']}/comments"
            headers = {
                "Authorization": f"token {GITHUB_TOKEN}",
                "Accept": "application/vnd.github.v3+json",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                comment_url,
                headers=headers,
                json={"body": reply},
                timeout=30
            )
            
            if response.status_code == 201:
                logger.info(f"Successfully commented on discussion #{discussion_data['number']}")
            else:
                logger.warning(f"Failed to comment on discussion: {response.status_code} - {response.text}")
                
        except Exception as e:
            logger.error(f"Error commenting on discussion: {str(e)}")
        
        logger.info(f"Successfully processed discussion #{discussion_data['number']}")
        
    except Exception as e:
        logger.error(f"Error processing discussion: {str(e)}")

def should_close_discussion(title, body):
    """Determine if a discussion should be flagged as spam"""
    if not title and not body:
        return True
    
    # Check for spam indicators
    spam_indicators = [
        "test", "xyz", "dummy", "spam", "unnecessary", "random",
        "asdf", "qwerty", "123", "abc", "hello world"
    ]
    
    content = f"{title} {body}".lower()
    
    # If title contains obvious spam indicators
    for indicator in spam_indicators:
        if indicator in content:
            return True
    
    # If content is too short or meaningless
    if len(content.strip()) < 10:
        return True
    
    # If it's just random characters
    if len(set(content.replace(" ", ""))) < 5:
        return True
    
    return False
