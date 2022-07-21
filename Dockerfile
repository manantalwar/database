FROM python:3.10-alpine

# Set some metadata using the OpenContainers annotations spec: https://github.com/opencontainers/image-spec/blob/main/annotations.md
LABEL org.opencontainers.image.title="LRC database application container"
LABEL org.opencontainers.image.description="Contains everything needed to run the LRC's tutoring and SI database"
LABEL org.opencontainers.image.authors="Learning Resource Center at UMass Amherst (lrc@umass.edu)"
LABEL org.opencontainers.image.url="https://github.com/umass-lrc/database"

# Copy Python code and pyproject.toml to /srv
WORKDIR /srv
COPY lrc_database/ .
COPY pyproject.toml .

# Install Poetry and Pip
RUN apk add \
    poetry \
    py3-pip

# Tell Poetry not to create a virtualenv so that packages are installed globally, then install runtime dependencies specified by pyproject.toml
RUN poetry config virtualenvs.create false && poetry install \
    --no-ansi \ 
    --no-dev \
    --no-interaction \
    --no-root

# Add the directory that Poetry installs packages to to Python's path so that they can be imported.
ENV PYTHONPATH "${PYTHONPATH}:/usr/lib/python3.10/site-packages"

CMD gunicorn --bind 0.0.0.0:8000 lrc_database.wsgi
