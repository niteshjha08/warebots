# WareBots: Warehouse Robotic Automation System
This project aims to model and simulate working of multiple robots in coordination to accomplish tasks which commonly occur in warehouses such as pick-and-place, packaging, labelling, etc.

### Instructions to run:
1. Clone the repo into catkin workspace's src.
2. Run `catkin_make`
3. Launch warehouse world by running : `roslaunch gantry_assembly_v2 warehouse.launch`
4. Control mobile robot by running : `python3 warebot_teleop.py`
5. Control gantry robot by running : `python3 gantry_teleop.py`
6. Control manipulator arm by running : `python3 arm_teleop.py`

### Robots
The choice of robots in the system is done considering the following:
- As different stations in the warehouse can be far apart, a mobile robot will be required to connect the workflow between these stations. Thus, a mobile robot with a flat top was modeled for this purpose.
- As most packages are cuboidal, a fixed structure with a mobile arm (cuboidal workspace) is suitable for beginning the warehousing task. Thus, a gantry robot was modeled for this purpose.
- At the offloading point, a number of actions can be required such as simple offloading, packing, printing. Thus, we would need more flexibility in degrees of freedom at one end of the workflow. Hence a manipulator arm was selected.

