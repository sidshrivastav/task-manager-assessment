# Use official Python image
FROM python:3.13-slim


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install build tools and dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    libssl-dev \
    libffi-dev \
    build-essential \
 && pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

# Clean up
RUN apt-get purge -y --auto-remove gcc \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

COPY . /app