# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set an environment variable to ensure Python output is sent straight to terminal (e.g. your container log)
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app/blogsphere/

# Copy the current directory contents into the container at /app/blogsphere/
COPY . /app/blogsphere/

# Install any needed packages specified in requirements.txt
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get remove -y gcc && \
    apt-get purge -y --auto-remove && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Make port 8888 available to the world outside this container
EXPOSE 8888  

# Define environment variable
ENV PORT=8888

# Run manage.py when the container launches
CMD ["python", "manage.py", "runserver", "0.0.0.0:8888"]
