# ROS2 Turtlesim Path Planning Project
![output-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/a929e0f9-31f0-44ee-a952-17da72b430d0)
## Description
This project demonstrates **path planning and navigation in ROS2 using Turtlesim**.  
It uses the **A\* algorithm** to plan a path on a grid, spawns turtles as obstacles, and moves a turtle along the computed path while avoiding obstacles.

**Features:**
- Spawn turtles at predefined obstacles.
- Compute the shortest path from start to goal using A\*.
- Move the turtle with smooth velocity control (`cmd_vel`) toward each waypoint.
- Optional pen control to visualize movement.

---

## Prerequisites
- ROS2 Humble
- Python 3.x
- `turtlesim` package installed

```bash
sudo apt install ros-humble-turtlesim
```

## Installation / Setup
```bash
# Clone the repository
git clone https://github.com/Opolalala/ros2-turtlesim-a-star-navigation

# Install dependencies
cd ros2_ws
rosdep install --from-paths src --ignore-src -r -y

# Build and source the workspace
colcon build
source install/setup.bash
```

## Running the Project
**Spawn Obstacle Turtles**
```bash
ros2 run turtlesim_controller spawn_node
```
**Move Turtle Along Path**
```bash
ros2 run turtlesim_controller waypoint_node
```

## Grid Configuration

The grid is a 2D list where:

0 → free cell

1 → obstacle

Example:
```bash
grid = [
    [0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 1, 1, 0],
    [1, 0, 0, 0, 0]
]
```
## Dependencies
- rclpy
- turtlesim
- geometry_msgs
- functools (built-in)
