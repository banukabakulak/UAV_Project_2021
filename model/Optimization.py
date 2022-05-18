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
        #swarmModel1.print_information()

        solution = swarmModel1.solve(log_output=False)
        # assert solution, "solve failed"
        #swarmModel1.report()
        #solution.display()

        #swarmModel1.export_as_lp("swarmModel1.lp")
        solution.export("solution.json")


"""
    def Stage2(self):
        instance = Instance.Instance()
        instance.readInstance('Agents.csv')
        swarmModel2 = Model('stage2')
        
        # Define ranges:
        R_t = range(0, instance.TimePeriod)
        R_l = instance.TypeAgents
        R_i = instance.AgentIndexSet
        R_j = range(0, instance.Cells)
        
        # Define IDs:
        idt = [t for t in R_t]
        idx = []
        for l in R_l:
            for i in range(len(R_i)):
                if l == i:
                    for a in R_i[i]:
                        idx.append((l, a))
        
        idj = [j for j in R_j]
        
        # Define decision variables:
        
        x = swarmModel2.binary_var_dict(idx, name="x")
        zlij0 = swarmModel2.binary_var_dict(idj, name="z")
        
        # Define obj func:
        for l in R_l:
            for i in range(len(R_i)):
                if l == i:
                    for a in R_i[i]:
        
        # Define balance constraint:
        
        for j in idj:
        zlij0 = swarmModel2.linear_expr()
        swarmModel2.add_constraint(zlij0 <= x[l, a])

"""
