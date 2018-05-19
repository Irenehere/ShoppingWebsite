import pyodbc

def searchDB(sql):
    '''连接指定的数据库并执行查询的sql语句，如果是查询语句的话返回的是元组的列表：[ (查询的内容) ]'''

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




#********************************得到账户的余额*********************************
def get_balance(userid):
    
    #判断用户是顾客还是商家,构造sql语句查询账户余额
    if 'c' in userid:
        sql = "SELECT customerbalance FROM T_Customer WHERE customerid='{}' ".format(userid)
    elif 'b' in userid:
        sql = "SELECT merchantbalance FROM T_Merchant WHERE merchantid='{}' ".format(userid)
    else:
        return -1
    
    results = searchDB(sql)
    #没有找到该用户的话说明出错了返回-1
    if len(results)<1:
        return -1
    
    balance = float(results[0][0])
    
    return balance


#更新账户的余额
def update_balance(userid,user_balance):
    
    if 'c' in userid:
        sql = "UPDATE T_Customer SET customerbalance={} WHERE customerid='{}' ".format(user_balance,userid)
    else:
        sql = "UPDATE T_Merchant SET merchantbalance={} WHERE merchantid='{}' ".format(user_balance,userid)
    
    return executeSql(sql)

def user_orders(userid):
    '''得到用户（顾客，商家）的订单记录'''
    if 'c' in userid:
        sql = "SELECT customerid,storeid,quantity,total,orderdate FROM T_Order WHERE customerid='{}' ".format(userid)
    else:
        sql = '''SELECT customerid,storeid,quantity,total,orderdate FROM T_Order
                 WHERE storeid in
                    (SELECT distinct(pa.storeid) FROM T_Productattribute pa,T_Product p
	                 WHERE pa.productid=p.productid and p.merchantid='{}')'''.format(userid)
    
    results = searchDB(sql)
    
    return results

def get_customer_name(customerid):
    '''根据顾客的id得到顾客的名称'''
    sql = "SELECT customername FROM T_Customer WHERE customerid='{}' ".format(customerid)
    results = searchDB(sql)
    return results

def get_product_info(storeid):
    '''根据库存id得到商品的名称和店铺的名称：[(shopname,productname)]'''
    productid = 'p'+storeid[1:13]
    sql = '''SELECT m.merchantname,p.productname
            FROM T_Merchant m,
                (SELECT merchantid,productname FROM T_Product WHERE productid='{}') p
            WHERE m.merchantid = p.merchantid'''.format(productid)
            
    return searchDB(sql)


#**********************************支付处理部分********************************
def confirm_paypassword(customerid,paypassword):
    '''验证输入的密码和用户的支付密码是否一致'''
    sql = "SELECT paymentcode FROM T_Customer WHERE customerid ='{}' ".format(customerid)
    #print(sql)
    results = searchDB(sql)
    
    if len(results)<1 : return "0"
    state = "1" if paypassword==results[0][0] else "0"
    return state

def get_order_info(orderids):
    '''根据订单id得到订单项的信息：[（库存id,总金额）]'''
    order_info = list()
    for orderid in orderids:
        sql = '''SELECT storeid,total FROM T_Orderitem WHERE orderid = '{}' '''.format(orderid)
        results = searchDB(sql)
        for storeid,total in results:
            order_info.append((storeid,float(total)))
    return order_info


def get_order_info_customer(orderids):
    '''确认退货时要得到每一个订单的总金额：[(customerid,total)]'''
    order_info = list()
    for orderid in orderids:
        sql = "SELECT o.customerid,oi.total FROM T_Order o,T_Orderitem oi where o.orderid=oi.orderid and o.orderid='{}' ".format(orderid)
        results = searchDB(sql)
        for customerid,total in results:
            order_info.append((customerid.rstrip(),float(total)))
    return order_info


# 4 确认支付
def pay_confirm(customerid,total,paypassword):
    
    '''当生成订单之后需要进行支付,total表示订单的总金额，支付成功返回“1”，否则返回“0”'''
    #首先需要验证支付的密码，当支付密码一样的话继续执行，否则返回303，表示支付密码不正确
    confirm_pass = confirm_paypassword(customerid,paypassword.strip())
    if confirm_pass == "0" : return "0"    

    
    #当账户金额大于订单金额时，从顾客的账户中减去相应的金额
    #当支付成功之后返回“1”，表示支付成功
    conn = pyodbc.connect('''DRIVER={SQL Server Native Client 10.0};SERVER=(local) \SQLEXPRESS;
                        DATABASE=ShoppingWeb;UID=shoppingwebadmin;PWD=shoppingweb123''')
    cur = conn.cursor()
    #验证账户金额是否大于账单的总金额，如果订单金额大于账户余额的话，返回"0“，表示账户余额不足
    sql = "SELECT customerbalance FROM T_Customer WHERE customerid='{}' ".format(customerid)
    cur.execute(sql)
    balance = float(cur.fetchone()[0])
    if total>balance : #如果余额不足的话
        cur.close()
        conn.close()
        return "0"
    
    #如果余额充足的话更新余额
    balance -= total
    sql = "UPDATE T_Customer SET customerbalance={} WHERE customerid='{}' ".format(balance,customerid)
    try:
        cur.execute(sql)
    except:
        print("Something Wrong when executing the sql")
        cur.rollback()
        cur.close()
        conn.close()
        return "0"

    conn.commit()
    cur.close()
    conn.close()

    return "1"
    

# 5 确认收货
def received_confirm_pay(orderids):
    
    #根据订单id得到每笔订单的金额和库存id：[(库存id,总金额）]
    order_info = get_order_info(orderids)

    #数据库的查询部分
    conn = pyodbc.connect('''DRIVER={SQL Server Native Client 10.0};SERVER=(local) \SQLEXPRESS;
                        DATABASE=ShoppingWeb;UID=shoppingwebadmin;PWD=shoppingweb123''')
    cur = conn.cursor()
    
    #根据库存id得到商家id
    shop_total = dict()#表示在这些订单项中店铺的总金额
    for storeid,tol in order_info:
        productid = 'p'+storeid[1:13]
        sql = "SELECT merchantid FROM T_Product WHERE productid='{}' ".format(productid)
        cur.execute(sql)

        shopid = cur.fetchone()[0].rstrip()#根据库存id得到店铺的id
        if shopid == "0" : continue
        shop_total[shopid] = shop_total.get(shopid,0) + tol
    
    
    #将每笔订单对应的金额转到商家的账户
    for shopid,total in shop_total.items():
        sql = "SELECT merchantbalance FROM T_Merchant WHERE merchantid='{}' ".format(shopid)
        cur.execute(sql)
        balance = float(cur.fetchone()[0])
        #更新余额
        balance += total 
        sql = "UPDATE T_Merchant SET merchantbalance={} WHERE merchantid='{}' ".format(balance,shopid)
        
        try:
            cur.execute(sql)
        except:
            print("Something Wrong when executing the sql")
            conn.rollback()
            cur.close()
            conn.close()
            return "0"

    conn.commit()
    cur.close()
    conn.close()

    return "1"


# 6 确认退货 
def agree_return_of_goods_pay(orderids):
    
    #根据订单id得到每笔订单的金额和库存id：[（顾客id,总金额）]
    order_info = get_order_info_customer(orderids)
    
    #将以上的整合成{顾客id：总金额}的形式
    customer_total = dict()
    for customerid,tol in order_info:
        customer_total[customerid] = customer_total.get(customerid,0) + tol
    
    
    #数据库的查询部分
    conn = pyodbc.connect('''DRIVER={SQL Server Native Client 10.0};SERVER=(local) \SQLEXPRESS;
                        DATABASE=ShoppingWeb;UID=shoppingwebadmin;PWD=shoppingweb123''')
    cur = conn.cursor()
    
    #将每笔订单的金额转到顾客对应的账户
    for customerid,total in customer_total.items():
        sql = "SELECT customerbalance FROM T_Customer WHERE customerid='{}' ".format(customerid)
        cur.execute(sql)
        balance = float(cur.fetchone()[0])
        #更新余额
        balance += total 
        sql = "UPDATE T_Customer SET customerbalance={} WHERE customerid='{}' ".format(balance,customerid)
        
        try:
            cur.execute(sql)
        except:
            print("Something Wrong when executing the sql")
            conn.rollback()
            cur.close()
            conn.close()
            return "0"

    conn.commit()
    cur.close()
    conn.close()

    return "1"
#*****************************************************************************
            
    
    

