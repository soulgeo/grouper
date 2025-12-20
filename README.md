## How to Run

1.  **Set up environment variables:**
    Copy the example environment file to create your local configuration:

    ```bash
    cp .env.example .env
    ```

    (You can usually leave the default values in `.env` as-is for local development with Docker.)

2.  **Start the development server:**
    Run the application using Docker Compose:
    ```bash
    docker-compose up --build
    ```

The application will be available at `http://localhost:8000`.
