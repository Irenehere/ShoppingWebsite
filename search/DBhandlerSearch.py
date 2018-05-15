import pyodbc
import datetime
import time

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




#***********************************索引模块***********************************
def index_info(commodity_id):
    '''从根据指定的商品id得到商品的信息，以用作后续的索引
        返回的数据的格式：[(商品名称，商品描述，商品分类)]
    '''
    sql = "SELECT productname,productdescribe,producttype FROM T_Product WHERE productid='{}' ".format(commodity_id)
    results = searchDB(sql)
    return results



def insert_index(commodity_id,keyword_weight):
    '''往数据库中插入索引，index_info的格式：{关键字：总的权重}'''
    #如果这个商品已经有过索引了，那么将其删除
    sql = "SELECT * FROM T_Index WHERE productid='{}' ".format(commodity_id)
    results = searchDB(sql)
    if len(results)>0:
        sql = "DELETE FROM T_Index WHERE productid='{}' ".format(commodity_id)
        state = executeSql(sql)
        if state == "0" : return "0"
        
    
    for keyword,weight in keyword_weight.items():
        #首先要得到关键字的id
        #如果不存在这个关键字，那么往关键字表中插入这个关键字（关键字和关键字类型），然后再得打关键字的id
        sql = "SELECT keywordid FROM T_Keyword WHERE keyword ='{}' ".format(keyword)
        results = searchDB(sql)
        
        if len(results)<1:
            #没有的话需要先插入到数据库中
            keywordid = getKeywordId()
            sql = "INSERT INTO T_Keyword(keywordid,keyword,keywordtype) VALUES('{}','{}',1)".format(keywordid,keyword)
            state = executeSql(sql)
            if state == "0" : return "0"#如果插入关键字出错的话，返回“0”
            time.sleep(1)
        else:
            #如果由的话需要从数据库中找到对应的keywordid
            keywordid = results[0][0]
        
        #将索引插入到数据库中
        sql = "INSERT INTO T_Index(productid,keywordid,price,weight) VALUES('{}','{}',0.01,{})".format(commodity_id,keywordid,weight)
        state = executeSql(sql)
        if state == "0" : return "0"
    
    return "1"
            
#*******************************************************************************



#***********************************商品查询************************************
def get_commodity_detail(commodity_id):
    '''得到指定商品详情页的商品信息：(name,pic,delivery,discount,price)
    '''
    sql = '''SELECT productname,productimage,delivery,discount,price FROM T_Product
            WHERE productid = '{}' '''.format(commodity_id)
    results = searchDB(sql)
    product_info = list()
    for name,pic,delivery,discount,price in results:
        product_info.append((name,pic,delivery.rstrip(),float(discount),float(price)))

    return product_info[0]


def search_based_on_keyword(keyword):
    '''基于单个关键字的搜索
    返回的结果：[(商品id，关键字权重，关键字出价 )]'''
    sql ='''SELECT i.productid,i.weight,i.price FROM T_Index i,(SELECT keywordid,keyword FROM T_Keyword) k
           WHERE i.keywordid = k.keywordid and k.keyword like '%{}%' '''.format(keyword)
    
    results = searchDB(sql)
    
    products = list()
    for productid,weight,price in results:
        products.append((productid.strip(),float(weight),float(price)))
    
    return products


def get_commodity_class(productid):
    '''得到商品的类别'''
    sql = "SELECT producttype FROM T_Product WHERE productid='{}' ".format(productid)
    results = searchDB(sql)
    return results[0][0]


def get_commodity_attrs(productid):
    '''得到商品的属性信息：[(属性，属性值)]'''
    sql = '''SELECT a.attributename,pa.attribute FROM T_ProductAttribute pa,T_Attribute a
            WHERE pa.attributeid = a.attributeid and pa.productid='{}' '''.format(productid)
    results = searchDB(sql)
    return results


def get_commodity_storeinfo(productid):
    '''得到商品的库存信息：[(storeid,storage,attrs),(storeid,storage,attrs)]'''
    storeids = 's'+productid[1:13]
    sql = "SELECT storeid,storage FROM T_Store WHERE storeid like '{}%' ".format(storeids)
    storages = searchDB(sql)
    
    if len(storages)<1 : return []
    
    store_info = list()#存放最终的结果
    
    #得到属性信息：
    for storeid,storage in storages:
        
        #根据storeid得到属性信息：
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
            store_info.append((storeid,storage))
        else:
            store_info.append((storeid,storage,productAttrsInfo))
    
    return store_info
    

def get_product_pics(productid):
    '''得到描述商品的图片信息'''
    sql = '''SELECT imageurl FROM T_Image WHERE productid='{}' 
            ORDER BY imageid ASC'''.format(productid)
    
    results = searchDB(sql)
    urls = list()
    for item in results:
        urls.append(item[0])
        
    return urls

def get_product_comments(productid):
    '''得到商品的评价信息:[customername,customerpic,level,comment]'''
    sql = '''SELECT c.customername,c.customericon,r.level,r.comment FROM T_Remark r,
            (SELECT customerid,customername,customericon FROM T_Customer) c
            WHERE r.customerid = c.customerid and r.productid='{}' '''.format(productid)
    results = searchDB(sql)
    
    return results
    
#****************************************************************************


#***********************************商品排序和筛选部分**************************
def get_commodity_sales(productid):
    '''根据商品的id得到商品的销量'''
    storeids = 's' + productid[1:]
    sql = '''SELECT * FROM T_Order o,T_Orderitem oi WHERE o.orderid = oi.orderid 
             and oi.storeid like '{}%' and o.ordercondition = '3' '''.format(storeids)
    #print(sql)
    results = searchDB(sql)
    return len(results)

def get_commodity_price(productid):
    '''得到商品的价格'''
    sql = "SELECT price FROM T_Product WHERE productid = '{}' ".format(productid)
    results = searchDB(sql)
    return float(results[0][0])


def get_commodity_district(productid):
    '''得到商品的地区'''
    sql='''SELECT m.merchantprovince FROM
          (SELECT productid,merchantid FROM T_Product) p,(SELECT merchantid,merchantprovince FROM T_Merchant) m
          WHERE p.merchantid = m.merchantid and p.productid='{}' '''.format(productid)
    results = searchDB(sql)
    return results[0][0].strip()

#****************************************************************************


#***********************************商品属性************************************
def get_commodity_info(commodity_ids):
    '''根据指定的多个商品的id得到他们的属性信息：[ (商品id，名称，图片，店铺，价格,销量,地区) ]'''
    product_info = list()
    
    for productid in commodity_ids:
        sql1 = '''SELECT p.productid,p.productname,p.productimage,m.merchantname,p.price,m.merchantprovince FROM
                (SELECT productid,productname,productimage,merchantid,price FROM T_Product) p,
                (SELECT merchantid,merchantname,merchantprovince FROM T_Merchant) m
                WHERE p.merchantid = m.merchantid and p.productid='{}' '''.format(productid)
        results = searchDB(sql1)
        
        #得到商品的销量
        storeids = 's' + productid[1:]
        sql2 = '''SELECT * FROM T_Order o,T_Orderitem oi WHERE o.orderid = oi.orderid 
                 and oi.storeid like '{}%' and o.ordercondition = '3' '''.format(storeids)
        sales = len(searchDB(sql2))
        
        #添加商品的信息 
        for item in results:
            product_info.append((item[0].rstrip(),item[1],item[2],item[3],float(item[4]),sales,item[5].rstrip()))
        
    return product_info



#****************************************************************************


#***********************************店铺查询***********************************
def get_shop_brief(productid):
    '''根据店铺的名称得到店铺的基本信息：(id,name,level(店铺商品的综合评分))'''
    #首先得到店铺的id和名称
    sql = '''SELECT merchantid,merchantname FROM T_Merchant WHERE merchantid in
            (SELECT merchantid FROM T_Product WHERE productid='{}')'''.format(productid)
    result = searchDB(sql)
    if len(result)<1 : return ()
    
    shopid = result[0][0].strip()
    shopname = result[0][1]
    
    #得到评论中该店铺的商品的评分的均值
    sql = '''SELECT sum(level),count(level) FROM T_Remark WHERE productid in 
            (SELECT productid FROM T_Product WHERE merchantid='{}')'''.format(shopid)
    
    result = searchDB(sql)
    
    if result[0][1] == 0 : level =  0
    else : level = result[0][0]/result[0][1]
    
    return (shopid,shopname,level)
    
    
def search_shop_based_on_keyword(keyword):
    '''返回形式：[店铺id]'''

def shopInfo_basic(shop_ids):
    '''得到这些店铺的大致信息：[ (店铺id，店铺名称，店铺照片，店铺类型）]'''


def shopInfo_detail(shop_id):
    '''得到这个店铺详细的信息：[id,店铺名称，店铺照片，店铺类型,店铺描述，地址]'''

def get_shop_commodities(shop_id):
    '''得到该店铺所有商品的id:[id,id]'''

#*******************************************************************************

#***********************************相似商品查询************************************
def searchSimilarItems(commodity_id):
    '''某个商品的相似商品：[(相似的商品id，相似度)，（相似的商品id，相似度）]'''
    
#*******************************************************************************

def getKeywordId():
    '''得到关键字的编号'''
    return 'k'+datetime.datetime.now().strftime('%Y%m%d%H%M%S')
