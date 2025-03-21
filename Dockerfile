FROM python:3.9-buster as Base

COPY pyproject.toml .

ARG DEBIAN_REPO="deb.debian.org"
ARG PIP_INDEX_URL="https://pypi.org/simple"

RUN echo "deb http://$DEBIAN_REPO/debian/ buster main contrib non-free" > /etc/apt/sources.list && \
    echo "deb-src http://$DEBIAN_REPO/debian/ buster main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb http://$DEBIAN_REPO/debian-security buster/updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb-src http://$DEBIAN_REPO/debian-security buster/updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb http://$DEBIAN_REPO/debian/ buster-updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb-src http://$DEBIAN_REPO/debian/ buster-updates main contrib non-free" >> /etc/apt/sources.list

RUN apt-get update && \
    apt-get install -y build-essential netcat-openbsd libpcre3-dev curl && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    uv venv && \
    . .venv/bin/activate && \
    uv sync && \
    apt-get remove -y python3-dev build-essential libpcre3-dev && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

FROM python:3.9-buster
ENV TZ=Asia/Shanghai

ARG DEBIAN_REPO="deb.debian.org"
RUN echo "deb http://$DEBIAN_REPO/debian/ buster main contrib non-free" > /etc/apt/sources.list && \
    echo "deb-src http://$DEBIAN_REPO/debian/ buster main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb http://$DEBIAN_REPO/debian-security buster/updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb-src http://$DEBIAN_REPO/debian-security buster/updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb http://$DEBIAN_REPO/debian/ buster-updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb-src http://$DEBIAN_REPO/debian/ buster-updates main contrib non-free" >> /etc/apt/sources.list

RUN apt-get update && \
    apt-get install -y tzdata && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    rm -rf /var/lib/apt/lists/*

COPY --from=Base /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
WORKDIR /app
COPY . /app
RUN chmod +x /app/start.sh

EXPOSE 8000

ENTRYPOINT ["/app/start.sh"]

