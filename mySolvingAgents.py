from Node import Node
from State import State
import networkx as nx
import matplotlib.pyplot as plt
import time

def astar_search(problem):

    return best_first_graph_search(problem, True)

def best_first_graph_search( problem, bolStar=False):

    node = Node(problem.initial)
    if(bolStar):
        frontier = myPriorityQueueStar(problem)
    else:
        frontier = myPriorityQueue(problem)
    frontier.myAppend(node)
    explored = set()

    # Preparing to draw the graph
    g = nx.Graph()
    pos = {}
    g.add_node(node.identifier)
    pos[node.identifier] = [node.depth, 0]
    deptY = {}
    deptY.update({0: [0, 0]})
    bolDraw = True

    while frontier.is_not_empty():
        node = frontier.myPop()
        if problem.goal_test(node.state):
            #draw solution
            nx.draw_networkx(g, pos, with_labels=True)
            plt.show()
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            #add node to the graph
            g.add_node(child.identifier)
            g.add_edge(child.identifier, node.identifier)
            if(child.depth in deptY):
                if(bolDraw):
                    deptY[child.depth][1] = (deptY[child.depth][1]+1)*(-1)
                    bolDraw = False
                else:
                    deptY[child.depth][1] = (deptY[child.depth][1]-1)*(-1)
                    bolDraw = True
            else:
                deptY.update({child.depth: [deptY[child.parent.depth][0]+deptY[child.parent.depth][1], 0]})
            pos[child.identifier] = [child.depth, deptY[child.depth][0]+deptY[child.depth][1]]
            #check if the child node is already in frontier or has been already explored
            if (state_is_not_in_list_of_states(child.state, explored) and state_is_not_in_list_of_states(child.state, [x.state for x in frontier.frontier])):
                frontier.myAppend(child)
            elif (state_is_not_in_list_of_states(child.state, [x.state for x in frontier.frontier]) == False):#if the node "child" is in the frontier
                if ( (child.path_cost) < frontier.element(child).path_cost):
                    frontier.myDelete(frontier.element(child))
                    frontier.myAppend(child)
    print("fail or no solution")
    return None

class myPriorityQueue():
    """
    best first graph version of frontier
    """
    def __init__(self, problem):
        self.frontier = []
        self.problem = problem

    def myAppend(self, node, lo=0, hi=None):
        if lo < 0:
            raise ValueError('lo must be non-negative')
        if hi is None:
            hi = len(self.frontier)
        while lo < hi:
            mid = (lo + hi) // 2
            if (node.path_cost) > (
                    self.frontier[mid].path_cost):
                hi = mid
            else:
                lo = mid + 1
        self.frontier.insert(lo, node)


    def is_not_empty(self):
        if(len(self.frontier)==0):
            return False
        else:
            return True

    def myPop(self):
        return self.frontier.pop()

    def element(self, node):
        return next((x for x in self.frontier if State.are_equal_states(node.state, x.state)))

    def myDelete(self, node):
        self.frontier.remove(node)


class myPriorityQueueStar(myPriorityQueue):
    """
    Astar version of frontier
    """
    def myAppend(self, node, lo=0, hi=None):
        """
        ordered insert in the state list
        :param node:  node
        """
        if lo < 0:
            raise ValueError('lo must be non-negative')
        if hi is None:
            hi = len(self.frontier)
        while lo < hi:
            mid = (lo + hi) // 2
            if (node.path_cost+self.problem.h(node)) > (self.frontier[mid].path_cost+self.problem.h(self.frontier[mid])):
                hi = mid
            else:
                lo = mid + 1
        self.frontier.insert(lo, node)

def state_is_not_in_list_of_states(state, listOfStates):
    """
    return true if the state element is not present in the list of states
    """
    for s in listOfStates:
        if ( State.are_equal_states(state, s) ):
            return False
    return True
