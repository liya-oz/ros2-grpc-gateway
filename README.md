<div>
  <img alt="License" src="https://img.shields.io/badge/license-MIT-blue">
  <img alt="Docker" src="https://img.shields.io/badge/Docker-distributed-blue?logo=docker">
  <img alt="ROS2" src="https://img.shields.io/badge/ROS2-Humble-blueviolet?logo=ros">
  <img alt="Flask" src="https://img.shields.io/badge/Flask-3.0-lightgrey?logo=flask">
  <img alt="React" src="https://img.shields.io/badge/React-19-61DAFB?logo=react">
  <img alt="Node.js" src="https://img.shields.io/badge/Node.js-22-339933?logo=nodedotjs">
</div>

# ROS2 Web Communication Bridge

**ros2-web-bridge** is a containerized prototype for **ROS2-based distributed communication and real-time state monitoring**. It demonstrates a modular architecture that decouples robot-side computation from external interfaces using a lightweight HTTP communication layer.

The system implements a layered communication design, where robot data generation, middleware transport, and visualization are separated into independent but interoperable components. 

---

## System Overview

The architecture is composed of three loosely coupled services orchestrated via **Docker Compose**:

- **ROS2 layer (robot node simulation)**  
  Runs a ROS2 *talker node* and exposes internal state through a lightweight HTTP bridge (`bridge_server.py`). This simulates a robot-side communication interface publishing `/chatter` data at `GET /latest` (port **9090** inside the network).

- **Backend layer (data aggregation interface)**  
  A Flask service that acts as a **middleware communication proxy**, polling the ROS2 bridge and exposing a stable API endpoint (`/api/chatter`, port **5000**) for external consumers.

- **Frontend layer (operator / monitoring interface)**  
  A web-based UI (React / Nginx) that consumes the backend API and visualizes real-time robot state at port **5173**.

This architecture enables **real-time system interaction without direct coupling between robotics middleware and user-facing applications**.

---

## Core Features

- **ROS2-to-Web Communication Bridge**  
  Converts ROS2 topic data into a network-accessible HTTP interface for external systems.

- **Layered Distributed Architecture**  
  Separates robot computation, communication middleware, and visualization layers.

- **Strict Decoupling of Concerns**  
  Web and backend layers remain independent of ROS2 dependencies, enabling modular system evolution.

- **Containerized Multi-Service Deployment**  
  Fully reproducible system using Docker Compose, reflecting deployment patterns used in robotic systems.

- **Extensible Communication Design**  
  New ROS2 topics or endpoints can be added without modifying higher-level application layers.

---

## Start Using

```bash
# 1) Create and configure .env file
# (Manually create a .env file with the following content)

echo 'ROS_DISTRO=humble
ROS_DOMAIN_ID=7
DEV_UID=1000
DEV_GID=1000' > .env

# 2) Build and run all services
docker compose up --build

# 3) Open in browser:
# Frontend UI
http://localhost:5173

# Backend API (proxies ROS2 message)
http://localhost:5000/api/chatter
```

> The **bridge** is available at `http://localhost:9090/latest` if you want to access it directly.

---

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
