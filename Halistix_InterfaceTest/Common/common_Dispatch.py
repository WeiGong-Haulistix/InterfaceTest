from rely.rely_readCases import *
from rely.rely_requests import *
from rely.rely_outputLogs import *
from rely.rely_count import *
from rely.rely_dealMethod import exchange_status
import json
import requests
from requests_toolbelt import MultipartEncoder
logger = FinalLogger.get_logger()


class CommonDispatch:
    def __init__(self, token):
        self.token = token
        self.header = {"Content-Type": "application/json;charset=UTF-8", "Content-Length": "40",
                       "Host": "saas-test.haulistix.com", "Authorization": "Bearer " + token}
        self.driver_header = {"Content-Type": "application/json;charset=UTF-8", "Authorization": "Bearer " + token}
        self.pod_header = {"Authorization": "Bearer " + token}

    def create_load(self, load_data, load, load_number):
        method = load_data['method']
        url = load_data['url']
        params = load_data['parameter']
        expect = load_data['expect']

        if load in params:
            params = params.replace(load, load_number)
        else:
            logger.error('Wrong parameters in new load data!')

        r = RequestMethod().request_method(method, url, self.header, params)
        data = json.loads(r.text)
        if str(expect) in str(data):
            print("Create load success!")
            logger.info("Create load success!")
            return True
        else:
            return data

    def view_load_list(self, load_list, load, load_number):
        method = load_list['method']
        url = load_list['url']
        params = load_list['parameter']
        expect = load_list['expect']
        r = RequestMethod().request_method(method, url, self.header, params)
        data = json.loads(r.text)
        if load in expect:
            expect = expect.replace(load, load_number)
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

    def check_owner_canceled(self, load_list, load_number):
        method = load_list['method']
        url = load_list['url']
        params = load_list['parameter']
        r = RequestMethod().request_method(method, url, self.header, params)
        data = json.loads(r.text)

        if load_number in data:
            print('Still find the Owner-canceled load in list!')
            logger.error('Still find the Owner-canceled load in list!')
            return False
        else:
            return True

    def check_load_status(self, load_list, load_number):
        method = load_list['method']
        url = load_list['url']
        params = load_list['parameter']
        expect = load_list['expect']
        expect_status = exchange_status(expect)
        r = RequestMethod().request_method(method, url, self.header, params)
        data = json.loads(r.text)

        if 'data' in data:
            list_info = data['data']
            for i in range(0, len(list_info)):
                if str(list_info[i]['loadNumber']) == str(load_number):
                    status_code = list_info[i]['orderStatus']
                    if str(expect_status) == str(status_code):
                        print(load_number + ' the current status is: ' + expect)
                        logger.info(load_number + ' the current status is: ' + expect)
                        return True
                    else:
                        continue
                else:
                    continue
        else:
            print('Return data error: ' + str(data))
            logger.error('Return data error: ' + str(data))
            return False

    def assign_load(self, assign_data, load_id):
        method = assign_data['method']
        url = assign_data['url']
        params = assign_data['parameter']
        if 'id' in params:
            paras = params.replace('id', str(load_id))
            RequestMethod().request_method(method, url, self.header, paras)
        else:
            print('Parameter error!')
            logger.error('Parameter error!')

    def driver_view_load(self, upcoming_data, load_id):
        button = upcoming_data['case']
        method = upcoming_data['method']
        url = upcoming_data['url']
        params = upcoming_data['parameter']
        expect = upcoming_data['expect']

        r = RequestMethod().request_method(method, url, self.driver_header, params)
        data = json.loads(r.text)
        if 'data' in data:
            upcoming_info = data['data']
            if "'orderId': id" in expect:
                expect = expect.replace("'orderId': id", "'orderId': " + str(load_id))
            else:
                pass

            if str(expect) in str(upcoming_info):
                print("The load is in " + button + " list!")
                return True
            else:
                print(button + ' info: ' + str(upcoming_info))
                print("expect: " + str(expect))
                logger.info(button + ' info: ' + str(upcoming_info))
        else:
            print("Wrong return data: " + str(data))
            logger.error("Wrong return data: " + str(data))
            return False

    def driver_deal_load(self, load_data, load_id):
        button = load_data['case']
        method = load_data['method']
        url = load_data['url']
        params = load_data['parameter']
        expect = load_data['expect']

        if 'id' in url:
            url = url.replace('id', str(load_id))

        if 'id' in params:
            params = params.replace('id', str(load_id))

        r = RequestMethod().request_method(method, url, self.driver_header, params)
        data = json.loads(r.text)
        if str(expect) in str(data):
            print("Driver " + button + " success!")
            logger.info("Driver " + button + " success!")
            return True
        else:
            print("Driver " + button + " Failed: " + str(data))
            logger.error("Driver " + button + " Failed: " + str(data))
            return data

    def upload_pod(self, pod_data, load_id):
        method = pod_data['method']
        url = pod_data['url']
        expect = pod_data['expect']

        if 'id' in url:
            url = url.replace('id', str(load_id))
        else:
            print('Parameter error!')
            logger.error('Parameter error!')
            return False

        cr = os.path.abspath(os.path.dirname(os.getcwd()))
        if "Halistix_InterfaceTest" in cr:
            file = cr + '\\Dependencies\\POD.jpg'
        else:
            file = cr + '\\Halistix_InterfaceTest\\Dependencies\\POD.jpg'
        files = {"files": ("POD.png", open(file, "rb"), "image/png")}

        r = requests.request(method, url=url, headers=self.pod_header, files=files)
        data = json.loads(r.text)
        if str(expect) in str(data):
            print("Upload POD success!")
            logger.info("Upload POD success!")
            return True
        else:
            print("Upload POD Failed: " + str(data))
            logger.error("Upload POD Failed: " + str(data))
            return data

    def saas_deal_load(self, load_data, load_id):
        button = load_data['case']
        method = load_data['method']
        url = load_data['url']
        params = load_data['parameter']
        expect = load_data['expect']

        if 'id' in url:
            url = url.replace('id', str(load_id))
        elif 'id' in params:
            params = params.replace('id', str(load_id))
        else:
            print('Parameter error!')
            logger.error('Parameter error!')
            return False
        if button in ("paid", "accept load", "cancel load"):
            header = self.header
        else:
            header = self.pod_header
        r = RequestMethod().request_method(method, url, header, params)
        data = json.loads(r.text)
        if str(expect) in str(data):
            print("Admin " + button + " success!")
            logger.info("Admin " + button + " success!")
            return True
        else:
            print("Admin " + button + " Failed: " + str(data))
            logger.error("Admin " + button + " Failed: " + str(data))
            return data

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

    def change_status(self, load_data, load_id):
        url = load_data['url']
        params = load_data['parameter']
        expect = load_data['expect']

        params = json.loads(params)
        params['orderId'] = str(load_id)
        params['orderStatus'] = exchange_status(params['orderStatus'])

        m = MultipartEncoder(params)
        headers = {'Content-Type': m.content_type, "Authorization": "Bearer " + self.token}
        print('The request url is:' + str(url))
        print('The request data is:' + str(params))
        r = requests.post(url, data=m, headers=headers)
        data = json.loads(r.text)

        if str(expect) in str(data):
            print('Change status success!')
            return True
        else:
            return data

    def open_exception(self, load_data, load_id):
        method = load_data['method']
        url = load_data['url']
        params = load_data['parameter']
        expect = load_data['expect']

        params = json.loads(params)
        params['orderId'] = str(load_id)
        params['fallback'] = exchange_status(params['fallback'])

        params = json.dumps(params)
        r = RequestMethod().request_method(method, url, self.header, str(params))
        data = json.loads(r.text)

        if str(expect) in str(data):
            print('Open exception success!')
            return True
        else:
            return data

    def close_exception(self, load_data, load_id):
        method = load_data['method']
        url = load_data['url']
        params = load_data['parameter']
        expect = load_data['expect']

        params = json.loads(params)
        params['orderId'] = str(load_id)

        params = json.dumps(params)
        r = RequestMethod().request_method(method, url, self.header, params)
        data = json.loads(r.text)

        if str(expect) in str(data):
            print('Close exception success!')
            return True
        else:
            return data


if __name__ == '__main__':
    token = "eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6IjdkYzY4YmJmLTc0MTMtNDUxZi1iZjJjLWU1MDU2ZThjZmUxNCJ9.ev1DOY" \
            "Byy32rSR5PESMYREZe9SPugZgvNLrj8hlr-vRorHxg7ykLlw751abnopIb6wRU7tbS5EmsImHHpUMIWA"
    data_list = {'method': 'put', 'url': 'http://saas-test.haulistix.com/api/saas/order/exception/pending',
                 'parameter': '{"fallback": 0, "orderId": "orderId"}',
                 'expect': "'code': 200, 'msg': 'success'"}
    lid = 34
    CommonDispatch(token).close_exception(data_list, lid)
