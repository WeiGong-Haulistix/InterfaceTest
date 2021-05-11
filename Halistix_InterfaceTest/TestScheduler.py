import sched
import time
from datetime import datetime
from RunTestcases import TestCases
from TestCases.test_Dispatch import *
schedule = sched.scheduler(time.time, time.sleep)


def execute_test(inc):
    print('Execute time: ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # TestDispatch().test_dispatch()
    TestCases.execute_cases()
    schedule.enter(inc, 0, execute_test, (inc,))


def main(inc=300):
    schedule.enter(0, 0, execute_test, (inc,))
    schedule.run()


main(86400)
