import re
import sys
import os

def verify_lifelines(mermaid_code, root_path):
    """
    Checks if lifelines in Mermaid code (participants/actors) correlate to files/classes in codebase.
    """
    # Extract participants
    participants = re.findall(r'participant\s+(\w+)', mermaid_code)
    actors = re.findall(r'actor\s+(\w+)', mermaid_code)
    
    findings = []
    
    for p in participants:
        # Heuristic: Check for Service, Page, Controller naming
        if "Service" in p:
            # Check src/api/services/ and subdirectories
            found = False
            for root, dirs, files in os.walk(os.path.join(root_path, "src")):
                for file in files:
                    if p.lower().replace("service", "") in file.lower():
                        found = True
                        break
            findings.append(f"Lifeline {p}: {'✅ Found in src/' if found else '⚠️ Not verified (Manual check needed)'}")
        elif "Page" in p:
            findings.append(f"Lifeline {p}: ✅ UI Layer (Conceptual)")
        elif p == "Payload" or p == "DB":
            findings.append(f"Lifeline {p}: ✅ Core Infra")
        else:
            findings.append(f"Lifeline {p}: 🔍 Unknown layer (Check naming convention)")
            
    return findings

if __name__ == "__main__":
    # Mock execution for builder verification
    test_code = """
    sequenceDiagram
        actor User
        participant LoginPage
        participant AuthService
        participant Payload
    """
    print("\n--- Running Lifeline Verification ---")
    results = verify_lifelines(test_code, os.getcwd())
    for r in results:
        print(r)
