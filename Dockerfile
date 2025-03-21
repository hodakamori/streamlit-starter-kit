FROM python:slim

WORKDIR /opt
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    r-base \
    r-base-dev \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    libomp-dev \
    clang \
    && rm -rf /var/lib/apt/lists/*

ENV RYE_HOME="/opt/rye"
ENV PATH="$RYE_HOME/shims:$PATH"
    
SHELL [ "/bin/bash", "-o", "pipefail", "-c" ]
RUN curl -sSf https://rye.astral.sh/get | RYE_INSTALL_OPTION="--yes" bash && \
    rye config --set-bool behavior.global-python=true && \
    rye config --set-bool behavior.use-uv=true


WORKDIR /app
COPY . .
RUN rye pin "$(cat .python-version)" && \
    rye sync --no-lock

EXPOSE 8501
