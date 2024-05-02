
# Use the official Python image as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN pip uninstall opencv-python opencv-python-headless -y
RUN pip install opencv-python-headless

# Copy the application code to the working directory
COPY . .

# Expose the port on which the Flask app will run
EXPOSE 5000

# Set the environment variable for Flask
ENV FLASK_APP=app.py

# Run the Flask app when the container starts
CMD ["flask", "run", "--host=0.0.0.0"]