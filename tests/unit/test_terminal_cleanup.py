import pytest
from pipecatapp.utils.terminal_cleanup import clean_terminal_output

def test_clean_terminal_output_carriage_returns():
    text = "Building...\n(Reading database ... \r(Reading database ... 5%\r(Reading database ... 10%\nDone."
    expected = "Building...\n(Reading database ... 10%\nDone."
    assert clean_terminal_output(text) == expected

def test_clean_terminal_output_ansi():
    text = "\x1b[0;35m[WARNING]: Invalid characters\x1b[0m\n\x1b[0;32mok: [localhost]\x1b[0m"
    expected = "[WARNING]: Invalid characters\nok: [localhost]"
    assert clean_terminal_output(text) == expected

def test_clean_terminal_output_both():
    text = "\x1b[0;35mTesting\x1b[0m\nProgress 0%\rProgress 50%\rProgress 100%\nDone."
    expected = "Testing\nProgress 100%\nDone."
    assert clean_terminal_output(text) == expected

def test_clean_terminal_output_trailing_cr():
    text = "Hello\rWorld\r\nGoodbye\r"
    expected = "World\nGoodbye"
    assert clean_terminal_output(text) == expected

def test_clean_terminal_output_non_string():
    assert clean_terminal_output(None) is None
    assert clean_terminal_output(123) == 123
