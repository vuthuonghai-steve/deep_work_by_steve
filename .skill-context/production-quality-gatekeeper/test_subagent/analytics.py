"""
Analytics module for file reading and aggregation operations.
"""

def read_and_aggregate(filepath: str) -> dict:
    """
    Reads a CSV file containing key-value pairs and aggregates the values.

    Args:
        filepath (str): The path to the input CSV file.

    Returns:
        dict: A dictionary containing aggregated values for each key.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file format or values are invalid.
    """
    data = {}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 2:
                    key = parts[0].strip()
                    try:
                        val = int(parts[1].strip())
                    except ValueError as e:
                        print(f"Skipping line due to value error: {line.strip()} - {e}")
                        continue
                    data[key] = data.get(key, 0) + val
    except FileNotFoundError as e:
        print(f"File not found error: {filepath}")
        raise e
    except Exception as e:
        print(f"Unexpected error occurred while reading file: {e}")
        raise e
    return data

