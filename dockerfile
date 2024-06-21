# syntax=docker/dockerfile:1

FROM python:3.11.9-slim-bullseye

# Install dependencies
ARG SETUP_COMMAND 

ARG PORT
ARG APPLICATION
ARG MAIN_FILE

WORKDIR /app
RUN pip3 install gunicorn
COPY requirements.txt requirements.txt
RUN ${SETUP_COMMAND}

COPY . .

# Setup entrypoint
RUN echo "gunicorn --bind 0.0.0.0:${PORT} ${MAIN_FILE}:${APPLICATION}" > /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Run app
CMD ["sh", "-c", "/app/entrypoint.sh"]

