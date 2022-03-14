import airsim

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


def distanceX(drone1, x1, y1, z1, drone2, x2, y2, z2):
    if drone1 == 'Drone0':
        x1 = 10
        y1 = 10
        z1 = 0
    elif drone2 == 'Drone0':
        x2 = 10
        y2 = 10
        z2 = 0
    elif drone1 == 'Drone1':
        x1 = 20
        y1 = 20
        z1 = 0
    elif drone2 == 'Drone1':
        x2 = 20
        y2 = 20
        z2 = 0
    elif drone1 == 'Drone2':
        x1 = 10
        y1 = 20
        z1 = 0
    elif drone2 == 'Drone2':
        x2 = 10
        y2 = 20
        z2 = 0
    elif drone1 == 'Drone3':
        x1 = 20
        y1 = 10
        z1 = 0
    elif drone2 == 'Drone3':
        x2 = 20
        y2 = 10
        z2 = 0
    drone1State = drone_state(drone1, x1, y1, z1)
    drone1_x = float(drone1State['x'])

    drone2State = drone_state(drone2, x2, y2, z2)
    drone2_x = float(drone2State['x'])

    dist = drone1_x - drone2_x

    return dist

def distanceY(drone1, x1, y1, z1, drone2, x2, y2, z2):
    if drone1 == 'Drone0':
        x1 = 10
        y1 = 10
        z1 = 0
    elif drone2 == 'Drone0':
        x2 = 10
        y2 = 10
        z2 = 0
    elif drone1 == 'Drone1':
        x1 = 20
        y1 = 20
        z1 = 0
    elif drone2 == 'Drone1':
        x2 = 20
        y2 = 20
        z2 = 0
    elif drone1 == 'Drone2':
        x1 = 10
        y1 = 20
        z1 = 0
    elif drone2 == 'Drone2':
        x2 = 10
        y2 = 20
        z2 = 0
    elif drone1 == 'Drone3':
        x1 = 20
        y1 = 10
        z1 = 0
    elif drone2 == 'Drone3':
        x2 = 20
        y2 = 10
        z2 = 0
    drone1State = drone_state(drone1, x1, y1, z1)
    drone1_y = float(drone1State['y'])

    drone2State = drone_state(drone2, x2, y2, z2)
    drone2_y = float(drone2State['y'])

    dist = drone1_y - drone2_y

    return dist


def distanceZ(drone1, x1, y1, z1, drone2, x2, y2, z2):
    if drone1 == 'Drone0':
        x1 = 10
        y1 = 10
        z1 = 0
    elif drone2 == 'Drone0':
        x2 = 10
        y2 = 10
        z2 = 0
    elif drone1 == 'Drone1':
        x1 = 20
        y1 = 20
        z1 = 0
    elif drone2 == 'Drone1':
        x2 = 20
        y2 = 20
        z2 = 0
    elif drone1 == 'Drone2':
        x1 = 10
        y1 = 20
        z1 = 0
    elif drone2 == 'Drone2':
        x2 = 10
        y2 = 20
        z2 = 0
    elif drone1 == 'Drone3':
        x1 = 20
        y1 = 10
        z1 = 0
    elif drone2 == 'Drone3':
        x2 = 20
        y2 = 10
        z2 = 0
    drone1State = drone_state(drone1, x1, y1, z1)
    drone1_z = float(drone1State['z'])

    drone2State = drone_state(drone2, x2, y2, z2)
    drone2_z = float(drone2State['z'])

    dist = drone1_z - drone2_z

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


