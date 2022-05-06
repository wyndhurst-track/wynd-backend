# Use an official Python runtime as a parent image
FROM python:3.7-slim
# Set the working directory to /app
WORKDIR /app
# Copy the current directory contents into the container at /app
COPY . /app
# Install Gunicorn3
RUN apt-get update && apt-get install default-libmysqlclient-dev gcc -y
# Install any needed packages specified in requirements.txt
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt
# Make port 5000 available to the world outside this container
EXPOSE 5000
# Define environment variable
ENV username root
# Run app.py when the container launches
CMD gunicorn --workers 1 --bind 0.0.0.0:5000 main:app
