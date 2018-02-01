import time
import random

# standing posture generator

directions = ['down', 'left', 'right', 'front', 'back', 'up']

options = ['grab', 'torsion']  # grab is for hands, torsion is for the core/torso

lower_joints = ['right knee', 'right foot', 'left knee', 'left foot']  # feet cannot go down; punta di piedi?
core_joints = ['head']
left_upper_joints = ['head', 'left elbow', 'left hand', 'both hands']  # by head we mean the head top, no sacrum
right_upper_joints = ['head', 'right elbow', 'right hand', 'both hands']
# what about shoulders?

def RandomDirectionFor(joint_name):
    if 'foot' in joint_name or 'hand' in joint_name:
        return random.randint(1, len(directions) - 1)  # feet cannot go down; hands down is the default
    if 'head' in joint_name:
        return random.randint(0, len(directions) - 2)  # head up is the default
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
    left = RandomJointWithDirection(left_upper_joints)
    PrintJointAndDirection(left)
    if not 'both' in left[1]:
        while True:
            right = RandomJointWithDirection(right_upper_joints)
            if not right[1] == left[1] and not 'hand' in right[1]:
                break
        PrintJointAndDirection(right)
    print('')

# todo: sequence, only change one thing from previous posture

while True:
    PrintPosture()
    time.sleep(1)
