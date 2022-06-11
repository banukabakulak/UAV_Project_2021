from model.Optimization import Optimization
from model.model_definition.Instance import Instance

instance = Instance()
instance.readInstance('model_input/Agents.csv')

optimization = Optimization()
optimization.Stage1(instance)
optimization.Stage2(instance)
optimization.Stage3(instance)

for agent in instance.Agents:
    print(agent.getName(), 'cell: ')
    agent.getCurrCell().print()