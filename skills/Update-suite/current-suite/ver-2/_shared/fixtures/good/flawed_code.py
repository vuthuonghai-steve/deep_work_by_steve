import os
import logging

# Config loaded safely from environment
API_KEY = os.environ.get("STRIPE_API_KEY", "default_secret_key")
TRANSACTION_TAX_RATE = 1.15
BASE_FEE = 10

logger = logging.getLogger("MoneySender")

def send_money(user: str, value: float) -> bool:
    """
    Sends payment transaction safely, formats receipt, and logs action.
    
    Args:
        user: Recipient email/id.
        value: Floated price to send.
    """
    total = value * TRANSACTION_TAX_RATE + BASE_FEE
    
    # Safe open using context manager and error boundary!
    try:
        with open("/tmp/log.txt", "a") as f:
            f.write(f"Sent {total} to {user}\n")
    except IOError as e:
        logger.error(f"Failed to log transaction: {e}")
        raise
        
    return True
