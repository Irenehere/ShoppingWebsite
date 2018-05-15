#推荐系统的文件：包括训练模型和为用户提供推荐
import math
import datetime
import DBhandler

#********************************基于内容的推荐**********************************
def recommend_on_features(customer_id,T0,N=20,beta=1):
    '''根据他的性别、年龄来推荐和他相同的人喜爱的商品'''
    #从数据库中找到和该用户特征相似的用户,得到相似用户的：购买商品、购买时间  { 用户：{购买物品：购买日期}}
    prefs = DBhandler.orders_based_on_customer_features(customer_id)

    #计算相似用户的商品的：流行度（基于时间的流行度）
    return popularItem(prefs,T0=T0,N=N,beta=beta)


def popularItem(prefs,T0,N=20,beta=1):
    '''计算基于时间的物品的流行度
    prefs的格式：{用户：{物品：购买日期}}
    返回的是：[(商品，商品的流行度)]
    '''
    #计算相似用户的商品的：流行度（基于时间的流行度）
    rec = dict()#推荐的物品
    for user,items in prefs.items():
        for item,time in items.items():
            #rec[item] = rec.get(item,0) + 1/(1+beta*(T0-time))
            rec[item] = rec.get(item,0) + 1/(1+beta*getIntervalDays(time,T0))

    #返回流行度最高的前N个商品的ID
    rank = sorted(rec.items(),key=lambda x:x[1],reverse=True)[:N]

    return rank

#*******************************************************************************


#***********************************基于ItemCF的推荐*****************************
def trainTimeBasedItemCF(alpha=1,sim_counts=0.8):
    '''训练基于时间的ItemCF模型：主要是得到物品的相似度表，然后更新到数据库中'''

    #计算物品的相似度
    ##得到用户和物品的数据：{用户：{物品：日期}}
    prefs = DBhandler.all_customer_orders()
    ##计算相似度
    similarity = TimeBasedItemSimilarity(prefs,alpha=alpha,sim_counts=sim_counts)

    #将物品的相似度更新到数据库中
    DBhandler.update_item_similarity(similarity)

def TimeBasedItemSimilarity(prefs,alpha=1,sim_counts=0.8):
    '''
    考虑时间因素的物品相似度的计算，

    1 prefs表示训练的数据：{用户：{物品：时间}}

    2 alpha:时间衰减参数，如果用户的兴趣变化很快快的话，需要较大的alpha值

    3 sim_counts表示每个物品取相似度最高的前sim_counts个数据，-1的话表示计算一个物品
    和所有其他物品的相似度， 小数的话表示返回的物品的比例

    3 返回结果的形式：{物品：{相似的物品：相似度}}

    注：如果要得到推荐该部电影的理由的话，将reasons和results出的注释解开就可以了（之所以不这样
    是因为之前没考虑到，如果修改的话要改很多其他的部分，略麻烦
    '''
    C=dict()#物品之间的相似度
    N=dict()#表示物品对应的数量

    for u,items in prefs.items():
        for item,t1 in items.items():
            N[item] = N.get(item,0) + 1
            C.setdefault(item,{})
            for item2,t2 in items.items():
                if item2 == item : continue
                #C[item][item2] = C[item].get(item2,0) + 1/(1+alpha*abs(t2-t1))
                C[item][item2] = C[item].get(item2,0) + 1/(1+alpha*getIntervalDays(t2,t1))

    Sim = dict()#相似度矩阵
    for item,related_items in C.items():
        for item2,c in related_items.items():
            Sim.setdefault(item,{})
            Sim[item][item2] = c/math.sqrt(N[item]*N[item2])

    #对于每一个物品而言，返回相似度最高的前sim_counts个物品
    results = {}
    for item in N.keys():
        sorted_sims = topMatches(Sim,item,n=sim_counts)
        results[item] = {other:sim for other,sim in sorted_sims}

    return results

def topMatches(similarity,person,n):
    '''
    根据给定的相似度字典得到某个用户/物品相似度最高的前n个用户/物品及其相似度
    n:可以是-1，小数或整数,-1的话表示计算一个用户和所有其他用户的相似度,小数的话表示返回的用户的比例
    '''
    if person not in similarity:
        print('User Not Found!')
        return

    sorted_sims = sorted(similarity[person].items(),key=lambda x:x[1],reverse=True)

    if n == -1 :#返回和该用户相似的所有用户的相似度
        return sorted_sims[:]
    elif n>0 and n<1:#如果为小数的话,返回一定的比例
        return sorted_sims[:math.ceil(n*len(similarity[person]))]
    else:
        return sorted_sims[:n]


def recommend_on_itemsimilarity(customer_id,T0,N=20,beta=1):
    '''基于物品相似度的推荐'''

    #首先从数据库中得到物品的相似度列表  {物品：{相似物品：相似度}}
    similarity = DBhandler.get_item_similarity()

    #从数据库中得到该顾客的购买记录{购买的物品：时间，购买的物品：时间}
    related_commodity = DBhandler.orders_based_on_customerId(customer_id)
    #related_commodity = {'Snakes on a Plane': 4.5,'Superman Returns': 4.0,'You, Me and Dupree': 1.0}

    #找到和购买的物品相似度较高的前N个产品
    rec_commodities = {}

    rec_reasons={} #表示推荐的解释{推荐的物品：{曾经购买过的物品：相似度}}

    for item,time in related_commodity.items():
        for sim_item,sim in similarity[item].items():
            if sim_item in related_commodity:continue #如果相似的物品是用户曾经购买过的话，直接跳过
            #tmp = sim/(1+beta*abs(T0-time))
            tmp = sim/(1+beta*getIntervalDays(time,T0))
            rec_commodities[sim_item] = rec_commodities.get(sim_item,0) + tmp
            #提供推荐的解释
            rec_reasons.setdefault(sim_item,{})
            rec_reasons[sim_item][item] = tmp

    rec=sorted(rec_commodities.items(),key=lambda x:x[1],reverse=True)[:N]
    rec_reason = [(item,sorted(reasons.items(),key=lambda x:x[1],reverse=True)[0][0]) for item,reasons in rec_reasons.items()]

    return rec,rec_reason

#******************************************************************************

#*****************************推荐部分******************************************
def getRecommendation(customer_id,N=10,beta = 1):
    '''从订单表中得到该顾客的购买记录，如果购买的记录为0的话，根据他的性别、年龄来推荐和他相同的人喜爱的商品'''

    customer_orders = DBhandler.orders_based_on_customerId(customer_id)#{item:date}
    #如果订单的数量大于0的话，根据基于时间的ItemCF和基于内容的推荐得到初始的推荐列表

    rec_reason = None 
    
    if len(customer_orders)<1:
        personal_recommendation = recommend_on_features(customer_id,T0=getCurrentDay(),N=2*N,beta=beta)
    else:
        personal_recommendation,rec_reason = recommend_on_itemsimilarity(customer_id,T0 = getCurrentDay(),N=2*N,beta=beta)
 
    '''
    personal_recommendation =  [('Superman Returns', 1.0107142857142857),
                        ('Snakes on a Plane', 0.9645604395604396),
                        ('The Night Listener', 0.7967032967032968),
                        ('You, Me and Dupree', 0.7130718954248366),
                        ('Lady in the Water', 0.6102941176470589),
                        ('Just My Luck', 0.46637426900584794)]'''

    #对初始的推荐列表进行过滤：过滤掉不属于商品推广列表中的的商品和用户不喜欢的商品
    #排序：根据相似度和推荐的出价来对推荐的结果加权，并据此进行排序，得到最终推荐的商品的ID
    rec_commodities = DBhandler.get_recommend_commodities()
    dislike_commodities = DBhandler.get_dislike_commodities(customer_id)#用户不喜欢的商品
    
    '''
    rec_commodities = [('Superman Returns', 2),
                        ('The Night Listener', 1),
                        ('You, Me and Dupree', 1.5),
                        ('Just My Luck',0.5)]'''
    rec_commodities = {item:price for item,price in rec_commodities}#将推荐的商品转换为字符串的形式

    recommendation = dict()
    for item,sim in personal_recommendation:
        if item not in rec_commodities : continue
        if item in dislike_commodities : continue
        recommendation[item] = sim*rec_commodities[item]

    rec_commodities_id = [item for item,rank in sorted(recommendation.items(),key=lambda x:x[1],reverse=True)]

    #得到商品的推荐理由
    recommend_reason = {}
    if rec_reason is not None:
        for rec,reason in rec_reason:
            recommend_reason[rec] = DBhandler.get_productname(reason)
            
    #还需要一个方法将商品的ID转换为商品属性信息，并以json的格式返回
    return getCommodityAttributes(rec_commodities_id,recommend_reason)


def getPopularItem(N=10,beta=1):
    '''返回在所有顾客中最热门的商品'''
    prefs = DBhandler.all_customer_orders()
    #计算相似用户的商品的：流行度（基于时间的流行度）
    popular_item = popularItem(prefs,T0 = getCurrentDay(),N=N,beta = beta)
    items = [item for item,popularity in popular_item]
    
    return getCommodityAttributes(items,{})


def getCommodityAttributes(commodity_ids,recommend_reason):
    '''根据给定的商品列表得到商品的属性信息，并以json的格式返回
        commodity_ids : 列表，表示推荐的商品的ID
    '''
    #得到商品的属性：[ (商品id，名称，图片，店铺，价格) ]
    attributes = DBhandler.get_recommend_commodities_attributes(commodity_ids)
    '''
    attributes = [(1,"苹果","/web/image/apple.png","涛哥的小店",1.5),
                (2,"梨","/web/image/peach.png","涛哥的小店",0.5),
                (3,"香蕉","/web/image/banana.png","涛哥的小店",1)]'''

    #将商品信息转换为json格式
    '''
    [{"id":commodity_id, "name":name, "pic":picture_url, "price":price,"reason":"reason"},
     {"id":commodity_id, "name":name, "pic":picture_url, "price":price,"reason":"reason"}
    ]
    '''
    has_reason = 0
    if len(recommend_reason)>0 : has_reason = 1
    
    js = "["
    for i in range(len(attributes)):
        item = attributes[i]
        js += '{"id":"'+str(item[0])+'","name":"'+item[1]+'","pic":"'+item[2]+'","shop":"'+item[3]+'","price":"'+str(item[4])+'"'
        if (has_reason):
            js += ',"reason":"'+recommend_reason[item[0]]+'"'
        js += '},'
    
    js = js[:-1] + ']'
        
    return js
#******************************************************************************


#时间处理的函数
def getCurrentDay():
    '''返回字符串形式的当前日期'''
    time = datetime.datetime.now()
    return time.strftime('%Y-%m-%d')

def getIntervalDays(time1,time2):
    t1 = datetime.datetime.strptime(time1,'%Y-%m-%d')
    t2 = datetime.datetime.strptime(time2,'%Y-%m-%d')
    return abs((t2-t1).days)
