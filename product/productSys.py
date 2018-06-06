# -*- coding: utf-8 -*-
"""
账户管理系统
"""
import pyodbc
import json
import datetime
import time


# ***************************数据库处理**************************************
def searchDB(sql):
    '''连接指定的数据库并执行查询的sql语句，如果是查询语句的话返回的是元组的列表：[ (查询的内容) ]
    '''

    # 连接数据库
    conn = pyodbc.connect(r'DRIVER={SQL Server Native Client 11.0};SERVER=(local) \SQLEXPRESS;'
                          r'DATABASE=Ubuy;UID=sa;PWD=13422138812a')
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
    conn = pyodbc.connect(r'DRIVER={SQL Server Native Client 11.0};SERVER=(local) \SQLEXPRESS;'
                          r'DATABASE=Ubuy;UID=sa;PWD=13422138812a')
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


# ******************************商品查询模块**********************************
def get_all_products(merchantid):
    '''根据商家的id得到该商家所有的商品信息,返回的格式：
      [{"productid":"id",
      "productimage":"url",
      "productname":"name",
      "productdate":"date",
      "price":"price",
      "productstate":"0",
      "allStorage":"storage"},
    {"productid":"id",
      "productimage":"url",
      "productname":"name",
      "productdate":"date",
      "price":"price",
      "productstate":"0",
      "allStorage":"storage"}]
    '''
    sql = "SELECT productid,productimage,productname,productdate,price," \
          "productstatement FROM T_Product WHERE merchantid='{}'".format(
        merchantid)
    productinfo = searchDB(sql)
    pdlist = []
    for product in productinfo:
        # 获取所有库存
        pid = product[0]
        sql2 = "select sum(storage) from T_Store where storeid in " \
               "(select storeid from T_Productattribute where productid = '{}')".format(pid)
        allstorage = searchDB(sql2)
        # 将所有商品信息添加到字典
        pd = {"productid": product[0],
              "productimage": product[1],
              "productname": product[2],
              "productdate": product[3],
              "price": str(product[4]),
              "productstate": str(product[5]),
              "allStorage": str(allstorage[0][0])}
        pdlist.append(pd)
    return str(pdlist).replace('\'', '\"')

def search_product_by_id(productid):
    ''''根据商品的id查询商品，返回的信息格式和上面的完全一样'''


def search_product_by_name(name):
    ''''根据商品的名称进行查询，返回的信息格式和上面的完全一样'''


# *******************************************************************************


# ******************************商品上架模块**********************************

def add_product(js):
    '''商家上架商品，传输的格式是js的格式，如下：
    { "productname":"name",
      "delivery":"1",
      "discount":"0.98",
      "price":"price",
      "productimage":"url",
      "productdescribe":"description",
      "productdetail":["url1","url2"]
      "producttype":"producttype"
      "merchantid":"merchantid"}

    如果成功插入数据库中，则返回商品的id,表示上架成功；否则返回"0"，表示上架失败，需要重新提交'''

    # 商品上架时需要分配productid,具体编码规则看报告中的库表设计
    # 插入到商品表的时候要将商品的状态设置为“0”，表示待审核

    # 插入商品表
    pdinfo = json.loads(js)
    # 创建productid
    a = datetime.datetime.now().strftime("%Y%m%d%H%M")
    pid = "p" + a
    date = time.strftime("%Y/%m/%d ",time.localtime())
    sql = "insert into T_product (productid,productname," \
          "delivery,discount,price,productimage,productdescribe,producttype," \
          "productstatement,productdate,recommend,recommendprice,merchantid)" \
          "values('{}','{}','{}',{},{},'{}','{}','{}','{}','{}',{},{},'{}')".format(
        pid, pdinfo["productname"], pdinfo["delivery"], float(pdinfo["discount"]), float(pdinfo["price"]),
        pdinfo["productimage"], pdinfo["productdescribe"], pdinfo["producttype"],"0",date,"0","0",pdinfo["merchantid"]
    )
    print(sql)
    stm = executeSql(sql)

    # 插入图片表
    images = pdinfo["productdetail"]
    for image in images:
        imageid = image[3]
        sql = "insert into T_Image(imageid,imageurl,productid)" \
              "values('{}','{}','{}')".format(imageid, image, pid)
        print(sql)
        stm2 = executeSql(sql)

    if stm == '1' and stm2 == '1':
        return pid
    else:
        return "0"


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



def add_attribute(js):
    '''为指定的商品添加一个属性,js的格式如下：
        {"productid":"id",
         "attrs":[{"attrname":"颜色","attrvalue":"白色"},
                   {"attrname":"尺寸","attrvalue":"小号"}],
         "storage":"99"}

    如果添加成功返回“1”，否则返回“0”
    '''
    pdattr = json.loads(js)
    attrs = pdattr["attrs"]
    productid = pdattr["productid"][1:13]
    snum = searchDB("select count(storeid) from T_Store where storeid like '{}'".format(str("%")+productid+str("%")))[0][0]
    storeid = 's' + productid + (str(snum + 1).zfill(2))
    print(storeid)
    producttype = searchDB("select producttype from T_Product where productid = '{}'".format(pdattr["productid"]))[0][0]
    for attr in attrs:
        attributeid = searchDB("select attributeid from T_Attribute "
                               "where attributename = '{}' and producttype = '{}'".format(
            attr["attrname"], producttype))[0][0]
        sql = "insert into T_Productattribute(productid,attributeid,attribute,storeid)" \
              "values('{}','{}','{}','{}')".format(pdattr["productid"], attributeid, attr["attrvalue"],
                                                   storeid)
        stm1 = executeSql(sql)
    sql2 = "insert into T_store(storeid,storage) values('{}',{})".format(storeid, pdattr["storage"])
    stm2 = executeSql(sql2)
    if stm1 == "1" and stm2 == "1":
        return "1"
    else:
        return "0"


def delete_attribute(js):
    '''删除属性,js的格式：
    {"productid":"id",
     "attrs":[{"attrname":"颜色","attrvalue":"白色"},
              {"attrname":"尺寸","attrvalue":"小号"}]}

    如果成功删除返回“1”，否则返回“0”  '''
    pdattr = json.loads(js)
    attrs = pdattr["attrs"]
    productid = pdattr["productid"]
    storeid =getStoreid(productid,attrs)
    sql = "delete from T_productattribute where productid = '{}' and storeid = '{}'".format(productid,
                                                                                            storeid)
    stm1 = executeSql(sql)
    sql2 = "delete from T_store where storeid = '{}'".format(storeid)
    stm2 = executeSql(sql2)
    if stm1 == "1" and stm2 == "1":
        return "1"
    else:
        return "0"

def get_attributes(productid):
    ''' 返回商品已有属性的数据格式

    返回的格式：
    [{"attrs":[{"attrname":"颜色","attrvalue":"白色"},
               {"attrname":"尺寸","attrvalue":"小号"}],
      "storage":"storage"},
     {"attrs":[{"attrname":"颜色","attrvalue":"白色"}],
      "storage":"storage"}]'''
    storeids = searchDB("select distinct storeid from T_productattribute where productid = '{}'".format(productid))
    lst = []
    for storeid in storeids:
        storeid = storeid[0]
        dict = {}
        attrlst = []
        attrs = searchDB("select attributeid,attribute from T_productattribute "
                         "where productid = '{}' and storeid = '{}'".format(productid, storeid))
        for attr in attrs:
            attrvalue = attr[1]
            attrid = attr[0]
            attrname = searchDB("select attributename from T_Attribute where attributeid = '{}'".format(attrid))[0][0]
            attr_dict = {"attrname": attrname, "attrvalue": attrvalue}
            attrlst.append(attr_dict)
        dict["attrs"] = attrlst
        storage = searchDB("select storage from T_Store where storeid = '{}'".format(storeid))[0][0]
        dict["storage"] = str(storage)
        lst.append(dict)
    return str(lst).replace('\'', '\"')


def to_be_checked_products():
    '''管理员得到要审核的商品,返回的格式如下：
    [{"merchantname":"name",
      "products":[{"productid":"id",
                  "productimage":"image",
                  "allStorage":"allStorage",
                  "price":"price"},
                  {"productid":"id",
                  "productimage":"image",
                  "allStorage":"allStorage",
                  "price":"price"}]},
    {"merchantname":"name",
    "products":[{"productid":"id",
                 "productimage":"image",
                 "allStorage":"allStorage",
                 "price":"price"},
                {"productid":"id",
                 "productimage":"image",
                 "allStorage":"allStorage",
                 "price":"price"}]} ]

    '''
    merchantids = searchDB("select merchantid from T_Merchant")
    cklst = []
    for merchantid in merchantids:
        merchantid = merchantid[0]
        dict = {}
        pdlist = get_all_products(merchantid)
        for pd in pdlist:
            ckpdlst = []
            if pd["productstate"] == "0":
                ckpd = {"productid": pd["productid"],
                        "productimage": pd["productimage"],
                        "allStorage": pd["allStorage"],
                        "price": pd["price"]}
            ckpdlst.append(ckpd)
        if ckpdlst:
            merchantname = \
                searchDB("select merchantname from T_Merchant where merchantid = '{}'".format(merchantid))[0][0]
            dict["merchantname"] = merchantname
            dict["products"] = ckpdlst
            cklst.append(dict)
    return str(cklst).replace('\'', '\"')


def checked_products(productids):
    '''管理员审核通过一些商品，将productids对应的商品的状态设置为1'''
    sql = "update T_Product set productstatement = '1' where productid in ({})".format(str(productids)[1:-1])
    stm = executeSql(sql)
    return stm


def disagree_products(productids):
    '''审核不通过一些商品，将productids对应的商品的状态设置为2'''
    sql = "update T_Product set productstatement = '2' where productid in ({})".format(str(productids)[1:-1])
    stm = executeSql(sql)
    return stm


# *******************************************************************************


# ******************************商品信息修改模块**********************************
def get_product_info(productid):
    '''根据商品的id得到商品的详细信息：
    { "productid":"id",
      "productname":"name",
      "delivery":"1",
      "discount":"0.98",
      "price":"price",
      "productimage":"url",
      "productdescribe":"description",
      "productdetail":["url1","url2"],
      "store":[{ "storeid":"id",
                "attrs":[{"attrname":"颜色","attrvalue":"白色"},
                                  {"attrname":"尺寸","attrvalue":"小号"}],
                "storage":"storage"}}]'''
    # 从商品表获取信息
    sql1 = "select productid,productname,delivery,discount,price,productimage,productdescribe" \
           " from T_Product where productid = '{}'".format(productid)
    pdinfo = searchDB(sql1)[0]
    dict = {"productid": pdinfo[0],
            "productname": pdinfo[1],
            "delivery": pdinfo[2],
            "discount": str(pdinfo[3]),
            "price": str(pdinfo[4]),
            "productimage": pdinfo[5],
            "productdescribe": pdinfo[6]}
    # 从图片表获取信息
    sql2 = "select imageurl from T_Image where productid = '{}'".format(productid)
    iminfo = searchDB(sql2)
    imlst = []
    for im in iminfo:
        imlst.append(im[0])
    dict["productdetail"] = imlst
    # 获取库存信息
    slst = []
    storeids = searchDB("select distinct storeid from T_Productattribute where productid = '{}'".format(productid))
    for storeid in storeids:
        sdict = {}
        storeid = storeid[0]
        sdict["storeid"] = storeid
        attrlst = []
        attrs = searchDB("select attributeid,attribute from T_productattribute "
                         "where productid = '{}' and storeid = '{}'".format(productid, storeid))
        for attr in attrs:
            attrvalue = attr[1]
            attrid = attr[0]
            attrname = searchDB("select attributename from T_Attribute where attributeid = '{}'".format(attrid))[0][0]
            attr_dict = {"attrname": attrname, "attrvalue": attrvalue}
            attrlst.append(attr_dict)
        sdict["attrs"] = attrlst
        storage = searchDB("select storage from T_Store where storeid = '{}'".format(storeid))[0][0]
        sdict["storage"] = str(storage)
        slst.append(sdict)
    dict["store"] = slst
    return str(dict).replace('\'', '\"')


def alter_product_info(js):
    '''修改商品的基本信息，传进来的js格式和商家商品的完全一样：
     {"productid":"productid",
     "productname":"name",
      "delivery":"1",
      "discount":"0.98",
      "price":"price",
      "productimage":"url",
      "productdescribe":"description",
      "productdetail":["url1","url2"]}
    '''

    pdinfo = json.loads(js)
    # 插入商品表
    productid = pdinfo["productid"]
    sql1 = "update T_Product " \
           "set productname = '{}',delivery = '{}',discount = {}, " \
           "price ={},productimage = '{}', productdescribe = '{}'" \
           "where productid = '{}'".format(
        pdinfo["productname"], pdinfo["delivery"], float(pdinfo["discount"]), float(pdinfo["price"]),
        pdinfo["productimage"], pdinfo["productdescribe"], productid)
    stm1 = executeSql(sql1)
    # 插入图片表
    sql2 = "delete from T_Image where productid = '{}'".format(productid)
    stm2 = executeSql(sql2)

    images = pdinfo["productdetail"]
    for image in images:
        inum = searchDB('select count(imageid) from T_Image')[0][0]
        imageid = 'i' + str(inum + 1).zfill(6)
        sql3 = "insert into T_Image(imageid,imageurl,productid)" \
               "values('{}','{}','{}')".format(imageid, image, productid)
        stm3 = executeSql(sql3)
    if stm1 == "1" and stm2 == "1" and stm3 == "1":
        return "1"
    else:
        return "0"


# *******************************************************************************

# ******************************商品下架模块**********************************
def delete_products(productids):
    '''删除productids对应的商品的信息（同时删掉T_Product,T_Productattribute,T_Storez中的信息)'''
    for productid in productids:
        sql1 = "delete from T_Product where productid = '{}'".format(productid)
        stm1 = executeSql(sql1)
        sql2 = "delete from T_Store where storeid in (" \
               "select distinct storeid from T_Productattribute where productid = '{}')".format(productid)
        stm2 = executeSql(sql2)
        sql3 = "delete from T_Productattribute where productid = '{}'".format(productid)
        stm3 = executeSql(sql3)
        if stm1 == "0" or stm2 == "0" or stm3 == "0":
            return "0"
    return "1"


# *******************************************************************************

# ******************************商品推广模块**********************************
'''这部分我放到推荐系统那里了'''
# *******************************************************************************
