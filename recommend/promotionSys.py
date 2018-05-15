
import DBhandler
import json

def get_products(shopid):
    '''根据店铺的id得到该店铺的所有商品,如果该店铺没有商品的话返回“0”，否则返回的格式：
    [{"productid":"id","productname":"name"},
     {"productid":"id","productname":"name"}]
    '''
    info = DBhandler.get_shop_items(shopid)
    if len(info)<1:
        return "0"
        
    js = '['
    for id,name in info:
        js+= '{"productid":"'+id+'","productname":"'+name+'"},'
    
    js = js[:-1] + ']'
    
    return js
 
#********************************关键字推广**********************************
def get_keywords():
    '''得到推广的关键字，返回的格式：
    [{"keywordid":"id","keyword":"keyword"},
     {"keywordid":"id","keyword":"keyword"} ]'''
    keywords = DBhandler.get_keywords()
    
    js = '['
    for id,keyword in keywords:
        js += '{"keywordid":"'+id+'","keyword":"'+keyword+'"},'
    
    js = js[:-1] + ']'
    
    return js

def get_my_promotion(shopid):
    '''得到店铺已有的关键字推广,返回的格式：当一个商品的不同关键字的出价不一样时，在不同行中显示
    [{"productid":"id","productname":"name",
      "price":"price",
      "keywords":["keyword1","keyword2"]},
     {"productid":"id","productname":"name",
      "keywords":["keyword1","keyword2"],
      "price":"price"}
    '''
    
    #首先得到该店铺一条推广的记录：[(productid,productname,keyword,price)]
    shop_promotions = DBhandler.shop_promotion(shopid)
    
    if len(shop_promotions)<1:
        return "0"
    
    #将数据转换为：{ productid:{price:[keyword1,keyword2]}}和{productid:productname}的格式
    shop_promotion_format = dict()
    for id,name,word,price in shop_promotions:
        shop_promotion_format.setdefault(id,{})
        shop_promotion_format[id].setdefault(price,[])
        shop_promotion_format[id][price].append(word)
        
    #将上述的格式转换为json的格式
    js  = '['
    for id,item1 in shop_promotion_format.items():
        for price,keywords in item1.items():
            js += '{"productid":"'+id+'","productname":"'+DBhandler.get_productname(id)+'","price":"'+str(price)+'","keywords":['
            for keyword in keywords:
                js += '"'+keyword+'",'
            js = js[:-1] + ']},'
    js = js[:-1] + ']'
    
    return js


def add_promotion_keywords(js):
    '''为商品添加关键字，js的格式：
    {"productid":"p201804281620",
      "keywords":["新款","潮流"],
      "price":"0.45"}'''
    
    #首先要将数据转换为[(productid,keyword,price)]的格式
    promotions = json.loads(js)
    promotions_info_format = list()
    productid = promotions["productid"]
    price = promotions["price"]
    for keyword in promotions["keywords"]:
        promotions_info_format.append((productid,keyword,price))
        
    #修改或插入推荐的信息： 
    state = DBhandler.add_alter_promotion(promotions_info_format)
    
    while state =="0":#当删除不成功时，连续删除
        #如果插入失败的话需要取消之前插入的索引
        state = DBhandler.cancel_add_alter_keywords(promotions_info_format)
        
    return state


def delete_keywords(js):
    '''删除关键字推广，js的格式：
    {"productid":"p201804281620","keywords":["新款"]}'''
    #将上述格式转换为[(productid,keyword)]的格式
    promotion = json.loads(js)
    promotion_info_format = list()
    productid = promotion["productid"]
    for keyword in promotion["keywords"]:
        promotion_info_format.append((productid,keyword))
    
    #返回删除的结果
    return DBhandler.delete_keywords(promotion_info_format)
#****************************************************************************


#***********************************推荐申请**********************************
def get_recommend_products(shopid):
    '''根据店铺id得到该店铺”我的推荐“中的内容,没有的话返回“0”，返回的格式：
    [{"productid":"id","productname":"name","recommendprice":"price"},
     {"productid":"id","productname":"name","recommendprice":"price"}]
    '''
    #得到店铺的推荐的商品[(id,name,price)]
    rec_items = DBhandler.get_shop_recommend_items(shopid)
    
    if len(rec_items)<1:
        return "0"
        
    #转换为js的格式
    js = '['
    for id,name,price in rec_items:
        js += '{"productid":"'+id+'","productname":"'+name+'","recommendprice":"'+str(price)+'"},'
    js = js[:-1] + ']'
    
    return js

def add_recommend(productid,price):
    '''为商品添加推荐'''
    state = DBhandler.add_recommend(productid,price)
    return "1" if state == "1" else "0"


def delete_recommendation(productid):
    '''取消某个商品的推荐'''
    state = DBhandler.delete_recommendation(productid)
    return "1" if state == "1" else "0"
#*****************************************************************************



#**************************************头条推广*******************************
def get_headline(shopid):
    '''得到该店铺申请的头条信息,返回的格式：
    [{"productid":"id","productname":"name","price":"price","state":"state"},
     {"productid":"id","productname":"name","price":"price","state":"state"}]
     '''
    #得到店铺申请的头条：[(id,price,state)]
    headlines = DBhandler.get_shop_headlines(shopid)
    if len(headlines)<1:
        return "0"
    
    #根据产品id得到名称{id:name}
    product_id_name = dict()
    for item in headlines:
       product_id_name[item[0]] = DBhandler.get_productname(item[0])
    
    #将信息组装成js的格式
    js = '['
    for id,price,state in headlines:
        js+='{"productid":"'+id+'","productname":"'+product_id_name[id]+'","price":"'+str(price)+'","state":"'+str(state)+'"},'
    js = js[:-1] + ']'
    
    return js
    

def add_headline(productid,price,img):
    '''为商品申请头条'''
    #如果该商品已经在T_Headline中存在了，那么更新价格；否则重新插入一条头条申请
    #无论是更新还是插入，都需要将状态设置为“0”
    state = DBhandler.add_headline(productid,price,img)
    return "1" if state == "1" else "0"

    
def delete_headline(productid):
    state = DBhandler.delete_headline(productid)
    return "1" if state == "1" else "0"

    
def to_be_checked_headlines():
    '''管理员界面显示所有的头条申请,返回的格式,当没有头条的时候返回“0”：
    [{"shopname":"name","productid":"productid","productname":"productname",
      "price":"99.9","date":"2018/05/06"},
    {"shopname":"name","productid":"productid","productname":"productname",
     "price":"99.9","date":"2018/05/06"}]'''

    #得到头条的基本信息：[(id,price,date)]
    headlines = DBhandler.get_to_be_checked_headlines()
    
    if len(headlines)<1:
        return "0"
    
    #将以上的信息组装成js的格式
    js = '['
    for id,price,date in headlines:
        js += '{"shopname":"'+DBhandler.get_shopname(id)+'","productid":"'+id+'","productname":"'+DBhandler.get_productname(id)+'",'
        js += '"price":"'+str(price)+'","date":"'+date+'"},'
    
    js = js[:-1] + ']'
    
    return js
    
def get_current_headlines():
    '''得到当前的头条,格式和上面的完全一样'''
    headlines = DBhandler.current_headlines()
    
    if len(headlines)<1:
        return "0"
    
    #将以上的信息组装成js的格式
    js = '['
    for id,price,date in headlines:
        js += '{"shopname":"'+DBhandler.get_shopname(id)+'","productid":"'+id+'","productname":"'+DBhandler.get_productname(id)+'",'
        js += '"price":"'+str(price)+'","date":"'+date+'"},'
    
    js = js[:-1] + ']'
    
    return js
    
""" 
在DBhandler中
def agree_headline(productids):
    return "0"
    '''同意这些商品的头条申请'''

def disagree_headline(productids):
    return "0"
    '''不同意这些商品的头条申请'''
 """  
#*****************************************************************************


#**************************************推荐反馈*******************************
"""放到DBhandler.py中了
def like_product(customerid,productid):
    '''用户喜欢某件商品'''
    
def dont_like_product(customerid,productid):
    '''用户不喜欢某件商品'''
  """ 
#*****************************************************************************

