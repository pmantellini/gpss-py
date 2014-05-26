

class Block:
    def __init__(self):
        self.transactions = []

    # Each Block type has its own routine which is executed when a Transaction
    # attempts to enter that Block type
    def addTransaction(self, transaction):
        raise NotImplementedError("Should have implemented this")

    def getNextSequentialBlock(self, transaction):
        raise NotImplementedError("Should have implemented this")


# ADVANCE Blocks and GENERATE Blocks are the only way to place a Transaction on the FEC.
# These blocks take a time increment as an operand and calculate the absolute time before
# placing the Transaction on the FEC. When the system clock reaches this absolute time,
# the Transaction is moved to the CEC so that it may resume its movement in the simulation.
# In this manner, a duration or inter arrival time can be simulated.
class Generate(Block):
    def __init__(self, med_value=0, deviation=0, first_tx=0, max_amount=0, priority=0):
        Block.__init__(self)
        self.med_value = med_value
        self.deviation = deviation
        self.first_tx = first_tx
        self.max_amount = max_amount
        self.priority = priority

    def getNewTransactions(clock_time):
        #TODO Implement logic of new transactions
        #TODO Set transactions as delayed or not (could be responsibility of transaction)
        pass


class Advance(Block):
    def __init__(self, max_value=0, deviation=0):
        Block.__init__(self)
        self.max_value = max_value
        self.deviation = deviation


class Terminate(Block):
    def __init__(self, amount=0, increment_counter=0):
        Block.__init__(self)
        self.amount = amount
        self.increment_counter = increment_counter

    def isTerminated(self):
        #TODO Implement termination logic
        return True
