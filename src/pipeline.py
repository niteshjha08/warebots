import rospy
from std_msgs.msg import Float64
rospy.init_node('warebot_teleop')

pub_steer_Fright = rospy.Publisher('/mobile_robot_group/controller_FR_steer/command', Float64, queue_size=10) # Add your topic here between ''. Eg '/my_robot/steering_controller/command'
pub_steer_Fleft = rospy.Publisher('/mobile_robot_group/controller_FL_steer/command', Float64, queue_size=10)

pub_move_Fleft = rospy.Publisher('/mobile_robot_group/controller_FL_drive/command', Float64, queue_size=10) # Add your topic for move here '' Eg '/my_robot/longitudinal_controller/command'
pub_move_Fright = rospy.Publisher('/mobile_robot_group/controller_FR_drive/command', Float64, queue_size=10)
pub_move_Rright = rospy.Publisher('/mobile_robot_group/controller_RR_drive/command', Float64, queue_size=10)
pub_move_Rleft = rospy.Publisher('/mobile_robot_group/controller_RL_drive/command', Float64, queue_size=10)

def left_turn():
    rate=rospy.Rate(1)
    count=0
    for i in range(4):
    # while(True):
        print("inside loop")
        pub_steer_Fright.publish(3)
        pub_steer_Fleft.publish(3)

        pub_move_Rleft.publish(6)
        pub_move_Rright.publish(-6)
        count+=1
        print(count)
        rate.sleep()
    pub_steer_Fright.publish(0.0)
    pub_steer_Fleft.publish(0.0)

    pub_move_Rleft.publish(0.0)
    pub_move_Rright.publish(0.0)

def right_turn():
    print("Turning Left")
    count=0
    rate=rospy.Rate(1)
    for i in range(5):
    # while(True):
        print("inside loop")
        pub_steer_Fleft.publish(-3)
        pub_steer_Fright.publish(-3)
        

        pub_move_Rleft.publish(6)
        pub_move_Rright.publish(-6)
        count+=1
        print(count)
        rate.sleep()
    pub_steer_Fright.publish(0.0)
    pub_steer_Fleft.publish(0.0)

    pub_move_Rleft.publish(0.0)
    pub_move_Rright.publish(0.0)

def move_forward(val):
    print("Moving Forward")
    rate=rospy.Rate(1)
    for i in range(val):
        pub_move_Rleft.publish(6)
        pub_move_Rright.publish(-6)
        pub_steer_Fright.publish(0.0)
        pub_steer_Fleft.publish(0.0)
        rate.sleep()
    pub_move_Rleft.publish(0.0)
    pub_move_Rright.publish(0.0)
    pub_steer_Fright.publish(0.0)
    pub_steer_Fleft.publish(0.0)

# left_turn()
# right_turn()
# move_forward(10)

if __name__=="__main__":
    move_forward(10)
    right_turn()
