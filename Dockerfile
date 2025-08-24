# Use Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy your Python script and any requirements file
COPY fetch_stock_data.py .
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set default command to run your script
CMD ["python", "fetch_stock_data.py"]
