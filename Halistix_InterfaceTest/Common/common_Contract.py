from rely.rely_readCases import *
from rely.rely_requests import *
from rely.rely_outputLogs import *
from rely.rely_count import *
from rely.rely_dealMethod import exchange_status
import json
import requests
logger = FinalLogger.get_logger()


class CommonContract:
    def __init__(self, token):
        self.header = {"Content-Type": "application/json;charset=UTF-8", "Content-Length": "40",
                       "Host": "saas-test.haulistix.com", "Authorization": "Bearer " + token}
        self.driver_header = {"Content-Type": "application/json;charset=UTF-8", "Authorization": "Bearer " + token}
        self.pod_header = {"Authorization": "Bearer " + token}

    def create_contract(self, load_data, load_number):
        method = load_data['method']
        url = load_data['url']
        params = load_data['parameter']
        expect = load_data['expect']

        if 'auto test contract' in params:
            params = params.replace('auto test contract', load_number)
        else:
            logger.error('Wrong parameters in new contract data!')

        r = RequestMethod().request_method(method, url, self.header, params)
        data = json.loads(r.text)
        if str(expect) in str(data):
            return True
        else:
            return data

    def view_contract_list(self, load_list, contract_number):
        method = load_list['method']
        url = load_list['url']
        params = load_list['parameter']
        r = RequestMethod().request_method(method, url, self.header, params)
        data = json.loads(r.text)

        if 'data' in data:
            list_info = data['data']
            for i in range(0, len(list_info)):
                if list_info[i]['contractNumber'] == contract_number:
                    contract_id = list_info[i]['id']
                    return contract_id
                else:
                    continue
        else:
            print('Return data error: ' + str(data))
            logger.error('Return data error: ' + str(data))
            return data

    def create_load(self, load_data, load_number, contract_id):
        method = load_data['method']
        url = load_data['url']
        params = load_data['parameter']
        expect = load_data['expect']

        if 'AutoTestContractLoad' in params and 'contractId' in params:
            params = (params.replace('AutoTestContractLoad', load_number)).replace('contractId', str(contract_id))

        else:
            logger.error('Wrong parameters in new load data!')

        r = RequestMethod().request_method(method, url, self.header, params)
        data = json.loads(r.text)
        if str(expect) in str(data):
            return True
        else:
            return data

    def view_load_list(self, load_list, load_number):
        method = load_list['method']
        url = load_list['url']
        params = load_list['parameter']
        expect = load_list['expect']
        r = RequestMethod().request_method(method, url, self.header, params)
        data = json.loads(r.text)
        if 'AutoTestContractLoad' in expect:
            expect = expect.replace('AutoTestContractLoad', load_number)
        else:
            logger.error('Wrong parameters in new load data!')

        if 'data' in data:
            list_info = data['data']
            for i in range(0, len(list_info)):
                if list_info[i]['loadNumber'] == load_number:
                    load_id = list_info[i]['id']
                    if str(expect) in str(list_info[i]):
                        print('New load list info correct!')
                        logger.info('New load list info correct!')
                        return load_id
                    else:
                        print('Expect result incorrect: ' + str(list_info[i]))
                        logger.error('Expect result incorrect: ' + str(list_info[i]))
                        return data
                else:
                    print('Can not find the id of load: ' + load_number)
                    logger.error('Can not find the id of load: ' + load_number)
                    return data
        else:
            print('Return data error: ' + str(data))
            logger.error('Return data error: ' + str(data))
            return data

    def assign_contract(self, load_list, contract_id):
        method = load_list['method']
        url = load_list['url']
        params = load_list['parameter']
        expect = load_list['expect']

        if 'id' in url:
            url = url.replace('id', str(contract_id))
        r = RequestMethod().request_method(method, url, self.header, params)
        data = json.loads(r.text)

        if str(expect) in str(data):
            print('Assign contract success!')
            logger.info('Assign contract success!')
            return True
        else:
            return False

    def edit_load(self, load_data, load_id, load_number):
        method = load_data['method']
        url = load_data['url']
        params = load_data['parameter']

        if 'load_id' in params:
            params = params.replace('load_id', str(load_id))
        else:
            print('Parameter error!')
            logger.error('Parameter error!')
            return False

        if 'INTERTESTGW' in params:
            params = params.replace('INTERTESTGW', str(load_number))
        else:
            print('Parameter error!')
            logger.error('Parameter error!')
            return False

        RequestMethod().request_method(method, url, self.header, params)
