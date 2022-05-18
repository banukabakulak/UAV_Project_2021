import math

#import Agent
#import Cell
import csv

from model.Agent import Agent


class Instance():
    def __init__(self):
        self.Cells = []
        self.BoundryCells = []
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

                    #print(f'the length of the array ,is {len(splitted_array)}')

                    self.width = int(splitted_array[0])
                    #print(f'\t{self.width} our width.')

                    self.height = int(splitted_array[1])
                    #print(f'\t{self.height} many gatenodes we have.')

                    self.euclideanDist = int(splitted_array[2])
                    #print(f'\t{self.euclideanDist} many types sensor we have.')

                    self.numberOfCells = int(splitted_array[3])
                    #print(f'\t{self.numberOfCells} many routers we have.')

                    self.numUAVTypes = int(splitted_array[4])
                    #print(f'\t{self.numUAVTypes} many gates we have.')

                    self.numTypelAgent = int(splitted_array[5])
                    #print(f'\t{self.numTypelAgent} many periods we have.')

                    self.planningHorizon = int(splitted_array[6])
                    #print(f'\t{self.planningHorizon} many periods we have.')

                    self.periodLength = int(splitted_array[7])
                    #print(f'\t{self.periodLength} many periodLength we have.')

                    self.scanPercentage = float(splitted_array[8])
                    #print(f'\t{self.scanPercentage} scanning percantage.')

                    self.alpha = float(splitted_array[9])
                    #print(f'\t{self.alpha} alpha we have.')

                    self.Budget = float(splitted_array[10])
                    #print(f'\t{self.Budget} alpha we have.')

                elif line_count == 2:
                    line_count += 1
                    pass
                elif 3 <= line_count < 3 + int(self.numUAVTypes + 1):  # info for sensors
                    line_count += 1
                    splitted_array = row[0].split(',')

                    # print(f'the length of the array ,is {len(splitted_array)}')

                    # print(splitted_array)

                    currAgent = Agent()

                    drone_0 = 0
                    drone_1 = 0
                    drone_2 = 0
                    for drone in drone_list:
                        # print("DRONE", drone)
                        if drone['Type'] == '0':
                            drone_0 += 1
                        elif drone['Type'] == '1':
                            drone_1 += 1
                        elif drone['Type'] == '2':
                            drone_2 += 1

                    currAgent.initialize(splitted_array)

                    self.TypeAgents.append(currAgent.type)
                    self.AgentsType.append(currAgent)
                    # self.TypeAgentIndices[currAgent.type] = []
                    # self.AgentIndexSet.append(self.TypeAgentIndices.values())

                    if currAgent.type == 0:
                        self.UGVs.append(currAgent)
                        self.TypeAgentIndices[currAgent.type] = list(range(0, drone_0))
                        self.AgentIndexSet.append(self.TypeAgentIndices.get(0))
                    else:
                        self.UAVs.append(currAgent)
                        self.TypeUAV.append(currAgent.type)

                        if currAgent.type == 1:
                            self.TypeAgentIndices[currAgent.type] = list(range(0, drone_1))
                            self.AgentIndexSet.append(self.TypeAgentIndices.get(1))
                        elif currAgent.type == 2:
                            self.TypeAgentIndices[currAgent.type] = list(range(0, drone_2))
                            self.AgentIndexSet.append(self.TypeAgentIndices.get(2))

                        # self.UAVs[int(currAgent.type)].printElement()

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

    def edgeLengthDetermination(self):
        self.readInstance('Agents.csv')

        scanTime = []

        for agent in self.AgentsType:
            scanTime.append(agent.scanTime)

        worst_scan_time = max(scanTime)
        A = (self.periodLength * self.planningHorizon) / worst_scan_time

        self.scanPercentage = (self.width * self.height) / A

        sens_range = []

        for agent in self.AgentsType:
            sens_range.append(math.sqrt((self.scanPercentage * self.periodLength) / (math.pi * agent.scanTime)))

        edgeLength = math.sqrt(2) * min(sens_range)

        return edgeLength


def read_settings(filename):
    file1 = open(filename, 'r')
    Lines = file1.readlines()

    line_array = []

    def extract_num(new_string):
        emp_str = ""
        for m in new_string:
            if m.isdigit():
                emp_str = emp_str + m
        return emp_str

    for i in range(len(Lines)):
        line = Lines[i]
        line = line.replace('"', '')
        line = line.strip()

        # line_array.append(line)
        # print(line)

        if line.startswith('Drone'):
            Drone = dict()
            drone = line[0:line.index(':')]

            x = extract_num(Lines[i + 2])
            y = extract_num(Lines[i + 3])
            z = extract_num(Lines[i + 4])
            Type = extract_num(Lines[i + 6])

            Drone['drone_name'] = drone
            Drone['x'] = x
            Drone['y'] = y
            Drone['z'] = z
            Drone['Type'] = Type

            line_array.append(Drone)
    return line_array


def AgentEqual(a, b):
    a.type = b.type
    a.bandwith = b.bandwith
    a.cost = b.cost
    a.rComm = b.rComm
    a.rSense = b.rSense
    a.withinRCover = b.withinRCover
    a.withinRComm = b.withinRComm
    a.reachCell = b.reachCell
    a.dataPacket = b.dataPacket
    a.eTrans = b.eTrans
    a.eReceive = b.eReceive
    a.eCon = b.eCon
    a.eBat = b.eBat
    a.maxLifetime = b.maxLifetime
    a.crDistance = b.crDistance
    a.minVel = b.minVel
    a.maxVel = b.maxVel
    a.maxAcc = b.maxAcc
    a.maxHAngle = b.maxHAngle
    a.minHAngle = b.minHAngle
    a.maxAltitude = b.maxAltitude
    a.minAltitude = b.minAltitude
    a.initAltitude = b.initAltitude
    a.initHeadAngle = b.initHeadAngle
    a.scanTime = b.scanTime
    a.maxScanTime = b.maxScanTime
    a.minDistance = b.minDistance
    a.distanceBoundaryCell = b.distanceBoundaryCell
