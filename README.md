# warebots
Using mobile robots, gantry robots and manipulator arms for pick and place in warehouse setting

### Instructions to run:
1. Clone the repo into catkin workspace's src.
2. Run `catkin_make`
3. Launch warehouse world by running : `roslaunch gantry_assembly_v2 warehouse.launch`
4. Control mobile robot by running : `python3 warebot_teleop.py`
5. Control gantry robot by running : `python3 gantry_teleop.py`
6. Control manipulator arm by running : `python3 arm_teleop.py`
