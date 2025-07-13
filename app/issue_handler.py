from github import Github
from app.config import GITHUB_TOKEN
from app.gemini import ai_reply
import logging

logger = logging.getLogger(__name__)
gh = Github(GITHUB_TOKEN)

async def handle_issue(payload):
    try:
        issue_data = payload["issue"]
        action = payload.get("action", "opened")
        repo_name = payload["repository"]["full_name"]
        
        # Only process newly opened issues
        if action != "opened":
            logger.info(f"Skipping issue #{issue_data['number']} - action: {action}")
            return
        
        logger.info(f"Processing issue #{issue_data['number']} in {repo_name}")
        
        repo = gh.get_repo(repo_name)
        issue = repo.get_issue(issue_data["number"])

        # Combine title and body for AI analysis
        content = f"{issue.title}\n\n{issue.body}" if issue.body else issue.title
        
        logger.info("Generating AI reply")
        reply = ai_reply(content)

        logger.info("Posting comment to issue")
        issue.create_comment(reply)
        
        # Check if issue should be closed (spam, unnecessary, etc.)
        if should_close_issue(issue.title, issue.body):
            logger.info(f"Closing issue #{issue_data['number']} - identified as spam/unnecessary")
            issue.create_comment("🤖 **Auto-closing:** This issue appears to be spam or unnecessary. If this was closed in error, please reopen with more details.")
            issue.edit(state="closed")
        else:
            issue.add_to_labels("triage")
        
        logger.info(f"Successfully processed issue #{issue_data['number']}")
        
    except Exception as e:
        logger.error(f"Error processing issue: {str(e)}")
        # Try to post error comment to issue
        try:
            issue_data = payload["issue"]
            repo_name = payload["repository"]["full_name"]
            repo = gh.get_repo(repo_name)
            issue = repo.get_issue(issue_data["number"])
            issue.create_comment(f"❌ **Error processing issue:** {str(e)}")
        except:
            logger.error("Failed to post error comment to issue")

def should_close_issue(title, body):
    """Determine if an issue should be automatically closed"""
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
