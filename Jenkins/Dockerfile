# Use the official Jenkins image as the base
FROM jenkins/jenkins:lts

# Switch to the root user to install system packages
USER root

# Install Python 3, pip3, and any necessary system dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-virtualenv && \
    rm -rf /var/lib/apt/lists/*

# Optionally install git (if not already included in the Jenkins base image)
RUN apt-get install -y git

# Ensure pip3 is updated to the latest version
RUN pip3 install --upgrade pip

# Switch back to the Jenkins user
USER jenkins

# Expose Jenkins port (optional, the default is 8080)
EXPOSE 8080

# Define the Jenkins home directory (optional)
ENV JENKINS_HOME /var/jenkins_home

# Run the Jenkins server
CMD ["java", "-jar", "/usr/share/jenkins/jenkins.war"]
