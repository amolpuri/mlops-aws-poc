FROM python:3.11-slim

# Set working directory
WORKDIR /opt/ml/processing

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy processing script
COPY preprocess.py .

# Default entry point
ENTRYPOINT ["python3", "preprocess.py"]
