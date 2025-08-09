

class Block:
    def __init__(self):
        self.transactions = []
        self.next_block = None

    # Each Block type has its own routine which is executed when a Transaction
    # attempts to enter that Block type
    def addTransaction(self, transaction):
        # Default just appends
        self.transactions.append(transaction)
        return transaction

    def getNextSequentialBlock(self, transaction):
        return self.next_block


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
        self.generated_count = 0

    def getNewTransactions(self, clock_time):
        new_transactions = []
        # Very naive: generate the first transaction at first_tx time and then one each med_value interval
        if self.max_amount and self.generated_count >= self.max_amount:
            return new_transactions
        if clock_time == self.first_tx:
            from GPSS import Transaction  # local import to avoid circular
            tx = Transaction()
            new_transactions.append(tx)
            self.generated_count += 1
        elif self.med_value > 0 and clock_time > self.first_tx:
            if (clock_time - self.first_tx) % self.med_value == 0:
                if not self.max_amount or self.generated_count < self.max_amount:
                    from GPSS import Transaction
                    tx = Transaction()
                    new_transactions.append(tx)
                    self.generated_count += 1
        return new_transactions


class Advance(Block):
    def __init__(self, max_value=0, deviation=0):
        Block.__init__(self)
        self.max_value = max_value
        self.deviation = deviation

    def addTransaction(self, transaction):
        # Delay transaction for max_value ticks (ignoring deviation for now)
        transaction.delayed = True
        transaction.setScheduledTime(transaction.getScheduledTime() + self.max_value)
        self.transactions.append(transaction)
        return transaction


class Terminate(Block):
    def __init__(self, amount=0, increment_counter=0):
        Block.__init__(self)
        self.amount = amount
        self.increment_counter = increment_counter
        self.terminated_count = 0

    def addTransaction(self, transaction):
        self.terminated_count += 1
        # Transaction ends here, do not append to list beyond bookkeeping
        return transaction

    def isTerminated(self):
        if self.amount == 0:
            return False
        return self.terminated_count >= self.amount
