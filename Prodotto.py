import random
from Compito import Compito

class Prodotto:
    def __init__(self, identif, doneCompiti, avaibleCompiti, unavaibleCompiti, compitiWorkingOn):
        self.id = identif
        self.doneCompiti = doneCompiti
        self.avaibleCompiti = avaibleCompiti
        self.unavaibleCompiti = unavaibleCompiti
        self.compitiWorkingOn = compitiWorkingOn

    @staticmethod
    def generateRandomProdotto(n, identif, prob=90):
        """
        Generate a random product with n tasks. A task has a probability (100-prob) to be linked to an other one as requirement. This method checks and prevends deadlock
        """
        doneCompiti = []
        avaibleCompiti = []
        unavaibleCompiti = []
        compitiWorkingOn = []

        listaCompiti = []
        for i in range(0, n):
            time = random.randint(1, 10)
            compitoId = Compito(i, time)
            listaCompiti.append(compitoId)

        for i in listaCompiti:
            avaible = True
            for j in listaCompiti:
                if (random.randint(0, 100) > prob and i.id != j.id and Prodotto.it_will_be_a_deadlock(i, j)):
                    i.requisiti.append(j)
                    avaible = False
            if (avaible):
                avaibleCompiti.append(i)
            else:
                unavaibleCompiti.append(i)

        p = Prodotto(identif, doneCompiti, avaibleCompiti, unavaibleCompiti, compitiWorkingOn)
        return p

    @staticmethod
    def copyCostructor(prodotto0, identif):
        """
        Returns a product that is a copy a product (product0), with his own identifier
        """
        id = identif
        doneCompiti = []
        avaibleCompiti = []
        unavaibleCompiti = []
        compitiWorkingOn = []

        for x in prodotto0.doneCompiti:
            compitoCopia = Compito(x.id, x.time)
            doneCompiti.append(compitoCopia)
        for x in prodotto0.avaibleCompiti:
            compitoCopia = Compito(x.id, x.time)
            avaibleCompiti.append(compitoCopia)
        for x in prodotto0.unavaibleCompiti:
            compitoCopia = Compito(x.id, x.time)
            unavaibleCompiti.append(compitoCopia)
        for x in prodotto0.compitiWorkingOn:
            compitoCopia = Compito(x.id, x.time)
            compitiWorkingOn.append(compitoCopia)

        listaTotaleCompiti = []  # creo una lista totale dei compiti
        for a in doneCompiti:
            listaTotaleCompiti.append(a)
        for b in avaibleCompiti:
            listaTotaleCompiti.append(b)
        for c in unavaibleCompiti:
            listaTotaleCompiti.append(c)
        for d in compitiWorkingOn:
            listaTotaleCompiti.append(d)

        Prodotto.requisitiMaker(prodotto0, doneCompiti, listaTotaleCompiti, "d")
        Prodotto.requisitiMaker(prodotto0, avaibleCompiti, listaTotaleCompiti, "a")
        Prodotto.requisitiMaker(prodotto0, unavaibleCompiti, listaTotaleCompiti, "u")
        Prodotto.requisitiMaker(prodotto0, compitiWorkingOn, listaTotaleCompiti, "w")

        prodottoCopia = Prodotto(id, doneCompiti, avaibleCompiti, unavaibleCompiti, compitiWorkingOn)
        return prodottoCopia

    @staticmethod
    def requisitiMaker(prodotto0, listaCompiti, listaTotaleCompiti, lettera):
        listaCompitiProdotto0 = []
        if (lettera == "d"):
            listaCompitiProdotto0 = prodotto0.doneCompiti
        else:
            if (lettera == "a"):
                listaCompitiProdotto0 = prodotto0.avaibleCompiti
            else:
                if (lettera == "u"):
                    listaCompitiProdotto0 = prodotto0.unavaibleCompiti
                else:
                    if (lettera == "w"):
                        listaCompitiProdotto0 = prodotto0.compitiWorkingOn


        for x in listaCompitiProdotto0:
            listRequisiti = []
            for y in x.requisiti:
                listRequisiti.append(y.id)
            for k1 in listaCompiti:
                if (x.id == k1.id):  # trovo l'equivalente compito nel nuovo prodotto
                    for k2 in listaTotaleCompiti:
                        for i in listRequisiti:
                            if (k2.id == i):
                                k1.requisiti.append(k2)

    @staticmethod
    def are_equal_product(product1, product2):
        """
        Verify if product1 and product2 are equivalent, and if is True returns True
        """
        if(product1.id != product2.id):
            return False
        for c1 in product1.doneCompiti:
            found = False
            for c2 in product2.doneCompiti:
                if(c1.id == c2.id and Compito.are_equal_compiti(c1, c2)):
                    found = True
                    break
            if (found == False):
                return False
        for c1 in product1.avaibleCompiti:
            found = False
            for c2 in product2.avaibleCompiti:
                if (c1.id == c2.id and Compito.are_equal_compiti(c1, c2)):
                    found = True
                    break
            if (found == False):
                return False
        for c1 in product1.unavaibleCompiti:
            found = False
            for c2 in product2.unavaibleCompiti:
                if (c1.id == c2.id and Compito.are_equal_compiti(c1, c2)):
                    found = True
                    break
            if (found == False):
                return False
        for c1 in product1.compitiWorkingOn:
            found = False
            for c2 in product2.compitiWorkingOn:
                if (c1.id == c2.id and Compito.are_equal_compiti(c1, c2)):
                    found = True
                    break
            if (found == False):
                return False
        return True

    @staticmethod
    def it_will_be_a_deadlock(compito1, compito2):
        listaR=[]
        for r in compito2.requisiti:
            listaR.append(r)
        while(listaR):
            r = listaR.pop()
            #se trovo la condizione di deadlock ritorno falso e non si formerà il link tra compito1 e compito2
            if (r.id == compito1.id):
                return False
            for r2 in r.requisiti:
                listaR.append(r2)
        return True

