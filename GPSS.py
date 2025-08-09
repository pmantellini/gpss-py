from chains import CurrentEventsChain, FutureEventsChain
from blocks import Generate, Terminate


class System:
    def __init__(self):
        self.transaction_scheduler = TransactionScheduler()
        self.subsystems = []
        self.terminated = False
        # safety cap to avoid infinite loops during early development
        self.max_ticks = 10000

    def addSubSystem(self, subsystem):
        self.subsystems.append(subsystem)

    def runSimulation(self):
        ticks = 0
        while not self.terminated and ticks < self.max_ticks:
            # Process active transactions if any
            if not self.transaction_scheduler.moveNextTransaction():
                # Advance time when no ready transactions
                clock_time = self.transaction_scheduler.advanceClock()
                for subsystem in self.subsystems:
                    new_transactions = subsystem.advanceClock(clock_time)
                    if new_transactions:
                        self.transaction_scheduler.addNewTransactions(new_transactions)
                    if subsystem.terminated:
                        self.terminated = True
                # Move any newly due future events into current events
                self.transaction_scheduler.replenishCecWithFecTransactions()
            ticks += 1


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
            next_block = active_transaction.getNextSequentialBlock()
            if next_block:
                # If block processing caused a delay, move to FEC instead of CEC
                if active_transaction.isDelayed():
                    self.future_events_chain.addTransaction(active_transaction)
                else:
                    # Unless something extraordinary occurs, replaces the Transaction
                    # in front of its peers (i.e. same priority) on the CEC.
                    self.current_events_chain.replaceActiveTransaction(active_transaction)
            return True
        else:
            return False

    def replenishCecWithFecTransactions(self):
        # Removes transactions from the fec for that scheduled time
        for transaction in self.future_events_chain.removeNextTransactions(self.clock):
            self.current_events_chain.addTransaction(transaction)

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
        self.id = id(self)  # simplistic unique id

    def getScheduledTime(self):
        return self.scheduled_time

    def setScheduledTime(self, scheduled_time):
        self.scheduled_time = scheduled_time

    def setCurrentBlock(self, block):
        self.current_block = block

    def getNextSequentialBlock(self):
        if not self.current_block:
            return None
        next_block = self.current_block.getNextSequentialBlock(self)
        self.current_block = next_block
        if next_block:
            # Let block accept the transaction (may mutate delay/schedule)
            try:
                next_block.addTransaction(self)
            except NotImplementedError:
                pass
        return next_block

    def isDelayed(self):
        return self.delayed


class SubSystem:
    def __init__(self):
        self.blocks = []
        self.generates = []
        self.terminates = []
        self.terminated = False
        self.first_block = None

    def addBlock(self, block):
        # Link sequentially
        if self.blocks:
            prev = self.blocks[-1]
            setattr(prev, "next_block", block)
        else:
            self.first_block = block

        # Classify special block types
        if isinstance(block, Generate):
            self.generates.append(block)
        if isinstance(block, Terminate):
            self.terminates.append(block)

        # Provide default next pointer
        if not hasattr(block, "next_block"):
            setattr(block, "next_block", None)

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
                # Seed the transaction's current block as the generate block
                transaction.current_block = generate
                # Immediately move to next block (generate is a pass-through)
                transaction.getNextSequentialBlock()
                new_transactions.append(transaction)
        return new_transactions

    def isTerminated(self):
        return self.terminated
