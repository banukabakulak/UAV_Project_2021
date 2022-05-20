import airsim
import formation
import time
import multiprocessing

# connect to the AirSim simulator
from model.Optimization import Optimization

client = airsim.MultirotorClient()
client.confirmConnection()


opti = Optimization()
opti.Stage1()
chosen_list = opti.chosen_drones()

f_list = []

for j in chosen_list:
    j.printAgent()
    client.enableApiControl(True, j.getName())
    client.armDisarm(True, j.getName())
    f_list.append(client.takeoffAsync(vehicle_name=j.getName()))

for c in f_list:
    c.join()

f_list.clear()

for j in chosen_list:
    f_list.append(client.moveByVelocityAsync(0, 0, -20, 5, vehicle_name=j.getName()))

for f in f_list:
    f.join()


"""
# airsim.wait_key('Press any key to takeoff')
f0 = client.takeoffAsync(vehicle_name="Drone0")
f1 = client.takeoffAsync(vehicle_name="Drone1")
f2 = client.takeoffAsync(vehicle_name="Drone2")
f3 = client.takeoffAsync(vehicle_name="Drone3")

f0.join()
f1.join()
f2.join()
f3.join()

f0 = client.moveByVelocityAsync(0, 0, -20, 5, vehicle_name="Drone0")
f1 = client.moveByVelocityAsync(0, 0, -20, 5, vehicle_name="Drone1")
f2 = client.moveByVelocityAsync(0, 0, -20, 5, vehicle_name="Drone2")
f3 = client.moveByVelocityAsync(0, 0, -20, 5, vehicle_name="Drone3")

f0.join()
f1.join()
f2.join()
f3.join()

targetX = [[0, -10, 10, -20], [10, 0, 0, -10], [10, 0, 0, -10], [20, 10, 10, 0]]
targetY = [[0, 10, -10, 0], [-10, 0, -20, -10], [10, 20, 0, 10], [0, 10, -10, 0]]
targetZ = [[0] * 4 for i in range(4)]


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

    

    if smallerThan(errorX, 13) and smallerThan(errorY, 13):
        moveable = False

    return moveable


def errorfunc(targetX, targetY, targetZ):
    currentX = formation.matrixX()
    currentY = formation.matrixY()
    currentZ = formation.matrixZ()

    errorX = [[0] * 4 for i in range(4)]
    errorY = [[0] * 4 for i in range(4)]
    errorZ = [[0] * 4 for i in range(4)]

    for i in range(4):
        for j in range(4):
            errorX[i][j] = targetX[i][j] - currentX[i][j]
            errorY[i][j] = targetY[i][j] - currentY[i][j]
            errorZ[i][j] = targetZ[i][j] - currentZ[i][j]

    return errorX, errorY, errorZ


prev_errorX, prev_errorY, prev_errorZ = [[0] * 4 for i in range(4)], [[0] * 4 for i in range(4)], [[0] * 4 for i in
                                                                                                   range(4)]

while isMove():
    curr_errorX, curr_errorY, curr_errorZ = errorfunc(targetX, targetY, targetZ)

    drone0_vx = 0
    drone0_vy = 0
    drone0_vz = 0

    drone1_vx = 0
    drone1_vy = 0
    drone1_vz = 0

    drone2_vx = 0
    drone2_vy = 0
    drone2_vz = 0

    drone3_vx = 0
    drone3_vy = 0
    drone3_vz = 0

    kp = 100
    kd = 1
    for i in range(4):
        if i == 0:
            drone0_vx = sum(curr_errorX[i]) * kp + kd * (sum(curr_errorX[i]) - sum(prev_errorX[i]))
            drone0_vy = sum(curr_errorY[i]) * kp + kd * (sum(curr_errorY[i]) - sum(prev_errorY[i]))
            drone0_vz = sum(curr_errorZ[i]) * kp + kd * (sum(curr_errorZ[i]) - sum(prev_errorZ[i]))
        elif i == 1:
            drone1_vx = sum(curr_errorX[i]) * kp + kd * (sum(curr_errorX[i]) - sum(prev_errorX[i]))
            drone1_vy = sum(curr_errorY[i]) * kp + kd * (sum(curr_errorY[i]) - sum(prev_errorY[i]))
            drone1_vz = sum(curr_errorZ[i]) * kp + kd * (sum(curr_errorZ[i]) - sum(prev_errorZ[i]))
        elif i == 2:
            drone2_vx = sum(curr_errorX[i]) * kp + kd * (sum(curr_errorX[i]) - sum(prev_errorX[i]))
            drone2_vy = sum(curr_errorY[i]) * kp + kd * (sum(curr_errorY[i]) - sum(prev_errorY[i]))
            drone2_vz = sum(curr_errorZ[i]) * kp + kd * (sum(curr_errorZ[i]) - sum(prev_errorZ[i]))
        elif i == 3:
            drone3_vx = sum(curr_errorX[i]) * kp + kd * (sum(curr_errorX[i]) - sum(prev_errorX[i]))
            drone3_vy = sum(curr_errorY[i]) * kp + kd * (sum(curr_errorY[i]) - sum(prev_errorY[i]))
            drone3_vz = sum(curr_errorZ[i]) * kp + kd * (sum(curr_errorZ[i]) - sum(prev_errorZ[i]))

    prev_errorX, prev_errorY, prev_errorZ = curr_errorX, curr_errorY, curr_errorZ

    print(prev_errorX)
    print(prev_errorY)
    print(prev_errorZ)
    print("-------------------------------------------")

    f0 = client.moveByVelocityZAsync(0, 0, -20, 0.2, vehicle_name="Drone0")
    f1 = client.moveByVelocityZAsync(0, 0, -20, 0.2, vehicle_name="Drone1")
    f2 = client.moveByVelocityZAsync(0, 0, -20, 0.2, vehicle_name="Drone2")
    f3 = client.moveByVelocityZAsync(0, 0, -20, 0.2, vehicle_name="Drone3")

    f0.join()
    f1.join()
    f2.join()
    f3.join()

    time.sleep(0.5)

    f0 = client.moveByVelocityZAsync(drone0_vx, drone0_vy, drone0_vz, 0.2, vehicle_name="Drone0")
    f1 = client.moveByVelocityZAsync(drone1_vx, drone1_vy, drone1_vz, 0.2, vehicle_name="Drone1")
    f2 = client.moveByVelocityZAsync(drone2_vx, drone2_vy, drone2_vz, 0.2, vehicle_name="Drone2")
    f3 = client.moveByVelocityZAsync(drone3_vx, drone3_vy, drone3_vz, 0.2, vehicle_name="Drone3")

    f0.join()
    f1.join()
    f2.join()
    f3.join()

    time.sleep(0.5)
"""

"""
    if sum(list(map(sum, errorX))) + sum(list(map(sum, errorY))) <= 0:
        moveable = False

    """
