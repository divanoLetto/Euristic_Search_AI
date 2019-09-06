
class Compito:
    def __init__(self, identif, time):
        self.id = identif
        self.time = time
        self.requisiti = []

    @staticmethod
    def are_equal_compiti(compito1, compito2):
        "check if compito1 and compito2 are equal"
        if(compito1.id!= compito2.id ):
            return False
        if(compito1.time != compito2.time ):
            return False
        return True
