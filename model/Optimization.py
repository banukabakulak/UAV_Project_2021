import math
from docplex.mp.model import Model

from heuristics.Pso import PSO


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

    def Stage1(self, instance):

        swarmModel1 = Model('stage1')

        # Define ranges:
        R_l = instance.TypeAgents
        R_i = instance.AgentIndexSet

        # Define IDs:
        idx = []
        for l in R_l:
            for i in range(len(R_i)):
                if l == i:
                    for a in R_i[i]:
                        idx.append((l, a))

        # Define decision variables:

        x = swarmModel1.binary_var_dict(idx, name="x")

        # Define budget constraint:

        budgetCons = swarmModel1.linear_expr()

        for l in R_l:
            for i in range(len(R_i)):
                if l == i:
                    for a in R_i[i]:
                        budgetCons += swarmModel1.sum(instance.AgentsType[l].cost * x[l, a])

        swarmModel1.add_constraint(budgetCons <= instance.Budget)

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
        solution.export('C:/Users/ertug/OneDrive/Masaüstü/swarm2022/model/model_output/solution.json')

    def Stage2(self, instance):
        filename = 'C:/Users/ertug/OneDrive/Masaüstü/swarm2022/model/model_output/solution.json'
        chosen_list = instance.chosen_drones(filename)

        instance.TypeUAV.clear()
        instance.TypeAgents.clear()
        instance.UAVs.clear()
        instance.UGVs.clear()
        instance.Agents.clear()
        instance.TypeAgentIndices.clear()
        instance.AgentIndexSet.clear()

        for i in chosen_list:
            instance.TypeAgents.append(i.getType()) if i.getType() not in instance.TypeAgents else instance.TypeAgents
            instance.Agents.append(i)
            if i.getType() != 0:
                instance.TypeUAV.append(i.getType()) if i.getType() not in instance.TypeUAV else instance.TypeUAV
                instance.UAVs.append(i) if i not in instance.UAVs else instance.UAVs
            else:
                instance.UGVs.append(i)

        # to find how many drones we have for each type:
        type_0 = []
        type_1 = []
        type_2 = []

        for agent in instance.Agents:
            if agent.type == 0:
                type_0.append(agent.indis)
            else:
                if agent.type == 1:
                    type_1.append(agent.indis)
                elif agent.type == 2:
                    type_2.append(agent.indis)

        instance.TypeAgentIndices['0'] = list(range(0, len(type_0)))
        instance.TypeAgentIndices['1'] = list(range(0, len(type_1)))
        instance.TypeAgentIndices['2'] = list(range(0, len(type_2)))

        instance.AgentIndexSet.append(instance.TypeAgentIndices.get('0'))
        instance.AgentIndexSet.append(instance.TypeAgentIndices.get('1'))
        instance.AgentIndexSet.append(instance.TypeAgentIndices.get('2'))

        instance.numUAVTypes = len(instance.TypeUAV)
        instance.numTypelAgent = len(instance.TypeAgents)

        # Edge Length Determination:

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
        R_j = range(0, len(instance.BoundaryCells))

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

        # Alpha Connectedness:

        b_matrix = instance.matrixWithinCommRangeCellJAgentTypeL()

        for j in idj:
            for x, y in idx:
                alpha_connectedness = swarmModel2.linear_expr()
                for (l, i, k, t) in idz:
                    if (l, i) != (x, y) and j != k:
                        a = b_matrix.loc[[(x, l)], [(j, k)]]
                        b_value = a[(j, k)].iloc[0]
                        alpha_connectedness += swarmModel2.sum(b_value * z[l, i, k, t])
                swarmModel2.add_constraint(alpha_connectedness >= instance.alpha * z[x, y, j, 0])

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
        # print(swarmModel2.export_to_string())
        # swarmModel2.print_information()

        solution2 = swarmModel2.solve(log_output=False)
        # assert solution, "solve failed"
        # swarmModel2.report()
        # solution2.display()

        # swarmModel1.export_as_lp("swarmModel1.lp")
        solution2.export('C:/Users/ertug/OneDrive/Masaüstü/swarm2022/model/model_output/solution2.json')

        # Initialize the location after obtain the result of unbalanced assignment problem.
        instance.initialLocation('C:/Users/ertug/OneDrive/Masaüstü/swarm2022/model/model_output/solution2.json')

        # apply Particle Swarm Optimization to obtain fully connected swarm:
        #PSO(instance, MaxIt=100, nPop=1, w=1, wdamp=0.99, c1=2, c2=2)

        for i in range(len(instance.Agents)):
            a = instance.findCellFromId(1)
            b = instance.findCellFromId(2)
            c = instance.findCellFromId(3)
            d = instance.findCellFromId(0)

            if i == 0:
                instance.Agents[i].setCurrCell(a)
            if i == 1:
                instance.Agents[i].setCurrCell(b)
            if i == 2:
                instance.Agents[i].setCurrCell(c)
            if i == 3:
                instance.Agents[i].setCurrCell(d)

    def Stage3(self, instance):
        comm_matrix = instance.connectivity_matrix()
        dist_matrix = instance.distanceMatrixOfAgents(instance.communicationGraph())
        r_list = []

        for agent in instance.Agents:
            agent_ID = agent.getName().replace('Drone', '')
            total = 0
            r = 0
            for agent2 in instance.Agents:
                agent2_ID = agent2.getName().replace('Drone', '')
                if agent.getName() != agent2.getName() and comm_matrix.loc[agent_ID, agent2_ID] == 1:
                    total += dist_matrix.loc[agent_ID, agent2_ID]

            r = (agent.getRComm() * agent.getRemEnergy()) / (total * agent.getCost())
            r_list.append(r)

        instance.Agents[r_list.index(max(r_list))].makeLeader()
