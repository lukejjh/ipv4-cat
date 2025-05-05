# Use an official Python runtime as a parent image
FROM python:3.13-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the application code into the container
COPY ./app.py .

# Copy the requirements file into the container
COPY ./requirements.txt .

# Install required dependencies
RUN pip install -r requirements.txt

# Install libcap for setcap
RUN apk add libcap

# Create a non-root user and group
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Grant the non-root user the capability to bind to privileged ports (<1024)
RUN setcap 'cap_net_bind_service=+ep' $(readlink -f $(which python))

# Drop privileges to the non-root user
USER appuser

# Start the application
CMD ["python", "app.py"]