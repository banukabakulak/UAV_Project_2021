import itertools
import math
import csv
import json
import pandas as pd
import re

from model.model_definition.Agent import Agent, AgentEqual
from model.model_definition.Cell import Cell
from heuristics.Bfs import isReachable, graphForBFS

from itertools import product
from itertools import permutations

from heuristics.Dijkstra import Graph

#sys.setrecursionlimit(15000)

class Instance():
    def __init__(self):
        self.Cells = []
        self.BoundaryCells = []
        self.DeniedCells = []
        self.TypeUAV = []
        self.TypeAgents = []
        self.TypeAgentIndices = {}
        self.AgentIndexSet = []
        self.TimePeriod = []
        self.UAVs = []
        self.UGVs = []
        self.AgentsType = []
        self.Agents = []
        self.width = None
        self.height = None
        self.euclideanDist = None
        self.numberOfCells = None
        self.numUAVTypes = None
        self.numTypelAgent = None
        self.planningHorizon = None
        self.periodLength = None
        self.scanPercentage = None
        self.alpha = None
        self.Budget = None
        self.edgeLength = None
        self.nRow = None
        self.nCol = None
        self.nCells = None
        self.chosenCell = []

    def readInstance(self, fileName):
        drone_list = read_settings('C:/Users/ertug/OneDrive/Belgeler/AirSim/settings.json')
        with open(fileName) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                    pass
                elif line_count == 1:
                    line_count += 1
                    splitted_array = row[0].split(',')
                    self.width = int(splitted_array[0])
                    self.height = int(splitted_array[1])
                    self.euclideanDist = int(splitted_array[2])
                    self.numberOfCells = int(splitted_array[3])
                    self.numUAVTypes = int(splitted_array[4])
                    self.numTypelAgent = int(splitted_array[5])
                    self.planningHorizon = int(splitted_array[6])
                    self.periodLength = int(splitted_array[7])
                    self.scanPercentage = float(splitted_array[8])
                    self.alpha = float(splitted_array[9])
                    self.Budget = float(splitted_array[10])
                elif line_count == 2:
                    line_count += 1
                    pass
                elif 3 <= line_count < 3 + int(self.numUAVTypes + 1):  # info for sensors
                    line_count += 1
                    splitted_array = row[0].split(',')

                    currAgent = Agent()
                    currAgent.initialize(splitted_array)

                    self.TypeAgents.append(currAgent.type) if currAgent.type not in self.TypeAgents else self.TypeAgents
                    self.AgentsType.append(currAgent)

                    if currAgent.type == 0:
                        self.UGVs.append(currAgent)

                    else:
                        self.UAVs.append(currAgent)
                        self.TypeUAV.append(currAgent.type)

        T_i = self.planningHorizon
        tau_i = self.periodLength
        num_period = int(T_i / tau_i)

        for i in range(1, num_period + 1):
            self.TimePeriod.append(i)

        for i in range(len(drone_list)):

            newAgent = Agent()
            drone = drone_list[i]

            if drone['Type'] == '0':
                AgentEqual(newAgent, self.AgentsType[0])
            elif drone['Type'] == '1':
                AgentEqual(newAgent, self.AgentsType[1])
            elif drone['Type'] == '2':
                AgentEqual(newAgent, self.AgentsType[2])

            newAgent.name = drone['drone_name']
            newAgent.basePosition = (float(drone['x']), float(drone['y']), float(drone['z']))
            self.Agents.append(newAgent)

        t_0 = 0
        t_1 = 0
        t_2 = 0

        for agent in self.Agents:
            if agent.getType() == 0:
                agent.setIndis(t_0)
                t_0 += 1
            elif agent.getType() == 1:
                agent.indis = t_1
                t_1 += 1
            elif agent.getType() == 2:
                agent.indis = t_2
                t_2 += 1

        type_0 = []
        type_1 = []
        type_2 = []

        for agent in self.Agents:
            if agent.type == 0:
                type_0.append(agent.indis)
            else:
                if agent.type == 1:
                    type_1.append(agent.indis)
                elif agent.type == 2:
                    type_2.append(agent.indis)

        self.TypeAgentIndices['0'] = list(range(0, len(type_0)))
        self.TypeAgentIndices['1'] = list(range(0, len(type_1)))
        self.TypeAgentIndices['2'] = list(range(0, len(type_2)))

        self.AgentIndexSet.append(self.TypeAgentIndices.get('0'))
        self.AgentIndexSet.append(self.TypeAgentIndices.get('1'))
        self.AgentIndexSet.append(self.TypeAgentIndices.get('2'))

    def chosen_drones(self, filename):
        chosen_list = []
        with open(filename) as json_file:
            data = json.load(json_file)

            for var in data['CPLEXSolution']['variables']:
                var_list = self.variableDivision(var['name'])

                for agent in self.Agents:
                    if var_list[0] == agent.getType() and var_list[1] == agent.getIndis():
                        chosen_list.append(agent)

        return chosen_list

    def edgeLengthDetermination(self):

        scanTime = []

        for agent in self.Agents:
            scanTime.append(agent.scanTime)

        worst_scan_time = max(scanTime)
        A = (self.periodLength * self.planningHorizon) / worst_scan_time

        self.scanPercentage = (self.width * self.height) / A

        sens_range = []

        for agent in self.Agents:
            sens_range.append(math.sqrt((self.scanPercentage * self.periodLength) / (math.pi * agent.scanTime)))

        edgeLength = math.sqrt(2) * min(sens_range)

        self.edgeLength = edgeLength

        return edgeLength

    def initializeCells(self):

        print('The edgeLength is ', self.edgeLength)

        self.nCol = math.ceil(self.width / self.edgeLength)
        self.nRow = math.ceil(self.height / self.edgeLength)
        print('width:', self.width)
        print('height:', self.height)

        self.nCells = self.nCol * self.nRow

        print(f'(nCol, nRow) = {(self.nCol, self.nRow)}')

        for j in range(self.nRow):
            if j % 2 == 0:
                for i in range(self.nCol):
                    currCell = Cell()
                    currCell.Id = j * self.nCol + (1 - j % 2) * i + (j % 2) * (self.nCol - i - 1)
                    currCell.row = j
                    currCell.col = i
                    currCell.edgeLength = self.edgeLength
                    currCell.center = [(1 - j % 2) * (self.edgeLength / 2.0 + self.edgeLength * i)
                                       + (j % 2) * (
                                               self.nCol * self.edgeLength - self.edgeLength / 2.0 - self.edgeLength * (
                                               self.nCol - i - 1))
                        , self.edgeLength / 2.0 + self.edgeLength * j]

                    currCell.corner1 = [currCell.center[0] - self.edgeLength / 2.0,
                                        currCell.center[1] - self.edgeLength / 2.0]
                    currCell.corner2 = [currCell.center[0] + self.edgeLength / 2.0,
                                        currCell.center[1] - self.edgeLength / 2.0]
                    currCell.corner3 = [currCell.center[0] + self.edgeLength / 2.0,
                                        currCell.center[1] + self.edgeLength / 2.0]
                    currCell.corner4 = [currCell.center[0] - self.edgeLength / 2.0,
                                        currCell.center[1] + self.edgeLength / 2.0]

                    self.Cells.append(currCell)
            else:
                for i in range(self.nCol - 1, -1, -1):
                    currCell = Cell()
                    currCell.Id = j * self.nCol + (1 - j % 2) * i + (j % 2) * (self.nCol - i - 1)
                    currCell.row = j
                    currCell.col = i
                    currCell.center = [(1 - j % 2) * (self.edgeLength / 2.0 + self.edgeLength * i)
                                       + (j % 2) * (
                                               self.nCol * self.edgeLength - self.edgeLength / 2.0 - self.edgeLength * (
                                               self.nCol - i - 1))
                        , self.edgeLength / 2.0 + self.edgeLength * j]

                    currCell.corner1 = [currCell.center[0] - self.edgeLength / 2.0,
                                        currCell.center[1] - self.edgeLength / 2.0]
                    currCell.corner2 = [currCell.center[0] + self.edgeLength / 2.0,
                                        currCell.center[1] - self.edgeLength / 2.0]
                    currCell.corner3 = [currCell.center[0] + self.edgeLength / 2.0,
                                        currCell.center[1] + self.edgeLength / 2.0]
                    currCell.corner4 = [currCell.center[0] - self.edgeLength / 2.0,
                                        currCell.center[1] + self.edgeLength / 2.0]

                    self.Cells.append(currCell)

    def initializeBoundaryCells(self):
        for i in range(self.nCol - 1):
            self.BoundaryCells.append(self.Cells[i])

        for i in range(self.nRow - 1):
            self.BoundaryCells.append(self.Cells[((i + 1) * self.nCol) - 1])
            self.BoundaryCells.append(self.Cells[(i + 1) * self.nCol])

        for i in range(self.nCol * (self.nRow - 1) + 1, len(self.Cells)):
            self.BoundaryCells.append(self.Cells[i])

    def distanceBtwBaseLocationAndBoundaryCells(self):

        distance_matrix = [[0 for col in range(len(self.BoundaryCells))] for row in range(len(self.Agents))]

        r = 0

        for agent in self.Agents:
            k = 0
            for cell in self.BoundaryCells:
                dist = math.sqrt(math.pow(agent.basePosition[0] - cell.center[0], 2) + math.pow(
                    agent.basePosition[1] - cell.center[1], 2))
                distance_matrix[r][k] = dist
                k += 1
            r += 1

        return distance_matrix

    def distanceMatrixBtwCells(self):
        distance_matrix = [[0 for col in range(len(self.Cells))] for row in range(len(self.Cells))]

        r = 0
        for cell1 in self.Cells:
            k = 0
            for cell2 in self.Cells:
                dist1 = math.sqrt(
                    math.pow(cell1.center[0] - cell2.center[0], 2) + math.pow(cell1.center[1] - cell2.center[1], 2))
                distance_matrix[r][k] = dist1
                k += 1
            r += 1
        return distance_matrix

    def distanceBtwTwoCells(self, cellId1, cellId2):

        if cellId1 == cellId2:
            return 0

        cell1 = self.findCellFromId(cellId1)
        cell2 = self.findCellFromId(cellId2)

        return math.sqrt(
            math.pow(cell1.center[0] - cell2.center[0], 2) + math.pow(cell1.center[1] - cell2.center[1], 2))

    def distanceMatrixOfAgents(self, edge_list):
        g = Graph()

        my_list = []

        for agent in self.Agents:
            index = agent.getName().replace('Drone', '')
            my_list.append(index)

        for node in my_list:
            g.addNode(node)

        for edge in edge_list:
            g.addEdge(edge[0].replace('Drone', ''), edge[1].replace('Drone', ''), edge[2])

        d_matrix = [[0 for col in range(len(my_list))] for row in range(len(my_list))]

        df = pd.DataFrame(data=d_matrix,
                          index=my_list,
                          columns=my_list)
        for m in my_list:
            d = g.dijkstra(g, m)
            dictDikstra = d[0]
            for node in dictDikstra.keys():
                df.loc[m, node] = dictDikstra[node]

        return df

    def matrixWithinCommRangeCellJAgentTypeL(self):
        agent_list = list(product(self.TypeAgents, repeat=2))

        R_cells = range(0, len(self.Cells))
        id_cells = [j for j in R_cells]

        cell_list = list(permutations(id_cells, 2))

        b_matrix = [[0 for col in range(len(cell_list))] for row in range(len(agent_list))]

        i = 0
        for agent in agent_list:
            k = 0
            for cell in cell_list:
                distance = self.distanceBtwTwoCells(cell[0], cell[1])
                r_comm = self.getRCommOfGivenType(agent[0])
                if distance <= r_comm:
                    b_matrix[i][k] = 1
                else:
                    b_matrix[i][k] = 0
                k += 1
            i += 1

        df = pd.DataFrame(data=b_matrix, index=agent_list, columns=cell_list)

        return df

    def getRCommOfGivenType(self, t):
        r_comm = 0
        for agent in self.Agents:
            if t == agent.getType():
                r_comm = agent.getRComm()
        return r_comm

    def readCurrentCell(self, filename):
        chosen_list = []
        with open(filename) as json_file:
            data = json.load(json_file)
            print(data['CPLEXSolution']['variables'])

            for var in data['CPLEXSolution']['variables']:
                chosen_agent = self.chosen_tuple(var['name'])

                type_0_list = []
                type_1_list = []
                type_2_list = []

                for i in range(len(self.Agents)):
                    if self.Agents[i].type == 0:
                        type_0_list.append(self.Agents[i])
                    elif self.Agents[i].type == 1:
                        type_1_list.append(self.Agents[i])
                    elif self.Agents[i].type == 2:
                        type_2_list.append(self.Agents[i])

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

    def variableDivision(self, var):
        my_list = []
        var = var[var.index('_') + 1:]
        while var is not None and '_' in var:
            index = var[0:var.index('_')]
            my_list.append(int(index))
            var = var[var.index('_') + 1:]
            if '_' not in var:
                my_list.append(int(var))
                break
        return my_list

    def initialLocation(self, filename):
        with open(filename) as json_file:
            data = json.load(json_file)
            for var in data['CPLEXSolution']['variables']:
                var_list = self.variableDivision(var['name'])

                for agent in self.Agents:
                    if var_list[0] == agent.getType() and var_list[1] == agent.getIndis():
                        agent.setCurrCell(self.BoundaryCells[var_list[2]])

    def isCommunicate(self, agent1, agent2):
        result = False
        distance = self.distanceBtwTwoCells(agent1.currCell.getID(), agent2.currCell.getID())
        if distance <= agent1.getRComm():
            result = True
        return result, distance

    def communicationGraph(self):
        graph = []

        for agent in self.Agents:
            for agent2 in self.Agents:
                if agent.getName() != agent2.getName():
                    isCommunicate = self.isCommunicate(agent, agent2)
                    if isCommunicate[0]:
                        graph.append((agent.getName(), agent2.getName(), isCommunicate[1]))
        return graph

    def connectivity_matrix(self):
        graph = graphForBFS(self.communicationGraph())
        key_list = list(graph.keys())
        my_list = []
        for agent in self.Agents:
            index = agent.getName().replace('Drone', '')
            my_list.append(index)

        c_matrix = [[0 for col in range(len(my_list))] for row in range(len(my_list))]

        df = pd.DataFrame(data=c_matrix,
                          index=my_list,
                          columns=my_list)
        for m in key_list:
            for n in key_list:
                if isReachable(graph, m, n):
                    df.loc[m, n] = 1
                else:
                    df.loc[m, n] = 0
        return df

    def whichBoundaryCell(self, n):
        for boundary_cell in self.BoundaryCells:
            if boundary_cell.getID() == n:
                return boundary_cell

    def whichBoundaryCellIndex(self, n):
        for i in range(len(self.BoundaryCells)):
            if self.BoundaryCells[i].getID() == n:
                return i

    def findCellFromId(self, id):
        c = Cell()
        for cell in self.Cells:
            if id == cell.getID():
                c = cell
        return c

    def inWhichCell_ID(self, x, y):
        for cell in self.Cells:
            if cell.isInCell(x, y):
                return cell.getID()

    def inWhichCell(self, x, y):
        for cell in self.Cells:
            if cell.isInCell(x, y):
                return cell

    def inWhichCellWithCenterInfo(self, x, y):
        for cell in self.Cells:
            if [x, y] == cell.getCenter():
                return cell.getID()

    def CostFunction(self, positions):
        new_cells = []
        for x, y in positions:
            new_cells.append(self.inWhichCell(x, y))

        for i in range(len(new_cells) - 1):
            for j in range(1, len(new_cells)):
                if new_cells[i].getID() == new_cells[j].getID():
                    new_cells[j] = self.findCellFromId(new_cells[j].getID() + 1)

        for i in range(len(self.Agents)):
            self.Agents[i].setCurrCell(new_cells[i])

        comm_matrix = self.connectivity_matrix()

        return comm_matrix.values.sum()

    def cost_func(self, my_list):
        the = list(itertools.combinations(my_list, 2))
        tot = 0
        for a, b in the:
            tot += abs(a - b)
        return tot

    def CostFunctionForCell(self):

        comm_matrix = self.connectivity_matrix()

        comm_should_be = len(self.Agents) * len(self.Agents)

        communication_rate = comm_matrix.values.sum()

        return comm_should_be - communication_rate

    def uniqueCellID(self, particle_pos):

        if len(set(particle_pos)) == len(particle_pos):
            return particle_pos

        my_set = list(set(particle_pos))

        a_list = []

        for m in my_set:
            how_many = 0
            for p in particle_pos:
                if p == m:
                    how_many += 1
            a_list.append([m, how_many])

        for a in a_list:
            if a[1] == 2:
                for p in range(len(particle_pos)):
                    if particle_pos[p] == a[0]:
                        particle_pos[p] += 1
                        break
            elif a[1] == 3:
                k = 0
                for p in range(len(particle_pos)):
                    if k == 0:
                        if particle_pos[p] == a[0]:
                            particle_pos[p] += 1
                            k += 1
                    if k == 1:
                        if particle_pos[p] == a[0]:
                            particle_pos[p] += 2
                            k += 1
                    if k == 2:
                        break
            elif a[1] == 4:
                k = 0
                for p in range(len(particle_pos)):
                    if k == 0:
                        if particle_pos[p] == a[0]:
                            particle_pos[p] += 1
                            k += 1
                    if k == 1:
                        if particle_pos[p] == a[0]:
                            particle_pos[p] += 2
                            k += 1
                    if k == 2:
                        if particle_pos[p] == a[0]:
                            particle_pos[p] += 3
                            k += 1
                    if k == 3:
                        break
        self.uniqueCellID(particle_pos)

    def createUniqueCellId(self, particle_pos):

        if (len(set(particle_pos)) == len(particle_pos)) and (all(len(self.Cells)-1 >= number >= 0 for number in particle_pos)):
            self.chosenCell = particle_pos
            return
        else:
            t1 = len(set(particle_pos)) != len(particle_pos)
            t2 = all(number > len(self.Cells)-1 for number in particle_pos)
            t3 = all(number >= 0 for number in particle_pos)
            while t1 or t2 or (not t3):
                for h in range(len(particle_pos)):
                    if particle_pos[h] == 0:
                        particle_pos[h] += 1
                    elif particle_pos[h] < 0:
                        particle_pos[h] = 0
                self.uniqueCellID(particle_pos)
                for h in range(len(particle_pos)):
                    if particle_pos[h] > len(self.Cells) - 1:
                        particle_pos[h] = len(self.Cells) - 1
                t1 = len(set(particle_pos)) != len(particle_pos)
                t2 = all(number > len(self.Cells) - 1 for number in particle_pos)
                t3 = all(number >= 0 for number in particle_pos)
        self.createUniqueCellId(particle_pos)


def find_negative(line):
    s_nums = re.findall(r'-?\d+', line)
    num = "".join(s_nums)
    return int(num)


def read_settings(filename):
    file1 = open(filename, 'r')
    lines = file1.readlines()

    line_array = []

    def extract_num(new_string):
        emp_str = ""
        for m in new_string:
            if m.isdigit():
                emp_str = emp_str + m
        return emp_str

    for i in range(len(lines)):
        line = lines[i]
        line = line.replace('"', '')
        line = line.strip()

        if line.startswith('Drone'):
            Drone = dict()
            drone = line[0:line.index(':')]

            x = find_negative(lines[i + 2])
            y = find_negative(lines[i + 3])
            z = find_negative(lines[i + 4])

            Type = extract_num(lines[i + 6])

            Drone['drone_name'] = drone
            Drone['x'] = x
            Drone['y'] = y
            Drone['z'] = z
            Drone['Type'] = Type

            line_array.append(Drone)
    return line_array



