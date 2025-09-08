FROM python:3.12-slim-trixie

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

COPY pyproject.toml uv.lock ./

RUN uv sync

# Copy the rest of your application code
COPY . .

# Expose the port uvicorn will be running on
EXPOSE 8000

# Run the service using uv run
# The --reload flag is useful for development but should be removed for production
CMD ["/root/.local/bin/uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]


# # Use a base image with Python 3.13.7
# FROM python:3.13.7-slim

# # Set the working directory
# WORKDIR /app

# # Install uv using the recommended installation method and set PATH in the same layer
# RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
#     export PATH="/root/.local/bin:$PATH" && \
#     uv --version

# # Copy your project's dependency files (pyproject.toml and uv.lock)
# COPY pyproject.toml uv.lock ./

# # Use uv sync to install the dependencies
# RUN /root/.local/bin/uv sync

# # Copy the rest of your application code
# COPY . .

# # Expose the port uvicorn will be running on
# EXPOSE 8000

# # Run the service using uv run
# # The --reload flag is useful for development but should be removed for production
# CMD ["/root/.local/bin/uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]