FROM jenkins/jenkins:lts

USER root

# Environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# Install essential packages and Python
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-setuptools \
    python3-wheel \
    git \
    curl \
    tzdata \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create directories and set permissions
RUN mkdir -p /var/lib/apt/lists/partial && \
    chmod -R 755 /var/lib/apt/lists && \
    chown -R root:root /var/lib/apt/lists

# Set up Python environment
RUN ln -sf /usr/bin/python3 /usr/local/bin/python && \
    ln -sf /usr/bin/python3 /usr/local/bin/python3 && \
    ln -sf /usr/bin/pip3 /usr/local/bin/pip && \
    ln -sf /usr/bin/pip3 /usr/local/bin/pip3

# Verify Python installation
RUN python3 --version && \
    pip3 --version

# Set up Jenkins user environment
RUN mkdir -p /home/jenkins/.local/bin && \
    chown -R jenkins:jenkins /home/jenkins/.local && \
    echo 'export PATH="/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/home/jenkins/.local/bin:$PATH"' >> /home/jenkins/.bashrc && \
    echo 'export PATH="/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/home/jenkins/.local/bin:$PATH"' >> /home/jenkins/.profile

# Install Jenkins plugins
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli -f /usr/share/jenkins/ref/plugins.txt

# Give jenkins user access to Python directories
RUN chown -R jenkins:jenkins /usr/local/lib/python3* || true && \
    chown -R jenkins:jenkins /usr/lib/python3* || true && \
    chown -R jenkins:jenkins /usr/bin/python3* || true && \
    chown -R jenkins:jenkins /usr/bin/pip3* || true

# Switch back to Jenkins user
USER jenkins

# Expose Jenkins ports
EXPOSE 8080 50000