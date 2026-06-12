FROM python:3.11-slim 

WORKDIR /app
# copy proto from repo root (for grpc generation)
COPY proto /app/proto
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir grpcio-tools
# generate protobuf modules
RUN python3 -m grpc_tools.protoc \
    -I /app/proto \
    --python_out=/app \
    --grpc_python_out=/app \
    /app/proto/ros.proto

COPY backend/app.py ./app.py

ENV GRPC_HOST=ros-grpc:50051

EXPOSE 5000

CMD ["python", "app.py"]