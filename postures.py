import time
import random

# standing posture generator

# todo: voice commands

directions = ['down', 'left', 'right', 'front', 'back', 'up']  # make sure 'down' remains only the first and 'up' remains only the last
# foot up and foot front are the same?

options = ['grab', 'torsion']  # grab is for hands, torsion is for the core/torso

lower_joints = ['right knee', 'right foot', 'left knee', 'left foot']  # feet cannot go down; punta di piedi?
core_joints = ['head']
left_upper_joints = ['head', 'left elbow', 'left hand', 'left hand', 'both hands']  # by head we mean the head top, no sacrum
right_upper_joints = ['head', 'right elbow', 'right hand', 'right hand', 'both hands']
# what about shoulders?

def RandomDirectionFor(joint_name):
    if 'foot' in joint_name or 'hand' in joint_name or 'elbow' in joint_name:
        return random.randint(1, len(directions) - 1)  # feet cannot go down; elbow down does not make sense in most cases; hands down is the default, but could be useful in the sequence case: relax, go back to default, if previously not in default position
    if 'head' in joint_name:
        return random.randint(0, len(directions) - 2)  # head up is the default, but could be useful in the sequence case: relax, go back to default, if previously not in default position
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

def GenerateNewPosture(previous):
    if previous == None:
        previous_lower_side = 'none'
    else:
        previous_lower_side = previous[0][1].partition(' ')[0]
    posture = []
    while True:
        lower = RandomJointWithDirection(lower_joints)
        if not previous_lower_side in lower[1]:  # alternate between left and right leg
            break
    posture.append(lower)
    while True:
        left = RandomJointWithDirection(left_upper_joints)
        if not left[2] == lower[2]:  # to avoid too many limbs in the same direction
            break
    posture.append(left)
    if not 'both' in left[1]:
        while True:
            right = RandomJointWithDirection(right_upper_joints)
            if not right[1] == left[1] and not right[2] == left[2] and not right[2] == lower[2] and not 'both' in right[1]:  # to avoid duplicates
                break
        posture.append(right)
    for p in posture:
        PrintJointAndDirection(p)
    print('')
    return posture

# todo: sequence, only change one thing from previous posture

previous_posture = None
while True:
    previous_posture = GenerateNewPosture(previous_posture)
    time.sleep(0.1)
