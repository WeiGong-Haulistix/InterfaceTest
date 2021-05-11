import json
import requests
from rely.rely_readCases import *
from rely.rely_requests import *


class Equipment:
    def __init__(self, token):
        self.header = {"Content-Type": "application/json;charset=UTF-8", "Content-Length": "40",
                       "Host": "saas-test.haulistix.com", "Authorization": "Bearer " + token}
        self.driver_header = {"Content-Type": "application/json;charset=UTF-8", "Authorization": "Bearer " + token}
        self.pod_header = {"Authorization": "Bearer " + token}

    def create_equipment(self, data_list, equip_number):
        method = data_list['method']
        url = data_list['url']
        params = data_list['parameter']
        expect = data_list['expect']

        params = json.loads(params)
        params['equipmentBasicInfoVo']['unitNumber'] = equip_number

        params = json.dumps(params)
        r = RequestMethod().request_method(method, url, self.header, params)
        data = json.loads(r.text)
        if str(expect) in str(data):
            print("Create equipment success!")
            logger.info("Create equipment success!")
            return True
        else:
            return data

    def view_equipment_list(self, data_list, equip_title, equip_number):
        method = data_list['method']
        url = data_list['url']
        params = data_list['parameter']
        expect = data_list['expect']

        if equip_title in expect:
            expect = expect.replace(equip_title, equip_number)
        r = RequestMethod().request_method(method, url, self.header, params)
        data = json.loads(r.text)

        if 'data' in data:
            list_info = data['data']
            for i in range(0, len(list_info)):
                if str(list_info[i]['unitNumber']) == str(equip_number):
                    if str(expect) in str(list_info[i]):
                        return True
                    else:
                        continue
                else:
                    continue
        else:
            print('Return data error: ' + str(data))
            logger.error('Return data error: ' + str(data))
            return False

    def get_equipment_id(self, data_list, equip_number):
        method = data_list['method']
        url = data_list['url']
        params = data_list['parameter']
        expect = data_list['expect']

        r = RequestMethod().request_method(method, url, self.header, params)
        data = json.loads(r.text)

        if 'data' in data:
            list_info = data['data']
            for i in range(0, len(list_info)):
                if str(list_info[i]['unitNumber']) == str(equip_number):
                    if str(expect) in str(list_info[i]):
                        equip_id = list_info[i]['id']
                        return equip_id
                    else:
                        continue
                else:
                    continue
        else:
            print('Return data error: ' + str(data))
            logger.error('Return data error: ' + str(data))
            return False

    def edit_equipment(self, data_list, equip_number, equip_id):
        method = data_list['method']
        url = data_list['url']
        params = data_list['parameter']
        expect = data_list['expect']

        params = json.loads(params)
        params['equipmentBasicInfoVo']['unitNumber'] = equip_number
        params['equipmentBasicInfoVo']['id'] = equip_id

        params = json.dumps(params)
        r = RequestMethod().request_method(method, url, self.header, params)
        data = json.loads(r.text)
        if str(expect) in str(data):
            print("Edit equipment success!")
            logger.info("Edit equipment success!")
            return True
        else:
            return data
