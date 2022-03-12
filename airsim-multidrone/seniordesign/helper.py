import airsim
import pprint
import math

client = airsim.MultirotorClient()


def drone_state(drone, x, y, z):
    dronestate = client.getMultirotorState(vehicle_name=drone).kinematics_estimated.position
    x_val = dronestate.x_val + x
    y_val = dronestate.y_val + y
    z_val = dronestate.z_val + z

    statedict = {
        'x': x_val,
        'y': y_val,
        'z': z_val
    }
    return statedict


def distance(drone1, x1, y1, z1, drone2, x2, y2, z2):
    drone1State = drone_state(drone1, x1, y1, z1)
    drone1_x = float(drone1State['x'])
    drone1_y = float(drone1State['y'])
    drone1_z = float(drone1State['z'])

    drone2State = drone_state(drone2, x2, y2, z2)
    drone2_x = float(drone2State['x'])
    drone2_y = float(drone2State['y'])
    drone2_z = float(drone2State['z'])

    dist_1_2 = math.sqrt(
        math.pow(drone1_x - drone2_x, 2) + math.pow(drone1_y - drone2_y, 2) + math.pow(drone1_z - drone2_z, 2))

    return dist_1_2


def distanceX(drone1, x1, y1, z1, drone2, x2, y2, z2):
    if drone1 == 'Drone0':
        x1 = 0
        y1 = 0
        z1 = 0
    elif drone2 == 'Drone0':
        x2 = 0
        y2 = 0
        z2 = 0
    elif drone1 == 'Drone1':
        x1 = 30
        y1 = 30
        z1 = 0
    elif drone2 == 'Drone1':
        x2 = 30
        y2 = 30
        z2 = 0
    elif drone1 == 'Drone2':
        x1 = 50
        y1 = 60
        z1 = 0
    elif drone2 == 'Drone2':
        x2 = 50
        y2 = 60
        z2 = 0
    elif drone1 == 'Drone3':
        x1 = 0
        y1 = 60
        z1 = 0
    elif drone2 == 'Drone3':
        x2 = 0
        y2 = 60
        z2 = 0
    drone1State = drone_state(drone1, x1, y1, z1)
    drone1_x = float(drone1State['x'])

    drone2State = drone_state(drone2, x2, y2, z2)
    drone2_x = float(drone2State['x'])

    dist = drone2_x - drone1_x

    return dist


def distanceY(drone1, x1, y1, z1, drone2, x2, y2, z2):
    if drone1 == 'Drone0':
        x1 = 0
        y1 = 0
        z1 = 0
    elif drone2 == 'Drone0':
        x2 = 0
        y2 = 0
        z2 = 0
    elif drone1 == 'Drone1':
        x1 = 30
        y1 = 30
        z1 = 0
    elif drone2 == 'Drone1':
        x2 = 30
        y2 = 30
        z2 = 0
    elif drone1 == 'Drone2':
        x1 = 50
        y1 = 60
        z1 = 0
    elif drone2 == 'Drone2':
        x2 = 50
        y2 = 60
        z2 = 0
    elif drone1 == 'Drone3':
        x1 = 0
        y1 = 60
        z1 = 0
    elif drone2 == 'Drone3':
        x2 = 0
        y2 = 60
        z2 = 0
    drone1State = drone_state(drone1, x1, y1, z1)
    drone1_y = float(drone1State['y'])

    drone2State = drone_state(drone2, x2, y2, z2)
    drone2_y = float(drone2State['y'])

    dist = drone2_y - drone1_y

    return dist


def distanceZ(drone1, x1, y1, z1, drone2, x2, y2, z2):
    if drone1 == 'Drone0':
        x1 = 0
        y1 = 0
        z1 = 0
    elif drone2 == 'Drone0':
        x2 = 0
        y2 = 0
        z2 = 0
    elif drone1 == 'Drone1':
        x1 = 30
        y1 = 30
        z1 = 0
    elif drone2 == 'Drone1':
        x2 = 30
        y2 = 30
        z2 = 0
    elif drone1 == 'Drone2':
        x1 = 50
        y1 = 60
        z1 = 0
    elif drone2 == 'Drone2':
        x2 = 50
        y2 = 60
        z2 = 0
    elif drone1 == 'Drone3':
        x1 = 0
        y1 = 60
        z1 = 0
    elif drone2 == 'Drone3':
        x2 = 0
        y2 = 60
        z2 = 0
    drone1State = drone_state(drone1, x1, y1, z1)
    drone1_z = float(drone1State['z'])

    drone2State = drone_state(drone2, x2, y2, z2)
    drone2_z = float(drone2State['z'])

    dist = drone2_z - drone1_z

    return dist


def matrixX():
    n = 4
    distance_matrix = [[0] * n for i in range(n)]

    for r in range(4):
        for k in range(4):
            if r == k:
                distance_matrix[r][k] = 0
            else:
                distance_matrix[r][k] = distanceX(("Drone" + str(r)), 0, 0, 0, ("Drone" + str(k)), 0, 0, 0)

    return distance_matrix


def matrixY():
    n = 4
    distance_matrix = [[0] * n for i in range(n)]

    for r in range(4):
        for k in range(4):
            if r == k:
                distance_matrix[r][k] = 0
            else:
                distance_matrix[r][k] = distanceY(("Drone" + str(r)), 0, 0, 0, ("Drone" + str(k)), 0, 0, 0)

    return distance_matrix


def matrixZ():
    n = 4
    distance_matrix = [[0] * n for i in range(n)]

    for r in range(4):
        for k in range(4):
            if r == k:
                distance_matrix[r][k] = 0
            else:
                distance_matrix[r][k] = distanceZ(("Drone" + str(r)), 0, 0, 0, ("Drone" + str(k)), 0, 0, 0)

    return distance_matrix
