
'''订单管理系统'''
import json
import DBhandlerOrder
import datetime
import time

#***********************************插入订单************************************
def get_customer_info(customerid):
    '''根据用户的id得到用户的基本信息，返回的格式：
    {"customername":"name",
    "address":"address",
    "phone":"phone"}
    '''
    #（用户名，手机号，省份，地址）
    customer = DBhandlerOrder.getCustomerInfo(customerid)
    js = '{"customername":"'+customer[0]+'","address":"'+customer[2].rstrip()+'省'+customer[3]+'","phone":"'+customer[1]+'"}'
    return js
    

def insert_order_buy(js):
    '''立即购买时需要插入订单，js的格式如下：
     {"customerid":"c201804281551",
     "storeid":"id",
     "num":"num",
     "total":"total}
     
    插入成功返回“1”，否则返回“0”
    '''
    order_info = json.loads(js)
    customerid = order_info["customerid"]
    storeid = order_info["storeid"]
    quantity = int(order_info["num"])
    total = float(order_info["total"])
    
    orderid = DBhandlerOrder.insertOrder(customerid,getCurrentDay())
    
    if orderid == "0" : return "0"
    
    state = DBhandlerOrder.insertOrderItem(orderid,storeid,quantity,total)
    
    #如果插入出错的话，也需要删除原本的订单
    if state == "0":
        DBhandlerOrder.cancelOrder(orderid)
    
    return state


def insert_order_cart(js):
    '''从购物车插入订单，js的格式如下：
     {"customerid":"c201804281545",
     "storeid":["s20180428155603","s20180428161803","s20180428162002"]}
     
    插入成功返回“1”，否则返回“0”
    '''
    #解析js得到购物车的数据：
    orders_info = json.loads(js)
    customerid = orders_info["customerid"]
    storeids = orders_info["storeid"]
    #得到在购车车表中存储的信息：{(库存id:(数量，订单金额)，库存id:(数量，订单金额)}
    cart_info = DBhandlerOrder.cartInfo(customerid,storeids)
    
    #根据库存id得到不同的店铺
    shop_store = dict()
    for storeid in cart_info.keys():
        shopid = DBhandlerOrder.get_shopid_based_on_storeid(storeid)
        shop_store.setdefault(shopid,[])
        shop_store[shopid].append(storeid)
    
    
    '''为不同的店铺生成不同的订单'''
    state = "1" #表示插入订单的状态
    inserted_orders = list()#表示已经插进去的订单，如果出错的话，需要将其全部去掉
    for shopid,storeids in shop_store.items():
        #首先插入订单信息
        
        orderid = DBhandlerOrder.insertOrder(customerid,getCurrentDay())
        time.sleep(1)
        #插入出错的情况
        if orderid == "0" : 
            #如果是第一个的话直接返回“0”
            if len(inserted_orders)<1: 
                return "0"
            else: #如果之前已经插入过一些数据了，将这些都删掉并返回错误信号
                DBhandlerOrder.cancelOrder(inserted_orders)
                return "0"
        
        #没出错的话表示新插入了一个订单
        inserted_orders.append(orderid)
        
        #依次往订单项总插入订单项
        for storeid in storeids:
            state = DBhandlerOrder.insertOrderItem(orderid,storeid,cart_info[storeid][0],cart_info[storeid][1])
            #如果插入出错的话，取消本次订单
            if state == "0": break
        
        #插入过程总一旦出错，将所有插入的订单删除，并结束循环
        if state == "0" : 
            DBhandlerOrder.cancelOrder(inserted_orders)
            return "0"
        
    return "1"
#*******************************************************************************



#***********************************订单处理************************************
"""
def cancelOrders(orderids):
    '''取消状态为“未付款”的订单
    orders[orderid1,orderid2]'''"""
    

def shipment_confirm(orders_id):
    '''确认发货'''

def received_confirm(orders_id):
    '''确认收货'''

def apply_for_return_of_goods(orders_id):
    '''申请退货'''

def agree_return_of_goods(orders_id):
    '''确认退货'''
#*******************************************************************************




#***********************************订单查询***********************************
'''订单查询返回的统一格式：
    {"orderid":"o20180503231820",
     "date":"date",
     "customername":"name",
     "total":"total",#订单的总金额
     "products":[{"productname":"白色的短袖",
                  "pic":"url",
                  "shop:"shop",
                  "attrs":[{"attrid":"a101","attrvalue":"白色"},
                          {"attrid":"a102","attrvalue":"小号"}]
                  "number":"num",
                  "price":"price"},
                {"productname":"黑色的帽子",
                 "shop":"shop",
                 "attrs":[{"attrid":"a101","attrvalue":"白色"}],
                 "number":"num",
                 "price":"price"} ]}'''
                 
def searchOrders(userid,orderid):
    '''根据订单的编号得到订单的信息'''
    if 'c' in userid:
        return get_orders_based_on_state('all',customerid=userid,orderid=orderid)
    else:
        return get_orders_based_on_state('all',shopid=userid,orderid=orderid)


def all_orders(userid):
    '''得到所有的订单'''
    if 'c' in userid:
        return get_orders_based_on_state('all',customerid=userid)
    else:
        return get_orders_based_on_state('all',shopid=userid)

def unshipped_orders(userid):
    '''得到未发货的订单的信息,订单状态为1'''
    if 'c' in userid:
        return get_orders_based_on_state('1',customerid=userid)
    else:
        return get_orders_based_on_state('1',shopid=userid)
    
def delivery_orders(userid):
    '''得到待收货的订单的信息'''
    if 'c' in userid:
        return get_orders_based_on_state('2',customerid=userid)
    else:
        return get_orders_based_on_state('2',shopid=userid)

def received_orders(userid):
    '''得到已收货的订单信息'''
    if 'c' in userid:
        return get_orders_based_on_state('3',customerid=userid)
    else:
        return get_orders_based_on_state('3',shopid=userid)

def return_orders(userid):
    '''得到待退货的订单信息'''
    if 'c' in userid:
        return get_orders_based_on_state('4',customerid=userid)
    else:
        return get_orders_based_on_state('4',shopid=userid)
    

def get_orders_based_on_state(state,customerid=None,shopid = None,orderid=None):
    '''根据订单的状态得到订单的信息：并以json的格式返回订单信息
    state: 'all','0','1','2',''3','4','5'
    '''
    #首先根据状态得到订单表中的信息：[(订单id,顾客id,库存id,订单状态，数量，金额，日期)]
    orders = DBhandlerOrder.getOrders_based_on_state(state,customerid=customerid,shopid=shopid,orderid=orderid)
    
    #如果没有订单的话，返回606，表示没有对应的订单信息
    if len(orders)<1:return "0"
    
    #根据顾客id得到顾客名称{顾客id：顾客名称}
    customers_name = {}
    storeids = []#得到所有的库存id
    for item in orders:
        customerid = item[1];storeid = item[2];
        if customerid not in customers_name:
            customers_name[customerid]= DBhandlerOrder.getCustomerInfo(customerid)[0]
        if storeid not in storeids : storeids.append(storeid)
    
    '''根据库存id得到商品的名称、属性等信息
    {库存id:(名称，json格式的属性)，库存id:(名称，json格式的属性)}
    [{"attrname":"颜色","attrvalue":"白色"},{"attridname":"尺寸","attrvalue":"小号"}]'''
    product_name_attr = DBhandlerOrder.productsInfo(storeids)
    
    #得到每个商品对应的价格：{库存id，(图片，店铺，价格）}
    product_pic_shop_price = DBhandlerOrder.getProductInfo(storeids)
    
    #将上面的信息封装成json的格式返回
    return ordersInfo(orders,customers_name,product_name_attr,product_pic_shop_price)


def ordersInfo(orders,customers_name,product_name_attr,product_pic_shop_price):
    '''以json的格式返回订单信息
    {"orderid":"o20180503231820",
     "date":"date",
     "customername":"name",
     "total":"total",#订单的总金额
     "products":[{"productname":"白色的短袖",
                  "pic":"url",
                  "shop:"shop",
                  "attrs":[{"attrid":"a101","attrvalue":"白色"},
                          {"attrid":"a102","attrvalue":"小号"}]
                  "number":"num",
                  "price":"price"},
                {"productname":"黑色的帽子",
                 "shop":"shop",
                 "attrs":[{"attrid":"a101","attrvalue":"白色"}],
                 "number":"num",
                 "price":"price"} ]}
    '''
    
    #首先要将同一个订单中的订单项合并在一起，合并的格式如下：
    '''{订单号：[顾客id,订单状态,日期,[(库存id,数量，金额)]]'''
    orders_groupby_orderid = {}
    for orderid,customerid,storeid,ordercondition,quantity,total,date in orders:
        if orderid not in orders_groupby_orderid:
            orders_groupby_orderid[orderid] = [customerid,ordercondition,date,[(storeid,quantity,total)]]
        else:
            orders_groupby_orderid[orderid][3].append((storeid,quantity,total))
        
    #得到json格式的数据
    ordersInfo = '['
    for orderid,items in orders_groupby_orderid.items():
        order_total = 0 #存储整个订单的总金额
        customerid = items[0];ordercondition = items[1];date=items[2]
        ordersInfo+='{"orderid":"'+orderid+'","customername":"'+customers_name[customerid]+'","products":['
        for storeid,quantity,total in items[3]:
            if type(product_name_attr[storeid]) == tuple:
                ordersInfo += '{"productname":"'+product_name_attr[storeid][0]+'","attrs":'+product_name_attr[storeid][1]+','
            else:
                ordersInfo += '{"productname":"'+product_name_attr[storeid]+'",'
            ordersInfo +='"pic":"'+product_pic_shop_price[storeid][0]+'","shop":"'+product_pic_shop_price[storeid][1] +'",'
            ordersInfo += '"price":"'+str(product_pic_shop_price[storeid][2])+'","quantity":"'+str(quantity)+'"},'
            order_total += total
        
        ordersInfo = ordersInfo[:-1]+'],"ordercondition":"'+ordercondition+'","tol":"'+str(order_total)+'","date":"'+date+'"},'
    
    ordersInfo = ordersInfo[:-1]+']'
    
    return ordersInfo
#*******************************************************************************



#***********************************订单删除***********************************
def deleteOrders(orders_id):
    '''从数据库中删除指定订单编号的订单'''
#*******************************************************************************


def getCurrentDay():
    '''返回字符串形式的当前日期'''
    time = datetime.datetime.now()
    return time.strftime('%Y-%m-%d')