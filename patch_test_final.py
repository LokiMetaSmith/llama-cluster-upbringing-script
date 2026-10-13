import re

with open('tests/unit/test_orchestrator_tool.py', 'r') as f:
    content = f.read()

def replace_func(match):
    return match.group(0).replace(
        'mock_client.post.return_value = mock_response',
        'mock_client.post.side_effect = error'
    )

content = re.sub(r'def test_dispatch_job_failure.*?assert "Error dispatching job: Internal Server Error" in result', replace_func, content, flags=re.DOTALL)

with open('tests/unit/test_orchestrator_tool.py', 'w') as f:
    f.write(content)
