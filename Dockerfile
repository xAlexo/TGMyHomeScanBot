# Use Ubuntu as base image since it has good SANE support
FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    sane-utils \
    libsane1 \
    && rm -rf /var/lib/apt/lists/*

# Create application directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements/production.txt requirements/production.txt

# Upgrade pip and install Python dependencies
RUN pip3 install --upgrade pip
RUN pip3 install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements/production.txt

# Copy application code
COPY . .

# Create config template
RUN echo "# Configuration template - set these environment variables" > config.py.template && \
    echo "import os" >> config.py.template && \
    echo "" >> config.py.template && \
    echo "# Telegram API configuration" >> config.py.template && \
    echo "TG_APP_ID = int(os.environ['TG_APP_ID'])" >> config.py.template && \
    echo "TG_API_HASH = os.environ['TG_API_HASH']" >> config.py.template && \
    echo "TG_BOT_API_TOKEN = os.environ['TG_BOT_API_TOKEN']" >> config.py.template && \
    echo "TG_APP_TITLE = os.environ.get('TG_APP_TITLE', 'MyHomeScan')" >> config.py.template && \
    echo "" >> config.py.template && \
    echo "# Scanner configuration" >> config.py.template && \
    echo "SCANNER = os.environ['SCANNER']" >> config.py.template && \
    echo "" >> config.py.template && \
    echo "# Access control" >> config.py.template && \
    echo "ALLOW_IDS = frozenset(map(int, os.environ['ALLOW_IDS'].split(',')))" >> config.py.template

# Create startup script
RUN echo "#!/bin/bash" > start.sh && \
    echo "# Generate config.py from environment variables" >> start.sh && \
    echo "cp config.py.template config.py" >> start.sh && \
    echo "" >> start.sh && \
    echo "# Start the bot" >> start.sh && \
    echo "python3 run.py" >> start.sh && \
    chmod +x start.sh

# Expose no ports (bot connects to Telegram API)
# Create volume for temporary files
VOLUME ["/tmp"]

# Set the entrypoint
ENTRYPOINT ["./start.sh"]