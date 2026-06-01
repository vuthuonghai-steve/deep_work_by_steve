#!/usr/bin/env python3
"""
gate_synthesizer.py — Dynamic Context-Aware Quality Gates Synthesizer.
Scans the task intent/code to dynamically generate 5-10 business and security gates in dynamic-gates.yaml.

Usage:
    python3 gate_synthesizer.py --task "<task_description_or_code>" --out <output_yaml_path>
"""

import sys
import argparse
import yaml
from pathlib import Path

DEFAULT_GATES = {
    "DEV-SEC-01": {
        "name": "Hardcoded Secrets Leak",
        "description": "Cấm gán cứng mật mã, khóa bảo mật Stripe/API trần trong code.",
        "type": "ast_secret_check",
        "severity": "blocking",
        "fix_hint": "Tải khóa bảo mật qua biến môi trường 'os.environ.get()'."
    },
    "DEV-STY-01": {
        "name": "snake_case Naming Style",
        "description": "Tên hàm phải viết bằng chuẩn snake_case chuẩn PEP 8.",
        "type": "ast_naming_snake",
        "severity": "blocking",
        "fix_hint": "Đổi tên hàm thành chữ thường ngăn cách bởi dấu gạch dưới."
    },
    "DEV-STY-02": {
        "name": "PascalCase Class Naming",
        "description": "Tên Class phải viết bằng chuẩn PascalCase chuẩn PEP 8.",
        "type": "ast_naming_pascal",
        "severity": "blocking",
        "fix_hint": "Đổi tên Class thành chữ cái đầu viết hoa, viết liền."
    },
    "DEV-CMT-01": {
        "name": "Function Docstring Coverage",
        "description": "Mọi hàm public phải có docstring giải thích hành vi.",
        "type": "ast_docstring_check",
        "severity": "blocking",
        "fix_hint": "Thêm docstring bọc trong ba dấu nháy kép giải thích tham số."
    }
}

STRIPE_FINTECH_GATES = {
    "FIN-STR-01": {
        "name": "Stripe Webhook Signature Authenticity",
        "description": "Bắt buộc xác thực chữ ký webhook Stripe để tránh giả mạo request.",
        "type": "regex_check",
        "pattern": r"stripe\.Webhook\.construct_event",
        "severity": "blocking",
        "fix_hint": "Bổ sung dòng gọi 'stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)'."
    },
    "FIN-TX-02": {
        "name": "Atomic Database Transaction Guard",
        "description": "Mọi thao tác ghi/cập nhật số dư tài khoản Stripe/Fintech phải bọc trong transaction.",
        "type": "regex_check",
        "pattern": r"transaction\.atomic\b|db\.transaction\b",
        "severity": "blocking",
        "fix_hint": "Bọc khối cập nhật số dư/database trong context manager 'with transaction.atomic():'."
    }
}

CONCURRENCY_GATES = {
    "CON-MUT-01": {
        "name": "Concurrency Mutex Synchronizer",
        "description": "Phát hiện thao tác với biến đếm/tài nguyên chung trong đa luồng mà thiếu Lock bảo vệ.",
        "type": "regex_check",
        "pattern": r"\.Lock\b|Lock\(",
        "severity": "blocking",
        "fix_hint": "Khai báo Lock và sử dụng 'with lock:' xung quanh tài nguyên chia sẻ tương tranh."
    }
}

PRIVACY_GATES = {
    "SEC-PII-01": {
        "name": "PII / Secrets Log Leak Protection",
        "description": "Nghiêm cấm ghi log mật khẩu hoặc CVV/thông tin nhạy cảm ở dạng plaintext.",
        "type": "regex_neg_check",
        "pattern": r"print\(.*password|logger\..*password|print\(.*cvv|logger\..*cvv",
        "severity": "blocking",
        "fix_hint": "Mã hóa dữ liệu nhạy cảm hoặc loại bỏ hoàn toàn các dòng print/log thông tin thô."
    }
}

def synthesize_gates(task_desc: str) -> dict:
    task_lower = task_desc.lower()
    gates = DEFAULT_GATES.copy()
    
    # 1. Fintech/Stripe Domain Detection
    if any(k in task_lower for k in ["stripe", "payment", "webhook", "fintech", "billing"]):
        print("💡 Detected Domain: Fintech / Stripe. Synthesizing transactional safety gates...")
        gates.update(STRIPE_FINTECH_GATES)
        
    # 2. Concurrency Domain Detection
    if any(k in task_lower for k in ["thread", "async", "concurrent", "multiprocess", "lock"]):
        print("💡 Detected Domain: Concurrency / Multithreading. Synthesizing sync guards...")
        gates.update(CONCURRENCY_GATES)
        
    # 3. Privacy/PII Domain Detection
    if any(k in task_lower for k in ["privacy", "pii", "user_data", "password", "personal"]):
        print("💡 Detected Domain: Privacy / PII Security. Synthesizing log scrubber gates...")
        gates.update(PRIVACY_GATES)
        
    return gates

def main():
    parser = argparse.ArgumentParser(description="Dynamic Quality Gates Synthesizer.")
    parser.add_argument("--task", required=True, help="Task description or intent")
    parser.add_argument("--out", required=True, help="Output YAML path")
    
    args = parser.parse_args()
    
    gates = synthesize_gates(args.task)
    
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    out_path.write_text(yaml.safe_dump(gates, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"🏆 Successfully synthesized {len(gates)} Quality Gates into: {args.out}")

if __name__ == "__main__":
    main()
