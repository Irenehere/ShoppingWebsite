# -*- coding: utf-8 -*-
import datetime
import DBhandlerPay


# ******************************1 账户余额************************************    
def get_balance_json(userid):
    
    balance = DBhandlerPay.get_balance(userid)
    
    if balance < 0:
        return "0"
    
    #返回json格式的账户余额
    '''{"userid":"userid","balance":"999.9"}'''
    balance_json='{"userid":"'+userid+'","balance":"'+str(balance)+'"}'
    
    return balance_json
#****************************************************************************

    
#********************************2 账户充值************************************
def charge(userid,money):
    '''充值成功的话“1”，如果充值失败的话返回“0”'''
    #检查money的格式
    if money<=0 : return "0"
        
    #得到账户的余额
    user_balance = DBhandlerPay.get_balance(userid)
    
    if user_balance < 0 : return "0"

    user_balance += money
    
    #更新数据库的余额
    return DBhandlerPay.update_balance(userid,user_balance)
#****************************************************************************


# 3 交易记录查询
def exchange_records(userid):
    "如果用户或商家没有交易记录的话，返回101，否则返回json格式的交易记录"
    #判断用户是顾客还是商家
    #构造sql语句从数据库中查询交易记录（订单表）订单状态为3的订单
    '''{"userid":"userid",
    "records":[{"customername":"customernam","shopname":"shopname",
                "productname":"productname","quantity":"quantity",
                "total":"total",
                "date":"date"},
                {"customername":"customernam","shopname":"shopname",
                 "productname":"productname","quantity":"quantity",
                 "total":"total",
                 "date":"date"}]}'''
    
    #从订单中找到用户对应的订单记录[(顾客id,库存id,数量，金额，下单日期)]
    results = DBhandlerPay.user_orders(userid)
    
    #没有交易的记录的话，返回101
    if len(results)<1:
        return "101"
    
    #对订单信息进行处理
    order_records = []
    #根据顾客id得到顾客的名称：{customerid:customername}
    customer_id_name={}
    #根据库存id得到店铺的名称和产品名称 {storeid:(shopname,productname)}
    storeid_shopname_productname = {}
    
    for customerid,storeid,quantity,total,orderdate in results:
        customerid = customerid[:13]
        if customerid not in customer_id_name : 
            customer_id_name[customerid] = DBhandlerPay.get_customer_name(customerid)[0][0]
        if storeid not in storeid_shopname_productname:
            storeid_shopname_productname[storeid] = DBhandlerPay.get_product_info(storeid)[0]
        total = float(total)
        orderdate = orderdate.strftime('%Y-%m-%d')
        order_records.append((customerid,storeid,quantity,total,orderdate))
    
    
    #将交易记录转换为json的格式
    js = '{"userid":"'+userid+'","records":['
    for record in order_records:
        customername = customer_id_name[record[0]]
        shopname = storeid_shopname_productname[record[1]][0]
        productname = storeid_shopname_productname[record[1]][1]
        quantity = record[2]
        total = record[3]
        date = record[4]
        js += '{"customername":"'+customername+'","shopname":"'+shopname+'","productname":"'+productname+'",'
        js += '"quantity":"'+str(quantity)+'","total":"'+str(total)+'","date":"'+date+'"},'
    js = js[:-1]+']}'
    
    return js


