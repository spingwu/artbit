import requests
import readConfig as readConfig
import os
from xlrd import open_workbook
import pandas
from xml.etree import ElementTree
from common import configHttp
from common.Log import MyLog as Log
import json
import numpy as np

localReadConfig = readConfig.ReadConfig()
proDir = readConfig.proDir
localConfigHttp = configHttp.ConfigHttp()
log = Log.get_log()
logger =log.get_logger()
caseNo = 0

def get_reqToken():
    url = 'http://139.196.15.68:8080/api/v1/loginByPhone'
    d = {'phone': '15221605356', 'password': '96e79218965eb72c92a549dd5a330112', 'countryCode': '86'}
    response= requests.post(url=url,data=d)
    info=response.json()
    data=info['data']
    reqToken=data['reqToken']
    return reqToken


def get_visitor_token():
    host = localReadConfig.get_http("BASEURL")
    response = requests.get(host+"/activity/274")
    info = response.json()
    token = info.get("info")
    logger.debug("Create token:%s"%(token))
    return token
def set_visitor_token_to_config():
    token_v = get_visitor_token()
    localReadConfig.set_headers("TOKEN_V",token_v)
def get_value_from_return_json(json,name1,name2):
    info = json['info']
    group = info[name1]
    value = group[name2]
    return value
def show_return_msg(response):
    url = response.url
    msg = response.text
    print("\n请求地址："+url)
    print("\n请求返回值:"+json.dumps(json.loads(msg), ensure_ascii=False, sort_keys=True, indent=4))

    # ****************************** read testCase excel by pandas********************************
def get_xls_bypandas(xls_name, sheet_name):
    """
    get interface data from xls file
    :return:
    """
    cls = []
    # get xls file's path

    xlsPath = os.path.join(proDir, "testFile", 'case')
    os.chdir(xlsPath)
    # get sheet by name
    table = pandas.read_excel(xls_name,sheet_name)

    arraydata = np.array(table)
    sheet = arraydata.tolist()

    return sheet

        # ****************************** read testCase excel by xlrd********************************
def get_xls_byxlrd(xls_name, sheet_name):
    """
    get interface data from xls file
    :return:
    """
    cls = []
    # get xls file's path
    xlsPath = os.path.join(proDir, "testFile", 'case', xls_name)
    data = pandas.read_excel()
    # open xls file
    file = open_workbook(xlsPath)
    # get sheet by name
    sheet = file.sheet_by_name(sheet_name)
    # get one sheet's rows
    nrows = sheet.nrows
    for i in range(nrows):
        if sheet.row_values(i)[0] != u'case_name':
            cls.append(sheet.row_values(i))
    return cls

# ****************************** read SQL xml ********************************
database = {}


def set_xml():
    """
    set sql xml
    :return:
    """
    if len(database) == 0:
        sql_path = os.path.join(proDir, "testFile", "SQL.xml")
        tree = ElementTree.parse(sql_path)
        for db in tree.findall("database"):
            db_name = db.get("name")
            # print(db_name)
            table = {}
            for tb in db.getchildren():
                table_name = tb.get("name")
                # print(table_name)
                sql = {}
                for data in tb.getchildren():
                    sql_id = data.get("id")
                    # print(sql_id)
                    sql[sql_id] = data.text
                table[table_name] = sql
            database[db_name] = table


def get_xml_dict(database_name, table_name):
    """
    get db dict by given name
    :param database_name:
    :param table_name:
    :return:
    """
    set_xml()
    database_dict = database.get(database_name).get(table_name)
    return database_dict


def get_sql(database_name, table_name, sql_id):
    """
    get sql by given name and sql_id
    :param database_name:
    :param table_name:
    :param sql_id:
    :return:
    """
    db = get_xml_dict(database_name, table_name)
    sql = db.get(sql_id)
    return sql
# ****************************** read interfaceURL xml ********************************


def get_url_from_xml(name):
    """
    By name get url from interfaceURL.xml
    :param name: interface's url name
    :return: url
    """
    url_list = []
    url_path = os.path.join(proDir, 'testFile', 'interfaceURL.xml')
    tree = ElementTree.parse(url_path)
    for u in tree.findall('url'):
        url_name = u.get('name')
        if url_name == name:
            for c in u.getchildren():
                url_list.append(c.text)

    url = '/v2/' + '/'.join(url_list)
    return url

if __name__ == "__main__":
    pass

    #set_visitor_token_to_config()
