from Common.common_user import *
from Common.common_login import *
import unittest


class TestUserManage(unittest.TestCase):

    def test_user_manage(self):
        admin_token = Login().login_by_admin()
        user_data = ReadCases().get_sheet_data('user')

        user_ids = []
        for case_data in user_data:
            if case_data['case'] == 'get user id':
                user_id = UserDeal.get_user_id(case_data['parameter'])
                user_ids.append(user_id)
            elif 'edit' in case_data['case']:
                print('*******************' + case_data['case'] + '*******************')
                parameter = case_data['parameter']
                phone_number = (json.loads(parameter))['userVo']['phonenumber']
                for users in user_ids:
                    if phone_number in users:
                        user_id = users[phone_number]
                        edit = UserDeal(admin_token).edit_user(case_data, user_id)
                        assert edit is True, case_data['case'] + 'failed: ' + str(edit)
                    else:
                        continue
            else:
                print('*******************' + case_data['case'] + '*******************')
                user = UserDeal(admin_token).user_case(case_data)
                assert user is True, case_data['case'] + 'failed: ' + str(user)

        print('*******************Clear environment*******************')
        UserDeal.delete_user()
