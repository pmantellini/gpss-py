import unittest
from GPSS import SubSystem, System
from blocks import Advance, Generate, Terminate


class SystemTests(unittest.TestCase):
    def test_create_system(self):
        # Test 1
        # GENERATE 60,30
        # ADVANCE 50,25
        # TERMINATE 1

        block1 = Generate(60, 30)
        block2 = Advance(50, 25)
        block3 = Terminate(1)

        subsystem1 = SubSystem()
        subsystem1.addBlock(block1)
        subsystem1.addBlock(block2)
        subsystem1.addBlock(block3)

        system1 = System()
        system1.addSubSystem(subsystem1)

        system1.runSimulation()








