
FROM python:3.12-slim


ENV AES_SECRET_KEY="Zx7wmZRTF97dvEvTHxL7zZJkF2HDjZn5cLDoQ77zA1k="

WORKDIR /app

RUN apt-get update && apt upgrade -y

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
