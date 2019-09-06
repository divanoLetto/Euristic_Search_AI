
class Node:
    counter = 0#static variable that is used to count the number of nodes and set their Id
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0

        self.identifier = Node.counter
        Node.counter = Node.counter+1

        if parent:
            self.depth = parent.depth + 1

    def __str__(self):
        if(self.action != None):
            stringa="Nodo con id: " + str(self.identifier) + " con azione: " + str(self.action[2]) + " con depth: " + str(self.depth) + " con path_cost: " + str(self.path_cost)
        else:
            stringa="Nodo con id: " + str(self.identifier) + " con path_cost: " + str(self.path_cost) + " con depth: " + str(self.depth)
        return stringa

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem):
        return [self.child_node(problem, action) for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        next_state = problem.result(self.state, action)

        next_node = Node(next_state, self, action, problem.path_cost(self.path_cost, self.state, action, next_state))
        h = problem.h(next_node)
        next_node.h = h
        return next_node