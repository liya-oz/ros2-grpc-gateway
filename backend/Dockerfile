FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENV GRPC_HOST=grpc-adapter:50051

EXPOSE 5000

CMD ["python", "app.py"]