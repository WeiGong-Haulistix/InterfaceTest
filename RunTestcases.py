import unittest
from TestCases.test_Dispatch import TestDispatch
from TestCases.test_LoadProcess import TestLoadProcess
from TestCases.test_ChangeStatus import TestChangeStatus
from TestCases.test_Contract import TestContract
from TestCases.test_UserManage import TestUserManage
from TestCases.test_Equipment import TestEquipment


class TestCases:
    @staticmethod
    def execute_cases():
        suite1 = unittest.TestLoader().loadTestsFromTestCase(TestDispatch)
        suite = unittest.TestSuite([suite1])
        # suite2 = unittest.TestLoader().loadTestsFromTestCase(TestLoadProcess)
        # suite3 = unittest.TestLoader().loadTestsFromTestCase(TestChangeStatus)
        # suite4 = unittest.TestLoader().loadTestsFromTestCase(TestContract)
        # suite5 = unittest.TestLoader().loadTestsFromTestCase(TestUserManage)
        # suite6 = unittest.TestLoader().loadTestsFromTestCase(TestEquipment)
        # suite = unittest.TestSuite([suite1, suite2, suite3, suite4, suite5, suite6])
        unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == "__main__":
    TestCases.execute_cases()
