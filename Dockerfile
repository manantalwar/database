FROM python:3.10-alpine

# Set some metadata using the OpenContainers annotations spec: https://github.com/opencontainers/image-spec/blob/main/annotations.md
LABEL org.opencontainers.image.title="LRC database application container"
LABEL org.opencontainers.image.description="Contains everything needed to run the LRC's tutoring and SI database"
LABEL org.opencontainers.image.authors="Learning Resource Center at UMass Amherst (lrc@umass.edu)"
LABEL org.opencontainers.image.url="https://github.com/umass-lrc/database"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /srv
# COPY lrc_database/ .
