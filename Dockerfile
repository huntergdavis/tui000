# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1  
ENV PYTHONUNBUFFERED=1         

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY package/ /app/package/
COPY tui000.py /app/

# Create the graveyard directory with appropriate permissions
RUN mkdir -p /app/graveyard && \
    chmod -R 755 /app/graveyard

# (Optional) Create a non-root user for enhanced security
RUN addgroup --system appgroup && adduser --system appuser --ingroup appgroup
RUN chown -R appuser:appgroup /app
USER appuser

# Define the default command to run the application
CMD ["python", "tui000.py"]

