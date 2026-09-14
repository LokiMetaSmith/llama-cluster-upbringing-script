# Stage 1: Build Moshi Rust Backend
FROM rust:1.80-slim-bookworm AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    pkg-config \
    libssl-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/moshi

# Copy the rust source code
COPY moshi/rust/ /usr/src/moshi/

# Build the moshi-backend standalone binary
# Use release profile and compile without GPU features for the lean image by default
RUN cargo build --release --bin moshi-backend

# Stage 2: Lean Runner Image
FROM debian:bookworm-slim

# Install runtime dependencies (OpenSSL is needed for HTTPS)
RUN apt-get update && apt-get install -y \
    ca-certificates \
    libssl3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the compiled binary from the builder
COPY --from=builder /usr/src/moshi/target/release/moshi-backend /usr/local/bin/moshi-backend

# Copy the config file
COPY moshi/rust/moshi-backend/config.json /app/config.json

# Create a non-root user
RUN useradd -m -s /bin/bash moshi
USER moshi

# Expose the default port
EXPOSE 8998

# Default command
ENTRYPOINT ["moshi-backend"]
CMD ["-r", "--config", "config.json", "standalone"]
