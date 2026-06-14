FROM public.ecr.aws/docker/library/python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

ENV DB_PATH=/data/cache.db
ENV PROXY_BASE_URL=http://127.0.0.1:3141
ENV PORT=3141

EXPOSE $PORT

CMD uvicorn main:app --host 0.0.0.0 --port $PORT
