FROM ghcr.io/charmbracelet/vhs:latest

USER root

# 1. Install system utilities and allow the release info change
RUN apt-get update --allow-releaseinfo-change && apt-get install -y --no-install-recommends \
    curl \
    jq \
    pv \
    zstd \
    && rm -rf /var/lib/apt/lists/*

# 2. Dynamically detect architecture (amd64 or arm64) and pull the matching binary archive
RUN ARCH=$(uname -m) && \
    if [ "$ARCH" = "x86_64" ]; then OLLAMA_ARCH="amd64"; else OLLAMA_ARCH="arm64"; fi && \
    curl -fsSL "https://ollama.com/download/ollama-linux-${OLLAMA_ARCH}.tar.zst" | tar --zstd -x -C /usr/

# 3. Route container Ollama CLI calls to the host VPS machine server
ENV OLLAMA_HOST="127.0.0.1:11434"

WORKDIR /vhs
ENTRYPOINT ["vhs"]
