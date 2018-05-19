
"""
注册登录系统
"""
import DBhandlerLog
import json

#*************************************注册部分*********************************
    
def customerSignIn(js):
    '''js的结构：customername,password,paymentcode,answer,phone,age,sex,province,address
    {"customername":"name","password":"pass","paymentcode":"code",
     "answer":"answer","phone":"phone","age":"21","sex":"1",
     "province":"province","address":"address"}'''
    
    customer_info = json.loads(js)
    name = customer_info["customername"];password=customer_info["password"];paymentcode = customer_info["paymentcode"]
    answer = customer_info["answer"];phone=customer_info["phone"];
    age = int(customer_info["age"]);sex = customer_info["sex"];
    province = customer_info["province"];address  = customer_info["address"]
     

    state = DBhandlerLog.add_customer(name,password,paymentcode,answer,phone,age,sex,province,address)
    if state == "0" : return "0"
    
    #返回结果“1”表示注册成功
    return "1"

def shopSignIn(name,password,merchanttype,description,answer,province,address):
    
    state = DBhandlerLog.add_shop(name,password,merchanttype,description,answer,province,address)
    if state == "0" : return "0"
    
    #返回结果“1”表示注册成功
    return "1"

#*****************************************************************************


#*************************************登录部分**********************************
def customerLogIn(customername,password):
    
    #从T_Cryptogram表和T_Customer表中得到customername对应的登录密码
    #如果没有结果的话，返回“0”,表示用户名或密码错误
    exist_customer = DBhandlerLog.ckeck_username(customername,customer=True)
    if exist_customer == "0" : return "0"
    
    #比较输入的密码和原密码，不匹配的话返回“0”,表示用户名或密码错误
    user_password = DBhandlerLog.get_password(exist_customer)
    
    #返回结果“1”表示登录成功，跳转到顾客首页
    if password == user_password:
        return "1"
    else:
        return "0"
    
    

def shopLogIn(shopname,password):
    
    '''从T_Merchant和T_Cryptogram中得到shopname对应的： password和merchantstatement
    如果没有结果的话，返回“0”,表示用户名或密码错误'''
    exist_shop = DBhandlerLog.ckeck_username(shopname,customer=False)
    if exist_shop == "0" : return "0"
    
    #如果店铺的状态为"0"待审核的话，返回“2”,表示店铺待审核
    state = DBhandlerLog.get_shop_state(exist_shop)
    
    if state == "0" : return "2"
    
    #如果店铺的状态为“2”未通过审核的话，返回“3”和remark(审核不通过的原因）
    if state == "2":
        reason = DBhandlerLog.get_failed_reason(exist_shop)
        return "3"+" {}".format(reason)
    
    #比较输入的密码和原密码，不匹配的话返回“0”
    user_password = DBhandlerLog.get_password(exist_shop)
    
    if user_password != password : return "0"
    #返回结果“1”表示登录成功
    
    return "1"

#*****************************************************************************  
    
    
#*************************************找回密码**********************************
def forget_password(userid,answer):

    '''忘记密码，需要输入用户名和密保问题来重置密码'''
    #根据userid得到该用户具体的密保问题(验证用户名是否存在的时候已经返回了用户id，不用再根据用户名查询用户
    orig_answer = DBhandlerLog.get_password_answer(userid)
    
    #将输入的密码答案和原来的答案进行对比，不一样的话返回“0”，表示密保问题错误
    if answer.strip() != orig_answer.strip(): return "0"
    #返回结果“1”表示可以重置密码
    return "1"
    

def reset_password(userid,newpassword):
    
    state = DBhandlerLog.alert_password(userid,newpassword)
    if state == "0" : return "0"
    return "1"

    
#*****************************************************************************  
    


#********************************管理员审核账户部分*****************************
def get_to_be_checked_shop():
    '''得到待审核的店铺的信息
[{"merchantid":"id",
  "merchantname":"name",
  "merchanttype":"type",
  "description":"description"},
  {"merchantid":"id",
  "merchantname":"name",
  "merchanttype":"type",
  "description":"description"}
'''
    #从数据中获取店铺的信息：[(id,name,type,description)]
    shops_info = DBhandlerLog.to_be_checked_shop_info()
    
    if len(shops_info)<1:
        return "0"
    
    #将数据转换为json的格式
    t = {'1':"服装",'2':'书籍','3':'母婴用品','4':'美妆','7':'百货'}
    js = '['
    for shopid,name,shoptype,description in shops_info:
        js += '{"merchantid":"'+shopid+'","merchantname":"'+name+'","merchanttype":"'+t.get(shoptype,"其他")
        js += '","description":"'+description+'"},'
    js = js[:-1] + ']'
    
    return js
        

def agree_shop(shopids):
    '''同意店铺的注册'''
    failed_shops = list()
    for shopid in shopids:
        state = DBhandlerLog.checked_shop(shopid)
        if state == "0" : failed_shops.append(shopid)
    
    #如果有不成功的，返回店铺的id
    if len(failed_shops)>1 : 
        ids =""
        for i in failed_shops:
            ids += i+" "
        return ids.rstrip()
    
    return "1"
    
    
def disagree_shop(shopid,reason):
    '''不同意店铺的注册，并写明注册不通过的原因'''
    state = DBhandlerLog.disagree_shop_register(shopid,reason)
    return state
#*****************************************************************************


