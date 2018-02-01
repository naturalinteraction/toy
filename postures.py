import time
import random

directions = ['down', 'up', 'left', 'right', 'front', 'back']

options = ['grab', 'torsion']  # grab is for hands, torsion is for the core/torso

lower_joints = ['right knee', 'right foot', 'left knee', 'left foot']  # feet cannot go down
core_joints = ['head', 'sacrum']  # by head we mean the head top
left_arm_joints = ['left elbow', 'left hand']
right_arm_joints = ['right elbow', 'right hand']
# what about shoulders?

def RandomDirectionFor(joint_name):
    if 'foot' in joint_name:
            return random.randint(1, len(directions) - 1)  # feet cannot go down
    return random.randint(0, len(directions) - 1)

def DirectionName(direction):
    return directions[direction]

def JointName(joint_names, joint):
    return joint_names[joint]

def RandomJointWithDirection(joints):
    joint = random.randint(0, len(joints) - 1)
    joint_name = JointName(joints, joint)
    direction = RandomDirectionFor(joint_name)
    direction_name = DirectionName(direction)
    return [joint, joint_name, direction, direction_name]

def PrintJointAndDirection(joint_and_direction):
    print(joint_and_direction[1] + '  >>>  ' + joint_and_direction[3])

def PrintPosture():
    PrintJointAndDirection(RandomJointWithDirection(lower_joints))
    PrintJointAndDirection(RandomJointWithDirection(core_joints))
    PrintJointAndDirection(RandomJointWithDirection(left_arm_joints))
    PrintJointAndDirection(RandomJointWithDirection(right_arm_joints))
    print('')

while True:
    PrintPosture()
    time.sleep(1)
