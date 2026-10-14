FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
      ca-certificates curl git python3 ripgrep bubblewrap socat procps xz-utils \
    && rm -rf /var/lib/apt/lists/*
# Node runs a project's verification tool (scripts/verify.mts), which needs 22.18 or newer;
# Debian's package is older. The archive is checked against the release's published checksums.
RUN v=22.22.3 arch=$(dpkg --print-architecture | sed 's/amd64/x64/') \
    && f=node-v$v-linux-$arch.tar.xz && cd /tmp \
    && curl -fsSLO "https://nodejs.org/dist/v$v/$f" \
    && curl -fsSL "https://nodejs.org/dist/v$v/SHASUMS256.txt" | grep " $f\$" | sha256sum -c - \
    && tar -xJf "$f" -C /usr/local --strip-components=1 --exclude='*.md' --exclude=LICENSE \
    && rm "$f"
RUN useradd -m -s /bin/bash eval
USER eval
WORKDIR /home/eval
RUN curl -fsSL https://claude.ai/install.sh | bash -s -- 2.1.289
ENV PATH=/home/eval/.local/bin:$PATH
