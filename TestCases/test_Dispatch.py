from Common.common_Dispatch import *
from rely.rely_dealMethod import *
from Common.common_login import *
import time
import unittest


class TestDispatch(unittest.TestCase):

    def test_dispatch(self):
        # logger = FinalLogger.get_logger()
        admin_token = Login().login_by_admin()
        driver_token = Login().login_by_driver()

        cases_data = ReadCases()
        dispatch_test_data = cases_data.get_sheet_data('dispatch')
        new_load_data = cases_data.get_case_data('dispatch', 'create new load')
        check_load_data = cases_data.get_case_data('dispatch', 'view load list')
        load_number = cases_data.get_load_number(new_load_data)

        dispatch = CommonDispatch(admin_token)
        driver = CommonDispatch(driver_token)

        print('*************Step1. Create new load***************')
        logger.info('*************Step1. Create new load***************')
        create = dispatch.create_load(new_load_data, 'INTERTESTGW', load_number)
        assert create is True, 'Create load failed: ' + str(create)

        print('*************View load list***************')
        logger.info('*************View load list***************')
        load_id = dispatch.view_load_list(check_load_data, 'INTERTESTGW', load_number)
        assert type(load_id) == int, 'View load list failed, return load id error: ' + str(load_id)

        for case_data in dispatch_test_data:
            # time.sleep(5)
            if case_data['case'] == "check load status":
                print('*************Check load status***************')
                logger.info('*************Check load status***************')
                status = dispatch.check_load_status(case_data, load_number)
                assert status is True, 'The status of load ' + str(load_number) + ' is incorrect!'
            elif case_data['case'] == "assign load":
                print('*************Step2. Assign load to driver***************')
                logger.info('*************Step2. Assign load to driver***************')
                dispatch.assign_load(case_data, load_id)
            elif case_data['case'] == "check upcoming":
                print('*************Check upcoming load by driver***************')
                logger.info('*************Check upcoming load in driver***************')
                upcoming = driver.driver_view_load(case_data, load_id)
                assert upcoming is True, 'View upcoming load list failed by driver!'
            elif case_data['case'] == "accept load":
                print('*************Step3. Driver accept load***************')
                logger.info('*************Step3. Driver accept load***************')
                accept = driver.driver_deal_load(case_data, load_id)
                assert accept is True, 'Driver accept the load failed!'
            elif case_data['case'] == "rate confirmation":
                print('*************Step4. Rate confirmation load***************')
                logger.info('*************Step4. Rate confirmation load***************')
                rate = dispatch.saas_deal_load(case_data, load_id)
                assert rate is True, 'Rate confirmation the load failed!'
            elif case_data['case'] == "heading to pickup":
                print('*************Step5. Driver heading to pickup***************')
                logger.info('*************Step5. Driver heading to pickup***************')
                accept = driver.driver_deal_load(case_data, load_id)
                assert accept is True, 'Driver heading to pickup the load failed!'
            elif case_data['case'] == "complete delivery":
                print('*************Step6. Driver complete delivery***************')
                logger.info('*************Step6. Driver complete delivery***************')
                accept = driver.driver_deal_load(case_data, load_id)
                assert accept is True, 'Driver complete delivery the load failed!'
            elif case_data['case'] == "upload POD":
                print('*************Step7. Driver upload POD***************')
                logger.info('*************Step7. Driver upload POD***************')
                accept = driver.upload_pod(case_data, load_id)
                assert accept is True, 'Driver Driver upload POD failed!'
            elif case_data['case'] == "POD approval":
                print('*************Step8. POD approval***************')
                logger.info('*************Step8. POD approval***************')
                rate = dispatch.saas_deal_load(case_data, load_id)
                assert rate is True, 'POD approval failed!'
            elif case_data['case'] == "paid":
                print('*************Step9. POD paid***************')
                logger.info('*************Step9. POD paid***************')
                rate = dispatch.saas_deal_load(case_data, load_id)
                assert rate is True, 'POD paid failed!'
            else:
                pass
