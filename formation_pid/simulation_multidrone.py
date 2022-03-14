import airsim
import formation
import time

# connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True, "Drone1")
client.enableApiControl(True, "Drone2")
client.enableApiControl(True, "Drone3")
client.enableApiControl(True, "Drone0")
client.armDisarm(True, "Drone1")
client.armDisarm(True, "Drone2")
client.armDisarm(True, "Drone3")
client.armDisarm(True, "Drone0")

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


def isMove():
    moveable = True

    targetX = [[0, -10, 10, -20], [10, 0, 0, -10], [10, 0, 0, -10], [20, 10, 10, 0]]
    targetY = [[0, 10, -10, 0], [-10, 0, -20, -10], [10, 20, 0, 10], [0, 10, -10, 0]]
    targetZ = [[0] * 4 for i in range(4)]

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

    if sum(list(map(sum, errorX))) + sum(list(map(sum, errorY))) < 10:
        moveable = False

    return moveable


while isMove():
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

    kp = 10000
    for i in range(4):
        if i == 0:
            drone0_vx = sum(errorX[i]) * kp
            drone0_vy = sum(errorY[i]) * kp
            drone0_vz = sum(errorZ[i]) * kp
        elif i == 1:
            drone1_vx = sum(errorX[i]) * kp
            drone1_vy = sum(errorY[i]) * kp
            drone1_vz = sum(errorZ[i]) * kp
        elif i == 2:
            drone2_vx = sum(errorX[i]) * kp
            drone2_vy = sum(errorY[i]) * kp
            drone2_vz = sum(errorZ[i]) * kp
        elif i == 3:
            drone3_vx = sum(errorX[i]) * kp
            drone3_vy = sum(errorY[i]) * kp
            drone3_vz = sum(errorZ[i]) * kp

    print("It is runnnniggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg")

    f0 = client.moveByVelocityZAsync(0, 0, -20, 1, vehicle_name="Drone0")
    f1 = client.moveByVelocityZAsync(0, 0, -20, 1, vehicle_name="Drone1")
    f2 = client.moveByVelocityZAsync(0, 0, -20, 1, vehicle_name="Drone2")
    f3 = client.moveByVelocityZAsync(0, 0, -20, 1, vehicle_name="Drone3")

    f0.join()
    f1.join()
    f2.join()
    f3.join()

    time.sleep(1)

    f0 = client.moveByVelocityZAsync(drone0_vx, drone0_vy, -20, 1, vehicle_name="Drone0")
    f1 = client.moveByVelocityZAsync(drone1_vx, drone1_vy, -20, 1, vehicle_name="Drone1")
    f2 = client.moveByVelocityZAsync(drone2_vx, drone2_vy, -20, 1, vehicle_name="Drone2")
    f3 = client.moveByVelocityZAsync(drone3_vx, drone3_vy, -20, 1, vehicle_name="Drone3")

    f0.join()
    f1.join()
    f2.join()
    f3.join()

    time.sleep(1)
