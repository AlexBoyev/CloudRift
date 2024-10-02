FROM python:3.8-slim

# Install networking tools
RUN apt-get update && apt-get install -y iputils-ping

# Copy your application files
WORKDIR /app
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Run the application
CMD ["python", "backend_api.py"]
