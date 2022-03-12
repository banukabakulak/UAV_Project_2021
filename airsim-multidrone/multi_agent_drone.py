import airsim
from seniordesign import helper
import time

# Use below in settings.json with Blocks environment
"""
{
	"SeeDocsAt": "https://github.com/Microsoft/AirSim/blob/master/docs/settings.md",
	"SettingsVersion": 1.2,
	"SimMode": "Multirotor",
	"ClockSpeed": 1,
	
	"Vehicles": {
		"Drone1": {
		  "VehicleType": "SimpleFlight",
		  "X": 4, "Y": 0, "Z": -2
		},
		"Drone2": {
		  "VehicleType": "SimpleFlight",
		  "X": 8, "Y": 0, "Z": -2
		}

    }
}
"""

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


def moveFunc():
    distance_x = helper.matrixX()
    distance_y = helper.matrixY()
    distance_z = helper.matrixZ()
    print(distance_x)
    print(distance_y)
    print(distance_z)
    e = 15
    movable = False
    for i in range(4):
        for l in range(4):
            if (distance_x[i][l] > 10 + e) or (distance_x[i][l] < 10 + e) or (distance_y[i][l] < 10 + e) or (
                    distance_y[i][l] > 10 + e) or (distance_z[i][l] > 10 + e) or (distance_z[i][l] < 10 + e):
                movable = True
                break
            else:
                break
    return movable


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

while moveFunc():
    print("Inside While")
    distance_x = helper.matrixX()
    distance_y = helper.matrixY()
    distance_z = helper.matrixZ()

    print("DISTANCE X")
    print(distance_x)
    print("DISTANCE Y")
    print(distance_y)
    print("DISTANCE Z")
    print(distance_z)

    for i in range(4):
        # for l in range(4):
        if i == 0:
            print(distance_x[i])
            print(distance_y[i])
            print(distance_z[i])
            drone0_vx = max(distance_x[i], key=abs) / 1
            drone0_vy = max(distance_y[i], key=abs) / 1
            drone0_vz = max(distance_z[i], key=abs) / 1
        elif i == 1:
            drone1_vx = max(distance_x[i], key=abs) / 1
            drone1_vy = max(distance_y[i], key=abs) / 1
            drone1_vz = max(distance_z[i], key=abs) / 1
        elif i == 2:
            drone2_vx = max(distance_x[i], key=abs) / 1
            drone2_vy = max(distance_y[i], key=abs) / 1
            drone2_vz = max(distance_z[i], key=abs) / 1
        elif i == 3:
            drone3_vx = max(distance_x[i], key=abs) / 1
            drone3_vy = max(distance_y[i], key=abs) / 1
            drone3_vz = max(distance_z[i], key=abs) / 1

    print("It is runnnniggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg")
    print(drone0_vx)
    print(drone0_vy)
    print(drone0_vz)

    f0 = client.moveByVelocityZAsync(drone0_vx, drone0_vy, -80, 1, vehicle_name="Drone0")
    f1 = client.moveByVelocityZAsync(drone1_vx, drone1_vy, -80, 1, vehicle_name="Drone1")
    f2 = client.moveByVelocityZAsync(drone2_vx, drone2_vy, -80, 1, vehicle_name="Drone2")
    f3 = client.moveByVelocityZAsync(drone3_vx, drone3_vy, -80, 1, vehicle_name="Drone3")

    time.sleep(1)

    f0.join()
    f1.join()
    f2.join()
    f3.join()

client.armDisarm(False, "Drone0")
client.armDisarm(False, "Drone1")
client.armDisarm(False, "Drone2")
client.armDisarm(False, "Drone3")

# client.reset()

# that's enough fun for now. let's quit cleanly
"""
client.enableApiControl(False, "Drone0")
client.enableApiControl(False, "Drone1")
client.enableApiControl(False, "Drone2")
client.enableApiControl(False, "Drone3")
"""
