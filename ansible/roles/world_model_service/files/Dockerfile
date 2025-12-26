# Use an official Python runtime as a parent image
FROM python:3.12-slim-bookworm

# Set the working directory in the container
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container at /app
COPY app.py .

# Define environment variables
# These can be overridden at runtime by Nomad
ENV MQTT_HOST="mqtt"
ENV MQTT_PORT=1883
ENV MQTT_TOPIC="#"

# Run app.py when the container launches
CMD ["python", "app.py"]
