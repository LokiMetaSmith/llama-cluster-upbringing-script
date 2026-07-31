import pytest
from unittest.mock import patch, MagicMock

from pipecatapp.network_scanner import get_local_ip

@patch('pipecatapp.network_scanner.socket.socket')
def test_get_local_ip_success(mock_socket_class):
    # Setup mock socket instance
    mock_socket_instance = MagicMock()
    mock_socket_class.return_value = mock_socket_instance

    # Configure getsockname to return a fake local IP
    mock_socket_instance.getsockname.return_value = ('192.168.1.50', 12345)

    # Call the function
    ip = get_local_ip()

    # Verify behavior
    mock_socket_instance.connect.assert_called_once_with(('10.255.255.255', 1))
    mock_socket_instance.getsockname.assert_called_once()
    mock_socket_instance.close.assert_called_once()

    assert ip == '192.168.1.50'

@patch('pipecatapp.network_scanner.socket.socket')
def test_get_local_ip_exception(mock_socket_class):
    # Setup mock socket instance
    mock_socket_instance = MagicMock()
    mock_socket_class.return_value = mock_socket_instance

    # Configure connect to raise an exception
    mock_socket_instance.connect.side_effect = OSError("Network is unreachable")

    # Call the function
    ip = get_local_ip()

    # Verify behavior
    mock_socket_instance.connect.assert_called_once_with(('10.255.255.255', 1))
    mock_socket_instance.getsockname.assert_not_called()
    mock_socket_instance.close.assert_called_once()

    # Fallback to localhost
    assert ip == '127.0.0.1'
