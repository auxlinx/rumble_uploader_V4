# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /rumble_uploader

# Install dependencies
COPY requirements.txt /rumble_uploader/
RUN pip install -r requirements.txt

# Copy project
COPY . /rumble_uploader/

# Use an official Python runtime as a parent image
# FROM python:3.8-slim-buster
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1
# WORKDIR rumble_uploader
# COPY requirements.txt rumble_uploader/
# RUN pip install -r requirements.txt
# COPY . rumble_uploader/
