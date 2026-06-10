import threading
import time
from typing import Dict, Any


class SharedState:

    def __init__(self):
        self.lock = threading.Lock()

        self.shared_data: Dict[str, Any] = {
            "chatter_latest": {
                "data": "",
                "seq": 0,
                "timestamp": 0.0,
            }
        }

    def update_chatter(self, data: str, seq: int):
        """Update latest ROS message"""
        with self.lock:
            self.shared_data["chatter_latest"].update({
                "data": data,
                "seq": seq,
                "timestamp": time.time(),
            })

    def get_chatter(self) -> dict:
        """Get latest chatter message"""
        with self.lock:
            return self.shared_data["chatter_latest"].copy()

    def update(self, key: str, value: dict):
        with self.lock:
            self.shared_data[key] = value
    
    def get(self, key: str) -> dict:
        with self.lock:
            return self.shared_data.get(key, {}).copy()


# Module-level singleton for in-process sharing
shared = SharedState()