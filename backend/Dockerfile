# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install uv for fast Python package management
RUN pip install uv

# Copy the pyproject.toml and uv.lock files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen

# Copy the rest of the application code
COPY . .

# Run the training script to generate the model and features
RUN uv run python train_cpu_model.py

# Expose port 8001
EXPOSE 8001

# Command to run the application
CMD ["uv", "run", "python", "server.py"]
