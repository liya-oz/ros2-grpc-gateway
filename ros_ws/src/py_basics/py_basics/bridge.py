import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from flask import Flask, jsonify
from threading import Thread, Lock
from rosidl_runtime_py import message_to_ordereddict

# a simple in-memory storage for the latest messages
latest_msgs = {}
_latest_lock = Lock()  # to avoid race conditions when accessing latest_msgs

class BridgeNode(Node):
    def __init__(self, topics):
        super().__init__('bridge_node')
        # universal subscription to multiple topics
        for topic, msg_type in topics:
            self.create_subscription(msg_type, topic, self._make_callback(topic), 10)

    def _make_callback(self, topic):
        def callback(msg):
            # store the latest message as JSON-friendly dict (works for complex msgs too)
            data = message_to_ordereddict(msg)
            with _latest_lock:
                latest_msgs[topic] = data
        return callback

app = Flask(__name__)

@app.route('/latest/<path:topic>', methods=['GET'])
def get_latest(topic):
    topic = "/" + topic
    with _latest_lock:
        return jsonify({topic: latest_msgs.get(topic, {})})

def main():
    rclpy.init()

    topics = [
        ("/chatter", String),
        # ("/odom", Odometry),
        # ("/etc", etc...),
    ]

    node = BridgeNode(topics)

    Thread(target=lambda: rclpy.spin(node), daemon=True).start()

    app.run(host="0.0.0.0", port=9090)

if __name__ == "__main__":
    main()
