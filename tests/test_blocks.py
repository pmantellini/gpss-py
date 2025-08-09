import unittest
from blocks import Generate, Advance, Terminate
from GPSS import Transaction

class BlockTests(unittest.TestCase):
    def test_generate_first(self):
        g = Generate(med_value=5, first_tx=0, max_amount=2)
        self.assertEqual(len(g.getNewTransactions(0)), 1)
        self.assertEqual(len(g.getNewTransactions(1)), 0)
        self.assertEqual(len(g.getNewTransactions(5)), 1)
        self.assertEqual(len(g.getNewTransactions(10)), 0)  # capped

    def test_advance_delay(self):
        adv = Advance(max_value=3)
        tx = Transaction()
        adv.addTransaction(tx)
        self.assertTrue(tx.isDelayed())
        self.assertEqual(tx.getScheduledTime(), 3)

    def test_terminate(self):
        term = Terminate(amount=2)
        t1, t2 = Transaction(), Transaction()
        term.addTransaction(t1)
        self.assertFalse(term.isTerminated())
        term.addTransaction(t2)
        self.assertTrue(term.isTerminated())

if __name__ == '__main__':
    unittest.main()
