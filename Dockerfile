# Dockerfile for Hugging Face Spaces deployment
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY model_service.py .
COPY static/ ./static/

# Copy model files (these will be large)
COPY tutor_model_lora/ ./tutor_model_lora/

# Expose port 7860 (Hugging Face Spaces default)
EXPOSE 7860

# Set environment variables
ENV HOST=0.0.0.0
ENV PORT=7860
ENV MODEL_PATH=tutor_model_lora
ENV MAX_SEQ_LENGTH=2048

# Run the application
CMD ["python", "app.py"]
