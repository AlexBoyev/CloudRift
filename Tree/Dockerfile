FROM python:3.9-slim

WORKDIR /app

# Copy only the necessary files and directories
COPY requirements.txt .
COPY Tree ./Tree

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the Python path to include the Tree directory
ENV PYTHONPATH=/app

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["python", "Tree/BST_Service.py"]