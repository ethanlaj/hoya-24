# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Install any needed packages specified in requirements.txt
# Ensure you have a requirements.txt in your application's directory listing all your dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Supervisord
RUN pip install supervisor

# Expose the port where the app runs
EXPOSE 8080

# The command to run the application using Gunicorn
CMD ["/usr/local/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]