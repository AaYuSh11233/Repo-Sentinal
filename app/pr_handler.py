from github import Github
from app.config import GITHUB_TOKEN
from app.checks import run_checks
from app.gemini import review_with_gemini
import logging

logger = logging.getLogger(__name__)
gh = Github(GITHUB_TOKEN)

async def handle_pr(payload):
    try:
        pr_data = payload["pull_request"]
        action = payload.get("action", "opened")
        repo_name = payload["repository"]["full_name"]
        
        # Only process newly opened PRs or synchronize events
        if action not in ["opened", "synchronize"]:
            logger.info(f"Skipping PR #{pr_data['number']} - action: {action}")
            return
        
        logger.info(f"Processing PR #{pr_data['number']} in {repo_name}")
        
        repo = gh.get_repo(repo_name)
        pr = repo.get_pull(pr_data["number"])

        # Check if PR should be closed (spam, unnecessary, etc.)
        if should_close_pr(pr.title, pr.body):
            logger.info(f"Closing PR #{pr_data['number']} - identified as spam/unnecessary")
            pr.create_issue_comment("🤖 **Auto-closing:** This PR appears to be spam or unnecessary. If this was closed in error, please reopen with more details.")
            pr.edit(state="closed")
            return

        branch = pr.head.ref
        clone_url = pr.head.repo.clone_url
        diff_url = pr.diff_url

        logger.info(f"Running checks for branch {branch}")
        checks_summary = run_checks(clone_url, branch)
        
        logger.info("Generating AI review")
        gemini_summary = review_with_gemini(diff_url)

        comment = "\n\n".join(checks_summary + [gemini_summary])

        logger.info("Posting comment to PR")
        pr.create_issue_comment(comment)
        pr.add_to_labels("needs-review")
        
        logger.info(f"Successfully processed PR #{pr_data['number']}")
        
    except Exception as e:
        logger.error(f"Error processing PR: {str(e)}")
        # Try to post error comment to PR
        try:
            pr_data = payload["pull_request"]
            repo_name = payload["repository"]["full_name"]
            repo = gh.get_repo(repo_name)
            pr = repo.get_pull(pr_data["number"])
            pr.create_issue_comment(f"❌ **Error processing PR:** {str(e)}")
        except:
            logger.error("Failed to post error comment to PR")

def should_close_pr(title, body):
    """Determine if a PR should be automatically closed"""
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
