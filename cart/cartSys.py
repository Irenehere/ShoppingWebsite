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



# ***********************显示购物车信息：****************************************
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
            "quantity":"2","total":"58"}]}'''

    sql = "select distinct storeid,quantity,shoppingcarttotal from T_Shoppingcart where customerid='{}'".format(customerid)
    items = searchDB(sql)
    cartinfo = []
    for item in items:
        storeid = item[0]
        quantity = item[1]
        # 根据库存id得到商品属性
        sql4 = "SELECT a.attributename,pa.attribute FROM T_Attribute a ,T_Productattribute pa " \
               "WHERE a.attributeid = pa.attributeid and pa.storeid='{}' ".format(storeid)
        attrs = searchDB(sql4)
        # 得到json格式的属性信息
        productAttrsInfo = '['
        for item in attrs:
            attrname = item[0]
            attrvalue = item[1]
            productAttrsInfo += '{"attrname":"' + attrname + '","attrvalue":"' + attrvalue + '"},'

        productAttrsInfo = productAttrsInfo[:-1] + ']'
        # 根据库存id得到商品id
        productid = 'p' + storeid[1:13]
        # 根据库存id得到商品名称
        sql2 = "SELECT productname FROM T_Product WHERE productid='{}' ".format(productid)
        productname = searchDB(sql2)[0][0]
        # 根据商品id得到商品图片、店铺名称、商品单价
        sql3 = "SELECT p.productimage,m.merchantname,p.price " \
               "FROM T_Product p,(SELECT merchantid,merchantname FROM T_Merchant) m " \
               "WHERE p.merchantid = m.merchantid and p.productid='{}'".format(productid)

        results = searchDB(sql3)[0]
        totalsum = results[2] * quantity


        dict = {"shopname": results[1],
                "products": [{"storeid": storeid, "pic": results[0], "name": productname,"attrs": productAttrsInfo,
                "quantity": item[1], "total": totalsum},
               {"storeid": storeid, "pic": results[0], "name": productname,
                "quantity": item[1], "total": totalsum}]}
        cartinfo.append(dict)
    return cartinfo


# ****************************************************************************************


# ******************删除购物车****************************************************************
def delete_cart_item(customerid, storeid):
    '''删除指定的购物车信息，成功返回"1",否则返回“0”'''
    sql = "DELETE FROM T_Shoppingcart where customerid = '{}' and storeid = '{}'".format(customerid, storeid)
    executeSql(sql)







