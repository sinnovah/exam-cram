# Linux Alpine version for Python 3.11.3 latest as at 2023-06-05
FROM python:3.11.3-alpine3.18

# Maintainer of the project
LABEL maintainer="sinnovah"

# Ensure python output is unbuffered to avoid delays
ENV PYTHONUNBUFFERED 1

# Copy local file & directory to docker image
COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app

# Default path to run commands from
WORKDIR /app

# Expose port 8000 to connect to the server
EXPOSE 8000

# Run the following commands on the image
RUN \
    # Create virtual environment
    # Avoids conflicts with base image & project dependencies
    python -m venv /py && \
    # Upgrade pip to latest version
    /py/bin/pip install --upgrade pip && \
    # Install dependencies
    /py/bin/pip install -r /tmp/requirements.txt && \
    # Remove tmp directory because requirements.txt 
    # is no longer needed. Keeps image light weight
    rm -rf /tmp && \
    # Add a new user to connect to the backend 
    # to avoid using the root user perminantly
    adduser \
        --disabled-password \
        --no-create-home \
        backend-user

# Path for python commands
ENV PATH="/py/bin:$PATH"

# Switch to non-root user
USER backend-user
