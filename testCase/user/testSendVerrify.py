import unittest
import paramunittest
from common import common
from common.Log import MyLog
import readConfig as readConfig
from common import configHttp as configHttp

data = common.get_xls_bypandas("user.xlsx", "sendVerifyCode")
Readconfig = readConfig.ReadConfig()
cf = configHttp.ConfigHttp()


@paramunittest.parametrized(*data)
class testLogin(unittest.TestCase):

    def setParameters(self, case_name, path, method, type, phone, countryCode, code, msg):
        self.case_name = str(case_name)
        self.path = str(path)
        self.method = str(method)
        self.type = str(type)
        self.phone = str(phone)
        self.countryCode = str(countryCode)
        self.code = int(code)
        self.msg = str(msg)

    def shortDescription(self):
        self.case_name

    def setUp(self):
        self.log=MyLog.get_log()
        self.logger=self.log.get_logger()

    def test_Login(self):
        self.url = self.path
        cf.set_url(self.url)
        data1 = {'type': self.type, 'phone': self.phone, 'countryCode': self.countryCode}
        cf.set_data(data1)
        self.response = cf.postWithData()
        self.checkResult()

    def tearDown(self):
        self.log.build_case_line(self.info)

    def checkResult(self):
        self.info = self.response.json()

        #common.show_return_msg(self.response)
        self.assertEqual(self.info['code'], self.code)
        self.assertEqual(self.info['msg'], self.msg)


if __name__ == "__main__":
    pass
