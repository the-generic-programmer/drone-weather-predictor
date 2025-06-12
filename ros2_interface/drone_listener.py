import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import pandas as pd
from datetime import datetime
import os

LOG_PATH = "../data/drone_logs.csv"

class DroneListener(Node):
    def __init__(self):
        super().__init__('drone_listener')
        self.subscription = self.create_subscription(
            String,
            'drone_data',
            self.listener_callback,
            10
        )
        self.subscription  # prevent unused variable warning
        self.init_log()
        self.get_logger().info("Drone listener initialized and waiting for messages...")

    def init_log(self):
        if not os.path.exists(LOG_PATH):
            pd.DataFrame(columns=['timestamp', 'latitude', 'longitude', 'altitude', 'speed', 'heading', 'temperature', 'humidity']).to_csv(LOG_PATH, index=False)
            self.get_logger().info("Log file created.")

    def listener_callback(self, msg):
        try:
            parts = msg.data.split(',')
            if len(parts) != 7:
                raise ValueError("Malformed message")

            entry = {
                'timestamp': datetime.utcnow().isoformat(),
                'latitude': float(parts[0]),
                'longitude': float(parts[1]),
                'altitude': float(parts[2]),
                'speed': float(parts[3]),
                'heading': float(parts[4]),
                'temperature': float(parts[5]),
                'humidity': float(parts[6]),
            }

            df = pd.DataFrame([entry])
            df.to_csv(LOG_PATH, mode='a', header=False, index=False)
            self.get_logger().info(f"Logged: {entry}")

        except Exception as e:
            self.get_logger().error(f"Error parsing message: {msg.data} | {e}")


def main(args=None):
    rclpy.init(args=args)
    node = DroneListener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
