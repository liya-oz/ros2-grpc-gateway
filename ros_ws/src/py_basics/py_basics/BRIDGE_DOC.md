## ROS2 - HTTP Bridge (Flask)

This bridge is a translator between ROS2 and the Web. It runs inside the ROS2 container and:

- Subscribes to one or more ROS2 topics (any message type)
- Stores the latest message for each topic
- Exposes them via an **HTTP REST API** (Flask)(JSON output)

## This way, non-ROS applications can fetch ROS2 data **without installing ROS2**.

## ⚙️ How it works

### 1. Subscriptions

- The `BridgeNode` class creates subscriptions to all topics listed in the `topics` array.
- Each subscription has a callback that saves the most recent message in the `latest_msgs` dictionary.
- Messages are converted into **JSON-friendly dictionaries** using:

```python
from rosidl_runtime_py import message_to_ordereddict
```

This preserves the original message structure (nested fields, arrays).

---

### 2. Storage

`latest_msgs` is a global dictionary:

```python
latest_msgs = {
  "/talker": {"data": "Hello"},
  "/cmd_vel": {"linear": {...}, "angular": {...}},
  ...
}
```

---

### 3. HTTP API

```json
{
  "/chatter": { "data": "Hello #1" }
}
```

---

### 4. Parallel execution

- **ROS2** collects messages and stores them in a dictionary.
- **Flask** serves them on request.

They run in **separate threads**

---

## Safety Notes

- Uses `rosidl_runtime_py.message_to_ordereddict` (official ROS2 utility).
- Safe: only converts message fields to dict, no code execution.
- Do **not** expose port `9090` publicly without protection.

ROS2 (bridge) <--internal--> Backend API <--external--> Frontend / Users

---
