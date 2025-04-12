# Stage 1: Builder Image
FROM python:3.12-slim AS builder-image

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install build dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    python3-venv python3-pip build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set up the virtual environment
RUN python3 -m venv /home/myuser/venv
ENV PATH="/home/myuser/venv/bin:$PATH"

# Install project dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir wheel
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runner Image
FROM python:3.12-slim AS runner-image

# Install runtime dependencies
RUN apt-get update && apt-get install --no-install-recommends -y python3-venv && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Add a non-root user
RUN useradd --create-home myuser

# Copy the virtual environment from the builder stage
COPY --from=builder-image /home/myuser/venv /home/myuser/venv

# Set up the application directory
USER myuser
RUN mkdir /home/myuser/code
WORKDIR /home/myuser/code
COPY . .

# Do not copy a local .env file; use runtime environment variables via Docker Compose or docker run

# Set up Python environment variables
ENV VIRTUAL_ENV=/home/myuser/venv
ENV PATH="/home/myuser/venv/bin:$PATH"
ENV PYTHONPATH="/home/myuser/code"

# Command to run the application (defaulting to schedule mode)
ENTRYPOINT ["python", "src/main.py", "--schedule"]
