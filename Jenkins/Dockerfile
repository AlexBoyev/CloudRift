# Stage 1: Use a Python base image to install Python and dependencies
FROM python:3.9-slim AS python-builder

# Install git (if needed for your setup)
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

# Ensure pip3 is updated to the latest version
RUN pip3 install --upgrade pip

# Optionally create virtualenv if needed (this can be customized)
RUN python3 -m venv /venv

# Stage 2: Use the official Jenkins image as the base
FROM jenkins/jenkins:lts

# Copy Python and git from the python-builder stage
COPY --from=python-builder /usr/local/bin/python3 /usr/local/bin/python3
COPY --from=python-builder /usr/local/bin/pip3 /usr/local/bin/pip3
COPY --from=python-builder /usr/bin/git /usr/bin/git
COPY --from=python-builder /venv /venv

# Optionally expose Jenkins port (8080 is the default)
EXPOSE 8080

# Define Jenkins home directory (optional)
ENV JENKINS_HOME /var/jenkins_home

# Use the virtualenv Python path (optional)
ENV PATH="/venv/bin:$PATH"

# Run the Jenkins server
CMD ["java", "-jar", "/usr/share/jenkins/jenkins.war"]
