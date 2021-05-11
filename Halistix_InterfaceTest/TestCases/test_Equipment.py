from rely.rely_dealMethod import *
from Common.common_login import *
from Common.common_Equipment import *
import time
import unittest


class TestEquipment(unittest.TestCase):

    def test_equipment(self):

        admin_token = Login().login_by_admin()

        cases_data = ReadCases()
        equipment_data = cases_data.get_sheet_data('equipment')
        new_equipment_data = cases_data.get_case_data('equipment', 'create equipment')
        equipment_names = [cases_data.get_load_number(new_equipment_data),
                           cases_data.get_load_number(new_equipment_data)]
        equipment = Equipment(admin_token)
        equip_ids = []

        for i in range(0, len(equipment_data)):
            case_data = equipment_data[i]
            if case_data['case'] == "create equipment":
                print('*************' + case_data['case'] + '***************')
                logger.info('*************Create new equipment***************')
                create = equipment.create_equipment(case_data, equipment_names[i])
                assert create is True, 'Create equipment failed: ' + str(create)
            elif case_data['case'] == "check equipment":
                print('*************' + case_data['case'] + '***************')
                logger.info('*************View equipment list***************')
                load_check = equipment.view_equipment_list(case_data, 'AutoTest Tractor', equipment_names[i-2])
                assert load_check is True, 'View equipment list failed!'
            elif case_data['case'] == "get equipment id":
                print('*************' + case_data['case'] + '***************')
                logger.info('*************Get equipment id***************')
                equip_id = equipment.get_equipment_id(case_data, equipment_names[i-4])
                equip_ids.append(equip_id)
                assert type(equip_id) == int, 'Get equipment id failed!'
            elif case_data['case'] == "edit equipment":
                print('*************' + case_data['case'] + '***************')
                logger.info('*************Get equipment id***************')
                edit = equipment.edit_equipment(case_data, equipment_names[i-6], equip_ids[i-6])
                assert edit is True, 'Edit equipment failed: ' + str(edit)
            elif case_data['case'] == "check edit":
                print('*************' + case_data['case'] + '***************')
                logger.info('*************View equipment list***************')
                load_check = equipment.view_equipment_list(case_data, 'AutoTest Tractor', equipment_names[i - 8])
                assert load_check is True, 'Check edited equipment list failed!'
