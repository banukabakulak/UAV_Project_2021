
class Cell():
    def __init__(self):
        self.Id = None
        self.row = None
        self.col = None
        self.center = None
        self.corner1 = None
        self.corner2 = None
        self.corner3 = None
        self.corner4 = None
        self.edgeLength = None
        self.edgeWidth = None
        self.deniedId = None
        self.deniedRow = None
        self.deniedCol = None
        self.deniedCenter = None
        self.deniedCorner1 = None
        self.deniedCorner2 = None
        self.deniedCorner3 = None
        self.deniedCorner4 = None
        self.deniedEdgeLength = None

    def print(self):
        print(
            f'id {self.Id}, center {self.center}, corner1 {self.corner1}, corner2 {self.corner2}, corner3 {self.corner3}, corner4 {self.corner4}, row {self.row}, col {self.col} ')

    def printID(self):
        print(f'id {self.Id}')

    def getID(self):
        return int(self.Id)


