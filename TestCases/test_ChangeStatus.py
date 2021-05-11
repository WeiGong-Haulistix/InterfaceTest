from Common.common_Dispatch import *
from rely.rely_dealMethod import *
from Common.common_login import *
import time
import unittest


class TestChangeStatus(unittest.TestCase):

    def test_change_status(self):
        admin_token = Login().login_by_admin()

        cases_data = ReadCases()
        change_status_data = cases_data.get_sheet_data('change status')
        new_load_data = cases_data.get_case_data('change status', 'create new load')
        check_load_data = cases_data.get_case_data('change status', 'view load list')
        load_number = cases_data.get_load_number(new_load_data)

        dispatch = CommonDispatch(admin_token)

        print('*************Create new load***************')
        logger.info('*************Create new load***************')
        create = dispatch.create_load(new_load_data, 'STATUSTEST', load_number)
        assert create is True, 'Create load failed: ' + str(create)

        print('*************View load list***************')
        logger.info('*************View load list***************')
        load_id = dispatch.view_load_list(check_load_data, 'STATUSTEST', load_number)
        assert type(load_id) == int, 'View load list failed, return load id error: ' + str(load_id)
        i = 1
        for case_data in change_status_data:
            i = i + 1
            if case_data['case'] == "change status":
                print('**************' + str(i) + '-' + str(case_data['case']) + '******************')
                status = dispatch.change_status(case_data, load_id)
                assert status is True, 'Change status failed!'
            elif case_data['case'] == "check load status":
                print('**************' + str(i) + '-' + str(case_data['case']) + '******************')
                check = dispatch.check_load_status(case_data, load_number)
                assert check is True, 'The result status incorrect!'
            elif case_data['case'] == "open exception":
                print('**************' + str(i) + '-' + str(case_data['case']) + '******************')
                check = dispatch.open_exception(case_data, load_id)
                assert check is True, 'Open exception status failed!'
            elif case_data['case'] == "close exception":
                print('**************' + str(i) + '-' + str(case_data['case']) + '******************')
                check = dispatch.close_exception(case_data, load_id)
                assert check is True, 'Close exception status failed!'
            elif case_data['case'] == "assign load":
                print('**************' + str(i) + '-' + str(case_data['case']) + '******************')
                dispatch.assign_load(case_data, load_id)
            else:
                pass
