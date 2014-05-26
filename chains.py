

# The Current Events Chain (CEC) is a linked list of ready Transactions
# which have Blocks yet to be entered before simulated time advances.
class CurrentEventsChain:
    def __init__(self):
        self.transactions = []

    def addTransaction(self, transaction):
        #TODO Implement transaction ordering logic
        self.transactions.append(transaction)

    # Although the CEC is kept in priority order, the Active Transaction
    # is usually returned to the CEC ahead of its peers.
    def replaceActiveTransaction(self, transaction):
        #TODO Implement transaction ordering logic
        self.transactions.append(transaction)

    def removeActiveTransaction(self):
        #TODO Implement active transaction selection logic
        for transaction in self.transactions:
            return transaction
        return None


# The Future Events Chain (FEC) is a time-ordered chain which holds
# Transactions which must wait for a later simulated time.
class FutureEventsChain:
    def __init__(self):
        self.transactions = []

    def addTransaction(self, transaction):
        #TODO Implement transaction ordering logic
        self.transactions.append(transaction)

    def removeNextTransactions(self, clock_time):
        transactions_to_remove = []
        for transaction in self.transactions:
            if transaction.getScheduledTime() == clock_time:
                transactions_to_remove.append(transaction)

        return transactions_to_remove
