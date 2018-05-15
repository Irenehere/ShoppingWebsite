
import DBhandlerSearch
import jieba
import math


#***********************************索引模块***********************************
def index(commodity_id):
    '''
    当商品通过审核或修改信息时，需要为其建立索引
    '''
    #首先需要从数据库中得到商品的信息：[(商品名称，商品描述，商品分类)]
    commodity_info = DBhandlerSearch.index_info(commodity_id)
    if len(commodity_info)<1:return "0"
    else: commodity_info = commodity_info[0]#(商品名称，商品描述，商品分类)

    #对各类描述进行分词处理，提取关键字并赋予关键字权重（名称:0.3,描述：0.2，分类：0.3）和出价（普通的索引默认出价为0.01）
    #注：如果一个词多处出现，比如在名称和描述中出现，那么将他们的权重加起来作为这个关键字的权重
    
    keyword_weight = dict() #{关键字：总的权重}
    class_keywords = {"1":("服装","衣服"),"2":("书籍","书"),"8":("水果")}#表示类别对应的关键字
    
    #分词并赋予权重
    weights = [0.3,0.2,0.3]
    stopwords = get_stopwords("stopwords.dat")#得到停用词
    
    for i in range(len(commodity_info)):
        
        if i == 2 :#如果是商品的分类的话
            for keyword in class_keywords.get(commodity_info[i],()):
                keyword_weight[keyword] = keyword_weight.get(keyword,0) + weights[i]
            continue
        
        for keyword in jieba.cut_for_search(commodity_info[i]):
            if keyword in stopwords : continue
            keyword_weight[keyword] = keyword_weight.get(keyword,0) + weights[i]

    #将索引更新到数据库中
    state = DBhandlerSearch.insert_index(commodity_id,keyword_weight)
    
    return state


def get_stopwords(path):
    stopwords = list()
    for line in open(path,encoding='utf-8'):
        stopwords.append(line.strip())
    return stopwords

#*******************************************************************************



#***********************************商品查询************************************
def get_attributes(keywords):
    '''搜索得到结果之后要动态生成属性返回
[{"attrname":"name","attrval":["val1","val2"]},
 {"attrname":"name","attrval":["val1","val2"]}]'''

    #首先按综合排序得到搜索的结果
    search_results = searchCommodities(keywords)
    sorted_results = comprehensive_rank(search_results)
    
    if len(sorted_results) < 1 : return "0"
    
    #得到搜索结果中的多数类 {类：[productid,producti]）}
    class_products = dict()
    for productid in sorted_results:
        c = DBhandlerSearch.get_commodity_class(productid)
        if c not in class_products:
            class_products.setdefault(c,[])
        class_products[c].append(productid)
    
    #排序
    majority_class_prod = [items for c,items in sorted(class_products.items(),key=lambda x:len(x[1]),reverse=True)][0]
    
    #得到多数类中每个产品的属性和属性值 [(属性，属性值)]
    attrs = list()
    for productid in majority_class_prod:
        attrs.extend(DBhandlerSearch.get_commodity_attrs(productid))
    
    #将以上的属性和属性值变成 {属性：[属性值，属性值]}的形式
    attr_values = dict()
    for attr,value in attrs:
        attr_values.setdefault(attr,[])
        if value not in attr_values.get(attr,[]):
            attr_values[attr].append(value)
            
    #转换为json格式的数据
    js = '['
    for attr,values in attr_values.items():
        js += '{"attrname":"'+attr+'","attrval":['
        for val in values:
            js += '"'+val+'",'
        js = js[:-1] + ']},'
    
    js = js[:-1] + ']'
    
    return js
 
 
def searchCommodities(keywords):
    '''根据给定的关键字查询商品id
    keywords:关键字的列表
    如果没找到返回：
    有找到结果的话返回[(productid,weight,price)]形式的列表
    '''
    
    #首先对关键字进行分词处理，得到很多的关键字
    keyword_bag = list()
    stopwords = get_stopwords("stopwords.dat")#得到停用词
    for keyword in keywords:
        for word in jieba.cut_for_search(keyword):
            if word in stopwords : continue
            keyword_bag.append(word)
    
    #得到搜索结果
    search_results = list()#搜索结果 [(productid,weight,price)]
    for keyword in keyword_bag:
        #基于单个关键字的查找，返回的结果 [(productid,weight,price)]
        #print(keyword)
        search_results.extend(DBhandlerSearch.search_based_on_keyword(keyword))

    #如果搜索得到的结果为空的话，返回一个空的列表
    if len(search_results)<1:
        return []

    #返回搜索得到的商品id
    return search_results



def getCommodityInfo_detail(commodity_id):
    """
得到商品的详细信息：返回的格式：
{"productname":"name","pic":"url",
 "delivery":"1","discount":"0.98",
 "price":"9.9","sales":"999",
 "stores":[{"storeid":"s20180506105411",
            "storage":"99",
            "attrs":[{"attrname":"颜色","attrvalue":"白色"},
                     {"attrname":"尺寸","attrvalue":"小号"}]},
           {"storeid":"s20180506105411",
            "storage":"99",
            "attrs":[{"attrname":"颜色","attrvalue":"白色"},
                     {"attrname":"尺寸","attrvalue":"大号"}]}]}
或:
    {"productname":"name","pic":"url",
     "delivery":"1","discount":"0.98",
     "price":"9.9","sales":"999",
     "stores":[{"storeid":"s20180506105411","storage":"99"} ]}
"""
    #首先根据commodity_id得到商品的基本信息：(name,pic,delivery,discount,price)
    basic_info = DBhandlerSearch.get_commodity_detail(commodity_id)
    
    #得到商品的销量
    sales = DBhandlerSearch.get_commodity_sales(commodity_id)
    
    #根据商品的productid得到商品的库存股信息：[(storeid,storage,attrs),(storeid,storage,attrs)]
    store_info = DBhandlerSearch.get_commodity_storeinfo(commodity_id)
    
    #将上面的信息组装成规定的格式
    js = '{"productid":"'+commodity_id+'","productname":"'+basic_info[0]+'","pic":"'+basic_info[1]+'",'
    js += '"delivery":"'+basic_info[2]+'","discount":"'+str(basic_info[3])+'",'
    js += '"price":"'+str(basic_info[4])+'","sales":"'+str(sales)+'","stores":['
    for item in store_info:
        if len(item) == 3:
            storeid = item[0];storage=item[1];attrs =item[2]
            js += '{"storeid":"'+storeid+'","storage":"'+str(storage)+'","attrs":'+attrs+'},'
        else:
            storeid = item[0];storage=item[1]
            js += '{"storeid":"'+storeid+'","storage":"'+str(storage)+'"},'
    
    js = js[:-1] + ']}'
    
    return js
            
            

    
def get_commodity_pics(commodity_id):
    '''根据商品的id得到商品详情的图片，返回的格式：
    ["url1","url2","url3"]'''
    urls = DBhandlerSearch.get_product_pics(commodity_id)
    if len(urls)>0:
        return str(urls).replace('\'','\"')
    else:
        return "0"


def get_commodity_comments(commodity_id):
    '''[{"customername":"name","pic":"url","level":"4","comment":"comment"},
        {"customername":"name","pic":"url","level":"4","comment":"comment"}]'''
    comments_info = DBhandlerSearch.get_product_comments(commodity_id)
    if len(comments_info)<1 : return "0"
    
    #转换为js的格式：
    js = '['
    for name,pic,level,comment in comments_info:
        js += '{"customername":"'+name+'","pic":"'+pic+'","level":"'+str(level)+'","comment":"'+comment+'"},'
    js = js[:-1] + ']'
    
    return js
        
#****************************************************************************



#***********************************排序模块***********************************
def comprehensive_rank(productids):
    
    '''对搜索结果根据关键字权重和关键字出价进行综合排序:权重*出价为综合得分
    productids的形式为：[ (商品id，关键字权重，关键字出价 )，(商品id，关键字权重，关键字出价 )]
    '''
    #进行综合排序
    #rank_items = [(1,0.3,0.01),(2,0.2,0.01),(3,0.5,0.1),(1,0.5,0.01)]
    
    rank = dict()
    for commodity_id,weight,price in productids:
        rank[commodity_id] = rank.get(commodity_id,0) + weight*price

    #对搜索得到的结果进行排序
    rank_results = sorted(rank.items(),key=lambda x:x[1],reverse = True)[:]
    commodity_ids = [id for id,rank in rank_results]

    return commodity_ids 



def sales_rank(products,asc):
    '''按照销量进行排序,返回的是排序完成之后的productids
    products的格式：[ (商品id，关键字权重，关键字出价 )，(商品id，关键字权重，关键字出价 )]
    '''
    product_sales = dict()#{productid:sales}
    
    for productid,weight,price in products:
        if productid in product_sales : continue
        product_sales[productid] = DBhandlerSearch.get_commodity_sales(productid)
    
    if asc==1:reverse = False
    else : reverse = True
    
    productids = [productid for productid,sales in sorted(product_sales.items(),key=lambda x:x[1],reverse=reverse)]
    
    return productids
    

def price_rank(products,asc):
    '''按照销量进行排序,返回的是排序完成之后的productids
    products的格式：[ (商品id，关键字权重，关键字出价 )，(商品id，关键字权重，关键字出价 )]
    '''
    product_price = dict()
    
    for productid,weight,price in products:
        if productid in product_price : continue
        product_price[productid] = DBhandlerSearch.get_commodity_price(productid)
        
    if asc==1:reverse = False
    else : reverse = True 
    
    productids = [productid for productid,price in sorted(product_price.items(),key=lambda x:x[1],reverse = reverse)]
    
    return productids
    
        
#*******************************************************************************



#***********************************筛选模块***********************************
def choose_price(productids,price):
    '''根据价格筛选产品，返回的是筛选后的productids
    price的格式："18-99"
    '''
    #对价格进行分解
    pieces = price.strip().split("-")
    min_price = float(pieces[0])
    max_price = float(pieces[1])
    
    result_productids = list()
    for productid in productids:
        price = DBhandlerSearch.get_commodity_price(productid)
        if price>=min_price and price<=max_price:
            result_productids.append(productid)
    
    return result_productids


def choose_district(productids,district):
    '''根据地区筛选产品，返回的是筛选后的productids'''
    result_productids = list()
    for productid in productids:
        product_district = DBhandlerSearch.get_commodity_district(productid)
        
        if product_district== district:
            result_productids.append(productid)
    
    return result_productids
    
#*******************************************************************************



#***********************************店铺查询************************************
def shop_brief_info(productid):
    '''根据店铺的名称得到店铺的简要信息，返回的数据格式：
    {"shopid":"id","shopname":"name","level":"4"} '''
    #根据店铺的名称得到店铺的基本信息：(id,name,level(店铺商品的综合评分))
    shop_info = DBhandlerSearch.get_shop_brief(productid)
    if len(shop_info) < 1 : return "0"
    
    #弄成js的格式
    js = '{"shopid":"'+shop_info[0]+'","shopname":"'+shop_info[1]+'","level":"'+str(shop_info[2])+'"}'
    
    return js
    



    
def searchShopes(keywords):
    '''根据给定的关键字查询店铺的id'''
    results = list()
    for keyword in keywords:
        results.extend(DBhandlerSearch.search_shop_based_on_keyword(keyword))

    return results


def getShopInfo_detail(shop_id):
    '''得到一个店铺详细的信息'''
    '''{"id":id,"pic":picture,"name":name,"type":type,"des":description,
        "adress":adress,
        "commoditiies": [
            {"id":commodity_id,"name":name,"pic":picture,"price":price,"sales":sales},
            {"id":commodity_id,"name":name,"pic":picture,"price":price,"sales":sales},
          ]
        }'''

    #店铺信息：[id,店铺名称，店铺照片，店铺类型,店铺描述，地址]
    shopInfo = DBhandlerSearch.shopInfo_detail(shop_id)
    shopInfo = ['A01','涛哥的小店','image/shop.png','综合','提供最好、最实惠的商品','广东']
    #得到这个店铺的所有商品id:[商品id]
    shop_commodities_id = DBhandlerSearch.get_shop_commodities(shop_id)

    shop_commodities_info = getCommoditiesAttr(shop_commodities_id)
    shop_commodities_info = [(1,'苹果','/web/image/apple.png',5.2,100),
                (2,"梨","/web/image/peach.png",3.8,50),
                (3,"香蕉","/web/image/banana.png",4.0,80)]

    #将其组装成为店铺信息
    js ='{"id":"'+shopInfo[0]+'","name":"'+shopInfo[1]+'","pic":"'+shopInfo[2]+'","type":"'+shopInfo[3]
    js += '","des":"'+shopInfo[4]+'","address":"'+shopInfo[5]+'","commodities":['

    for i in range(len(shop_commodities_info)-1):
        item = shop_commodities_info[i]
        js += '{"id":"'+str(item[0])+'","name":"'+item[1]+'","pic":"'+item[2]+'","price":"'
        js += str(item[3])+'","sales":"'+str(item[4])+'"},'

    item = shop_commodities_info[len(shop_commodities_info)-1]
    js += '{"id":"'+str(item[0])+'","name":"'+item[1]+'","pic":"'+item[2]+'","price":"'
    js += str(item[3])+'","sales":"'+str(item[4])+'"}]}'

    return js
#*******************************************************************************



#***********************************相似商品查询查询******************************
def searchSimilarItems(commodity_id):
    '''搜指定商品相似的商品'''
    #从数据库中得到某个商品的相似商品：[(相似的商品id，相似度)，（相似的商品id，相似度）]
    sim_items = DBhandlerSearch.searchSimilarItems(commodity_id)

    #对商品进行排序
    sorted_items =[item for item,sim in sorted(sim_items,key=lambda x:x[1],reverse = True)]

    #得到相似商品的基本属性信息
    items_info = getCommoditiesAttr(sorted_items)

    return items_info

#*******************************************************************************



#***********************************查询接口模块***********************************
def search_keywords_products(keywords,page,nums_page=20,rank=0,asc=0,price=None,district=None):
    
    '''根据关键字进行商品的查询，
    keywords表示关键字的列表["白色","短袖"]，
    page表示当前的第几页，all表示所有的结果
    
    rank:表示排序的算法：0表示综合排序，1表示按销量排序，2表示按价格排序
    
    asc:0表示降序排列，1表示升序排列
    
    price:表示按价格进行筛选，格式为"18-99.9"
    
    district：按地区进行筛选，格式为"广东"
    '''
    
    #首先调用searchCommodities(keywords)得到关键字对应的所有商品id和权重和价格
    products = searchCommodities(keywords)
    
    #如果所有的匹配的商品没有的话，返回“0”
    if len(products)<1 : return "0"
    
    #排序：根据不同的排序类型选择不同的算法进行排序
    if rank == 1:
        ranked_productids = sales_rank(products,asc)
    elif rank == 2:
        ranked_productids = price_rank(products,asc)
    else:
        ranked_productids = comprehensive_rank(products)


    #筛选
    if price is not None:
        choosed_ranked_productids = choose_price(ranked_productids,price)
        if len(choosed_ranked_productids)<1:return "0"
        
    if district is not None:
        choosed_ranked_productids = choose_district(ranked_productids,district)
        if len(choosed_ranked_productids)<1:return "0"
    
    
    #组装最后返回的信息：
    """{"allpages":"10","currentpage":"1",
    "products":[{"id":commodity_id,"name":name,"pic":picture,"shop":shop,
                 "price":price,"sales":sales,"district":district},
                {"id":commodity_id,"name":name,"pic":picture,"shop":shop,
                 "price":price,"sales":sales,"district":district}] }"""
    
    #需要根据返回结果的个数和当前的页数来组装部分的结果
    if price is not None or district is not None:
        result_ids = choosed_ranked_productids
    else:
        result_ids = ranked_productids
    
    #对页数的处理
    allpages = math.ceil(len(result_ids)/nums_page)
    if page>allpages : page = 1 #如果请求的超过最大的页数的话，返回首页
    page_choosed_ranked_productids = result_ids[(page-1)*nums_page:page*nums_page]
    
    js = '{"allpages":"' + str(allpages)+'","currentpage":"'+str(page)+'","products":'
    
    #然后调用getCommoditiesAttr(searchRes)得到上面"Products"后的内容
    js = js + getCommoditiesAttr(page_choosed_ranked_productids) + '}'
    
    return js

#*******************************************************************************




#**************************返回商品的属性或店铺的信息*****************************

def getCommoditiesAttr(commodity_ids):
    '''根据给定的商品id列表返回商品的大致属性信息,返回的信息的格式：
[{"id":commodity_id,"name":name,"pic":picture,"shop":shop,"price":price,"sales":sales,"district":district},
 {"id":commodity_id,"name":name,"pic":picture,"shop":shop,"price":price,"sales":sales,"district":district}
]'''

    #首先要从数据库中查找到商品呢的属性信息：[ (商品id，名称，图片，店铺，价格,销量,地区) ]
    commodity_info = DBhandlerSearch.get_commodity_info(commodity_ids)

    #然后将这些转换为json的形式并返回
    '''{"id":commodity_id,"name":name,"pic":picture,"shop":shop,"price":price,"sales":sales,"district":district}'''

    '''commodity_info = [(1,'苹果','/web/image/apple.png','水果大王',5.2,100,'广东'),
            (2,"梨","/web/image/peach.png","涛哥的小店",3.8,50,'福建'),
            (3,"香蕉","/web/image/banana.png","涛哥的小店",4.0,80,'广东')]'''

    js = '['
    for i in range(len(commodity_info)-1):
        item = commodity_info[i]
        js += '{"id":"'+str(item[0])+'","name":"'+item[1]+'","pic":"'+item[2]+'","shop":"'+item[3]+'","price":"'
        js += str(item[4])+'","sales":"'+str(item[5])+'","district":"'+item[6]+'"},'

    item = commodity_info[len(commodity_info)-1]
    js += '{"id":"'+str(item[0])+'","name":"'+item[1]+'","pic":"'+item[2]+'","shop":"'+item[3]+'","price":"'
    js += str(item[4])+'","sales":"'+str(item[5])+'","district":"'+item[6]+'"}]'

    return js


def getShopInfo_basic(shop_ids):
    '''得到每个店铺的大致信息信息'''
    #从数据库中得到指定店铺的信息 [ (店铺id，店铺名称，店铺照片，店铺类型）]
    shops_info = DBhandlerSearch.shopInfo_basic(shop_ids)

    shops_info = [(1,'涛哥的小店','png','综合'),(2,'水果王','fruit.png','水果'),(3,'木人书店','book.png','书店')]

    #将上面的信息转换为json的格式范湖
    js = '['
    for i in range(len(shops_info)-1):
        item = shops_info[i]
        js += '{"id":"'+str(item[0])+'","name":"'+item[1]+'","pic":"'+item[2]+'","type":"'+item[3]+'"},'

    item = shops_info[len(shops_info)-1]
    js += '{"id":"'+str(item[0])+'","name":"'+item[1]+'","pic":"'+item[2]+'","type":"'+item[3]+'"}]'

    return js

#*******************************************************************************
