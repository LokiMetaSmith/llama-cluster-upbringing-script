import re

def clean_terminal_output(text: str) -> str:
    """
    Cleans raw terminal output by resolving carriage returns (\\r) and
    stripping ANSI escape sequences, mimicking how a real terminal displays it.
    """
    if not isinstance(text, str):
        return text

    # Strip ANSI escape sequences (e.g. colors, cursor movement)
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    text = ansi_escape.sub('', text)

    # Split into lines (handling \n as the primary line separator)
    lines = text.split('\n')

    cleaned_lines = []
    for line in lines:
        if '\r' in line:
            # A carriage return moves the cursor to the beginning of the line.
            # Usually, whatever is printed after the \r overwrites what was there.
            # So the last segment separated by \r is the final visible output.
            parts = line.split('\r')
            final_part = parts[-1] if parts[-1] != '' else (parts[-2] if len(parts) > 1 else '')
            cleaned_lines.append(final_part)
        else:
            cleaned_lines.append(line)

    return '\n'.join(cleaned_lines)
