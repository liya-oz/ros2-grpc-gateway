FROM ros:humble

RUN apt-get update && apt-get install -y \
    python3-pip \
    protobuf-compiler

RUN pip3 install grpcio grpcio-tools

WORKDIR /app

COPY proto /app/proto
COPY ros-grpc /app

# generate protobuf INSIDE container
RUN python3 -m grpc_tools.protoc \
    -I ./proto \
    --python_out=/app \
    --grpc_python_out=/app \
    ./proto/ros.proto

CMD ["bash", "-c", "source /opt/ros/humble/setup.bash && python3 grpc_server.py"]