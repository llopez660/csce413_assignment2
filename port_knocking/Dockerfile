FROM python:3.11-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y \
    iptables knockd netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh ./

RUN chmod +x entrypoint.sh

COPY knockd.conf /

CMD [ "./entrypoint.sh" ]