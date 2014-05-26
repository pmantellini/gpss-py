from chains import CurrentEventsChain, FutureEventsChain


class System:
    def __init__(self):
        self.transaction_scheduler = TransactionScheduler()
        self.subsystems = []
        self.terminated = False

    def addSubSystem(self, subsystem):
        self.subsystems.append(subsystem)

    def runSimulation(self):
        while not self.terminated:
            if not self.transaction_scheduler.moveNextTransaction():
                # If there is no remaining transactions in the CEC
                # advances clock
                clock_time = self.transaction_scheduler.advanceClock()
                # Tells each subsystem to run generates for new clock.
                for subsystem in self.subsystems:
                    new_transactions = subsystem.advanceClock(clock_time)
                    if new_transactions:
                        self.transaction_scheduler.addNewTransactions(new_transactions)
                    if subsystem.terminated:
                        self.terminated = True
                # Replenish CEC with FEC next transactions
                self.transaction_scheduler.replenishCecWithFecTransactions()


class TransactionScheduler:
    def __init__(self):
        self.current_events_chain = CurrentEventsChain()
        self.future_events_chain = FutureEventsChain()
        self.clock = 0

    def moveNextTransaction(self):
        # Removes the Active Transaction from the CEC,
        active_transaction = self.current_events_chain.removeActiveTransaction()

        if active_transaction:
            # Calls the routine for the next sequential Block (NSB)
            if active_transaction.getNextSequentialBlock():
                # Unless something extraordinary occurs, replaces the Transaction
                # in front of its peers (i.e. same priority) on the CEC.
                self.current_events_chain.replaceActiveTransaction(active_transaction)
            return True
        else:
            return False

    def replenishCecWithFecTransactions(self):
        # Removes transactions from the fec for that scheduled time
        for transaction in self.future_events_chain.removeNextTransactions(self.clock):
            self.current_events_chain.append(transaction)

    def addNewTransactions(self, transactions):
        for transaction in transactions:
            if transaction.isDelayed():
                self.future_events_chain.addTransaction(transaction)
            else:
                self.current_events_chain.addTransaction(transaction)

    def advanceClock(self):
        self.clock += 1
        return self.clock


class Transaction:
    def __init__(self):
        self.scheduled_time = 0
        self.current_block = None
        self.delayed = False

    def setScheduledTime(self, scheduled_time):
        self.scheduled_time = scheduled_time

    def setCurrentBlock(self, block):
        self.current_block = block

    def getNextSequentialBlock(self):
        return self.current_block.getNextSequentialBlock(self)

    def isDelayed(self):
        return self.delayed


class SubSystem:
    def __init__(self):
        self.blocks = []
        self.generates = []
        self.terminates = []
        self.terminated = False

    def addBlock(self, block):
        self.blocks.append(block)

    def advanceClock(self, clock_time):
        # Check terminates for finish conditions and set attribute to True
        for terminate in self.terminates:
            if terminate.isTerminated():
                self.terminated = True
        # Check generates for new transactions
        new_transactions = []
        for generate in self.generates:
            for transaction in generate.getNewTransactions(clock_time):
                new_transactions.append(transaction)
        return new_transactions

    def isTerminated(self):
        return self.terminated
