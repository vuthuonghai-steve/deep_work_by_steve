"""
my_service.py — Production-grade data processing service.
"""

def read_file_lines(file_path):
    """Read lines from a file using standard context manager.
    
    Args:
        file_path (str): Path to the source file.
        
    Returns:
        list: Stripped lines of text.
    """
    data = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            data.append(line.strip())
    return data

def validate_data(data):
    """Filter and capitalize raw text data.
    
    Args:
        data (list): Raw list of strings.
        
    Returns:
        list: Filtered and capitalized strings.
    """
    valid_data = []
    for item in data:
        if not item:
            continue
        valid_data.append(item.upper())
    return valid_data

def write_file_lines(output_path, lines):
    """Safely write formatted lines to a target file.
    
    Args:
        output_path (str): Destination path.
        lines (list): List of processed lines to write.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        with open(output_path, "w", encoding="utf-8") as out:
            for item in lines:
                out.write(item + "\n")
        return True
    except OSError as e:
        print(f"ERROR: Failed to write to {output_path}: {e}")
        return False

def process_data(file_path, output_path):
    """Coordinate the complete load-validate-write pipeline.
    
    Args:
        file_path (str): Path to input file.
        output_path (str): Path to output file.
        
    Returns:
        bool: True if pipeline finishes successfully, False otherwise.
    """
    try:
        # Load Phase
        raw_data = read_file_lines(file_path)
        
        # Validation Phase
        valid_data = validate_data(raw_data)
        
        # Formatting Phase
        formatted = [f"PROCESSED_ITEM: {item}" for item in valid_data]
        
        # Delivery Phase
        success = write_file_lines(output_path, formatted)
        return success
    except Exception as e:
        print(f"CRITICAL: Data processing failed: {e}")
        return False
