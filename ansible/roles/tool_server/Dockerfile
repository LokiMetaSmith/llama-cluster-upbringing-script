FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r ansible/roles/python_deps/files/requirements.txt

CMD ["python", "tool_server.py"]
