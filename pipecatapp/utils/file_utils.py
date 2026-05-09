import hashlib

def calculate_line_hash(line: str) -> str:
    """Calculates a short, stable hash for a line of text.

    Normalizes trailing whitespace (including \\r vs \\n) to ensure
    hashes remain stable across environments, but preserves leading
    whitespace for indentation precision.
    """
    normalized_line = line.replace('\n', '').replace('\r', '').rstrip(' \t')
    return hashlib.sha256(normalized_line.encode('utf-8')).hexdigest()[:4] # Increased to 4 chars for fewer collisions

def generate_file_hashes(filepath: str) -> list[tuple[int, str, str]]:
    """Reads a file and generates a list of (line_number, hash, content)."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()

    result = []
    for i, line in enumerate(lines):
        line_hash = calculate_line_hash(line)
        result.append((i + 1, line_hash, line))
    return result
