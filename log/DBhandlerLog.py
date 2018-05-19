# -*- coding: utf-8 -*-
"""
控制数据库部分
"""
import pyodbc
import datetime

def searchDB(sql):
    '''负责从数据库中执行查询的sql语句'''
    #连接数据库
    conn = pyodbc.connect('''DRIVER={SQL Server Native Client 10.0};SERVER=(local) \SQLEXPRESS;
                        DATABASE=ShoppingWeb;UID=shoppingwebadmin;PWD=shoppingweb123''')
    cur = conn.cursor()
    #查询并返回结果
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
    #查询并返回结果
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


#*************************************注册部分*********************************
def get_customerid():
    return 'c'+datetime.datetime.now().strftime('%Y%m%d%H%M')

def get_shopid():
    return 'b'+datetime.datetime.now().strftime('%Y%m%d%H%M')

def add_customer(name,password,paymentcode,answer,phone,age,sex,province,address):
   '''新增用户，往数据库中插入数据'''
   customerid = get_customerid()
   
    #将customername,paymentcode,phone,age,sex,province,address插入到T_Custommer表中；并返回顾客的id
   sql = '''INSERT INTO T_Customer(customerid,customername,gender,age,customerbalance,paymentcode,phonenumber,
            customerprovince,customeraddress) 
            VALUES('{}','{}','{}',{},0,'{}','{}','{}','{}')'''.format(customerid,name,sex,age,paymentcode,phone,province,address)
   state = executeSql(sql)
   if state == '0' : return "0"
   #将customerid,password,answer插入到密码表T_Cryptogram中
   sql = '''INSERT INTO T_Cryptogram VALUES('{}','{}','{}',1)'''.format(customerid,password,answer)
   state = executeSql(sql)
   if state == "0" : return "0"
    
   return "1"


def add_shop(name,password,merchanttype,description,answer,province,address):
   '''新增用户，往数据库中插入数据'''
   shopid = get_shopid()
   #将name,merchanttype,description,province,address插入到商家表T_Merchant中，将其状态设置为待审核
   sql = '''INSERT INTO T_Merchant(merchantid,merchantname,merchanttype,
           merchantbalance,merchantdescribe,merchantstatement,merchantprovince,merchantaddress) 
            VALUES('{}','{}','{}',0,'{}','0','{}','{}')'''.format(shopid,name,merchanttype,description,province,address)
   state = executeSql(sql)
   if state == '0' : return "0"
   
    #将merchantid,password,ansver插入到密码表T_Cryptogram中
   sql = '''INSERT INTO T_Cryptogram VALUES('{}','{}','{}',1)'''.format(shopid,password,answer)
   state = executeSql(sql)
   if state == "0" : return "0"

    
   return "1"

#*****************************************************************************

#*************************************登录部分**********************************
def ckeck_username(username,customer=True):
    '''检测用户名是否存在，存在的话返回顾客或商家的id，否则返回0
    customer 表示检测的是否为顾客的用户名
    '''
    if customer : 
        sql = '''SELECT userid FROM T_Cryptogram WHERE userid in
                (SELECT customerid FROM T_Customer
                 WHERE customername = '{}')'''.format(username)
    else : 
        sql = '''SELECT userid FROM T_Cryptogram WHERE userid in
                (SELECT merchantid FROM T_Merchant
                 WHERE merchantname = '{}')'''.format(username)
    
    results = searchDB(sql)
    if len(results)<1:
        return "0"
    else:
        return results[0][0].rstrip()


def get_password(userid):
    '''根据顾客或商家的id得到密码'''
    sql = '''SELECT password FROM T_Cryptogram WHERE userid='{}' '''.format(userid)
    results = searchDB(sql)
    return results[0][0]

def get_shop_state(shopid):
    '''根据店铺的id得到店铺的状态'''
    sql = "SELECT merchantstatement FROM T_Merchant WHERE merchantid='{}' ".format(shopid)
    results = searchDB(sql)
    return results[0][0].rstrip()

def get_failed_reason(shopid):
    '''得到店铺审核不通过的原因'''
    sql = "SELECT remark FROM T_Merchant WHERE merchantid='{}' ".format(shopid)
    results = searchDB(sql)
    
    if len(results[0][0])<1:
        return "审核不通过"
    else:
        return results[0][0]
#***************************************************************************** 


#*************************************找回密码**********************************
def get_password_answer(userid):
    '''得到用户的密保问题的答案'''
    sql = "SELECT answer FROM T_Cryptogram WHERE userid='{}' ".format(userid)
    results = searchDB(sql)
    return results[0][0]

def alert_password(userid,password):
    sql = "UPDATE T_Cryptogram set password='{}' WHERE userid='{}' ".format(password,userid)
    state = executeSql(sql)
    return state
#***************************************************************************** 



#********************************管理员审核账户部分*****************************
def to_be_checked_shop_info():
    sql = '''SELECT merchantid,merchantname,merchanttype,merchantdescribe
            FROM T_Merchant WHERE merchantstatement='0' '''
    results = searchDB(sql)
    
    if len(results)<1:
        return results
    
    shops_info = list()
    for shopid,name,t,des in results:
        shops_info.append((shopid.rstrip(),name,t,des))
        
    return shops_info


def checked_shop(shopid):
    '''同意某个店铺的注册信息'''
    sql = "UPDATE T_Merchant SET merchantstatement='1' WHERE merchantid='{}' ".format(shopid)
    state = executeSql(sql)
    return state

def disagree_shop_register(shopid,reason):
    '''不同意店铺的注册'''
    sql = "UPDATE T_Merchant SET merchantstatement='2',remark='{}' WHERE merchantid='{}' ".format(reason,shopid)
    state = executeSql(sql)
    return state

#***************************************************************************** 