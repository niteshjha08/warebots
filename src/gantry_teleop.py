#!/usr/bin/env python
import rospy


from std_msgs.msg import Float64

import sys, select, termios, tty
from gantry_assembly_v2.srv import Attach, AttachRequest, AttachResponse

msg = """
Control The Gantry!
---------------------------
Moving around:
        i    
   j    k    l
        ,  
      g  , f : to open/close grip  
q/z : increase/decrease max speeds by 10%
w/x : increase/decrease only linear speed by 10%
e/c : increase/decrease only angular speed by 10%
space key, k : force stop
anything else : stop smoothly
CTRL-C to quit
"""
moveBindings = {
        'i':(1,0,0),
        'j':(0,1,0),
        'l':(0,-1,0),
        ',':(-1,0,0),
        'g':(0,0,1),
        'f':(0,0,-1)
           }

speedBindings={
        'q':(1.1,1.1),
        'z':(.9,.9),
        'w':(1.1,1),
        'x':(.9,1),
        'e':(1,1.1),
        'c':(1,.9),
          }

z_low_lim=-0.80
z_upper_lim=-0.02
curr_z=-0.02

gripper_low_lim=-0.55601
gripper_upper_lim=0
curr_gripper=0


def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def vels(speed,turn):
    return "currently:\tspeed %s\tturn %s " % (speed,turn)

speed=8
turn=0.5
curr_z=-0.02
curr_gripper=0
if __name__=="__main__":
    x=0
    z=0
   
    gripper=0
    count = 0
    settings = termios.tcgetattr(sys.stdin)
    
    rospy.init_node('gantry_teleop')
    # attach_srv = rospy.ServiceProxy('/link_attacher_node/attach',
    #                                 Attach)
    # attach_srv.wait_for_service()
    # rospy.loginfo("Created ServiceProxy to /link_attacher_node/attach")
    # # Link them
    # rospy.loginfo("Attaching gripper_base and box")
    # req = AttachRequest()
    # req.model_name_1 = "gantry_assembly_v2"
    # req.link_name_1 = "gripper_1"
    # req.model_name_2 = "unit_box"
    # req.link_name_2 = "link"

    # attach_srv.call(req)

    pub_h_slider = rospy.Publisher('/controller_h_slider/command', Float64, queue_size=10) # Add your topic here between ''. Eg '/my_robot/steering_controller/command'
    pub_v_slider = rospy.Publisher('/controller_v_slider/command', Float64, queue_size=10) # Add your topic for move here '' Eg '/my_robot/longitudinal_controller/command'
    pub_gripper1 = rospy.Publisher('/controller_joint1_gripper/command', Float64, queue_size=10)
    pub_gripper2 = rospy.Publisher('/controller_joint2_gripper/command', Float64, queue_size=10)
    
    
    try:
        print (msg)
        print (vels(speed,turn))
        while(1):
            key = getKey()
            if key in moveBindings.keys():
                x = moveBindings[key][0]
                z = moveBindings[key][1]
                gripper=moveBindings[key][2]
                count = 0
            elif key in speedBindings.keys():
                speed = speed * speedBindings[key][0]
                turn = turn * speedBindings[key][1]
                count = 0
            elif key == ' ' or key == 'k' :
                x = 0
                z = 0
                gripper=0
                control_speed = 0
                control_turn = 0
            else:
                count = count + 1
                if count > 4:
                    x = 0
                    z = 0
                    gripper=0
                if (key == '\x03'):
                    break
            if(key=='l' or key == 'L'):
                # l lowers it, j raises it
                if(curr_z>z_low_lim):
                    curr_z-=0.01
                else:
                    curr_z=z_low_lim

            if(key=='j' or key == 'J'):
                # l lowers it, j raises it
                if(curr_z<z_upper_lim):
                    curr_z+=0.01
                else:
                    curr_z=z_upper_lim

            if(key=='g' or key == 'g'):
                # l lowers it, j raises it
                if(curr_gripper>gripper_low_lim):
                    curr_gripper-=0.01
                else:
                    curr_gripper=gripper_low_lim
            
            if(key=='f' or key == 'f'):
                # l lowers it, j raises it
                if(curr_gripper<gripper_upper_lim):
                    curr_gripper+=0.01
                else:
                    curr_gripper=gripper_upper_lim

            if(key=='a' or key=='A'):
                attach_srv = rospy.ServiceProxy('/link_attacher_node/attach',
                                                Attach)
                attach_srv.wait_for_service()
                rospy.loginfo("Created ServiceProxy to /link_attacher_node/attach")
                # Link them
                rospy.loginfo("Attaching gripper_base and box")
                req = AttachRequest()
                req.model_name_1 = "gantry_assembly"
                req.link_name_1 = "gripper_1"
                req.model_name_2 = "unit_box"
                req.link_name_2 = "link"

                attach_srv.call(req)

            if(key=='a' or key=='A'):
                attach_srv = rospy.ServiceProxy('/link_attacher_node/attach',
                                                Attach)
                attach_srv.wait_for_service()
                rospy.loginfo("Created ServiceProxy to /link_attacher_node/attach")
                # Link them
                rospy.loginfo("Attaching gripper_base and box")
                req = AttachRequest()
                req.model_name_1 = "gantry_assembly"
                req.link_name_1 = "gripper_1"
                req.model_name_2 = "unit_box"
                req.link_name_2 = "link"

                attach_srv.call(req)

            if(key=='d' or key=='D'):
                attach_srv = rospy.ServiceProxy('/link_attacher_node/detach',
                                    Attach)
                attach_srv.wait_for_service()
                rospy.loginfo("Created ServiceProxy to /link_attacher_node/detach")

                # Link them
                rospy.loginfo("Detaching cube1 and cube2")
                req = AttachRequest()
                req.model_name_1 = "gantry_assembly"
                req.link_name_1 = "gripper_1"
                req.model_name_2 = "unit_box"
                req.link_name_2 = "link"

                attach_srv.call(req)

                    

            pub_v_slider.publish(curr_z)
            # print("Current z: ",curr_z)
            pub_h_slider.publish(x*10)
            # pub_v_slider.publish(z*1)
            pub_gripper1.publish(curr_gripper)
            pub_gripper2.publish(curr_gripper)
            # print("x:",x," z: ",z,' g: ',gripper)
    except Exception as e:
        print (e)

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)