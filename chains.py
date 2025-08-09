

# The Current Events Chain (CEC) is a linked list of ready Transactions
# which have Blocks yet to be entered before simulated time advances.
class CurrentEventsChain:
    def __init__(self):
        self.transactions = []

    def addTransaction(self, transaction):
        # Insert maintaining FIFO (simple for now)
        self.transactions.append(transaction)

    # Although the CEC is kept in priority order, the Active Transaction
    # is usually returned to the CEC ahead of its peers.
    def replaceActiveTransaction(self, transaction):
        # Reinsert at front (naive implementation)
        self.transactions.insert(0, transaction)

    def removeActiveTransaction(self):
        if not self.transactions:
            return None
        return self.transactions.pop(0)


# The Future Events Chain (FEC) is a time-ordered chain which holds
# Transactions which must wait for a later simulated time.
class FutureEventsChain:
    def __init__(self):
        self.transactions = []

    def addTransaction(self, transaction):
        # Simple append; will sort when extracting
        self.transactions.append(transaction)

    def removeNextTransactions(self, clock_time):
        ready = []
        remaining = []
        for transaction in self.transactions:
            if transaction.getScheduledTime() <= clock_time:
                # reset delayed flag now that it's ready
                transaction.delayed = False
                ready.append(transaction)
            else:
                remaining.append(transaction)
        self.transactions = remaining
        return ready
