# Use Python 3.12 as base image (Debian-based)
FROM python:3.12

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies (SANE utils + airscan + avahi/dbus for mDNS/WSD)
RUN apt-get update && apt-get install -y --no-install-recommends \
    sane-utils \
    libsane1 \
    sane-airscan \
    avahi-daemon \
    dbus \
    iputils-ping \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Ensure SANE backends are enabled (add if missing)
RUN set -eux; \
    if ! grep -qE '^[[:space:]]*airscan[[:space:]]*$' /etc/sane.d/dll.conf; then \
        echo "airscan" >> /etc/sane.d/dll.conf; \
    fi; \
    if ! grep -qE '^[[:space:]]*epson2[[:space:]]*$' /etc/sane.d/dll.conf; then \
        echo "epson2" >> /etc/sane.d/dll.conf; \
    fi

# Create application directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements/production.txt requirements/production.txt

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements/production.txt

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

# Create startup script (launch dbus+avahi, quick SANE self-check, then run bot)
RUN echo "#!/bin/bash" > /app/start.sh && \
    echo "set -euo pipefail" >> /app/start.sh && \
    echo "" >> /app/start.sh && \
    echo "# Generate config.py from environment variables" >> /app/start.sh && \
    echo "cp -f /app/config.py.template /app/config.py" >> /app/start.sh && \
    echo "" >> /app/start.sh && \
    echo "# Start DBus (needed by avahi-daemon) and Avahi for mDNS/WS-Discovery" >> /app/start.sh && \
    echo "mkdir -p /run/dbus" >> /app/start.sh && \
    echo "dbus-daemon --system --fork || true" >> /app/start.sh && \
    echo "avahi-daemon --no-drop-root --daemonize || true" >> /app/start.sh && \
    echo "" >> /app/start.sh && \
    echo "# Quick SANE discovery check (non-fatal)" >> /app/start.sh && \
    echo "SANE_DEBUG_AIRSCAN=\${SANE_DEBUG_AIRSCAN:-0} scanimage -L || true" >> /app/start.sh && \
    echo "" >> /app/start.sh && \
    echo "# Start the bot" >> /app/start.sh && \
    echo "exec python /app/run.py" >> /app/start.sh && \
    chmod +x /app/start.sh

# Expose no ports (bot connects to Telegram API)
VOLUME ["/tmp"]

# Set the entrypoint
ENTRYPOINT ["/app/start.sh"]
