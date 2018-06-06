"""
购物车管理系统
"""
import json
import datetime
import pyodbc

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


# ***********************添加到购物车**************************************
'''
添加购物车：

传进来的参数的格式：
    {"customerid":"c201804281551",
     "storeid":"id",
     "num":"num",
     "total":"total}


返回："1"表示成功，"0"表示失败
'''
def getcartid():
    '''得到订单的编号'''
    return 'z'+datetime.datetime.now().strftime('%Y%m%d%H%M%S')

def add_cart(js):
    cart_info = json.loads(js)
    customerid = cart_info["customerid"]
    storeid = cart_info["storeid"]
    quantity = int(cart_info["num"])
    total = float(cart_info["total"])
    date = cart_info["date"]

    sql = "select storage from T_Store where storeid = '{}'".format(storeid)
    storagem = searchDB(sql)
    if storagem:
        sql2 = "SELECT quantity FROM T_Shoppingcart where customerid = '{}' and storeid = '{}'".format(customerid,storeid)
        cartnum = searchDB(sql2)
        if cartnum :
            numm = int(cartnum[0][0]) + quantity
            # 根据库存id得到商品id
            productid = 'p' + storeid[1:13]
            sql4 = "SELECT p.price FROM T_Product p WHERE  p.productid='{}'".format(productid)
            print(sql4)
            result = searchDB(sql4)
            total = numm * float(result[0][0])
            sql5 = "update T_Shoppingcart set quantity = '{}' , shoppingcarttotal = '{}' where customerid = '{}' and storeid = '{}'".format(
                numm, total, customerid, storeid)
            print(sql5)
            return executeSql(sql5)
        else:
            cartid = getcartid()
            sql3 = "INSERT INTO T_Shoppingcart(cartid,customerid,storeid,quantity,shoppingcarttotal,date) VALUES('{}','{}','{}',{},{},'{}')".format(
                cartid,customerid, storeid, quantity, total,date)
            return executeSql(sql3)
    else:
        print("库存不足！")
        return "0"



# ***********************显示购物车信息：***********************************************************
def cart_info(customerid):
    '''根据顾客id得到购物车的信息，如果没有购物车信息的话返回“0”，否则返回以下格式的数据：
[{"shopname":"name",
"products":[{"storeid":"id","pic":"url","name":"name",
           "attrs":[{"attrname":"颜色","attrvalue":"白色"},
                    {"attrname":"尺寸","attrvalue":"小号"}],
            "quantity":"2","total":"58"},
           {"storeid":"id","pic":"url","name":"name",
            "quantity":"2","total":"58"}]},
{"shopname":"name",
"products":[{"storeid":"id","pic":"url","name":"name",
           "attrs":[{"attrname":"颜色","attrvalue":"白色"},
                    {"attrname":"尺寸","attrvalue":"小号"}],
            "quantity":"2","total":"58"},
           {"storeid":"id","pic":"url","name":"name",
           "quantity":"2","total":"58"}]}]'''

    sql = "select distinct storeid from T_Shoppingcart where customerid='{}'".format(customerid)
    items = searchDB(sql)
    # 根据库存id得到不同的店铺
    shop_store = dict()
    for item in items:
        storeid = item[0]
        shopname = get_shopname_based_on_storeid(storeid)
        shop_store.setdefault(shopname,[])
        shop_store[shopname].append(storeid)

    '''为不同的店铺生成不同的信息'''
    cartallinfo = '['
    for shopname, storeids in shop_store.items():
        cartinfo = '{"shopname":"' + shopname + '","products":"' + '['
        for storeid in storeids:
            cartinfo += pInfo(customerid,storeid) + '",'
        cartinfo = cartinfo[:-1] + ']},'
    cartallinfo = cartallinfo[:-1] + ']'
    return cartallinfo


# 产品属性信息
def productsInfo(customerid):
    '''根据顾客id得到一系列属性等信息,格式如下：
           [{"storeid":"id","pic":"url","name":"name",
           "attrs":[{"attrname":"颜色","attrvalue":"白色"},
                    {"attrname":"尺寸","attrvalue":"小号"}],
            "quantity":"2","total":"58"},
           {"storeid":"id","pic":"url","name":"name",
            "quantity":"2","total":"58"}]'''

    sql = "select distinct storeid from T_Shoppingcart where customerid='{}'".format(customerid)
    items = searchDB(sql)
    productsInfo = '['
    for item in items:
        storeid = item[0]
        # 得到商品的名称
        productid = 'p' + storeid[1:13]
        sql2 = "SELECT productname FROM T_Product WHERE productid='{}' ".format(productid)
        productname = searchDB(sql2)[0][0]
        sql5 = "SELECT p.productimage FROM T_Product p WHERE  p.productid='{}'".format(productid)
        productimage = searchDB(sql5)[0][0]
        sql6 = "SELECT  p.price FROM T_Product p WHERE  p.productid='{}'".format(productid)
        productprice = searchDB(sql6)[0][0]

        # 得到商品的属性
        sql3 = '''SELECT a.attributename,pa.attribute FROM T_Attribute a ,T_Productattribute pa
                WHERE a.attributeid = pa.attributeid and pa.storeid='{}' '''.format(storeid)
        attrs = searchDB(sql3)
        # 得到该商品的数量和价格
        sql4 = "select quantity,shoppingcarttotal from T_Shoppingcart where customerid = '{}' and storeid = '{}'".format(customerid, storeid)
        quantity_total = searchDB(sql4)
        # 数量：quantity_total[0][0]  价格:quantity_total[0][1]
        quantity = str(quantity_total[0][0])

        totalsum = str(productprice * quantity_total[0][0])

        # 得到json格式的属性信息
        productAttrsInfo = '['
        for item in attrs:
            attrname = item[0]
            attrvalue = item[1]
            productAttrsInfo += '{"attrname":"' + attrname + '","attrvalue":"' + attrvalue + '"},'
        productAttrsInfo = productAttrsInfo[:-1] + ']'

        productInfo1 = '{"storeid":"' + storeid + '","pic":"' + productimage + '","name"："' + productname + '","attrs":' + productAttrsInfo + ',"quantity":"' + quantity + '","total":"' + totalsum + '"}'
        productInfo2 = '{"storeid":"' + storeid + '","pic":"' + productimage + '","name"："' + productname + '","quantity":"' + quantity + '","total":"' + totalsum + '"}'

        if len(productAttrsInfo) < 2:
            productsInfo += productInfo2+','
        else:
            productsInfo += productInfo1 + ','

    productsInfo = productsInfo[:-1] + ']'
    return productsInfo

def get_shopname_based_on_storeid(storeid):
    '''根据库存id得到店铺的名称'''
    productid = 'p' + storeid[1:13]
    results = searchDB( "SELECT m.merchantname FROM T_Product p,(SELECT merchantid,merchantname FROM T_Merchant) m " \
          "WHERE p.merchantid = m.merchantid and p.productid='{}'".format(productid))
    shopname = results[0][0]
    return shopname

# ****************************************************************************************


# ******************删除购物车****************************************************************
def delete_cart_item(customerid, storeid):
    '''删除指定的购物车信息，成功返回"1",否则返回“0”'''
    sql = "DELETE FROM T_Shoppingcart where customerid = '{}' and storeid = '{}'".format(customerid, storeid)
    executeSql(sql)




