# syntax=docker/dockerfile:1

FROM python:3.11.9-slim-bullseye

# Install dependencies

ARG PORT

WORKDIR /app
RUN pip3 install gunicorn
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Setup entrypoint
RUN echo "gunicorn --bind 0.0.0.0:${PORT} main:app" > /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Run app
CMD ["sh", "-c", "/app/entrypoint.sh"]

