from app.pr_handler import handle_pr
from app.issue_handler import handle_issue
from app.discussion_handler import handle_discussion
from app.alerts_handler import handle_alerts
import logging

logger = logging.getLogger(__name__)

async def handle_event(event: str, payload: dict):
    try:
        logger.info(f"Handling {event} event")
        
        if event == "pull_request":
            await handle_pr(payload)
        elif event == "issues":
            await handle_issue(payload)
        elif event == "discussion":
            await handle_discussion(payload)
        elif event in ["code_scanning_alert", "secret_scanning_alert", "dependabot_alert"]:
            await handle_alerts(event, payload)
        else:
            logger.info(f"Unhandled event type: {event}")
            
    except Exception as e:
        logger.error(f"Error handling {event} event: {str(e)}")
        raise
