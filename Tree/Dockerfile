# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install networking tools
RUN apt-get update && apt-get install -y iputils-ping

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app/Tree
COPY . /app/Tree

# Set the working directory to /app (one level up from Tree)
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r Tree/requirements.txt

# Expose port 5001 (match Flask internal port with what Nginx is expecting)
EXPOSE 5001

# Set the Python path to include the app directory
ENV PYTHONPATH="/app:${PYTHONPATH}"

# Run BST_Service.py when the container launches
CMD ["python", "-c", "from Tree.BST_Service import app; app.run(host='0.0.0.0', port=5001)"]
