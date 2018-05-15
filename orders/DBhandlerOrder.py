import datetime
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



#*****************************插入订单******************************************
def insertOrder(customerid,date):
    '''将一条订单插入到订单表中，并将订单的状态设置为已支付“1”'''
    orderid = getOrderid()
    sql = "INSERT INTO T_Order(orderid,customerid,ordercondition,orderdate) VALUES('{}','{}','1','{}')".format(orderid,customerid,date)
    state = executeSql(sql)
    
    return orderid if state=="1" else "0"

def insertOrderItem(orderid,storeid,quantity,total):
    '''插入一条订单项到数据库中'''
    sql = "INSERT INTO T_Orderitem(orderid,storeid,quantity,total) VALUES('{}','{}',{},{})".format(orderid,storeid,quantity,total)
    return executeSql(sql)

def cancelOrder(orderids):
    '''当插入订单有错时，需要删除数据库中的相关数据'''
    for orderid in orderids:
        sql1 = "DELETE FROM T_Order WHERE orderid='{}' ".format(orderid)
        sql2 = "DELETE FROM T_Orderitem WHERE orderid='{}' ".format(orderid)
    
        executeSql(sql1)
        executeSql(sql2)

def cartInfo(customerid,storeids):
    '''根据storeid和customersid从数据库中得到购物车的信息：数量，价格
    {(库存id:(数量，订单金额)，库存id:(数量，订单金额)}'''
    productsInfo = {}
    for storeid in storeids:
       sql = '''SELECT quantity,shoppingcarttotal FROM T_Shoppingcart
               WHERE customerid='{}' and storeid='{}' '''.format(customerid,storeid)
       number,tol = searchDB(sql)[0]
       productsInfo[storeid] = (number,float(tol))

    return productsInfo 


def get_shopid_based_on_storeid(storeid):
    '''根据库存id得到店铺的id'''
    productid = 'p'+storeid[1:13]
    sql = "SELECT merchantid FROM T_Product WHERE productid='{}' ".format(productid)
    results = searchDB(sql)
    
    return results[0][0].strip()
    



def getStoreid(productid,attrs):
    '''根据单个的商品id和属性得到库存id;
       属性的格式：attrs: [{"attrname":"颜色","attrvalue":"白色"},
                          {"attrname":"尺寸","attrvalue":"小号"}]
    '''
    #首先要根据商品id和属性的名称得到属性的id
    #然后根据商品id,属性id，属性值从T_Productattribute表中得到库存id并返回
    storeids  = []
    for attr in attrs:
        sql = '''SELECT pa.storeid FROM T_ProductAttribute pa,
                 (SELECT p.productid,a.attributeid FROM T_Product p,T_Attribute a
                  WHERE p.producttype = a.producttype and p.productid = '{}' and a.attributename='{}') m
	                   WHERE pa.productid = m.productid and pa.attributeid = m.attributeid
                      and pa.attribute='{}' '''.format(productid,attr["attrname"],attr["attrvalue"])
        #print(sql)

        storeid_one_attr = searchDB(sql)
        storeids.append(storeid_one_attr)

    #得到该属性组合对应的唯一的库存id:根据库存id出现的次数来找到在结果中都出现的库存id
    counts = {}
    for item in storeids:
        for result in item:
            storeid = result[0]
            counts[storeid] = counts.get(storeid,0) + 1
    for storeid,count in counts.items():
        if count == len(storeids):
            return storeid


def getProductDiscount(productid):
    '''得到商品的折扣信息'''
    sql = "SELECT discount FROM T_Product WHERE productid='{}'".format(productid)
    result = searchDB(sql)

    return float(result[0][0])



def getStorage(storeid):
    '''根据库存id得到商品的库存'''
    sql = "SELECT storage FROM T_Store WHERE storeid = '{}'".format(storeid)
    result = searchDB(sql)

    return result[0][0]



def getCustomerInfo(customerid):
    '''根据顾客id得到顾客的信息：（用户名，手机号，省份，地址）'''
    sql = "SELECT customername,phonenumber,customerprovince,customeraddress FROM T_Customer WHERE customerid='{}'".format(customerid)
    result = searchDB(sql)

    return result[0]


"""
def insertOrder(customerid,storeid,state,number,tol,date,orderid=None):
    '''将订单信息（顾客id,库存id，订单状态，数量，金额）插入到数据库中'''
    #首先需要生成订单编号
    if orderid is None:
        orderid = getOrderid()
        sql1 = "INSERT INTO T_Order(orderid,customerid,ordercondition,orderdate) VALUES('{}','{}','{}','{}')".format(orderid,customerid,state,date)
        executeSql(sql1)
        
    sql2 ="INSERT INTO T_Orderitem(orderid,storeid,quantity,total) VALUES('{}','{}',{},{})".format(orderid,storeid,number,tol)
    state = executeSql(sql2)
    #返回订单编号
    return orderid
"""

def productsInfo(storeids):
    '''根据库存id得到商品的名称、属性等信息，storeids是一个列表
    {库存id:(名称，json格式的属性)，库存id:(名称，json格式的属性)}

    属性的格式： [{"attrname":"颜色","attrvalue":"白色"},{"attridname":"尺寸","attrvalue":"小号"}]
    注：属性可以没有，那么结果为{库存id:名称}'''

    productsInfo = {}
    for storeid in storeids:
        #得到商品的名称
        productid = 'p'+storeid[1:13]
        sql = "SELECT productname FROM T_Product WHERE productid='{}' ".format(productid)
        productname = searchDB(sql)[0][0]

        #得到商品的属性
        sql = '''SELECT a.attributename,pa.attribute FROM T_Attribute a ,T_Productattribute pa
                WHERE a.attributeid = pa.attributeid and pa.storeid='{}' '''.format(storeid)
        attrs = searchDB(sql)
        #得到json格式的属性信息
        productAttrsInfo='['
        for item in attrs:
            attrname = item[0];attrvalue = item[1]
            productAttrsInfo += '{"attrname":"'+attrname+'","attrvalue":"'+attrvalue+'"},'

        productAttrsInfo = productAttrsInfo[:-1]+']'

        if len(productAttrsInfo)<2:
            productsInfo[storeid] = productname
        else:
            productsInfo[storeid] = (productname,productAttrsInfo)

    return productsInfo

#******************************************************************************



#***********************************订单处理************************************
def shipment_confirm(orderids):
    '''确认发货'''
    for orderid in orderids:
        sql = "UPDATE T_Order SET ordercondition='2' WHERE orderid = '{}' and ordercondition='1' ".format(orderid)
        state = executeSql(sql)
        if state =="0" : return "0"
        
    return "1"

def received_confirm(orderids):
    '''确认收货'''
    leftovers = []
    for orderid in orderids:
        sql = "UPDATE T_Order SET ordercondition='3' WHERE orderid = '{}' and ordercondition='2' ".format(orderid)
        executeSql(sql)
        #检验是否达到收货的条件
        sql = "SELECT * FROM T_Order WHERE orderid = '{}' and ordercondition='3' ".format(orderid)
        result = searchDB(sql)
        if len(result)<1:
            leftovers.append(orderid)

    if len(leftovers)<1:
        return "1"
    else:
        return str(leftovers).replace('\'','\"')


def apply_for_return_of_goods(orderids):
    '''申请退货'''
    leftovers = []
    for orderid in orderids:
        sql = "UPDATE T_Order SET ordercondition='4' WHERE orderid = '{}' and ordercondition in ('1','2') ".format(orderid)
        executeSql(sql)
        
        #检查是否真的可以退货
        sql = "SELECT * FROM T_Order WHERE orderid = '{}' and ordercondition='4' ".format(orderid)
        result = searchDB(sql)
        if len(result)<1:
            leftovers.append(orderid)

    if len(leftovers)<1:
        return "1"
    else:
        return str(leftovers).replace('\'','\"')


def agree_return_of_goods(orderids):
    '''确认退货'''
    for orderid in orderids:
        sql = "UPDATE T_Order SET ordercondition='5' WHERE orderid = '{}' and ordercondition='4' ".format(orderid)
        executeSql(sql)

    return "1"


def deleteOrders(orderids):
    '''从数据库中删除指定订单编号的订单'''
    
    unable_delete_orders = []#保存未删除的订单
    for orderid in orderids:
        sql = "DELETE FROM T_Order WHERE orderid = '{}' and (ordercondition='3' or ordercondition='5') ".format(orderid)
        #print(sql)
        executeSql(sql)
        
        #检查是否真的删除了
        sql = "SELECT * FROM T_Order WHERE orderid='{}' ".format(orderid)
        result = searchDB(sql)
        if len(result)>0:  #搜索的结果大于0，说明在订单表中没能删除这个订单，那么在订单项中也不能删除相关订单项
            unable_delete_orders.append(orderid)
            continue
        
        #如果确实删除了的话，需要删除订单项中的记录
        sql = "DELETE FROM T_Orderitem WHERE orderid ='{}' ".format(orderid)
        executeSql(sql)


    if len(unable_delete_orders)<1:
        return "1"
    else:
        return str(unable_delete_orders).replace('\'','\"')




def cancelOrders(orderids):
    '''取消状态为“未付款”的订单
    orders[orderid1,orderid2]'''

    for orderid in orderids:
        sql = "DELETE FROM T_Order WHERE orderid = '{}' and ordercondition='0' ".format(orderid)
        sql2 = "DELETE FROM T_Orderitem WHERE orderid='{}' ".format(orderid)
        executeSql(sql)
        executeSql(sql2)

    #检查是否已经删掉了
    leftovers = []
    for orderid in orderids:
        sql = "SELECT * FROM T_Order WHERE orderid = '{}' and ordercondition='0' ".format(orderid)
        result = searchDB(sql)
        if len(result)>0:
            leftovers.append(orderid)

    if len(leftovers)<1:
        return "1"
    else:
        return str(leftovers).replace('\'','\"')
#*******************************************************************************


#***********************************订单查询************************************
def getOrders_based_on_state(state,customerid=None,shopid = None,orderid=None):
    '''根据订单的状态来查询订单信息，
    返回的格式：[(订单id,顾客id,库存id,订单状态，数量，金额，日期)]
    '''
    if customerid is not None:
        #sql = "SELECT orderid,customerid,storeid,ordercondition,quantity,total,orderdate FROM T_Order WHERE customerid='{}' ".format(customerid)
        sql = '''SELECT o.orderid,o.customerid,oi.storeid,o.ordercondition,oi.quantity,oi.total,o.orderdate FROM T_Order o,T_Orderitem oi 
                WHERE o.orderid=oi.orderid and o.customerid='{}' '''.format(customerid)
    if shopid is not None:
        sql = '''SELECT o.orderid,o.customerid,oi.storeid,o.ordercondition,oi.quantity,oi.total,o.orderdate FROM T_Order o,T_Orderitem oi
                 WHERE o.orderid = oi.orderid and oi.storeid in
                     (SELECT distinct(pa.storeid) FROM T_Productattribute pa,T_Product p
	                  WHERE pa.productid=p.productid and p.merchantid='{}') '''.format(shopid)

    if state!='all':
        sql += "and o.ordercondition='{}' ".format(state)

    if orderid is not None:
        sql += "and o.orderid='{}' ".format(orderid)

    #print(sql)

    results = searchDB(sql)

    orders = []
    for row in results:
        orderid = row[0];customerid = row[1][:13]
        storeid = row[2];ordercondition=row[3]
        quantity = row[4];total = float(row[5])
        date = row[6].strftime('%Y-%m-%d')
        one = (orderid,customerid,storeid,ordercondition,quantity,total,date)
        orders.append(one)

    return orders



def getProductInfo(storeids):
    '''根据库存id得到商品的图片，店铺，价格{库存id:(图片，店铺，价格）}'''
    productsInfo = {}

    for storeid in storeids:
        #得到商品的名称
        productid = 'p'+storeid[1:13]
        sql = '''SELECT p.productimage,m.merchantname,p.price 
                    FROM T_Product p,(SELECT merchantid,merchantname FROM T_Merchant) m 
                    WHERE p.merchantid = m.merchantid and p.productid='{}' '''.format(productid)
        results = searchDB(sql)
        productsInfo[storeid] =(results[0][0],results[0][1],float(results[0][2]))

    return productsInfo
#*******************************************************************************

def getOrderid():
    '''得到订单的编号'''
    return 'o'+datetime.datetime.now().strftime('%Y%m%d%H%M%S')
