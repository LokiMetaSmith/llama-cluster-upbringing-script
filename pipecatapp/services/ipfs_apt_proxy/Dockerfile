FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

ENV DB_PATH=/data/cache.db
ENV PORT=3142

EXPOSE $PORT

CMD python3 main.py
