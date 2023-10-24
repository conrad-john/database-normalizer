# database-normalizer
Class project for CS5300, spins up a FastAPI application inside a Docker container with endpoints for taking in a database schema, determining its normal form, and generating SQL queries to achieve a specified higher level of normalization.

## Prerequisites

Before you get started, ensure you have the following software installed on your system:

- Python 3.x
- Docker

## Running the Application

1. Clone this repository or create your FastAPI application using the provided Dockerfile as a reference.

2. Build the Docker image by running the following command in the project directory:

   ```bash
   docker build -t database-normalizer .

3. Run the Docker container from the image:

   '''bash
   docker run -d -p 80:80 database-normalizer

4. You can now access the application at hhtp://localhost:80 in a web browser or via an HTTP client.