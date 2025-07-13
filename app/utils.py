import hmac
import hashlib
import logging

logger = logging.getLogger(__name__)

def verify_signature(secret, body, signature_header):
    if not secret or not body or not signature_header:
        logger.warning("Missing required parameters for signature verification")
        return False
    
    try:
        expected_signature = "sha256=" + hmac.new(
            secret.encode(), body, hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected_signature, signature_header)
    except Exception as e:
        logger.error(f"Signature verification error: {str(e)}")
        return False
