from app.config import GEMINI_API_KEY, GEMINI_URL
import requests
import logging

logger = logging.getLogger(__name__)

def review_with_gemini(diff_url):
    try:
        # Fetch diff content
        diff_response = requests.get(diff_url, timeout=30)
        diff_response.raise_for_status()
        diff_text = diff_response.text
        
        if not diff_text.strip():
            return "🤖 **Gemini AI Review:** No diff content found to review."
        
        payload = {
            "contents": [
                {"parts": [{"text": f"Review this PR diff for style, security, and quality:\n{diff_text}"}]}
            ]
        }
        
        resp = requests.post(
            GEMINI_URL,
            headers={"Content-Type": "application/json", "X-goog-api-key": GEMINI_API_KEY},
            json=payload,
            timeout=60
        )
        resp.raise_for_status()
        
        data = resp.json()
        
        if "candidates" not in data or not data["candidates"]:
            return "🤖 **Gemini AI Review:** Unable to generate review at this time."
            
        review_text = data["candidates"][0]["content"]["parts"][0]["text"]
        return "🤖 **Gemini AI Review:**\n" + review_text
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Gemini API request error: {str(e)}")
        return "🤖 **Gemini AI Review:** Unable to connect to AI service. Please try again later."
    except KeyError as e:
        logger.error(f"Unexpected Gemini API response format: {str(e)}")
        return "🤖 **Gemini AI Review:** Received unexpected response from AI service."
    except Exception as e:
        logger.error(f"Gemini review error: {str(e)}")
        return "🤖 **Gemini AI Review:** An error occurred while generating the review."

def ai_reply(text):
    try:
        if not text or not text.strip():
            return "🤖 **Gemini AI Reply:** No content provided to respond to."
            
        payload = {
            "contents": [
                {"parts": [{"text": f"Reply to the following GitHub Issue/Discussion:\n{text}"}]}
            ]
        }
        
        resp = requests.post(
            GEMINI_URL,
            headers={"Content-Type": "application/json", "X-goog-api-key": GEMINI_API_KEY},
            json=payload,
            timeout=60
        )
        resp.raise_for_status()
        
        data = resp.json()
        
        if "candidates" not in data or not data["candidates"]:
            return "🤖 **Gemini AI Reply:** Unable to generate reply at this time."
            
        reply_text = data["candidates"][0]["content"]["parts"][0]["text"]
        return "🤖 **Gemini AI Reply:**\n" + reply_text
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Gemini API request error: {str(e)}")
        return "🤖 **Gemini AI Reply:** Unable to connect to AI service. Please try again later."
    except KeyError as e:
        logger.error(f"Unexpected Gemini API response format: {str(e)}")
        return "🤖 **Gemini AI Reply:** Received unexpected response from AI service."
    except Exception as e:
        logger.error(f"Gemini reply error: {str(e)}")
        return "🤖 **Gemini AI Reply:** An error occurred while generating the reply."
