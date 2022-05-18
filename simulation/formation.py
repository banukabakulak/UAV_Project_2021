import airsim
from model.Instance import Instance

client = airsim.MultirotorClient()


def drone_state(drone):
    dronestate = client.getMultirotorState(vehicle_name=drone.getName()).kinematics_estimated.position
    basePosition = drone.getBasePosition()
    x_val = dronestate.x_val + float(basePosition[0])
    y_val = dronestate.y_val + float(basePosition[1])
    z_val = dronestate.z_val + float(basePosition[2])

    statedict = {
        'x': x_val,
        'y': y_val,
        'z': z_val
    }
    return statedict


def distanceX(drone1, drone2):

    drone1State = drone_state(drone1)
    drone1_x = float(drone1State['x'])

    drone2State = drone_state(drone2)
    drone2_x = float(drone2State['x'])

    dist = drone1_x - drone2_x

    return dist


def distanceY(drone1, drone2):

    drone1State = drone_state(drone1)
    drone1_y = float(drone1State['y'])

    drone2State = drone_state(drone2)
    drone2_y = float(drone2State['y'])

    dist = drone1_y - drone2_y

    return dist


def distanceZ(drone1, drone2):

    drone1State = drone_state(drone1)
    drone1_z = float(drone1State['z'])

    drone2State = drone_state(drone2)
    drone2_z = float(drone2State['z'])

    dist = drone1_z - drone2_z

    return dist


def matrixX():
    ins = Instance()
    ins.readInstance('C:/Users/ertug/OneDrive/Masaüstü/swarm2022/model/Agents.csv')

    n = len(ins.Agents)
    distance_matrix = [[0] * n for i in range(n)]

    r = 0

    for agent in ins.Agents:
        k = 0
        for agent2 in ins.Agents:
            if agent == agent2:
                distance_matrix[r][k] = 0
            else:
                distance_matrix[r][k] = distanceX(agent, agent2)
            k += 1
        r += 1

    return distance_matrix


def matrixY():
    ins = Instance()
    ins.readInstance('C:/Users/ertug/OneDrive/Masaüstü/swarm2022/model/Agents.csv')

    n = len(ins.Agents)
    distance_matrix = [[0] * n for i in range(n)]

    r = 0

    for agent in ins.Agents:
        k = 0
        for agent2 in ins.Agents:
            if agent == agent2:
                distance_matrix[r][k] = 0
            else:
                distance_matrix[r][k] = distanceY(agent, agent2)
            k += 1
        r += 1

    return distance_matrix


def matrixZ():
    ins = Instance()
    ins.readInstance('C:/Users/ertug/OneDrive/Masaüstü/swarm2022/model/Agents.csv')

    n = len(ins.Agents)
    distance_matrix = [[0] * n for i in range(n)]

    r = 0

    for agent in ins.Agents:
        k = 0
        for agent2 in ins.Agents:
            if agent == agent2:
                distance_matrix[r][k] = 0
            else:
                distance_matrix[r][k] = distanceZ(agent, agent2)
            k += 1
        r += 1

    return distance_matrix

