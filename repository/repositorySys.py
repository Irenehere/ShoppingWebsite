'''库存管理系统的数据库接口部分'''
import pyodbc
#***********************************数据库处理************************************
def searchDB(sql):
    '''连接指定的数据库并执行查询的sql语句，如果是查询语句的话返回的是元组的列表：[ (查询的内容) ]
    '''

    #连接数据库
    conn = pyodbc.connect(r'DRIVER={SQL Server Native Client 11.0};SERVER=(local) \SQLEXPRESS;'
                          r'DATABASE=Ubuy;UID=sa;PWD=13422138812a')
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
    conn = pyodbc.connect(r'DRIVER={SQL Server Native Client 11.0};SERVER=(local) \SQLEXPRESS;'
                          r'DATABASE=Ubuy;UID=sa;PWD=13422138812a')
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


#***********************************商品进货************************************
def addCommodityNums(commodity_id,commodity_attrs,num):
    '''增加指定商品库存，并将进货信息增加到数据库中'''


def stock_records(commodity_id):
    '''根据指定的商品id得到商品的进货记录'''
#*********************************************************************************


#***********************************商品销售************************************
def sell(orderid):
    '''在支付成功之后需要减小商品的库存'''
    sql = "select storeid,quantity from T_Order where orderid = '{}'".format(orderid)
    rs = searchDB(sql)[0]
    storeid,quantity = rs[0],rs[1]
    storage = searchDB("select storage from T_Store where storeid = '{}'".format(storeid))[0][0]
    storage_new = int(storage)- int(quantity)
    sql2 = "update T_Store set " \
           "storage = {} where storeid = '{}'".format(storage_new,storeid)
    stm = executeSql(sql2)
    return stm

#********************************************************************************

#***********************************商品退货************************************
def return_products(orderid):
    '''成功退货之后需要减小商品的库存'''
#********************************************************************************