FROM python:3.11-slim

WORKDIR /app

# Install dependencies for paramiko libary 
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Paramiko for SSH simulation
RUN pip install paramiko

COPY honeypot.py logger.py ./

# Create logs directory
RUN mkdir -p /app/logs

EXPOSE 22

CMD ["python", "-u", "honeypot.py"]
