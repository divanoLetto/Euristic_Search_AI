from Prodotto import *

class State:
    def __init__(self, doneProductList, undoneProductList, numberFreeEmployer):
        self.doneProductList = doneProductList
        self.undoneProductList = undoneProductList
        self.numberFreeEmployer = numberFreeEmployer

    @staticmethod
    def copyCostructor(state):
        doneProductList = []
        undoneProductList = []
        numberFreeEmployer = state.numberFreeEmployer
        for x in state.doneProductList:
            y = Prodotto.copyCostructor(x, x.id)
            doneProductList.append(y)
        for x in state.undoneProductList:
            y = Prodotto.copyCostructor(x, x.id)
            undoneProductList.append(y)

        newState = State(doneProductList, undoneProductList, numberFreeEmployer)
        return newState

    @staticmethod
    def createInitialState(n, m, k, prob):
        doneProductList = []
        undoneProductList = []
        numberFreeEmployer = m

        p0 = Prodotto.generateRandomProdotto(n, 0, prob)
        undoneProductList.append(p0)
        for i in range(1, k):
            p = Prodotto.copyCostructor(p0, i)
            undoneProductList.append(p)
        initialState = State(doneProductList, undoneProductList, numberFreeEmployer)
        return initialState

    @staticmethod
    def are_equal_states(state1, state2):
        """
        Check if state1 is equivalent to state2
        """
        if( len(state1.doneProductList) != len(state2.doneProductList) or len(state1.undoneProductList) != len(state2.undoneProductList) or state1.numberFreeEmployer != state2.numberFreeEmployer):
            return False
        else:
            for p1 in state1.doneProductList:
                found = False
                for p2 in state2.doneProductList:
                    if(p1.id==p2.id and Prodotto.are_equal_product(p1, p2)):
                        found = True
                        break
                if( found==False ):
                    return False
            for p1 in state1.undoneProductList:
                found = False
                for p2 in state2.undoneProductList:
                    if( p1.id==p2.id and Prodotto.are_equal_product(p1, p2) ):
                        found = True
                        break
                if( found==False ):
                    return False
            return True
