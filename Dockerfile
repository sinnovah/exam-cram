# Linux Alpine version for Python 3.11.3 latest as at 2023-06-05
FROM python:3.11.3-alpine3.18

# Maintainer of the project
LABEL maintainer="sinnovah"

# Ensure python output is unbuffered to avoid delays
ENV PYTHONUNBUFFERED 1

# Copy local files & app directory to docker image
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app

# Default path to run commands from
WORKDIR /app

# Expose port 8000 to connect to the server
EXPOSE 8000

# When using docker-compose for dev, this argument is overidden to true
ARG DEV=false

# Run the following commands on the image
RUN \
    # Create virtual environment
    # Avoids conflicts with base image & project dependencies
    python -m venv /py && \
    # Upgrade pip to the latest version
    /py/bin/pip install --upgrade pip && \
    # Install postgresql client
    apk add --update --no-cache postgresql-client && \
    # Install build dependencies for packages in requirements file
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    # Install dependencies
    /py/bin/pip install -r /tmp/requirements.txt && \
    # Install development dependencies if in dev mode
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    # Remove tmp directory because requirements files
    # are no longer needed. Keeps image light weight
    rm -rf /tmp && \
    # Remove build dependencies
    apk del .tmp-build-deps && \
    # Add a new user to connect to the backend 
    # to avoid using the root user permanently
    adduser \
        # Connect directly with no password
        --disabled-password \
        # Don't create a user home directory
        --no-create-home \
        # Username
        backend-user

# Saves typing /py/bin everytime when running commands
ENV PATH="/py/bin:$PATH"

# Switch to non-root backend user
USER backend-user
