# Using official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container to /backend
WORKDIR /backend

# Copy the current directory contents into the container at /backend
COPY . /backend/

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgeos-dev \
    libproj-dev

# Install Python libraries
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install lxml
# Download the NLTK stopwords resource
RUN python -m nltk.downloader stopwords punkt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run app.py when the container launches
CMD ["python3", "app.py"]
