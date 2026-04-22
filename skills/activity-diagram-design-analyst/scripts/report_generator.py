import sys

def generate_report(findings, output_path):
    """
    Tao bao cao Findings tu danh sach loi phat hien duoc.
    """
    with open(output_path, 'w') as f:
        f.write("# Findings Report - Activity Diagram Audit\n\n")
        f.write("| ID | Severity | Description | Recommendation |\n")
        f.write("|:---|:---|:---|:---|\n")
        for fnd in findings:
            f.write(f"| {fnd['id']} | {fnd['severity']} | {fnd['desc']} | {fnd['rec']} |\n")
    
    print(f"✅ Da tao bao cao tai: {output_path}")

if __name__ == "__main__":
    # Stub data
    mock_findings = [
        {"id": "CF-01", "severity": "🔴 Critical", "desc": "Thieu Merge node tai luong thanh toan.", "rec": "Them Merge node truoc khi vao Action 'Cap nhat don hang'."}
    ]
    generate_report(mock_findings, "findings_report.md")
