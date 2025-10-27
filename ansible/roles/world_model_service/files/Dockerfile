# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container at /app
COPY app.py .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variables
# These can be overridden at runtime by Nomad
ENV MQTT_HOST="mqtt"
ENV MQTT_PORT=1883
ENV MQTT_TOPIC="#"

# Run app.py when the container launches
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]