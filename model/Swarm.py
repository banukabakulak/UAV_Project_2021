#import Instance
#import Optimization as OPTI
import json

from model.Instance import Instance
from model.Optimization import Optimization

ins = Instance()
ins.readInstance('C:/Users/ertug/OneDrive/Masaüstü/swarm2022/model/Agents.csv')
opti = Optimization()
opti.Stage1()




"""
print(ins.AgentsType)
print(ins.UGVs)
print(ins.UAVs)
print(ins.TypeAgentIndices)
print(ins.AgentIndexSet)
"""
