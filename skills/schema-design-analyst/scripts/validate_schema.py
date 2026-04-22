import sys
import yaml
import os

def extract_contract_fields(contract_data):
    fields = set()
    
    def _walk(node, in_fields=False):
        if isinstance(node, dict):
            if 'fields' in node and isinstance(node['fields'], list):
                for f in node['fields']:
                    if isinstance(f, dict) and 'name' in f:
                        fields.add(f['name'])
                    elif isinstance(f, str):
                        fields.add(f.split(':')[0].strip())
                    _walk(f, True)
            else:
                for k, v in node.items():
                    if k == 'name' and in_fields:
                        fields.add(v)
                    _walk(v, in_fields)
        elif isinstance(node, list):
            for item in node:
                _walk(item, in_fields)
                
    _walk(contract_data)
    
    # Standard Payload CMS fields
    fields.update(['id', 'createdAt', 'updatedAt', '_status', '_id', 'slug', 'blockType'])
    return fields

def extract_schema_fields(schema_data):
    fields = set()
    
    def _walk(node):
        if isinstance(node, dict):
            if 'fields' in node and isinstance(node['fields'], list):
                for f in node['fields']:
                    if isinstance(f, dict) and 'name' in f:
                        fields.add(f['name'])
                    _walk(f)
            else:
                for k, v in node.items():
                    _walk(v)
        elif isinstance(node, list):
            for item in node:
                _walk(item)
                
    _walk(schema_data)
    return fields

def validate(schema_path, contract_path):
    if not os.path.exists(schema_path):
        print(f"Error: Schema file not found at {schema_path}")
        return False
        
    if not os.path.exists(contract_path):
        print(f"Error: Contract file not found at {contract_path}")
        return False
        
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_data = yaml.safe_load(f)
            
        with open(contract_path, 'r', encoding='utf-8') as f:
            contract_data = yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading YAML: {e}")
        return False
        
    contract_fields = extract_contract_fields(contract_data)
    schema_fields = extract_schema_fields(schema_data)
    
    hallucinated = schema_fields - contract_fields
    
    if hallucinated:
        print("🔴 BLOCK: Phát hiện các field rác / ảo giác do AI tự bịa ra/thay đổi tên:")
        for f in hallucinated:
            print(f"  - {f}")
        print("\nYêu cầu: Sửa lại tên field trong schema cho trùng chữ với hợp đồng, xoá bỏ nếu là field thừa.")
        return False
        
    print("✅ Schema design an toàn, 100% field khớp với hợp đồng.")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python validate_schema.py <path_to_schema_yaml> <path_to_contract_yaml>")
        sys.exit(1)
        
    schema_path = sys.argv[1]
    contract_path = sys.argv[2]
    
    if validate(schema_path, contract_path):
        sys.exit(0)
    else:
        sys.exit(1)
