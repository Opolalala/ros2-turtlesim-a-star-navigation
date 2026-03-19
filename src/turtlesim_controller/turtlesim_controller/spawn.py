#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from turtlesim.srv import Spawn
from turtlesim.srv import SetPen
from functools import partial
import time

class MyNode(Node):
    def __init__(self):
        super().__init__("spawn_node")
        self.client = self.create_client(Spawn, "/spawn")
        while not self.client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for service...")

        self.pen_client = self.create_client(SetPen, '/turtle1/set_pen')
        while not self.pen_client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for pen service...")


        self.grid = [
            [0, 0, 0, 1, 0],
            [0, 1, 0, 1, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 1, 1, 0],
            [1, 0, 0, 0, 0]
        ]

        self.counter = 0
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if self.grid[row][col] == 1:
                    self.get_logger().info(f"{row} , {col}")
                    self.call_spawn_service((row*2)+0.5, (col*2)+0.5, f"turtle_{self.counter}")
                    time.sleep(0.1)
                    self.counter +=1


    def call_spawn_service(self, x, y, name):

        request = Spawn.Request()
        request.x = float(x)
        request.y = float(y)
        request.name = name

        future = self.client.call_async(request)
        future.add_done_callback(partial(self.callback_spawn_turtle))

    def callback_spawn_turtle(self, future):
        try:
            response = future.result()
        except Exception as e:
            self.get_logger().error("Service call failed: %r" % (e,))


def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
