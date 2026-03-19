import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
from turtlesim.srv import TeleportAbsolute
from functools import partial
from turtlesim.srv import SetPen
from turtlesim_controller.astar import A_Star

class Turtle_GTG(Node):
    def __init__(self):
        super().__init__("waypoint_node")

        self.client = self.create_client(TeleportAbsolute, "/turtle1/teleport_absolute")
        while not self.client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for teleport service...")

        self.pen_client = self.create_client(SetPen, "/turtle1/set_pen")
        while not self.pen_client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for set_pen service...")

        self.goal_index = 0
        self.pen_off = False
        self.disable_pen(3,1)

        self.cmd_vel_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.pose_sub = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        self.pose = Pose()


        self.grid = [
            [0, 0, 0, 1, 0],
            [0, 1, 0, 1, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 1, 1, 0],
            [1, 0, 0, 0, 0]
        ]

        self.path = A_Star(self.grid, (0,0), (4,4))
        self.world_path = [[(el*2)+0.5 for el in subpath] for subpath in self.path]


    def timer_callback(self):
        if self.goal_index >= len(self.world_path):
            self.get_logger().info("All goals reached.")
            self.timer.cancel()
            return
        x, y = self.world_path[self.goal_index]
        self.go_to_goal(x, y)


    def pose_callback(self, data):
        self.pose = data

    def go_to_goal(self,x,y):
        goal = Pose()
        goal.x = x
        goal.y = y

        new_vel = Twist()

        # Ecludian Distance
        distance_to_goal = math.sqrt( (goal.x - self.pose.x)**2  + (goal.y - self.pose.y)**2 )
        # Angle to Goal
        angle_to_goal =math.atan2(goal.y - self.pose.y , goal.x - self.pose.x)

        distance_tolerance = 0.1
        angle_tolerance = 0.01

        angle_error = angle_to_goal - self.pose.theta

        kp_linear = 1.5
        kp_angular = 4.0

        if abs(angle_error) > angle_tolerance:
            new_vel.angular.z = kp_angular * angle_error
        else :
            if( distance_to_goal ) >= distance_tolerance:
                new_vel.linear.x = kp_linear * distance_to_goal
            else :
                new_vel.linear.x= 0.0
                self.get_logger().info("Goal Reached ")
                self.goal_index+=1

        self.cmd_vel_pub.publish(new_vel)


    def call_teleport_service(self, x, y):
        request = TeleportAbsolute.Request()
        request.x = float(x)
        request.y = float(y)

        future = self.client.call_async(request)
        future.add_done_callback(partial(self.callback_teleport_turtle))

    def callback_teleport_turtle(self, future):
        try:
            response = future.result()
            self.disable_pen(3, 0)
        except Exception as e:
            self.get_logger().error("Service call failed: %r" % (e,))


    def disable_pen(self, width, off):
        request = SetPen.Request()

        request.r = 0
        request.g = 0
        request.b = 0
        request.width = width
        request.off = off
        if request.off == 1:
            self.pen_off = True



        future = self.pen_client.call_async(request)
        future.add_done_callback(partial(self.callback_pen_turtle))

    def callback_pen_turtle(self, future):
        try:
            response = future.result()
            if not self.pen_off:
                self.timer = self.create_timer(0.1, self.timer_callback)
            elif self.pen_off:
                self.pen_off = False
                self.call_teleport_service(0.5,0.5)
        except Exception as e:
            self.get_logger().error("Service call failed: %r" % (e,))


def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = Turtle_GTG()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
