from Problem import *
from mySolvingAgents import astar_search, best_first_graph_search
import time as tm

def test():
    k = 2
    n = 10
    m = 10
    prob = 10

    listOfTimes=[]
    for i in range(0, 10):
        #create a random initial state with m employers and k copies of a product that have n task
        initState = State.createInitialState(n, m, k, 100-prob)
        theProblem = RealProblem(initState)
        printProblem(theProblem)

        #a_star algorithm
        start=tm.time()
        solutionNode = astar_search(theProblem)
        #solutionNode = best_first_graph_search(theProblem)
        end=tm.time()
        print("The required time was: "+ str(end-start))
        listOfTimes.append(end-start)
    sum=0
    for time in listOfTimes:
        sum+=time
    media=sum/len(listOfTimes)
    print("The medium time was: "+ str(media))


if __name__ == '__main__':
    test()