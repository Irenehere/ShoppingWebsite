# -*- coding: utf-8 -*-
"""
账户管理系统
"""
import pyodbc
import json
import datetime


def searchDB(sql):
    '''连接指定的数据库并执行查询的sql语句，如果是查询语句的话返回的是元组的列表：[ (查询的内容) ]'''

    # 连接数据库
    conn = pyodbc.connect('''DRIVER={SQL Server Native Client 10.0};SERVER=(local) \SQLEXPRESS;
                        DATABASE=ShoppingWeb;UID=shoppingwebadmin;PWD=shoppingweb123''')
    cur = conn.cursor()
    # 查询并返回结果
    cur.execute(sql)
    result = []
    for row in cur:
        result.append(row)

    cur.close()
    conn.close()

    return result


def executeSql(sql):
    '''执行除查询之外的sql语句'''
    conn = pyodbc.connect('''DRIVER={SQL Server Native Client 10.0};SERVER=(local) \SQLEXPRESS;
                        DATABASE=ShoppingWeb;UID=shoppingwebadmin;PWD=shoppingweb123''')
    cur = conn.cursor()
    # 查询并返回结果
    try:
        cur.execute(sql)
    except:
        print("Something Wrong when executing the sql")
        cur.close()
        conn.close()
        return "0"

    conn.commit()
    cur.close()
    conn.close()

    return "1"



# ******************************商家信息审核模块**********************************

def to_be_checked_merchant():
    '''待审核的商家信息，返回的格式：
[{"merchantid":"id",
  "merchantname":"name","merchanttype":"type",
  "merchantdescripe":"description"},

 {"merchantid":"id",
  "merchantname":"name","merchanttype":"type",
  "merchantdescripe":"description"}]
  '''
    sql = "select merchantid,merchantname,merchanttype,merchantdescribe from T_Merchant" \
          " where merchantstatement = '0'"
    tobecheckinfo = searchDB(sql)
    tobechecklist = []
    for info in tobecheckinfo:
        tobecheck = {"merchantid": info[0],
                 "merchantname": info[1], "merchanttype": info[2],
                 "merchantdescripe": info[3]}
        tobechecklist.append(tobecheck)
    return str(tobechecklist).replace('\'', '\"')


def agree_merchant(merchantid):
    '''同意一个商家的注册'''
    sql = "update T_Merchant set merchantstatement = '1' where merchantid='{}' ".format(merchantid)
    return executeSql(sql)


def agree_merchants(merchantids):
    '''同意多个商家的注册'''
    for merchantid in mechantids:
        sql = "update T_Merchant set merchantstatement = '1' where merchantid='{}' ".format(merchantid)
        results = executeSql(sql)
        if results == "0":
            return "0"
        else:
            continue
    return "1"


def not_agree_merchant(merchantid, reason):
    '''拒绝一个商家的注册，reason为拒绝的原因'''
    sql = "update T_Merchant SET merchantstatement='2',remark='{}' WHERE merchantid='{}' ".format(reason, merchantid)
    return executeSql(sql)

    # 设置商家的状态并将原因写入到remark字段内


# *************************************************************************************************


# ******************************基础信息管理模块***************************************************
def get_customer_info(customerid):
    '''根据顾客的id得到顾客的基本信息,返回的信息格式：
    {"customericon":"url","customername":"name",
     "phone":"phone","age":"age","sex":"sex",
     "address":"address"}
    '''
    sql = "select customericon,customername,phone,age,sex,customeraddress from T_Customer" \
          "where customerid='{}'".format(customerid)
    cusinfo = searchDB(sql)[0]
    dict = {"customericon": cusinfo[0],
            "customername": cusinfo[1],
            "phone": cusinfo[2],
            "age": cusinfo[3],
            "sex": cusinfo[4],
            "address": cusinfo[5]}
    return str(dict).replace('\'', '\"')


def alter_customer_info(js):
    '''修改用户的基本信息,js的格式：
    {"修改的字段":"值","修改的字段":"值"}
    '''
    cusinfo = json.loads(js)
    customerid = cusinfo["customerid"]
    sql = "update T_Customer set customername = '{}',gender = '{}'," \
          "age = '{}',customerbalance = '{}',paymentcode = '{}',customerprovince = '{}'," \
          "customeraddress = '{}',customericon = '{}' where customerid = '{}'".format(cusinfo["customername"],
                                                                                      cusinfo["gender"],
                                                                                      cusinfo["age"],
                                                                                      cusinfo["customerbalance"],
                                                                                      cusinfo["paymentcode"],
                                                                                      cusinfo["customerprovince"],
                                                                                      cusinfo["customeraddress"],
                                                                                      cusinfo["customericon"],
                                                                                      cusinfo["customerid"])
    return executeSql(sql)


def get_merchant_info(merchantid):
    '''得到商家的基本信息,格式如下：
    {"merchantname":"name","merchanttype":"type",
     "merchantdescribe":"description",
     "address":"address"}
    '''
    sql = "select merchantname,merchanttype,merchantdescribe,merchantaddress from T_Merchant" \
          " where merchantid='{}'".format(merchantid)
    merinfo = searchDB(sql)[0]
    dict = {"merchantname": merinfo[0],
            "merchanttype": merinfo[1],
            "merchantdescribe": merinfo[2],
            "address": merinfo[3]}
    return str(dict).replace('\'', '\"')


def alter_merchant_info(js):
    '''修改用的基本信息,js的格式：
    {"修改的字段":"值","修改的字段":"值"}
       '''
    merinfo = json.loads(js)
    merchantid = merinfo["merchantid"]
    sql = "update T_Merchant set merchantname = '{}',merchanttype = '{}'," \
          "merchantbalance = '{}',merchantdescribe = '{}',merchantstatement = '{}'," \
          "merchantprovince= '{}',merchantaddress = '{}',merchanticon = '{}'where merchantid = '{}'".format(
        merinfo["merchantname"], merinfo["merchanttype"], merinfo["merchantbalance"],
        merinfo["merchantdescribe"], merinfo["merchantstatement"], merinfo["merchantprovince"],
        merinfo["merchantaddress"], merinfo["merchanticon"], merinfo["merchantid"])
    return executeSql(sql)



def chage_password(userid, oldpassword, newpassword):
    '''修改密码'''
    sql = "select password from T_Cryptogram WHERE userid='{}' ".format(userid)
    old = searchDB(sql)[0][0]
    if old == oldpassword:
        sql2 = "update T_Cryptogram set password='{}' WHERE userid='{}' ".format(newpassword,userid)
        return executeSql(sql2)



    # 从库表中得到用户id对应的密码，检验输入的原密码是否正确，不正确的话返回“0“,表示密码不正确

    # 更新用户id对应的密码

    # 返回“1”表示更新成功
# *******************************************************************************
