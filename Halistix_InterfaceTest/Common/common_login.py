import json
import requests
from rely.rely_readCases import *
from rely.rely_requests import *


class Login(object):
    def __init__(self):
        self.header = {"Content-Type": "application/json;charset=UTF-8", "Content-Length": "66",
                       "Host": "saas-test.haulistix.com"}

    def login_by_admin(self):
        login = self.login('admin login')
        return login

    def login_by_driver(self):
        login = self.login('driver login')
        return login

    def login(self, case):
        print('******' + case + '******')
        paras = ReadCases().get_sheet_data('login')
        for login in paras:
            if login['case'] == case:
                method = login['method']
                url = login['url']
                parameter = login['parameter']
                expect = login['expect']

                r = RequestMethod().request_method(method, url, self.header, parameter)
                data = json.loads(r.text)
                if 'code' in data:
                    status = data['code']
                    if str(status) == str(expect):
                        token = data['data']
                        print('Login success by ' + case)
                        return token
                    else:
                        print('Login failed, the response code is: ' + str(status))
                        return data
                else:
                    return data


if __name__ == '__main__':
    result = Login().login_by_driver()
