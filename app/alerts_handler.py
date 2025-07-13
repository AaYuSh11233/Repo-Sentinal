from github import Github
from app.config import GITHUB_TOKEN
import logging

logger = logging.getLogger(__name__)
gh = Github(GITHUB_TOKEN)

async def handle_alerts(event: str, payload: dict):
    try:
        repo_name = payload["repository"]["full_name"]
        
        logger.info(f"Processing {event} alert in {repo_name}")
        
        repo = gh.get_repo(repo_name)
        title = f"{event.replace('_', ' ').title()} detected"
        
        # Extract relevant information without exposing sensitive data
        alert_info = {
            "alert_type": event,
            "repository": repo_name,
            "timestamp": payload.get("created_at", "Unknown"),
            "severity": payload.get("alert", {}).get("severity", "Unknown"),
            "state": payload.get("alert", {}).get("state", "Unknown")
        }
        
        body = f"""## Security Alert Detected

**Alert Type:** {alert_info['alert_type']}
**Repository:** {alert_info['repository']}
**Severity:** {alert_info['severity']}
**State:** {alert_info['state']}
**Timestamp:** {alert_info['timestamp']}

Please review this security alert and take appropriate action."""
        
        logger.info("Creating security issue")
        issue = repo.create_issue(title=title, body=body, labels=["security"])
        
        logger.info(f"Successfully created security issue #{issue.number}")
        
    except Exception as e:
        logger.error(f"Error processing alert: {str(e)}")
        # Try to create issue with error message
        try:
            repo_name = payload["repository"]["full_name"]
            repo = gh.get_repo(repo_name)
            repo.create_issue(
                title="Alert Processing Error",
                body=f"Error processing {event} alert: {str(e)}",
                labels=["security", "error"]
            )
        except:
            logger.error("Failed to create error issue for alert")
