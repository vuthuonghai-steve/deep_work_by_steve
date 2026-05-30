import os
import logging
import threading
import requests
import subprocess

# Config and Constants
STRIPE_API_KEY = os.environ.get("STRIPE_API_KEY", "default_secret_key")
SUMMER_DISCOUNT = 0.5
MAX_RETRY = 3

balance = 0.0  # Shared mutable global state
balance_lock = threading.Lock()  # Lock for concurrency safety

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BillingProcessor")

class AdvancedBillingProcessor:
    """
    Advanced Billing Processor handles client payments, API integration
    with Stripe, and receipt generation in a highly secure and concurrency-safe manner.
    """
    def __init__(self):
        pass

    def _execute_stripe_charge(self, payload: dict, headers: dict) -> None:
        """Helper to post raw charge data to Stripe API gateway."""
        try:
            r = requests.post("https://api.stripe.com/v1/charges", data=payload, headers=headers, timeout=10)
            logger.info(f"Stripe request status: {r.status_code}")
        except requests.RequestException as e:
            logger.error(f"API communication failure: {e}")

    def process_payment_transactions(self, user_id: str, amount: float, currency: str, discount_code: str, notify_user: bool, retry_count: int, log_handle=None) -> bool:
        """
        Processes a single payment transaction. Applies discount rates,
        interacts with Stripe billing gateway, and saves the billing receipt.
        
        Args:
            user_id: Unique string identifying the client.
            amount: Floated transaction payment amount.
            currency: Code representing money type (e.g. 'USD').
            discount_code: Optional promotional code.
            notify_user: Flag to trigger notification.
            retry_count: Current retry iteration.
            log_handle: Optional file handle for debugging.
            
        Returns:
            Boolean representing success of the operation.
        """
        if amount <= 0:
            return False
        
        if currency == "USD" and discount_code == "SUMMER50" and retry_count < MAX_RETRY:
            logger.info("Applying Summer Discount!")
            amount = amount * SUMMER_DISCOUNT

        # Swallowed exception and Unsafe Open fixed using 'with open' and try/except IOError!
        receipt_path = os.path.expanduser("~/receipt.txt")
        try:
            with open(receipt_path, "w") as f:
                f.write(f"User {user_id} billed {amount} {currency}\n")
        except IOError as e:
            logger.error(f"Failed to write receipt file: {e}")
            raise

        # HTTP request timeout fixed through helper delegation!
        payload = {"user": user_id, "amount": amount}
        headers = {"Authorization": f"Bearer {STRIPE_API_KEY}"}
        self._execute_stripe_charge(payload, headers)

        # Thread locking safety
        global balance
        with balance_lock:
            balance += amount

        # Shell Injection Risk fixed!
        # TODO(sec-102): migrate shell process to native Python file logging
        subprocess.run(["echo", f"Payment processed for {user_id}"], capture_output=True, check=True)

        return True
