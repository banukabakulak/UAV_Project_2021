#import Instance
#import Optimization as OPTI
import json

from model.Instance import Instance
from model.Optimization import Optimization

ins = Instance()
ins.readInstance('C:/Users/ertug/OneDrive/Masaüstü/swarm2022/model/Agents.csv')
opti = Optimization()
opti.Stage1()


def chosen_tuple(string_a):
    initial = string_a[string_a.index('_') + 1:]
    index = initial[0:initial.index('_')]

    rest = string_a[string_a.index('_') + 1:]
    number = rest[rest.index('_') + 1:]

    return index, number


def chosen_drones(filename):
    chosen_list = []
    with open(filename) as json_file:
        data = json.load(json_file)
        print(data['CPLEXSolution']['variables'])

        for var in data['CPLEXSolution']['variables']:
            chosen_agent = chosen_tuple(var['name'])

            type_0_list = []
            type_1_list = []
            type_2_list = []

            for i in range(len(ins.Agents)):
                if ins.Agents[i].type == 0:
                    type_0_list.append(ins.Agents[i])
                elif ins.Agents[i].type == 1:
                    type_1_list.append(ins.Agents[i])
                elif ins.Agents[i].type == 2:
                    type_2_list.append(ins.Agents[i])

            if int(chosen_agent[0]) == 0:
                for i in range(len(type_0_list)):
                    if int(chosen_agent[1]) == i:
                        chosen_list.append(type_0_list[i])
            elif int(chosen_agent[0]) == 1:
                for i in range(len(type_1_list)):
                    if int(chosen_agent[1]) == i:
                        chosen_list.append(type_1_list[i])
            elif int(chosen_agent[0]) == 2:
                for i in range(len(type_2_list)):
                    if int(chosen_agent[1]) == i:
                        chosen_list.append(type_2_list[i])

    return chosen_list


chosen_list = chosen_drones('solution.json')

for j in chosen_list:
    j.printAgent()
    print(j.getName())

"""
print(ins.AgentsType)
print(ins.UGVs)
print(ins.UAVs)
print(ins.TypeAgentIndices)
print(ins.AgentIndexSet)
"""
