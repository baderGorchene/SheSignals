# Autism Screening Application

This repository contains a full-stack application for autism screening.

- **Frontend**: A Next.js web application.
- **Backend**: A FastAPI Python application serving a machine learning model.

## Running the Application Locally

### Prerequisites

- Node.js (for the frontend)
- Python 3.12+ (for the backend)
- `uv` (for backend package management)

### Starting the Backend

1. Navigate to the `backend/` directory:
   ```bash
   cd backend
   ```
2. Install dependencies (if you haven't already):
   ```bash
   uv sync
   ```
3. Train the machine learning model (required before starting the server):
   ```bash
   uv run python train_cpu_model.py
   ```
4. Start the FastAPI server:
   ```bash
   uv run python server.py
   ```
   The backend will run on `http://localhost:8001`.

### Starting the Frontend

1. Open a new terminal and navigate to the `frontend/` directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the Next.js development server:
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:3000`.

## Running with Docker Compose

You can also run both the frontend and backend using Docker Compose.

1. Make sure you have Docker and Docker Compose installed.
2. From the root directory, run:
   ```bash
   docker-compose up --build
   ```
   This will build the images, train the model, and start both the frontend and backend services.
   - Frontend: `http://localhost:3000`
   - Backend: `http://localhost:8001`
