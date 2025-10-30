# syntax=docker/dockerfile:1

FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

# Set the working directory in the container
WORKDIR /kindleDisplay

COPY . .
RUN uv sync

ENV PYTHONPATH=/kindleDisplay

CMD [ "uv", "run", "python3", "-m" , "flask", "--app", "run",  "run", "--host=0.0.0.0", "--port=5050"]
