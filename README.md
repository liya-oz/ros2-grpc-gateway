<div align="center">

![License](https://img.shields.io/badge/license-MIT-blue)
![Docker](https://img.shields.io/badge/Docker-distributed-blue?logo=docker)
![ROS2](https://img.shields.io/badge/ROS2-Humble-blueviolet?logo=ros)
![gRPC](https://img.shields.io/badge/gRPC-Enabled-00ADD8?logo=grpc)
![Flask](https://img.shields.io/badge/Flask-3.0-lightgrey?logo=flask)
![React](https://img.shields.io/badge/React-19-61DAFB?logo=react)
![Node.js](https://img.shields.io/badge/Node.js-22-339933?logo=nodedotjs)

</div>

# ROS2 gRPC Gateway

A containerized prototype for real-time ROS2 data streaming, backend aggregation, and UI monitoring.

### Architecture

```text
ROS2 node             #publishes robot/topic data
   ↓
ROS2 gRPC Adapter     #subscribes to ROS topics and streams updates
   ↓
Flask Backend         #consumes gRPC data and exposes HTTP endpoints
   ↓
React Frontend        #displays live robot state
```

## Protobuf is used

- `proto/ros.proto`
- `ros_pb2.py`
- `ros_pb2_grpc.py`

### to generate gRPC Code

```bash
python3 -m grpc_tools.protoc \
  -I proto \
  --python_out=. \
  --grpc_python_out=. \
  proto/ros.proto
```

## StartUsing

### 1. **Create `.env` file**

```env
ROS_DISTRO=humble
ROS_DOMAIN_ID=7
DEV_UID=1000
DEV_GID=1000
```
Or, run:
```bash
echo 'ROS_DISTRO=humble
ROS_DOMAIN_ID=7
DEV_UID=1000
DEV_GID=1000' > .env
```

### 2. **Build and start all services**
```bash
docker compose up --build
```
- The first build may take several minutes
- All services (ros2, backend, frontend) will start up with logs streaming in the terminal

---

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:5000/api/chatter
- **gRPC Adapter:** `ros-grpc:50051`

##  **To stop the system**

Press `Ctrl+C` in your terminal to stop all services and clean up.

Or, to stop and remove containers:
```bash
docker compose down
```

---

## **Rebuild Images (after source code changes)**

If you change backend, frontend, or ROS2 code, rebuild and restart:
```bash
docker compose up --build
```
## Prerequisites

- Docker
- Docker Compose
- Git
- Node.js 22+ for local frontend development

## License

MIT