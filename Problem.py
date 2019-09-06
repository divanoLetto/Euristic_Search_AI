from State import State
from Prodotto import Prodotto
import math

class Problem(object):

    def __init__(self, initial, goal=None):
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        raise NotImplementedError

    def result(self, state, action):
        raise NotImplementedError

    def goal_test(self, state):
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        return c + 1

    def value(self, state):
        raise NotImplementedError

    def h(self, node):
        raise NotImplementedError


class RealProblem(Problem):

    def __init__(self, initial):
        #total number of employers
        self.numberOfEmployers = initial.numberFreeEmployer

        #create the goal state from the initial state: every product and task must be done
        goalDoneProductList = []
        for product in initial.undoneProductList:
            goalNewProduct = Prodotto.copyCostructor(product, product.id)
            goalDoneProductList.append(goalNewProduct)
        goalUndoneProductList = []

        goalState = State(goalDoneProductList, goalUndoneProductList, initial.numberFreeEmployer)

        super().__init__(initial, goalState)

    def actions(self, state):
        """
        return the actions avaible from a state: they can be labeled as 'action' if they corrisponds to a choice of assigment (an employer start working on a specific task),
         or 'update' if they corrispods to the only possible choice of increment the timer (this appends when there are no free employers or/and there are no avaible task)
        """
        listActions = []
        if (state.numberFreeEmployer>0):
            found =False
            for p in state.undoneProductList:
                for c in p.avaibleCompiti:
                    found = True
                    action = [p.id, c.id, "assign"]
                    listActions.append(action)
            if( found==False ):
                action = [0, 0, "update"]
                listActions.append(action)
        else:
            action = [0, 0, "update"]
            listActions.append(action)
        return listActions


    def result(self, state, action):
        """return the new state resulted by  an action performed in a state"""
        newState = State.copyCostructor(state)

        if(action[2]=="assign"):
            for p in newState.undoneProductList:
                if(p.id==action[0]):
                    for c in p.avaibleCompiti[:]:
                        if( c.id==action[1] ):
                            p.avaibleCompiti.remove(c)
                            p.compitiWorkingOn.append(c)
                            newState.numberFreeEmployer = newState.numberFreeEmployer-1

        else:
            if(action[2]=="update"):
                for p in newState.undoneProductList:
                    for c in p.compitiWorkingOn:
                        c.time = c.time - 1

                for p in newState.undoneProductList:
                    for c in p.compitiWorkingOn[:]:
                        # se ho svolto interamente il compito
                        if (c.time == 0):
                            p.compitiWorkingOn.remove(c)
                            p.doneCompiti.append(c)
                            #se un compito non disponibile risulta avere tutti i requisiti ultimati, diventa disponibile
                            for cU in p.unavaibleCompiti[:]:
                                if(is_now_avaible(cU, p)):
                                    p.unavaibleCompiti.remove(cU)
                                    p.avaibleCompiti.append(cU)
                            newState.numberFreeEmployer = newState.numberFreeEmployer + 1

                # se ho svolto interamente il prodotto
                for p in newState.undoneProductList[:]:
                    if ( len(p.compitiWorkingOn)==0 and len(p.avaibleCompiti)==0 and len(p.unavaibleCompiti)==0):
                        newState.undoneProductList.remove(p)
                        newState.doneProductList.append(p)
        return newState

    def goal_test(self, state):
        if( len(state.undoneProductList)==len(self.goal.undoneProductList) and len(state.doneProductList)==len(self.goal.doneProductList) and state.numberFreeEmployer==self.goal.numberFreeEmployer):
            return True
        else:
            return False

    def path_cost(self, c, state1, action, state2):
        """
        the path_cost represents the number of clock passed, an 'assigment' action doesn't required any time, an 'update' action add 1 unit clock to the path_cost
        """
        if(action[2]=="assign"):
            return c
        else:
            if (action[2] == "update"):
                return c+1

    def h(self, node):
        """return the max from tree heuristic"""

        #euristica il minimo numero di turni rimanenti è il tempo del compito con tempo maggiore
        maxHeuristicOne=self.h1(node)

        # euristica il minimo numero di turni rimanenti è il il minimo tempo richiesto a completare il compito bloccato considerando tutti i suoi requisiti svolti in successione
        maxHeuristicTwo=self.h2(node)

        #euristica il minimo numero di turni rimanenti è la somma dei dempi dei compiti fratto il numero di impiegati
        maxHeuristicTree = self.h3(node, self.numberOfEmployers)

        heuristic_value = max(maxHeuristicOne, maxHeuristicTwo, maxHeuristicTree)

        return heuristic_value

    @staticmethod
    def h1(node):
        """The time required by the node is at least the max time required by a homework"""
        massimo = 0
        listOfCompiti = []
        for p in node.state.undoneProductList:
            listOfCompiti = listOfCompiti + p.unavaibleCompiti + p.avaibleCompiti + p.compitiWorkingOn
        for comp in listOfCompiti:
            if comp.time > massimo:
                massimo = comp.time
        return massimo

    @staticmethod
    def h2(node):
        """The time required by the node is at least the time required by the 'longest' chain of unavaibleCompiti"""
        massimo = 0
        for p in node.state.undoneProductList:
            for unavCompito in p.unavaibleCompiti:
                tempMax = maxPathFromCompitoUnavaible(unavCompito)
                if (tempMax > massimo):
                    massimo = tempMax
        return massimo

    @staticmethod
    def h3(node, numberOfEmployers):
        """The time required by the node is at least the time of the summatory of all the homeworks diveded by the total number of employers"""
        listaOfCompiti = []
        for p in node.state.undoneProductList:
            listaOfCompiti += p.compitiWorkingOn+p.avaibleCompiti+p.unavaibleCompiti
        sum = 0
        for c in listaOfCompiti:
            sum += c.time
        massimo = math.ceil(sum/numberOfEmployers)

        return massimo

def maxPathFromCompitoUnavaible(unavCompito):
    if(len(unavCompito.requisiti)==0):
        return unavCompito.time
    return unavCompito.time + max([maxPathFromCompitoUnavaible(req) for req in unavCompito.requisiti])

def is_now_avaible(compito, prodotto):
    for r in compito.requisiti:
        bol=False
        for d in prodotto.doneCompiti:
            if(d.id==r.id):
                bol=True
        if(bol==False):
            return False
    return True

def printProblem(problem):

    print("Il numero di impiegati iniziali liberi/totali è " + str(problem.initial.numberFreeEmployer))
    k= len(problem.initial.undoneProductList) + len(problem.initial.doneProductList)
    print("Il numero di prodotti totali è "+ str(k))
    n= len(problem.initial.undoneProductList[0].avaibleCompiti) + len(problem.initial.undoneProductList[0].unavaibleCompiti) + len(problem.initial.undoneProductList[0].compitiWorkingOn)
    print("Ciascun prodotto ha "+ str(n) +" compiti:")
    print("  di cui " + str(len(problem.initial.undoneProductList[0].avaibleCompiti)) + " disponibili a essere eseguiti, ovvero i compiti numero: ", end=" ")
    for c in problem.initial.undoneProductList[0].avaibleCompiti:
        print(str(c.id), end=" ")
    print()
    print("  di cui " + str(len(problem.initial.undoneProductList[0].compitiWorkingOn)) + " in lavorazione")
    print("  di cui " + str(len(problem.initial.undoneProductList[0].unavaibleCompiti)) + " non ancora disponibili in quanto richiedono il completamento di altri, in particolare per ogni prodotto: ")
    for v in problem.initial.undoneProductList[0].unavaibleCompiti:
        print("    il compito "+ str(v.id)+ " ha come prerequisiti i compiti:", end=" ")
        for y in v.requisiti:
            print(str(y.id), end=" ")
        print()
    somma = 0
    for z in problem.initial.undoneProductList[0].avaibleCompiti:
        somma = somma+z.time
    for k in problem.initial.undoneProductList[0].unavaibleCompiti:
        somma = somma + k.time
    somma = somma*len(problem.initial.undoneProductList)
    listaTuttiCompiti=problem.initial.undoneProductList[0].avaibleCompiti+problem.initial.undoneProductList[0].unavaibleCompiti
    listaTuttiCompiti.sort(key=lambda x: x.id)
    print("I tempi dei vari compiti sono: ")
    for x in listaTuttiCompiti:
       print("   il compito " +str(x.id)+" ha tempo "+ str(x.time))
    print("La somma di tutti i tempi di lavorazione è: " + str(somma))

