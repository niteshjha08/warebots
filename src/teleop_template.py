#!/usr/bin/env python
import rospy


from std_msgs.msg import Float64

import sys, select, termios, tty

msg = """
Control Your Toy!
---------------------------
Moving around:
   u    i    o
   j    k    l
   m    ,    .
q/z : increase/decrease max speeds by 10%
w/x : increase/decrease only linear speed by 10%
e/c : increase/decrease only angular speed by 10%
space key, k : force stop
anything else : stop smoothly
CTRL-C to quit
"""

moveBindings = {
        'i':(1,0),
        'o':(1,-1),
        'j':(0,1),
        'l':(0,-1),
        'u':(1,1),
        ',':(-1,0),
        '.':(-1,1),
        'm':(-1,-1),
           }

speedBindings={
        'q':(1.1,1.1),
        'z':(.9,.9),
        'w':(1.1,1),
        'x':(.9,1),
        'e':(1,1.1),
        'c':(1,.9),
          }

def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

speed = 8
turn = 0.5

def vels(speed,turn):
    return "currently:\tspeed %s\tturn %s " % (speed,turn)

if __name__=="__main__":
    settings = termios.tcgetattr(sys.stdin)
    
    rospy.init_node('gantry_teleop')

    pub_h_slider = rospy.Publisher('/controller_h_slider/command', Float64, queue_size=10) # Add your topic here between ''. Eg '/my_robot/steering_controller/command'
    pub_v_slider = rospy.Publisher('/controller_v_slider/command', Float64, queue_size=10) # Add your topic for move here '' Eg '/my_robot/longitudinal_controller/command'
    pub_gripper1 = rospy.Publisher('/controller_joint1_gripper/command', Float64, queue_size=10)
    pub_gripper2 = rospy.Publisher('/controller_joint2_gripper/command', Float64, queue_size=10)
    
    x = 0
    th = 0
    status = 0
    count = 0
    acc = 0.1
    target_speed = 0
    target_turn = 0
    control_speed = 0
    control_turn = 0
    try:
        print (msg)
        print (vels(speed,turn))
        while(1):
            key = getKey()
            if key in moveBindings.keys():
                x = moveBindings[key][0]
                th = moveBindings[key][1]
                count = 0
            elif key in speedBindings.keys():
                speed = speed * speedBindings[key][0]
                turn = turn * speedBindings[key][1]
                count = 0

                print (vels(speed,turn))
                if (status == 14):
                    print (msg)
                status = (status + 1) % 15
            elif key == ' ' or key == 'k' :
                x = 0
                th = 0
                control_speed = 0
                control_turn = 0
            else:
                count = count + 1
                if count > 4:
                    x = 0
                    th = 0
                if (key == '\x03'):
                    break

            target_speed = speed * x
            target_turn = turn * th

            if target_speed > control_speed:
                control_speed = min( target_speed, control_speed + 0.1 )
            elif target_speed < control_speed:
                control_speed = max( target_speed, control_speed - 0.1 )
            else:
                control_speed = target_speed

            if target_turn > control_turn:
                control_turn = min( target_turn, control_turn + 0.1 )
            elif target_turn < control_turn:
                control_turn = max( target_turn, control_turn - 0.1 )
            else:
                control_turn = target_turn

            pub_h_slider.publish(control_turn) # publish the turn command.
            pub_v_slider.publish(control_speed) # publish the turn command.
            
            
            # pub_move_Fleft.publish(control_speed) # publish the control speed.
            # pub_move_Fright.publish(-control_speed) 
            # pub_move_Rleft.publish(control_speed) # publish the control speed.
            # pub_move_Rright.publish(-control_speed)
       


    except Exception as e:
        print (e)

    # finally:
        # pub_steer_Fright.publish(control_turn)
        # pub_steer_Fleft.publish(control_turn)
        # pub_move_Fleft.publish(control_speed)
        # pub_move_Fright.publish(control_speed)
        # pub_move_Rleft.publish(control_speed)
        # pub_move_Rright.publish(control_speed)
        # twist = Twist()
        # twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
        # twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
        # pub.publish(twist)

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)