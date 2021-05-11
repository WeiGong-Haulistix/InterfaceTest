from Common.common_Dispatch import *
from rely.rely_readCases import *
from rely.rely_outputLogs import *
from rely.rely_dealMethod import *
from Common.common_login import *
import time
import unittest


class TestLoadProcess(unittest.TestCase):

    def test_load_process(self):
        admin_token = Login().login_by_admin()
        driver_token = Login().login_by_driver()

        cases_data = ReadCases()
        dispatch_test_data = cases_data.get_sheet_data('load process')
        new_load_data = cases_data.get_case_data('load process', 'create new load')
        check_load_data = cases_data.get_case_data('load process', 'view load list')
        load_number = cases_data.get_load_number(new_load_data)

        dispatch = CommonDispatch(admin_token)
        driver = CommonDispatch(driver_token)
        print('*************Create new load***************')
        logger.info('*************Create new load***************')
        create = dispatch.create_load(new_load_data, 'INTERTESTGW', load_number)
        assert create is True, 'Create load failed: ' + str(create)

        print('*************View load list***************')
        logger.info('*************View load list***************')
        load_id = dispatch.view_load_list(check_load_data, 'INTERTESTGW', load_number)
        assert type(load_id) == int, 'View load list failed, return load id error: ' + str(load_id)

        for case_data in dispatch_test_data:
            # time.sleep(10)
            if case_data['case'] == "edit load":
                print('*************Edit load***************')
                logger.info('*************Edit load***************')
                dispatch.edit_load(case_data, load_id, load_number)
            elif case_data['case'] == "check load status":
                print('*************Check load status***************')
                logger.info('*************Check load status***************')
                status = dispatch.check_load_status(case_data, load_number)
                assert status is True, 'The status of load ' + str(load_number) + ' is incorrect!'
            elif case_data['case'] == "assign load":
                print('*************Assign load to driver***************')
                logger.info('*************Assign load to driver***************')
                dispatch.assign_load(case_data, load_id)
            elif case_data['case'] == "check upcoming":
                print('*************Check upcoming load by driver***************')
                logger.info('*************Check upcoming load in driver***************')
                upcoming = driver.driver_view_load(case_data, load_id)
                assert upcoming is True, 'View upcoming load list failed by driver!'
            elif case_data['case'] == "check in progress":
                print('*************Check in progress load by driver***************')
                logger.info('*************Check in progress load in driver***************')
                upcoming = driver.driver_view_load(case_data, load_id)
                assert upcoming is True, 'View in progress load list failed by driver!'
            elif case_data['case'] == "check canceled":
                print('*************Check canceled load by driver***************')
                logger.info('*************Check canceled load in driver***************')
                upcoming = driver.driver_view_load(case_data, load_id)
                assert upcoming is True, 'View upcoming load list failed by driver!'
            elif case_data['case'] == "accept load":
                print('*************Driver accept load***************')
                logger.info('*************Driver accept load***************')
                accept = driver.driver_deal_load(case_data, load_id)
                assert accept is True, 'Driver accept the load failed!'
            elif case_data['case'] == "refuse load":
                print('*************Driver refuse load***************')
                logger.info('*************Driver refuse load***************')
                accept = driver.driver_deal_load(case_data, load_id)
                assert accept is True, 'Driver accept the load failed!'
            elif case_data['case'] == "cancel load":
                print('*************Saas cancel load***************')
                logger.info('*************Saas cancel load***************')
                accept = dispatch.saas_deal_load(case_data, load_id)
                assert accept is True, 'Saas cancel the load failed!'
            elif case_data['case'] == "rate confirmation":
                print('*************Rate confirmation load***************')
                logger.info('*************Rate confirmation load***************')
                rate = dispatch.saas_deal_load(case_data, load_id)
                assert rate is True, 'Rate confirmation the load failed!'
            elif case_data['case'] == "heading to pickup":
                print('*************Driver heading to pickup***************')
                logger.info('*************Driver heading to pickup***************')
                accept = driver.driver_deal_load(case_data, load_id)
                assert accept is True, 'Driver heading to pickup the load failed!'
            elif case_data['case'] == "complete delivery":
                print('*************Driver complete delivery***************')
                logger.info('*************Driver complete delivery***************')
                accept = driver.driver_deal_load(case_data, load_id)
                assert accept is True, 'Driver complete delivery the load failed!'
            elif case_data['case'] == "upload POD":
                print('*************Driver upload POD***************')
                logger.info('*************Driver upload POD***************')
                accept = driver.upload_pod(case_data, load_id)
                assert accept is True, 'Driver Driver upload POD failed!'
            elif case_data['case'] == "POD approval":
                print('*************POD approval***************')
                logger.info('*************POD approval***************')
                rate = dispatch.saas_deal_load(case_data, load_id)
                assert rate is True, 'POD approval failed!'
            elif case_data['case'] == "paid":
                print('*************POD paid***************')
                logger.info('*************POD paid***************')
                rate = dispatch.saas_deal_load(case_data, load_id)
                assert rate is True, 'POD paid failed!'
            elif case_data['case'] == "check owner canceled result":
                print('*************check owner canceled result***************')
                logger.info('*************check owner canceled result***************')
                cancel = dispatch.check_owner_canceled(case_data, load_id)
                assert cancel is True, 'Check owner canceled load failed!'
            else:
                pass
