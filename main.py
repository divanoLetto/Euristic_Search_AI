from Problem import *
from mySolvingAgents import astar_search, best_first_graph_search
import time

def main():
    k = int(input("Enter the number of products:"))
    n = int(input("Enter the number of task for product:"))
    m = int(input("Enter the number of employers:"))
    prob = int(input("Enter the probability of creating a requirement link between two tasks (default 10%):"))
    prob = 100 - prob

    #create a random initial state with m employers and k copies of a product that have n task
    initState = State.createInitialState(n, m, k, prob)
    theProblem = RealProblem(initState)
    printProblem(theProblem)

    #a_star algorithm
    solutionNode = astar_search(theProblem)
    printSolution(solutionNode)

def printSolution(node):
    print("The required time was: "+str( node.path_cost ))
    listOfAction=[]
    while(node.parent):
        listOfAction.append(node.action)
        node = node.parent
    listOfAction.reverse()
    for action in listOfAction:
        if(action[2]=="assign"):
            print("Assign an employer to the task number "+ str(action[2])+" of the product number "+ str(action[1]))
        else:
            print("wait 1 clock cycle")

if __name__ == '__main__':
    main()


