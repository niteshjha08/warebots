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

### Gantry Robot
The gantry robot used in the application was modelled in SolidWorks with dimensions appropriate for boxes that will be used.
<img src="https://github.com/niteshjha08/warebots/blob/main/media/gantry_model.png" width="800">

For forward and inverse kinematics of the gantry, DH parameters are calculated.
<img src="https://github.com/niteshjha08/warebots/blob/main/media/gantry_DH.png" width="800">

Plugging the values into the DH matrix, we get this matrix:

<img src="https://github.com/niteshjha08/warebots/blob/main/media/DHtable_gantry.png" width="400">

### Manipulator Arm
The manipulator arm is taken from open-source CAD website, and used in the project.
<img src="https://github.com/niteshjha08/warebots/blob/main/media/arm_model.png" width="300">

The DH parameters of the arm are as calculated.
<img src="https://github.com/niteshjha08/warebots/blob/main/media/arm_DH.png" width="300">

Plugging the values into DH matrix, we get this:

<img src="https://github.com/niteshjha08/warebots/blob/main/media/DHtable_arm.png" width="400">

The resultant workspace of the arm is obtained at finite angle steps in the reachable workspace.

<img src="https://github.com/niteshjha08/warebots/blob/main/media/workspace_arm.png" width="800">

### Teleoperation of robots

The robot CAD models are exported into URDF (Universal Robot Description Format). To give them motion, transmission blocks are added in the URDF, and the controllers for the transmission elements are specified. Controller types for the robots depend on the requirement of that joint, it can be effort-position, effort-velocity, velocity-velocity.
The PID values of these joints are tuned by trial-error for stable motion.

When the URDFs are launched, they subscribe to the topic [namespace/joint_controller_name]/command. To teleoperate this, we create ROS nodes which publish values on these topics.
The teleoperation is done by binding keys 'w','a','s','d' with commands of motion in respective directions (front, back, down for gantry, and forward, left, right for mobile robot)

Mobile robot teleop:
<img src="https://github.com/niteshjha08/warebots/blob/main/media/warebot_teleop.gif" width="800">

Gantry robot teleop:
<img src="https://github.com/niteshjha08/warebots/blob/main/media/gantry_teleop.gif" width="800">

Manipulator arm teleop:
<img src="https://github.com/niteshjha08/warebots/blob/main/media/arm_teleop.gif" width="800">


These three teleoperations can then be coordinated to perform pick and place action as shown:

<img src="https://github.com/niteshjha08/warebots/blob/main/media/warebot_output.gif" width="800">
