FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
      ca-certificates curl git python3 ripgrep bubblewrap socat procps \
    && rm -rf /var/lib/apt/lists/*
RUN useradd -m -s /bin/bash eval
USER eval
WORKDIR /home/eval
RUN curl -fsSL https://claude.ai/install.sh | bash -s -- 2.1.289
ENV PATH=/home/eval/.local/bin:$PATH
