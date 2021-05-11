import xlrd
import os
import json
from rely.rely_count import *


class ReadCases(object):
    def __init__(self):
        cr = os.path.abspath(os.path.dirname(os.getcwd()))
        if 'Halistix_InterfaceTest' not in cr:
            case_path = cr + '/Halistix_InterfaceTest/Dependencies/testData.xls'
        else:
            case_path = cr + '/Dependencies/testData.xls'
        self.workbook = xlrd.open_workbook(case_path)
        self.url_head = 'http://saas-test.haulistix.com'

    def read_cases(self, case):
        case_data = []
        for row in case.get_rows():
            method_column = row[1]
            method_value = method_column.value
            if method_value != '方法':
                case_value = row[0].value
                url_value = self.url_head + str(row[2].value)
                parameter_value = row[3].value
                expect_value = row[4].value
                params = (case_value, method_value, url_value, parameter_value, expect_value)
                case_data.append(params)
        return case_data

    def get_sheet_data(self, sheet):
        table = self.workbook.sheet_by_name(sheet)
        row_num = table.nrows
        col_num = table.ncols
        s = []
        key = table.row_values(0)

        if row_num <= 1:
            print("No data!")
        else:
            for i in range(1, row_num):
                d = {}
                values = table.row_values(i)
                for j in range(col_num):
                    if key[j] == 'url':
                        values[j] = self.url_head + values[j]
                    d[key[j]] = values[j]

                s.append(d)
            return s

    def get_case_data(self, sheet, case):
        sheet_data = self.get_sheet_data(sheet)
        for cases in sheet_data:
            if cases['case'] == case:
                return cases

    @staticmethod
    def get_load_number(load_data):
        parameter = load_data['parameter']
        load_para = json.loads(parameter)
        if load_data['case'] == 'create new load':
            old = load_para['freightOrderVo']['loadNumber']
            load_number = old + str(ExecuteCount.count())
            return load_number
        elif load_data['case'] == 'create new contract':
            old = load_para['contractTemplateVo']['contractNumber']
            load_number = old + str(ExecuteCount.count())
            return load_number
        elif load_data['case'] == 'create equipment':
            old = load_para['equipmentBasicInfoVo']['unitNumber']
            load_number = old + str(ExecuteCount.count())
            return load_number


if __name__ == '__main__':
    new_load_data = ReadCases().get_case_data('contract', 'create new contract')
    # print(result)
    re = ReadCases().get_load_number(new_load_data)
    print(re)
