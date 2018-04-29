import pyodbc
import datetime
import os

'''
这个文件主要的作用就是将电影的数据写入到数据库MoviesRate.sqlite中 ,
并以字典的形式返回数据库中的数据，
'''

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

#*******************************协同过滤部分***************************************
def productid_from_storeid(storeid):
    '''根据库存id得到商品id'''
    return 'p'+storeid[1:13]

def all_customer_orders():
    '''得到所有顾客的订单'''
    #构造sql语句得到所有顾客的订单：[(顾客id,商品id, 购买日期)]
    sql = '''SELECT customerid,storeid,orderdate FROM T_Order ORDER BY orderdate ASC'''
    results = searchDB(sql)
    #将三元组转换我字典的形式：{用户：[购买物品：日期]}并返回
    orders = dict()
    for customerid,storeid,date in results:
        customerid = customerid.rstrip()
        orders.setdefault(customerid,{})
        orders[customerid][productid_from_storeid(storeid)] = date.strftime('%Y-%m-%d')

    return orders


def update_item_similarity(similarity):
    '''将物品的相似度列表更新到数据库中
    similarity的形式： {物品：{相似物品：相似度}}
    '''
    #首先需要将字典转换为三元组的形式： [ (物品，相似物品，相似度)]
    sims = []
    for item1,items in similarity.items():
        for item2,sim in items.items():
            sims.append([item1,item2,sim])

    #将三元组的每一条插入到数据库中
    conn = pyodbc.connect('''DRIVER={SQL Server Native Client 10.0};SERVER=(local) \SQLEXPRESS;
                        DATABASE=ShoppingWeb;UID=shoppingwebadmin;PWD=shoppingweb123''')
    cur = conn.cursor()
    #得到原有表的相似度：
    exist_sim = []
    cur.execute("SELECT productid1,productid2 FROM T_Itemsimilarity")
    for p1,p2 in cur:
        exist_sim.append((p1.rstrip(),p2.rstrip()))
    #如果相似度存在的话更新，否则进行插入操作
    count = 0
    for item1,item2,sim in sims:
        if (item1,item2) in exist_sim:
            cur.execute('''UPDATE T_Itemsimilarity SET similarity=?
                        WHERE productid1=? and productid2=?''',(sim,item1,item2))
        else:
            cur.execute("INSERT INTO T_Itemsimilarity VALUES(?,?,?)",(item1,item2,sim))

        count += 1
        if count%100 == 0 :conn.commit()

    conn.commit()
    cur.close()
    conn.close()


def get_item_similarity():
    '''从数据库中得到形似度列表'''
    #{物品：{相似物品：相似度}}
    sql = "SELECT * FROM T_Itemsimilarity"
    results = searchDB(sql)

    itemsim = dict()
    for p1,p2,sim in results:
        p1 = p1.rstrip()
        p2 = p2.rstrip()
        itemsim.setdefault(p1,{})
        itemsim[p1][p2] = float(sim)

    return itemsim


def orders_based_on_customerId(customer_id):
    '''根据顾客的id从数据库中查找到订单'''
    #根据id构造sql语句查找到订单记录： [ (购买的物品，日期 ) ]
    sql = "SELECT storeid,orderdate FROM T_Order WHERE customerid= '"+customer_id+"'"
    results = searchDB(sql)
    #将元组的形式转换为字典的形式 { 购买的物品：日期 }
    related_products = dict()
    for storeid,date in results:
        related_products[productid_from_storeid(storeid)] = date.strftime('%Y-%m-%d')

    return related_products


#******************************************************************************


#*****************************基于用户特征的推荐*********************************
def orders_based_on_customer_features(customer_id):
    '''根据顾客的id从数据库中找到类似的顾客，再得到他们的购买记录'''
    #首先得到该顾客的sex和age
    sql = "SELECT gender,age FROM T_Customer WHERE customerid= '{}'".format(customer_id)
    result = searchDB(sql)
    gender,age = result[0]

    #然后构造sql语句从订单表中找到和该顾客类似的顾客的购买记录得到三元组
    sql = '''SELECT o.customerid,o.storeid,o.orderdate FROM T_Order o
            WHERE o.customerid in
                (SELECT customerid FROM T_Customer
                WHERE gender={} and age>={} and age<={})'''.format(gender,age-3,age+3)
    results = searchDB(sql)

    #将三元组转换为字典的形式返回 { 用户：{购买物品：购买日期}}
    orders = dict()
    for customerid,storeid,date in results:
        customerid = customerid.rstrip()
        orders.setdefault(customerid,{})
        orders[customerid][productid_from_storeid(storeid)] = date.strftime('%Y-%m-%d')

    return orders
    
#******************************************************************************

#*********************************过滤部分*************************************
def get_recommend_commodities():
    '''得到推广列表中的商品及其出价
       返回的结果形式：[(推广的商品ID,出价)]
    '''
    sql = "SELECT productid,recommendprice FROM T_Product WHERE recommend='1' "
    results = searchDB(sql)
    rec_products = []
    for pid,price in results:
        rec_products.append((pid[:13],float(price)))
    return rec_products
    

#******************************************************************************

#*********************************得到推荐商品的属性信息**************************
def get_recommend_commodities_attributes(commodity_ids):
    '''给定商品id，得到推荐的商品的相关信息
        commodity_ids :列表，表示推荐的商品的id
        返回的形式[ (商品id，名称，图片，价格) ]
    '''
    sql = '''SELECT p.productid,p.productname,p.productimage,m.merchantname,p.price
            FROM T_Product p,(SELECT merchantid,merchantname FROM T_Merchant) m
            WHERE p.merchantid = m.merchantid '''
    results = searchDB(sql)
    
    commodities_attr = {}
    for pid,name,image,merchant,price in results:
        pid = pid[:13]
        if pid not in commodity_ids : continue
        commodities_attr[pid] = (name,image,merchant,float(price))
   
    #对删选得到的结果进行排序
    sorted_results = []
    for pid in commodity_ids:
        name,image,merchant,price = commodities_attr[pid]
        sorted_results.append((pid,name,image,merchant,price))
    
    return sorted_results
#******************************************************************************
