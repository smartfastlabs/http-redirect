FROM python:3.12-slim-bullseye

# Create folder system for all the code to go
ENV APP_DIR /app

WORKDIR $APP_DIR

RUN apt-get update && apt-get install -y gcc 

# Copy in requirements on their own so that pip install can be cached
COPY requirements.txt $APP_DIR/
RUN python -m pip install pip-tools
RUN pip install -r requirements.txt

COPY . .

