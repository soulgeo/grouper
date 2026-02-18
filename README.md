# Grouper

A full-stack social media clone web application, built with Django and HTMX for the purposes of the Software as a Service class assignment at the University of Piraeus. Functionalities include: user authentication and authorization, creating posts and liking other users' posts, searching and filtering through users and posts and chatting with other users through real-time chat powered by web sockets.\
\
The application is dockerized and deployed to the cloud using fly.io, and can be accessed at https://grouper.fly.dev/

## How to Run

Below are instructions on how to run the application on a development environment. Docker and docker-compose are required.

1.  **Clone this repository:**
    ```bash
    git clone https://github.com/soulgeo/grouper.git
    ```

2.  **Set up environment variables:**
    Copy the example environment file to create your local configuration:
    ```bash
    cp .env.example .env
    ```

    (You can usually leave the default values in `.env` as-is for local development with Docker.)

3.  **Start the development server:**
    Run the application using Docker Compose:
    ```bash
    docker-compose up --build
    ```

The application will be available at `http://localhost:8000`.
