import pytest
from pipecatapp.utils.file_utils import calculate_line_hash, generate_file_hashes
import tempfile
import os

def test_calculate_line_hash_basic():
    """Test standard string yields a 4-character hash."""
    line = "def example_function():"
    result = calculate_line_hash(line)
    assert isinstance(result, str)
    assert len(result) == 4

def test_calculate_line_hash_trailing_whitespace():
    """Test stability with varying trailing whitespace."""
    base_line = "print('hello')"
    hash1 = calculate_line_hash(base_line)
    hash2 = calculate_line_hash(base_line + "   ")
    hash3 = calculate_line_hash(base_line + "\t")
    hash4 = calculate_line_hash(base_line + "\n")
    hash5 = calculate_line_hash(base_line + "\r\n")
    hash6 = calculate_line_hash(base_line + " \t\r\n")

    assert hash1 == hash2 == hash3 == hash4 == hash5 == hash6

def test_calculate_line_hash_leading_whitespace():
    """Test that leading whitespace changes the hash."""
    base_line = "x = 1"
    hash1 = calculate_line_hash(base_line)
    hash2 = calculate_line_hash(" " + base_line)
    hash3 = calculate_line_hash("    " + base_line)
    hash4 = calculate_line_hash("\t" + base_line)

    assert hash1 != hash2
    assert hash1 != hash3
    assert hash1 != hash4
    assert hash2 != hash3
    assert hash3 != hash4

def test_calculate_line_hash_empty_string():
    """Test empty strings and strings containing only whitespace."""
    empty_hash = calculate_line_hash("")
    spaces_hash = calculate_line_hash("   ")
    tabs_hash = calculate_line_hash("\t\t")
    newlines_hash = calculate_line_hash("\n\r\n")

    assert empty_hash == spaces_hash == tabs_hash == newlines_hash
    assert len(empty_hash) == 4

def test_generate_file_hashes():
    """Test generating file hashes from a temporary file."""
    content = "line1\n  line2 \n\nline4\r\n"

    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
        f.write(content)
        temp_path = f.name

    try:
        result = generate_file_hashes(temp_path)

        assert len(result) == 4

        # Line 1
        assert result[0][0] == 1
        assert result[0][1] == calculate_line_hash("line1")
        assert result[0][2] == "line1"

        # Line 2
        assert result[1][0] == 2
        assert result[1][1] == calculate_line_hash("  line2 ")
        assert result[1][2] == "  line2 "

        # Line 3
        assert result[2][0] == 3
        assert result[2][1] == calculate_line_hash("")
        assert result[2][2] == ""

        # Line 4
        assert result[3][0] == 4
        assert result[3][1] == calculate_line_hash("line4")
        assert result[3][2] == "line4"
    finally:
        os.unlink(temp_path)
