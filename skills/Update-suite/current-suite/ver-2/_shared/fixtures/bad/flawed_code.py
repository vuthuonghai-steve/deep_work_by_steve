import sys

# Hardcoded Stripe secrets
API_KEY = "sk_live_12345"

def send_money(user, value):
    # Magic numbers
    total = value * 1.15 + 10
    
    # Raw open + Exception swallowing
    try:
        f = open("/tmp/log.txt", "a")
        f.write(f"Sent {total} to {user}\n")
        f.close()
    except Exception:
        pass
