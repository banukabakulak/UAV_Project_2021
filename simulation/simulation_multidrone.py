import airsim
import formation
import time

# connect to the AirSim simulator
from model.model_definition.Instance import Instance
from model.Optimization import Optimization

client = airsim.MultirotorClient()
client.confirmConnection()

ins = Instance()
ins.readInstance('C:/Users/ertug/OneDrive/Masaüstü/swarm2022/model/Agents.csv')
opti = Optimization()

opti.Stage1(ins)
opti.Stage2(ins)

a = ins.communicationGraph()
print(ins.distanceMatrixOfAgents(a))
print(ins.connectivity_matrix(ins.graphForBFS(a)))

f_list = []

for j in ins.Agents:
    j.printAgent()
    print('base position:', j.getBasePosition())
    print('current cell:')
    j.getCurrCell().print()
    client.enableApiControl(True, j.getName())
    client.armDisarm(True, j.getName())
    f_list.append(client.takeoffAsync(vehicle_name=j.getName()))

for c in f_list:
    c.join()

f_list.clear()

for j in ins.Agents:
    f_list.append(client.moveByVelocityAsync(0, 0, -50, 5, vehicle_name=j.getName()))

for f in f_list:
    f.join()

time.sleep(1)

f_list.clear()

for j in ins.Agents:
    f_list.append(client.moveByVelocityAsync(0, 0, 0, 1, vehicle_name=j.getName()))

for f in f_list:
    f.join()

time.sleep(1)

f_list.clear()

for j in ins.Agents:
    agent_cell_center = j.getCurrCell().getCenter()
    print(agent_cell_center)
    t = 30
    v_x = (agent_cell_center[0] - formation.drone_state(j)['x']) / t
    v_y = (agent_cell_center[1] - formation.drone_state(j)['y']) / t
    f_list.append(client.moveByVelocityAsync(v_x, v_y, 0, t, vehicle_name=j.getName()))

for f in f_list:
    f.join()

time.sleep(1)

f_list.clear()

for j in ins.Agents:
    f_list.append(client.moveByVelocityAsync(0, 0, 0, 1, vehicle_name=j.getName()))

for f in f_list:
    f.join()

time.sleep(1)


def sum_2_dim(myarray):
    sum = 0
    for i in range(len(myarray)):
        for j in range(len(myarray[0])):
            sum = sum + abs(myarray[i][j])
    return sum


def smallerThan(target_matrix, k):
    res = 0
    for i in range(len(target_matrix)):
        for j in range(len(target_matrix[0])):
            if abs(target_matrix[i][j]) <= k:
                res = res + 1

    if res == len(target_matrix) * len(target_matrix[0]):
        return True
    else:
        return False


def isMove():
    moveable = True

    targetX = [[0, -10, 10, -20], [10, 0, 0, -10], [10, 0, 0, -10], [20, 10, 10, 0]]
    targetY = [[0, 10, -10, 0], [-10, 0, -20, -10], [10, 20, 0, 10], [0, 10, -10, 0]]
    targetZ = [[0] * 4 for i in range(4)]

    errorX, errorY, errorZ = errorfunc(targetX, targetY, targetZ)

    if smallerThan(errorX, 15) and smallerThan(errorY, 15):
        moveable = False

    return moveable


def errorfunc(targetX, targetY, targetZ):
    currentX = formation.matrixX(ins)
    currentY = formation.matrixY(ins)
    currentZ = formation.matrixZ(ins)

    errorX = [[0] * 4 for i in range(4)]
    errorY = [[0] * 4 for i in range(4)]
    errorZ = [[0] * 4 for i in range(4)]

    for i in range(4):
        for j in range(4):
            errorX[i][j] = targetX[i][j] - currentX[i][j]
            errorY[i][j] = targetY[i][j] - currentY[i][j]
            errorZ[i][j] = targetZ[i][j] - currentZ[i][j]

    return errorX, errorY, errorZ


def pid_formation():
    # Drones are in their initial cells!

    targetX = [[0, -10, 10, -20], [10, 0, 0, -10], [10, 0, 0, -10], [20, 10, 10, 0]]
    targetY = [[0, 10, -10, 0], [-10, 0, -20, -10], [10, 20, 0, 10], [0, 10, -10, 0]]
    targetZ = [[0] * 4 for i in range(4)]

    prev_errorX, prev_errorY, prev_errorZ = [[0] * 4 for i in range(4)], [[0] * 4 for i in range(4)], [[0] * 4 for i in
                                                                                                       range(4)]
    f_list_for_z = []
    f_list_for_formation = []

    while isMove():
        curr_errorX, curr_errorY, curr_errorZ = errorfunc(targetX, targetY, targetZ)

        # drone_vx = 0
        # drone_vy = 0
        # drone_vz = 0

        kp = 100
        kd = 1

        for i in range(len(ins.Agents)):
            drone_vx = sum(curr_errorX[i]) * kp + kd * (sum(curr_errorX[i]) - sum(prev_errorX[i]))
            drone_vy = sum(curr_errorY[i]) * kp + kd * (sum(curr_errorY[i]) - sum(prev_errorY[i]))
            drone_vz = sum(curr_errorZ[i]) * kp + kd * (sum(curr_errorZ[i]) - sum(prev_errorZ[i]))

            f = client.moveByVelocityAsync(0, 0, 0, 0.2, vehicle_name=ins.Agents[i].getName())
            f_list_for_z.append(f)

            f = client.moveByVelocityAsync(drone_vx, drone_vy, drone_vz, 0.2, vehicle_name=ins.Agents[i].getName())
            f_list_for_formation.append(f)

        prev_errorX, prev_errorY, prev_errorZ = curr_errorX, curr_errorY, curr_errorZ

        for f in f_list_for_z:
            f.join()

        time.sleep(0.5)

        for f in f_list_for_formation:
            f.join()

        time.sleep(0.5)

        f_list_for_z.clear()
        f_list_for_formation.clear()

        for j in ins.Agents:
            if formation.drone_state(j)['z'] > 0:
                f = client.moveByVelocityAsync(0, 0, -50, 5, vehicle_name=j.getName())
                f.join()
                time.sleep(1)

    f_list_state_stabil = []

    for j in ins.Agents:
        f_list_state_stabil.append(client.moveByVelocityAsync(0, 0, 0, 1, vehicle_name=j.getName()))

    for c in f_list_state_stabil:
        c.join()

    time.sleep(1)


pid_formation()

f_list.clear()

for j in ins.Agents:
    t = 30
    v_x = (ins.Cells[0].getCenter()[0] - formation.drone_state(j)['x']) / t
    v_y = (ins.Cells[0].getCenter()[1] - formation.drone_state(j)['y']) / t
    f_list.append(client.moveByVelocityAsync(v_x, v_y, 0, t, vehicle_name=j.getName()))

for f in f_list:
    f.join()

time.sleep(1)

f_list.clear()

for j in ins.Agents:
    f_list.append(client.moveByVelocityAsync(0, 0, 0, 1, vehicle_name=j.getName()))

for f in f_list:
    f.join()

time.sleep(1)

f_list.clear()

for j in ins.Agents:
    t = 30
    v_x = (ins.Cells[9].getCenter()[0] - formation.drone_state(j)['x']) / t
    v_y = (ins.Cells[9].getCenter()[1] - formation.drone_state(j)['y']) / t
    f_list.append(client.moveByVelocityAsync(v_x, v_y, 0, t, vehicle_name=j.getName()))

for f in f_list:
    f.join()

time.sleep(1)

f_list.clear()

for j in ins.Agents:
    f_list.append(client.moveByVelocityAsync(0, 0, 0, 1, vehicle_name=j.getName()))

for f in f_list:
    f.join()

time.sleep(1)

f_list.clear()

for j in ins.Agents:
    t = 30
    v_x = (ins.Cells[10].getCenter()[0] - formation.drone_state(j)['x']) / t
    v_y = (ins.Cells[10].getCenter()[1] - formation.drone_state(j)['y']) / t
    f_list.append(client.moveByVelocityAsync(v_x, v_y, 0, t, vehicle_name=j.getName()))

for f in f_list:
    f.join()

time.sleep(1)

f_list.clear()

for j in ins.Agents:
    f_list.append(client.moveByVelocityAsync(0, 0, 0, 1, vehicle_name=j.getName()))

for f in f_list:
    f.join()

time.sleep(1)

f_list.clear()

for j in ins.Agents:
    t = 30
    v_x = (ins.Cells[19].getCenter()[0] - formation.drone_state(j)['x']) / t
    v_y = (ins.Cells[19].getCenter()[1] - formation.drone_state(j)['y']) / t
    f_list.append(client.moveByVelocityAsync(v_x, v_y, 0, t, vehicle_name=j.getName()))

for f in f_list:
    f.join()

time.sleep(1)

f_list.clear()

for j in ins.Agents:
    f_list.append(client.moveByVelocityAsync(0, 0, 0, 1, vehicle_name=j.getName()))

for f in f_list:
    f.join()

time.sleep(1)
