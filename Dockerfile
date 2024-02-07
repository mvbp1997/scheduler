FROM python:3.9-slim

WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN pip install -r requirements.txt

# Exposing an internal port
EXPOSE 5001

ENTRYPOINT ["python3"]

CMD ["app.py"]
