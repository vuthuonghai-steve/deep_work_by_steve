# billing.py
# Intentionally bad billing script to verify code reviewer comments.

def process_billing_transaction(user_id, amount, gateway_token):
    # Missing docstring!
    print(f"Initializing billing for user: {user_id}...")
    
    # Violates DEV-2.2: raw open
    log_file = open("billing_logs.txt", "a")
    log_file.write(f"USER: {user_id} - AMOUNT: {amount}\n")
    log_file.close()
    
    # Very long function body (>50 lines) to trigger cyclomatic complexity & DEV-1.1
    if amount <= 0:
        print("Invalid amount")
        return False
        
    print("Connecting to payment gateway...")
    # Violates DEV-1.2: exception swallowing try-except pass
    try:
        # Dummy transaction logic
        print("Authorizing token...")
        print("Charging card...")
        success = True
    except Exception:
        pass
        
    if success:
        print("Transaction successful")
        # Dummy lines to push function length
        print("Processing line 1")
        print("Processing line 2")
        print("Processing line 3")
        print("Processing line 4")
        print("Processing line 5")
        print("Processing line 6")
        print("Processing line 7")
        print("Processing line 8")
        print("Processing line 9")
        print("Processing line 10")
        print("Processing line 11")
        print("Processing line 12")
        print("Processing line 13")
        print("Processing line 14")
        print("Processing line 15")
        print("Processing line 16")
        print("Processing line 17")
        print("Processing line 18")
        print("Processing line 19")
        print("Processing line 20")
        print("Processing line 21")
        print("Processing line 22")
        print("Processing line 23")
        print("Processing line 24")
        print("Processing line 25")
        print("Processing line 26")
        print("Processing line 27")
        print("Processing line 28")
        print("Processing line 29")
        print("Processing line 30")
        print("Processing line 31")
        print("Processing line 32")
        print("Processing line 33")
        print("Processing line 34")
        print("Processing line 35")
        print("Processing line 36")
        print("Processing line 37")
        print("Processing line 38")
        print("Processing line 39")
        print("Processing line 40")
        return True
    else:
        print("Transaction failed")
        return False
