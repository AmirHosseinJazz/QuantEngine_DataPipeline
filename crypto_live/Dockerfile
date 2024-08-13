# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

RUN apt-get update && apt-get install -y curl

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir confluent-kafka confluent-kafka[avro] fastavro


COPY ./requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

RUN chmod +x /app/entrypoint.sh
# Run main.py when the container launches
ENTRYPOINT [ "/app/entrypoint.sh" ]
