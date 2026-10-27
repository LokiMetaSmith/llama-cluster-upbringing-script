import os
import pytest
from fastapi.testclient import TestClient

def test_hello_world_agent():
    # Setup token FIRST, before importing the app
    os.environ['TOOL_SERVER_API_KEY'] = 'test_token'

    from pipecatapp.tool_server import app
    client = TestClient(app)

    headers = {
        'Authorization': 'Bearer test_token',
        'Content-Type': 'application/json'
    }

    response = client.post(
        '/run_tool/',
        json={
            'tool': 'hello_world_agent',
            'method': 'execute',
            'args': {
                'action': 'say_hello',
                'message': 'Jules'
            }
        },
        headers=headers
    )

    assert response.status_code == 200
    assert response.json() == {'result': 'Hello World! You said: Jules'}
