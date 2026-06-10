<div>
  <img alt="License" src="https://img.shields.io/badge/license-MIT-blue">
  <img alt="Docker" src="https://img.shields.io/badge/Docker-distributed-blue?logo=docker">
  <img alt="ROS2" src="https://img.shields.io/badge/ROS2-Humble-blueviolet?logo=ros">
  <img alt="Flask" src="https://img.shields.io/badge/Flask-3.0-lightgrey?logo=flask">
  <img alt="React" src="https://img.shields.io/badge/React-19-61DAFB?logo=react">
  <img alt="Node.js" src="https://img.shields.io/badge/Node.js-22-339933?logo=nodedotjs">
</div>

ROS2 (DDS/pub-sub)
   ↓
ROS2 gRPC Adapter (subscribes to ROS topics, exposes gRPC stream)
   ↓
REST Backend (consumes gRPC stream, business API)
   ↓
React UI

proto/ros.proto          ✔ contract
ros_pb2.py               ✔ generated messages
ros_pb2_grpc.py          ✔ generated service skeleton

BY COMMAND : python3 -m grpc_tools.protoc \
  -I proto \
  --python_out=. \
  --grpc_python_out=. \
  proto/ros.proto

gRPC server
  ├── StreamChatter()
  └── fake loop (time.sleep)

gRPC client
  └── receives stream


  generated/     ← protobuf generated code
proto/         ← .proto contracts

ros-grpc/      ← ROS runtime nodes (subscribers/publishers), a shared in-memory buffer layer


ROS callback → writes to shared
gRPC → reads from the same shared
Flask → consumes gRPC


- Implement SharedState singleton for thread-safe in-memory storage
- Add ROS2 subscriber node to ingest 'chatter' topic messages
- Introduce gRPC server with StreamChatter server-streaming RPC
- Add sequence-based deduplication for message streaming
- Implement Flask API gateway consuming gRPC stream (MVP integration)
- Use polling-based streaming loop (MVP: sleep-based, upgradeable to event-driven model)
- Ensure safe concurrent access using threading.Lock across ROS and gRPC threads

# ROS2 grpc gateway

 is a containerized prototype for **ROS2-based distributed communication and real-time state monitoring**. It demonstrates a modular architecture that decouples robot-side computation from external interfaces using a lightweight grpc communication layer.

The system implements a layered communication design, where robot data generation, middleware transport, and visualization are separated into independent but interoperable components. 

---

## System Overview

The architecture is composed of three loosely coupled services orchestrated via **Docker Compose**:

- **ROS2 layer (robot node simulation)**  
  Runs a ROS2 *talker node*. The ROS2 runtime is integrated into the **ROS2 gRPC Adapter** process which subscribes to topics and updates an in-process `SharedState` singleton.

- **Backend layer (data aggregation interface)**  
  A Flask service that acts as a **middleware communication proxy**, consuming data from the ROS2 gRPC Adapter over gRPC (adapter exposes port **50051**).

- **Frontend layer (operator / monitoring interface)**  
  A web-based UI (React / Nginx) that consumes the backend API and visualizes real-time robot state at port **5173**.

Connection notes:
- The gRPC adapter runs the ROS subscriber and the gRPC server in the same Python process so that `SharedState` is truly in-process and thread-safe.
- The adapter exposes gRPC on port `50051` (container name `ros-grpc` in compose). The backend should connect using the `GRPC_HOST` env var (default `ros-grpc:50051`).
- The previous HTTP bridge is not required for the backend in this deployment; the backend now prefers gRPC. A fallback HTTP bridge remains optional for compatibility.

This architecture enables **real-time system interaction without direct coupling between robotics middleware and user-facing applications**.
c
---

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

- **Frontend UI:**  
  [http://localhost:5173](http://localhost:5173) 

- **Backend API:**  
  [http://localhost:5000/api/chatter](http://localhost:5000/api/chatter)

- **ROS2 Bridge raw endpoint:**  


---

##  **To stop the system**

Press `Ctrl+C` in your terminal to stop all services and clean up.

Or, to stop and remove containers:
```bash
docker compose down
```

---

## 🛠 **Rebuild Images (after source code changes)**

If you change backend, frontend, or ROS2 code, rebuild and restart:
```bash
docker compose up --build
```
## Prerequisites

* **Docker**: [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)
* **Docker Compose**: [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)
* **Git**
* **Node.js 22+** *(only if building React UI locally before containerizing)*: [https://nodejs.org/](https://nodejs.org/)

---

## Tech Stack

* **Common:** Docker, Docker Compose
* **ROS 2:** Humble Hawksbill (Python talker via `rclpy`)
* **Bridge:** Python `bridge_server.py` (simple HTTP server)
* **Backend:** Flask 3.0 (dev server; swap to Gunicorn for prod)
* **Frontend:** Nginx serving static UI (React-ready)

---

## Project Structure

```text
ros2-web-bridge/
├── ros_ws/
│   ├── src/
│   │   └── py_basics/
│   │       ├── package.xml
│   │       ├── setup.py
│   │       ├── resource/py_basics
│   │       ├── launch/mvp.launch.py
│   │       └── py_basics/               
│   └── ros2.dev.Dockerfile
├── backend/
│   ├── app.py
│   └── requirements.txt
├── frontend/
│   └── index.html                        # or React build output
├── docker-compose.yml
├── .env
└── README.md
```

---

## License

MIT
