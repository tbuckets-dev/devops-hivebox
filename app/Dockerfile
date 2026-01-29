# Instructions to build a Docker image for the Hivebox application
FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add the application code to the container
COPY app.py .
COPY hivebox.py .

# Command to run the application
CMD ["python", "./app.py"]
