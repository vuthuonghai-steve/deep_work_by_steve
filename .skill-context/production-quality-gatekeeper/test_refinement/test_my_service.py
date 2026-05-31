# test_my_service.py
import pytest
from my_service import process_data

def test_process_data(tmp_path):
    input_file = tmp_path / "input.txt"
    input_file.write_text("line1\nline2\n")
    
    output_file = tmp_path / "output.txt"
    
    # Assert successful execution
    assert process_data(str(input_file), str(output_file)) is True
    
    # Assert output has been processed
    content = output_file.read_text()
    assert "PROCESSED_ITEM: LINE1" in content
    assert "PROCESSED_ITEM: LINE2" in content
