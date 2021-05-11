from rely.rely_outputLogs import *
import xlrd
logger = FinalLogger.get_logger()


def exchange_status(status):
    cr = os.path.abspath(os.path.dirname(os.getcwd()))
    if "Halistix_InterfaceTest" in cr:
        path = os.path.abspath(os.path.dirname(os.getcwd())) + '/Dependencies/LoadStatus.xls'
    else:
        path = os.path.abspath(os.path.dirname(os.getcwd())) + '/Halistix_InterfaceTest/Dependencies/LoadStatus.xls'

    workbook = (xlrd.open_workbook(path)).sheet_by_name('status')
    for row in workbook.get_rows():
        code_value = row[0].value
        status_value = row[1].value
        if status == code_value:
            return status_value
        elif status == status_value:
            return code_value
        else:
            continue


if __name__ == '__main__':
    result = exchange_status('paid')
    print(result)
