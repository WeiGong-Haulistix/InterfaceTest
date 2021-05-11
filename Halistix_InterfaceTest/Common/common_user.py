from rely.rely_dealMethod import *
from Common.common_login import *
from rely.rely_connectDB import *


class UserDeal:
    def __init__(self, token):
        self.header = {"Content-Type": "application/json;charset=UTF-8", "Content-Length": "40",
                       "Host": "saas-test.haulistix.com", "Authorization": "Bearer " + token}

    def user_case(self, user_data):
        r = RequestMethod().request_method(user_data['method'], user_data['url'], self.header, user_data['parameter'])
        data = json.loads(r.text)
        if str(user_data['expect']) in str(data):
            print(user_data['case'] + ' success!')
            return True
        else:
            return data

    def edit_user(self, user_data, user_id):
        method = user_data['method']
        url = user_data['url']
        params = user_data['parameter']

        if 'user_id' in params:
            params = params.replace('user_id', str(user_id))
        else:
            logger.error('Wrong parameters in new load data!')
        r = RequestMethod().request_method(method, url, self.header, params)
        data = json.loads(r.text)
        if str(user_data['expect']) in str(data):
            print(user_data['case'] + ' success!')
            return True
        else:
            return data

    @staticmethod
    def get_user_id(phone_number):

        sql = 'SELECT user_id FROM `sys_user` WHERE phonenumber=' + str(phone_number)
        res = ConnectDB().connect_select(sql)
        user_id = {phone_number: res[0]}
        return user_id

    @staticmethod
    def delete_user():
        sql = 'DELETE FROM `sys_user` WHERE user_name LIKE "AutoTest%"'
        ConnectDB().connect_delete(sql)


if __name__ == "__main__":
    UserDeal.get_user_id('7079311851')
