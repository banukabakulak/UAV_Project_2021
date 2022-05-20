import csv


class Agent():
    def __init__(self):
        # self.node = Node(-1, 0)
        self.name = None
        self.type = None
        self.bandwith = None
        self.cost = None
        self.rComm = None
        self.rSense = None
        self.withinRCover = None
        self.withinRComm = None
        self.reachCell = None
        self.dataPacket = None
        self.eTrans = None
        self.eReceive = None
        self.eCon = None
        self.eBat = None
        self.maxLifetime = None
        self.crDistance = None
        self.minVel = None
        self.maxVel = None
        self.maxAcc = None
        self.maxHAngle = None
        self.minHAngle = None
        self.maxAltitude = None
        self.minAltitude = None
        self.basePosition = None
        self.initAltitude = None
        self.initHeadAngle = None
        self.scanTime = None
        self.maxScanTime = None
        self.minDistance = None
        self.distanceBoundaryCell = None

    def initialize(self, splittedArray):
        self.type = int(splittedArray[0])
        self.bandwith = float(splittedArray[1])
        self.cost = float(splittedArray[2])
        self.rComm = float(splittedArray[3])
        self.rSense = float(splittedArray[4])
        self.withinRCover = float(splittedArray[5])
        self.withinRComm = float(splittedArray[6])
        self.reachCell = float(splittedArray[7])
        self.dataPacket = float(splittedArray[8])
        self.eTrans = float(splittedArray[9])
        self.eReceive = float(splittedArray[10])
        self.eCon = float(splittedArray[11])
        self.eBat = float(splittedArray[12])
        self.maxLifetime = float(splittedArray[13])
        self.crDistance = float(splittedArray[14])
        self.minVel = float(splittedArray[15])
        self.maxVel = float(splittedArray[16])
        self.maxAcc = float(splittedArray[17])
        self.maxHAngle = float(splittedArray[18])
        self.minHAngle = float(splittedArray[19])
        self.maxAltitude = float(splittedArray[20])
        self.minAltitude = float(splittedArray[21])
        self.basePosition = float(splittedArray[22])
        self.initAltitude = float(splittedArray[23])
        self.initHeadAngle = float(splittedArray[24])
        self.scanTime = float(splittedArray[25])
        self.maxScanTime = float(splittedArray[26])
        self.minDistance = float(splittedArray[27])
        self.distanceBoundaryCell = float(splittedArray[28])

    def printAgent(self):
        print(f'type {self.type}, cost {self.cost}, rComm {self.rComm}, name {self.name}')

    def getName(self):
        return self.name

    def getBasePosition(self):
        return self.basePosition

    def getType(self):
        return self.type



