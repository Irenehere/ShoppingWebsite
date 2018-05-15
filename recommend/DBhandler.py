import pyodbc
import datetime
import time

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
        conn.commit()
        cur.close()
        conn.close()
        return "0"

    conn.commit()
    cur.close()
    conn.close()

    return "1"
    
    
#*******************************协同过滤部分***************************************
def productid_from_storeid(storeid):
    '''根据库存id得到商品id'''
    return 'p'+storeid[1:13]

def all_customer_orders():
    '''得到所有顾客的订单'''
    #构造sql语句得到所有顾客的订单：[(顾客id,库存id, 购买日期)]
    sql = '''SELECT o.customerid,oi.storeid,o.orderdate FROM T_Order o,T_Orderitem oi 
             WHERE o.orderid = oi.orderid and o.ordercondition='3' ORDER BY o.orderdate'''
    results = searchDB(sql)
    
    #得到用户喜欢的商品
    sql = "SELECT customerid,productid,date FROM T_Customertaste WHERE taste = 1"
    likes = searchDB(sql)
    
    #合并用户的订单和喜欢的物品
    results.extend(likes)
    
    #将三元组转换我字典的形式：{用户：[购买物品：日期]}并返回
    orders = dict()
    for customerid,storeid,date in results:
        customerid = customerid.rstrip()
        orders.setdefault(customerid,{})
        if 's' in storeid:
            productid = productid_from_storeid(storeid)
        else:
            productid = storeid[:13]
        orders[customerid][productid] = date.strftime('%Y-%m-%d')

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
    sql = '''SELECT oi.storeid,o.orderdate FROM T_Order o,T_Orderitem oi 
             WHERE o.orderid = oi.orderid and o.ordercondition='3' and o.customerid='{}' '''.format(customer_id)
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
    if len(result)<1:print('NOT SUCH CUSTOMER!')
    gender,age = result[0]

    #然后构造sql语句从订单表中找到和该顾客类似的顾客的购买记录得到三元组
    sql = '''SELECT o.customerid,oi.storeid,o.orderdate FROM T_Order o,T_Orderitem oi 
             WHERE o.orderid = oi.orderid and o.ordercondition='3' and o.customerid in 
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
    sql = "SELECT productid,recommendprice FROM T_Product WHERE recommend=1 "
    results = searchDB(sql)
    rec_products = []
    for pid,price in results:
        rec_products.append((pid[:13],float(price)))
    return rec_products

def get_dislike_commodities(customerid):
    '''得到顾客不喜欢的商品的id,返回商品id的列表'''
    sql = "SELECT productid FROM T_Customertaste WHERE taste=0 "
    results = searchDB(sql)
    
    dislike_items = []
    for productid in results:
        productid = productid[0][:13]
        dislike_items.append(productid)
        
    return dislike_items
    

#******************************************************************************

#*********************************得到推荐商品的属性信息*************************
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

def get_productname(productid):
    '''根据商品的id得到商品的名称'''
    sql = "SELECT productname FROM T_Product WHERE productid = '{}' ".format(productid)
    result = searchDB(sql)
    return result[0][0].rstrip()

def get_shopname(productid):
    '''根据商品id得到店铺的名称'''
    sql = '''SELECT merchantname FROM T_Merchant WHERE merchantid in 
            (SELECT merchantid FROM T_Product WHERE productid='{}')'''.format(productid)
    results = searchDB(sql)
    return results[0][0]
#******************************************************************************



#***************************商品推广部分***************************************
def get_shop_items(shopid):
    '''得到店铺的所有商品：[(id,name),(id,name)]'''
    sql = "SELECT productid,productname FROM T_Product WHERE merchantid='{}' ".format(shopid)
    results = searchDB(sql)
    products = list()
    for id,name in results:
        id = id[:13]
        products.append((id,name))
        
    return products

def get_shop_recommend_items(shopid):
    '''得到某个店铺推荐的商品信息：[(id,name,price)]'''
    sql = '''SELECT productid,productname,recommendprice FROM T_Product 
             WHERE merchantid='{}' and recommend=1 '''.format(shopid)
    results = searchDB(sql)
    shop_recitem_info = list()
    for id,name,price in results:
        id = id[:13]
        price = float(price)
        shop_recitem_info.append((id,name,price))
    return shop_recitem_info
    
def add_recommend(productid,price):
    '''为商品添加或修改推荐的价格'''
        #更新T_Product中的内容：if recommend="1", update recommendprice
    #else set recommend = "1" and set recommendprice
    #首先得到指定商品的推荐状态
    sql = "SELECT recommend FROM T_Product WHERE productid='{}' ".format(productid)
    results = searchDB(sql)
    rec_state = results[0][0]
    if rec_state == 0 :
        sql = "UPDATE T_Product SET recommend=1,recommendprice={} WHERE productid='{}' ".format(price,productid)
    else:
        sql = "UPDATE T_Product SET recommendprice={} WHERE productid='{}' ".format(price,productid)
        
    return executeSql(sql)

def delete_recommendation(productid):
    '''删除某个商品的推荐'''
    sql = "UPDATE T_Product SET recommend=0 WHERE productid='{}' ".format(productid)
    return executeSql(sql)
   

def get_shop_headlines(shopid):
    '''根据店铺的id得到店铺的头条[(id,price,state)]''' 
    sql = '''SELECT productid,price,statement FROM T_Headline WHERE productid in 
            (SELECT productid FROM T_Product where merchantid='{}') '''.format(shopid)
    results = searchDB(sql)
    headlines = list()
    for id,price,state in results:
        headlines.append((id[:13],float(price),state))
    
    return headlines

def add_headline(productid,price,img):
    '''为商品申请头条'''
    #如果该商品已经在T_Headline中存在了，那么更新价格；否则重新插入一条头条申请
    #无论是更新还是插入，都需要将状态设置为“0”
    sql = "SELECT * FROM T_Headline WHERE productid='{}' ".format(productid)
    results = searchDB(sql)
    if len(results)>0:
        sql = "UPDATE T_Headline SET price={},image='{}',date='{}',statement=0 WHERE productid='{}' ".format(price,img,getCurrentDay(),productid)
    else:
        sql = "INSERT INTO T_Headline(productid,image,date,price,statement) VALUES('{}','{}','{}',{},0)".format(productid,img,getCurrentDay(),price)

    #print(sql)
    return executeSql(sql)

def delete_headline(productid):
    sql = "DELETE FROM T_Headline WHERE productid='{}' ".format(productid)
    return executeSql(sql)

def get_to_be_checked_headlines():
    '''管理员界面得到待审核的头条信息'''
    #返回：[(id,price,date)]
    sql = "SELECT productid,price,date FROM T_Headline WHERE statement=0 ORDER BY price DESC"
    results = searchDB(sql)
    headlines_info = list()
    for id,price,date in results:
        id = id[:13]
        price = float(price)
        date = date.strftime('%Y-%m-%d')
        headlines_info.append((id,price,date))
    
    return headlines_info

def current_headlines():
    #返回：[(id,price,date)]
    sql = "SELECT productid,price,date FROM T_Headline WHERE statement=1"
    results = searchDB(sql)
    headlines_info = list()
    for id,price,date in results:
        id = id[:13]
        price = float(price)
        date = date.strftime('%Y-%m-%d')
        headlines_info.append((id,price,date))
    
    return headlines_info

def agree_headline(productids):
    '''同意这些商品的头条申请'''
    for productid in productids:
        sql = "UPDATE T_Headline SET statement=1 WHERE productid='{}' ".format(productid)
        executeSql(sql)
    return "0"


def disagree_headline(productids):
    '''不同意这些商品的头条申请'''
    for productid in productids:
        sql = "UPDATE T_Headline SET statement=2 WHERE productid='{}' ".format(productid)
        executeSql(sql)
    return "0"



"""关键字推广部分"""
def get_keywords():
    '''得到所有的推广关键字[(id,keyword)]'''
    sql = '''SELECT k.keywordid,k.keyword
                FROM T_Keyword k,T_Index i
                WHERE k.keywordid = i.keywordid
                GROUP BY k.keywordid,k.keyword
                ORDER BY count(distinct i.productid) DESC'''
                
    results = searchDB(sql)
    return results

def shop_promotion(shopid):
    '''得到店铺的关键字推荐[(productid,productname,keyword,price)]'''
    sql ='''SELECT p.productid,p.productname,k.keyword,i.price FROM T_Index i,T_Keyword k,
                    (SELECT productid,productname FROM T_Product WHERE merchantid='{}') p
            WHERE i.keywordid = k.keywordid and i.productid = p.productid'''.format(shopid)
    
    results = searchDB(sql)
    shop_promotion = list()
    for id,name,word,price in results:
        shop_promotion.append((id[:13],name,word,float(price)))
    
    return shop_promotion



def add_alter_promotion(promotion_info):
    '''修改或新增商品的关键字推广信息,[(productid,keyword,price)]'''
    #将(productid,keywordid,price)插入到T_Index中，如果该商品对应的关键字已经存在了，那么执行更新操作
    #如果不存在的话，执行插入操作
    for productid,keyword,price in promotion_info:
        #首先查找有没有这个关键字，没有的话先插入到数据库中，然后再进行后续的操作
        sql = "SELECT keywordid FROM T_Keyword WHERE keyword ='{}' ".format(keyword)
        results = searchDB(sql)
        
        if len(results)<1:
            #没有的话需要先插入到数据库中
            keywordid = getKeywordid()
            sql = "INSERT INTO T_Keyword(keywordid,keyword,keywordtype) VALUES('{}','{}',0)".format(keywordid,keyword)
            state = executeSql(sql)
            if state == "0" : return "0"#如果插入关键字出错的话，返回“0”
            time.sleep(1)
        else:
            #如果由的话需要从数据库中找到对应的keywordid
            keywordid = results[0][0]
            
        #看当前的索引在索引表中是否存在
        sql = "SELECT * FROM T_Index WHERE productid='{}' and keywordid='{}' ".format(productid,keywordid)
        results = searchDB(sql)
        if len(results)> 0:
            sql = "UPDATE T_Index SET price={} WHERE productid='{}' and keywordid='{}' ".format(price,productid,keywordid)
        else:
            sql ='''INSERT INTO T_Index(productid,keywordid,price,weight) 
                    VALUES('{}','{}',{},0.4)'''.format(productid,keywordid,price)
        #print(sql)
        state = executeSql(sql)
        if state =="0":return "0"
    
    return "1"


def cancel_add_alter_keywords(promotion_info):
    '''当插入出错的时候，需要删掉已经插入进去的关键字和索引,[(productid,keyword,price)]'''
    for productid,keyword,price in promotion_info:
        #看有没有这个关键字
        sql = "SELECT keywordid FROM T_Keyword WHERE keyword ='{}' ".format(keyword)
        results = searchDB(sql)
        
        if len(results)<1:continue #没有这个关键字说明还没有插入进去
        
        #如果已经存在的话，删除索引表中对应的索引
        keywordid = results[0][0]
        sql = "DELETE T_Index WHERE productid='{}' and keywordid='{}' ".format(productid,keywordid)
        state = executeSql(sql)
        if state =="0" : return "0"
    
    return "1"
        
        
    
def get_keywordid(keyword):
    '''根据关键字的名称得到关键字的id'''
    sql = "SELECT keywordid FROM T_Keyword WHERE keyword ='{}' ".format(keyword)
    results = searchDB(sql)
    return results[0][0]


def delete_keywords(promotion_info):
    '''删除商品的关键字[(productid,keyword)]'''
    for productid,keyword in promotion_info:
        keywordid = get_keywordid(keyword)
        sql = "DELETE FROM T_Index WHERE productid='{}' and keywordid='{}' ".format(productid,keywordid)
        state = executeSql(sql)
        if state == "0" : return "0"
        
    return "1"
#******************************************************************************



#***************************推荐反馈部分***************************************
def like_product(customerid,productid):
    '''用户喜欢某件商品，返回结果为“1”表示成功'''
    sql = "SELECT * FROM T_Customertaste WHERE customerid='{}' and productid='{}' ".format(customerid,productid)
    results = searchDB(sql)
    if len(results)>0:
        sql = '''UPDATE T_Customertaste SET date='{}' WHERE customerid='{}' 
                 and productid='{}' '''.format(getCurrentDay(),customerid,productid)
    else:
        sql = '''INSERT INTO T_Customertaste(customerid,productid,taste,date)
                VALUES('{}','{}',1,'{}')'''.format(customerid,productid,getCurrentDay())
    
    return executeSql(sql)
    
    
    
def dont_like_product(customerid,productid):
    '''用户不喜欢某件商品'''
    sql = "SELECT * FROM T_Customertaste WHERE customerid='{}' and productid='{}' ".format(customerid,productid)
    results = searchDB(sql)
    if len(results)>0:
        sql = '''UPDATE T_Customertaste SET taste=0 WHERE customerid='{}' 
                 and productid='{}' '''.format(customerid,productid)
    else:
        sql = '''INSERT INTO T_Customertaste(customerid,productid,taste,date)
                VALUES('{}','{}',0,'{}')'''.format(customerid,productid,getCurrentDay())
    
    return executeSql(sql)
#******************************************************************************

def getCurrentDay():
    '''返回字符串形式的当前日期'''
    time = datetime.datetime.now()
    return time.strftime('%Y-%m-%d')

def getKeywordid():
    return 'k'+datetime.datetime.now().strftime('%Y%m%d%H%M%S')
