FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /opt/app

# Install packages
COPY requirements.txt ../.
RUN pip install --no-cache-dir -r ../requirements.txt

# Copy-in application directory
COPY app/ /opt/app

