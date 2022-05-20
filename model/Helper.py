from model.Instance import Instance
from model.Optimization import Optimization

ins = Instance()
ins.readInstance('C:/Users/ertug/OneDrive/Masaüstü/swarm2022/model/Agents.csv')
opti = Optimization()
opti.Stage1()

opti = Optimization()
opti.Stage2(ins)



