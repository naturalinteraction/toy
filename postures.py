import time
import random

# standing posture generator

# GRIPE = Gestural Reduced Instruction Pose Expression
# PRI[S]PE = Postural Reduced Instruction [Standing] Pose Expression

directions = ['down', 'left', 'right', 'front', 'back', 'up']  # make sure 'down' remains only the first and 'up' remains only the last
# foot up and foot front are the same?

options = ['grab', 'torsion']  # grab is for hands, torsion is for the core/torso

lower_joints = ['right knee', 'right foot', 'right foot', 'left knee', 'left foot', 'left foot']  # feet cannot go down; punta di piedi?
core_joints = ['head']
left_upper_joints = ['head', 'left elbow', 'left hand', 'left hand', 'left hand']  # by head we mean the head top, no sacrum
right_upper_joints = ['head', 'right elbow', 'right hand', 'right hand', 'right hand']
# what about shoulders?

def RandomDirectionFor(joint_name):
    if 'foot' in joint_name or 'knee' in joint_name or 'elbow' in joint_name:
        return int(random.uniform(1, len(directions) - 0.001))  # feet cannot go down; elbow down does not make sense in most cases; hands down is the default, but could be useful in the sequence case: relax, go back to default, if previously not in default position
    if 'head' in joint_name:
        return int(random.uniform(0, len(directions) - 1.001))  # head up is the default, but could be useful in the sequence case: relax, go back to default, if previously not in default position
    return int(random.uniform(0, len(directions) - 0.001))

def DirectionName(direction):
    return directions[direction]

def JointName(joint_names, joint):
    return joint_names[joint]

def RandomJointWithDirection(joints):
    joint = int(random.uniform(0, len(joints) - 0.001))
    joint_name = JointName(joints, joint)
    direction = RandomDirectionFor(joint_name)
    direction_name = DirectionName(direction)
    return [joint, joint_name, direction, direction_name]

def PrintJointAndDirection(joint_and_direction):
    print(joint_and_direction[1] + '  >>>  ' + joint_and_direction[3])

def GenerateNewPosture(previous):
    random.seed(time.time())
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
    if True:
        while True:
            right = RandomJointWithDirection(right_upper_joints)
            if not right[1] == left[1] and not right[2] == lower[2]:  # to avoid duplicates
                break
        posture.append(right)
    for p in posture:
        PrintJointAndDirection(p)
    print('')
    return posture

def ChangeLower(previous):
    if previous == None:
        previous_lower_side = 'none'
    else:
        previous_lower_side = previous[0][1].partition(' ')[0]
    posture = previous
    while True:
        lower = RandomJointWithDirection(lower_joints)
        if not previous_lower_side in lower[1]:  # alternate between left and right leg
            break
    posture[0] = lower
    PrintJointAndDirection(lower)
    print('')
    return posture

def ChangeUpper(previous, change_left):
    posture = previous
    lower = previous[0]
    if True:  # change only one side
        posture = previous
        left = posture[1]
        right = posture[2]
        while True:
            if change_left:
                left = RandomJointWithDirection(left_upper_joints)
            else:
                right = RandomJointWithDirection(right_upper_joints) 
            if not right[1] == left[1] and ((not right[2] == lower[2] and not change_left and not right[2] == previous[2][2]) or (not left[2] == previous[1][2] and change_left and not left[2] == lower[2])):  # to avoid duplicates
                break 
        if change_left:
            posture[1] = left
        else:
            posture[2] = right
        if change_left:
            PrintJointAndDirection(left)
        else:
            PrintJointAndDirection(right)
    print('')
    return posture

last_pose_change = -1

def ChangeSomething(previous_posture):
    global last_pose_change
    last_pose_change = (last_pose_change + 1) % 3
    if last_pose_change == 0:
        return last_pose_change,ChangeLower(previous_posture)
    if last_pose_change == 1:
        return last_pose_change,ChangeUpper(previous_posture, True)
    return last_pose_change,ChangeUpper(previous_posture, False)

# mancano due gambe distese dritte verso terra
