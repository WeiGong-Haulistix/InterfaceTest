import requests
import json
from rely.rely_outputLogs import *
logger = FinalLogger.get_logger()


class RequestMethod(object):

    @staticmethod
    def request_method(method, url, header, parameter):
        print('The request url is : ' + str(url))
        print('The request header is : ' + str(header))
        logger.info('The request url is : ' + str(url))
        logger.info('The request header is : ' + str(header))
        if parameter != '':
            print('The request data is ' + str(method) + ': ' + str(parameter))
            logger.info('The request data is' + str(method) + ': ' + str(parameter))

        if method == '':
            pass
        else:
            if parameter == '':
                data = requests.request(method, url, headers=header, data={})
                if data.text == '':
                    return data
                else:
                    print('The response data is: ' + str(json.loads(data.text)))
                    return data
            else:
                data = requests.request(method, url, headers=header, data=parameter)
                if data.text == '':
                    return data
                else:
                    print('The response data is: ' + str(json.loads(data.text)))
                    return data
