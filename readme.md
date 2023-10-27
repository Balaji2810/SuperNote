# User Documentation

This document provides instructions for setting up and using a Docker-compose-based application that includes a backend, Minio, and JWT token authentication. You can interact with the provided API endpoints after configuring the environment as described below.

## Prerequisites

Before proceeding, ensure you have the following installed on your system:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Running the Application

To run the application, follow these steps:

1. Clone the application repository from the source.

2. In the application directory, open a terminal and run the following command to build and start the application:

   ```bash
   docker-compose up --build
   ```

3. Once the containers are up and running, you can access the Minio service and set the API key and API secret.

## Configuring Minio

1. Access the Minio web interface at [http://localhost:9001](http://localhost:9001) in your web browser.

2. Log in with the following credentials:

   - User: `root`
   - password: `root@root`

3. After logging in, go to the "My Secrets" section in the Minio web interface to set a new API key and API secret. Remember these values for the next step.

4. Update the Minio configuration in the `docker-compose.yml` file under the "backend" section. Modify the following environment variables with the values you set in Minio:

   ```yaml
   environment:
     - S3_ACCESS=your-api-key
     - S3_SECRET=your-api-secret
   ```

5. Save the `docker-compose.yml` file.

## Using JWT Token

The JWT token is set in cookies with the keyword "token" during the authentication process. It is automatically handled by the application for secure access to the protected endpoints.

## Accessing API Documentation

You can access the API documentation for this application at [http://localhost:8000/docs](http://localhost:8000/docs). The API documentation provides information on the available endpoints and their usage.

## Available API Endpoints

### POST /api/signup

- Description: Add User

### POST /api/login

- Description: Login

### DELETE /api/logout

- Description: Logout

### GET /api/users

- Description: Get Users

### POST /api/notes

- Description: Add Note

### GET /api/notes

- Description: Get Note

### GET /api/notes/shared

- Description: Get Shared Note

### POST /api/notes/share

- Description: Share Note

### POST /api/notes/{note_id}

- Description: Push Data

### GET /api/notes/{note_id}

- Description: Get Data

### POST /api/file/{note_id}

- Description: Push File

### GET /api/file/{key}

- Description: Get File

You can use these endpoints to interact with the application's features. Make sure you are logged in and have the necessary permissions to access certain endpoints.

That's it! You are now set up and ready to use the application with the provided API endpoints. Enjoy using the features of this application.