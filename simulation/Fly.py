import airsim
import formation
from model.model_definition.Instance import Instance
from model.Optimization import Optimization
import time

client = airsim.MultirotorClient()
client.confirmConnection()

ins = Instance()
ins.readInstance('C:/Users/ertug/OneDrive/Masaüstü/swarm2022/model/Agents.csv')
opti = Optimization()

opti.Stage1(ins)
opti.Stage2(ins)

client.enableApiControl(True, 'Drone0')
client.enableApiControl(True, 'Drone2')
client.armDisarm(True, 'Drone0')
client.armDisarm(True, 'Drone2')
f1 = client.takeoffAsync(vehicle_name='Drone0')
f2 = client.takeoffAsync(vehicle_name='Drone2')

f1.join()
f2.join()

print('ilk konum', formation.drone_state(ins.Agents[2]))
print('ilk konum', formation.drone_state(ins.Agents[0]))

f1 = client.moveByVelocityAsync(0, 0, -10, 2, vehicle_name='Drone0')
f2 = client.moveByVelocityAsync(0, 0, -10, 2, vehicle_name='Drone2')

f1.join()
f2.join()

time.sleep(2)

print('yükseliş', formation.drone_state(ins.Agents[2]))
print('yükseliş', formation.drone_state(ins.Agents[0]))

f1 = client.moveByVelocityAsync(0, 10, 0, 5, vehicle_name='Drone0')
f2 = client.moveByVelocityAsync(0, 10, 0, 5, vehicle_name='Drone2')

f1.join()
f2.join()

time.sleep(1)

f1 = client.moveByVelocityAsync(0, 0, 0, 2, vehicle_name='Drone0')
f2 = client.moveByVelocityAsync(0, 0, 0, 2, vehicle_name='Drone2')

f1.join()
f2.join()


print('final', formation.drone_state(ins.Agents[2]))
print('final', formation.drone_state(ins.Agents[0]))

"""
x_val = (50-(100))/5
y_val = (50-(-50))/5
f = client.moveByVelocityAsync(x_val, y_val, 0, 5, vehicle_name='Drone0')
f.join()
"""

for agent in ins.Agents:
    agent.printAgent()