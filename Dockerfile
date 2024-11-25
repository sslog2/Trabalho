FROM python:3.10.15

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file to the container
COPY requirements.txt /code/

# Install the required packages including GDAL
RUN apt-get update \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the project files into the container
COPY . /code/
