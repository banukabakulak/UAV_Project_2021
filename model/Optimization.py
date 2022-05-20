import json

from model.Instance import Instance
import math
from docplex.mp.model import Model


class Optimization():
    def __init__(self):
        self.L = None
        self.withinLifetime = None
        self.isAgentOperation = None
        self.isLeader = None
        self.altitudeOfAgent = None
        self.velocityOfAgent = None
        self.isInCellJ = None
        self.amountOfDataFlow = None

    def Stage1(self):
        instance = Instance()
        instance.readInstance('C:/Users/ertug/OneDrive/Masaüstü/swarm2022/model/Agents.csv')
        swarmModel1 = Model('stage1')

        # Define ranges:
        R_t = range(1, instance.TimePeriod[-1] + 1)
        R_l = instance.TypeAgents
        R_i = instance.AgentIndexSet

        # Define IDs:
        idt = [t for t in R_t]
        idx = []
        for l in R_l:
            for i in range(len(R_i)):
                if l == i:
                    for a in R_i[i]:
                        idx.append((l, a))

        # Define decision variables:

        x = swarmModel1.binary_var_dict(idx, name="x")

        # L = swarmModel1.continuous_var(lb=1, ub=instance.planningHorizon, name='L')

        # nt = swarmModel1.binary_var_dict(idt, name='n')

        # Define budget constraint:

        budgetCons = swarmModel1.linear_expr()

        for l in R_l:
            for i in range(len(R_i)):
                if l == i:
                    for a in R_i[i]:
                        budgetCons += swarmModel1.sum(instance.AgentsType[l].cost * x[l, a])

        swarmModel1.add_constraint(budgetCons <= instance.Budget)

        """
        # Define lifetime constraint:

        for i in idt:
            lifeTimeCons = swarmModel1.linear_expr()
            lifeTimeCons = lifeTimeCons + (i - 1) + instance.planningHorizon * nt[i]

            swarmModel1.add_constraint(L <= lifeTimeCons)

        """

        # Define obj func:

        term_1 = 0

        for l in R_l:
            for i in range(len(R_i)):
                if l == i:
                    for a in R_i[i]:
                        term_1 += math.pi * math.pow(instance.AgentsType[l].rSense, 2) * x[l, a]

        term_2 = 0

        for l in R_l:
            for i in range(len(R_i)):
                if l == i:
                    for a in R_i[i]:
                        term_2 += instance.AgentsType[l].maxLifetime * x[l, a]

        term_3 = 0

        for l in R_l:
            for i in range(len(R_i)):
                if l == i:
                    for a in R_i[i]:
                        term_3 += (instance.AgentsType[l].cost * (
                                instance.planningHorizon * instance.periodLength / 3600)) * x[l, a]

        term_4 = 0

        for l in R_l:
            for i in range(len(R_i)):
                if l == i:
                    for a in R_i[i]:
                        term_4 += instance.AgentsType[l].minDistance * x[l, a]

        a1 = 10
        a2 = 10
        a3 = 10
        a4 = 10

        obj_func_value = a1 * term_1 + a2 * term_2 - a3 * term_3 - a4 * term_4

        # Objective Function:
        swarmModel1.maximize(obj_func_value)
        # print(smartFarmModel.export_to_string())
        # swarmModel1.print_information()

        solution = swarmModel1.solve(log_output=False)
        # assert solution, "solve failed"
        # swarmModel1.report()
        # solution.display()

        # swarmModel1.export_as_lp("swarmModel1.lp")
        solution.export("C:/Users/ertug/OneDrive/Masaüstü/swarm2022/model/solution.json")

    def chosen_tuple(self, string_a):
        initial = string_a[string_a.index('_') + 1:]
        index = initial[0:initial.index('_')]

        rest = string_a[string_a.index('_') + 1:]
        number = rest[rest.index('_') + 1:]

        return index, number

    def chosen_drones(self):
        ins = Instance()
        ins.readInstance('C:/Users/ertug/OneDrive/Masaüstü/swarm2022/model/Agents.csv')
        self.Stage1()

        filename = 'C:/Users/ertug/OneDrive/Masaüstü/swarm2022/model/solution.json'

        chosen_list = []
        with open(filename) as json_file:
            data = json.load(json_file)
            print(data['CPLEXSolution']['variables'])

            for var in data['CPLEXSolution']['variables']:
                chosen_agent = self.chosen_tuple(var['name'])

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

    def Stage2(self, instance):
        chosen_list = self.chosen_drones()

        instance.TypeUAV.clear()
        instance.TypeAgents.clear()
        instance.UAVs.clear()
        instance.UGVs.clear()
        instance.Agents.clear()
        instance.TypeAgentIndices.clear()
        instance.AgentIndexSet.clear()

        # to find how many drones we have for each type:
        drone_0 = 0
        drone_1 = 0
        drone_2 = 0
        for drone in chosen_list:
            # print("DRONE", drone)
            if drone.getType() == 0:
                drone_0 += 1
            elif drone.getType() == 1:
                drone_1 += 1
            elif drone.getType() == 2:
                drone_2 += 1

        instance.TypeAgentIndices[0] = list(range(0, drone_0))
        instance.AgentIndexSet.append(instance.TypeAgentIndices.get(0))

        instance.TypeAgentIndices[1] = list(range(0, drone_1))
        instance.AgentIndexSet.append(instance.TypeAgentIndices.get(1))

        instance.TypeAgentIndices[2] = list(range(0, drone_2))
        instance.AgentIndexSet.append(instance.TypeAgentIndices.get(2))

        for i in chosen_list:
            instance.TypeAgents.append(i.getType()) if i.getType() not in instance.TypeAgents else instance.TypeAgents
            instance.Agents.append(i)
            if i.getType() != 0:
                instance.TypeUAV.append(i.getType()) if i.getType() not in instance.TypeUAV else instance.TypeUAV
                instance.UAVs.append(i) if i not in instance.UAVs else instance.UAVs
            else:
                instance.UGVs.append(i)

        instance.numUAVTypes = len(instance.TypeUAV)
        instance.numTypelAgent = len(instance.TypeAgents)

        instance.edgeLengthDetermination()

        instance.initializeCells()
        instance.initializeBoundaryCells()

        # decrease some cells from the boundary cells due to denied zone:

        # Let's calculate Stage 2:
        swarmModel2 = Model('stage2')

        # Define ranges:
        R_t = [0]
        R_l = instance.TypeAgents
        R_i = instance.AgentIndexSet
        R_j = range(0, len(instance.BoundryCells))

        # Define IDs:
        idt = [t for t in R_t]
        idx = []
        for l in R_l:
            for i in range(len(R_i)):
                if l == i:
                    for a in R_i[i]:
                        idx.append((l, a))

        idj = [j for j in R_j]

        idz = [(x, y, j, t) for x, y in idx for j in R_j for t in R_t]

        print('idt', idt)
        print('idx', idx)
        print('idj', idj)
        print('idz', idz)
        print('idz', idz[2][2])

        # Define decision variables:
        z = swarmModel2.binary_var_dict(idz, name="z")

        for (l, i, j, t) in idz:
            for x, y in idx:
                if (l, i) == (x, y):
                    swarmModel2.add_constraint(z[l, i, j, t] <= 1, ctname='assignment_1')

        for x, y in idx:
            assignment_2 = swarmModel2.linear_expr()
            for (l, i, j, t) in idz:
                if (l, i) == (x, y):
                    assignment_2 += swarmModel2.sum(z[l, i, j, t])
            swarmModel2.add_constraint(assignment_2 == 1)

        for j in idj:
            assignment_3 = swarmModel2.linear_expr()
            for x, y in idx:
                assignment_3 += swarmModel2.sum(z[x, y, j, 0])
            swarmModel2.add_constraint(assignment_3 <= 1)

        # Define obj func:
        distance_matrix = instance.distanceBtwBaseLocationAndBoundaryCells()

        obj_func_value = 0
        d = 0
        for x, y in idx:
            for (l, i, j, t) in idz:
                if (l, i) == (x, y):
                    obj_func_value += swarmModel2.sum(z[l, i, j, t] * distance_matrix[d][j])
            d += 1

        # Objective Function:
        swarmModel2.minimize(obj_func_value)
        print(swarmModel2.export_to_string())
        swarmModel2.print_information()

        solution2 = swarmModel2.solve(log_output=False)
        # assert solution, "solve failed"
        #swarmModel2.report()
        solution2.display()

        # swarmModel1.export_as_lp("swarmModel1.lp")
        # solution2.export("C:/Users/ertug/OneDrive/Masaüstü/swarm2022/model/solution2.json")


