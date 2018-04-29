1. 文件说明

RecommendationSys.py : 推荐系统的主要文件

DBhandler.py : 对数据库处理的文件

popularItem.py : 得到最热门的商品

recommend.py : 得到用户的推荐商品

2. 调用

（1）得到用户的推荐：Python recommend.py c201804291551 10

 c201804291551 ： 顾客的id
 
 10 : 表示推荐的数量
 
 （2）得到热门的商品：Python popularItem.py 10
 
 10 : 表示推荐的数量

3. 返回值

类型：返回每一个商品的id,名称，图片url，店铺名称，价格

格式；

[{"id":"p201804281611","name":"名称","pic":"/web/imag.png","shop":"店铺名","price":"5.2"},

 {"id":"p201804281620","name":"名称","pic":"/web/imag.png","shop":"店铺名","price":"200.0"}]

