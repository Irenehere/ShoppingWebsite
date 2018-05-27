<html>
<head>
<meta charset='utf-8'/>
<title>Welcome to UBUY!</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0"/>
<link rel="shortcut icon" href="/web/image/bitbug_favicon.ico" />
<link rel="stylesheet" href="/web/home/orderMana.css?ver=2314" type="text/css"/>
<link rel="stylesheet" href="/web/home/css/index.css?ver=300" type="text/css"/>

<script src='/jquery/jquery-1.7.2.min.js'></script>
</head>
<body>
<div id='top_bg'>
<div id='top'>
<?php 
	if (isLogin()){/*判断是否登录*/
		echo "<a>欢迎来到ubuy！</a><a class='cname' href='/web/myubuy.php?item=basicdata'>".$_SESSION['cname']."</a>";
		echo "<a href='' id='exit'>退出登录</a>";
	} else {
		echo "<a href='/web/login.html?redirectURL=/web/index.php' class='login'>登陆</a>";
		echo "<a href='/web/register.html?redirectURL=/web/index.php' class='register'>注册</a>";
	}
?>
<a href='/web/index.php'style='margin-left:670px;'>首页</a>
<div class='my'><a href='/web/myubuy.php?item=basicdata'>我的</a><span></span>
<ul class='mylist'>
<li><a href='/web/index.php?type=myubuy&item=basicdata'>基础资料</a></li>
<li><a href='/web/index.php?type=myubuy&item=moneymag'>资金管理</a></li>
<li><a href='/web/index.php?type=myubuy&item=ordermag'>订单管理</a></li>

</ul>
</div>
<a class='cart' href='/web/myubuy.php?item=shopcart'><span>购物车</span><i></i></a>

</div>
</div>
<div id='total'>
<div id='orderkinds'>
<span><i class='send'></i><i>待发货</i></span>

<span><i class='receive'></i><i>待收货</i></span>

<span><i class='cancel'></i><i>申请退货</i></span>
</div>
<div id='orderlist'>
<div class='topopt'>
<input type='text'/><input type='button' value='搜索'/>
<span><i class='idel'></i><i>批量删除</i></span>
</div>
<div class='toptitle'>
<span class='t_i'><input type="checkbox" value="Bike" /></span>
<span class='t_c_a'>全选</span>
<span class='t_g'>商品</span>
<span class='t_a'>属性</span>
<span class='t_p'>单价</span>
<span class='t_n'>数量</span>
<span class='t_p_t'>实付款</span>
</div>
<div class='ordercontent'>
<div class='oitem'>
	<div class='itemtitle'>
	<span class='it_i'><input type="checkbox" value="Bike" /></span>
	<span class='it_n'>订单号:dd1212323323</span>
	<span class='it_t'>2018/03/21</span>
	<span class='it_sn'><a href=''>海澜之家旗舰店</a></span>
	<span class='idel'></span>
	</div>
	<div class='itemleft'>
	<div class='igoods'>
	<span class='iimg'></span>
	<span class='ititle'><a href=''>HLA海澜之家短袖T恤男基础款简约圆领HNTBJ2E153A藏青(F3)175/92A(50)</a></span>
	<span class='iattr'>粉色;XL</span>
	<span class='iprice'><i>￥</i><i class='p'>58.00</i></span>
	<span class='inum'>1</span>
	</div>
	</div>
	<div class='itemright'>
	<span class='it_p'><i>￥</i><i class='p'>58.00</i></span>
	</div>
</div>
<div class='oitem' style='height:180px;'>
	<div class='itemtitle'>
	<span class='it_i'><input type="checkbox" value="Bike" /></span>
	<span class='it_n'>订单号:dd1212323323</span>
	<span class='it_t'>2018/03/21</span>
	<span class='it_sn'><a href=''>海澜之家旗舰店</a></span>
	<span class='idel'></span>
	</div>
	<div class='itemleft' style='height:159px;'>
	<div class='igoods'>
	<span class='iimg'></span>
	<span class='ititle'><a href=''>HLA海澜之家短袖T恤男基础款简约圆领HNTBJ2E153A藏青(F3)175/92A(50)</a></span>
	<span class='iattr'>粉色;XL</span>
	<span class='iprice'><i>￥</i><i class='p'>58.00</i></span>
	<span class='inum'>2</span>
	</div>
	<div class='igoods'>
	<span class='iimg'></span>
	<span class='ititle'><a href=''>HLA海澜之家短袖T恤男基础款简约圆领HNTBJ2E153A藏青(F3)175/92A(50)</a></span>
	<span class='iattr'>粉色;XL</span>
	<span class='iprice'><i>￥</i><i class='p'>58.00</i></span>
	<span class='inum'>1</span>
	</div>
	</div>
	<div class='itemright' style='margin-top:42px'>
	<span class='it_p'><i>￥</i><i class='p'>174.00</i></span>
	</div>
</div>
<div class='oitem' style='height:180px;'>
	<div class='itemtitle'>
	<span class='it_i'><input type="checkbox" value="Bike" /></span>
	<span class='it_n'>订单号:dd1212323323</span>
	<span class='it_t'>2018/03/21</span>
	<span class='it_sn'><a href=''>海澜之家旗舰店</a></span>
	<span class='idel'></span>
	</div>
	<div class='itemleft' style='height:159px;'>
	<div class='igoods'>
	<span class='iimg'></span>
	<span class='ititle'><a href=''>HLA海澜之家短袖T恤男基础款简约圆领HNTBJ2E153A藏青(F3)175/92A(50)</a></span>
	<span class='iattr'>粉色;XL</span>
	<span class='iprice'><i>￥</i><i class='p'>58.00</i></span>
	<span class='inum'>2</span>
	</div>
	<div class='igoods'>
	<span class='iimg'></span>
	<span class='ititle'><a href=''>HLA海澜之家短袖T恤男基础款简约圆领HNTBJ2E153A藏青(F3)175/92A(50)</a></span>
	<span class='iattr'>粉色;XL</span>
	<span class='iprice'><i>￥</i><i class='p'>58.00</i></span>
	<span class='inum'>1</span>
	</div>
	</div>
	<div class='itemright' style='margin-top:42px'>
	<span class='it_p'><i>￥</i><i class='p'>174.00</i></span>
	</div>
</div>
<div class='oitem'>
	<div class='itemtitle'>
	<span class='it_i'><input type="checkbox" value="Bike" /></span>
	<span class='it_n'>订单号:dd1212323323</span>
	<span class='it_t'>2018/03/21</span>
	<span class='it_sn'><a href=''>海澜之家旗舰店</a></span>
	<span class='idel'></span>
	</div>
	<div class='itemleft'>
	<div class='igoods'>
	<span class='iimg'></span>
	<span class='ititle'><a href=''>HLA海澜之家短袖T恤男基础款简约圆领HNTBJ2E153A藏青(F3)175/92A(50)</a></span>
	<span class='iattr'>粉色;XL</span>
	<span class='iprice'><i>￥</i><i class='p'>58.00</i></span>
	<span class='inum'>1</span>
	</div>
	</div>
	<div class='itemright'>
	<span class='it_p'><i>￥</i><i class='p'>58.00</i></span>
	</div>
</div>
<div class='oitem' style='height:180px;'>
	<div class='itemtitle'>
	<span class='it_i'><input type="checkbox" value="Bike" /></span>
	<span class='it_n'>订单号:dd1212323323</span>
	<span class='it_t'>2018/03/21</span>
	<span class='it_sn'><a href=''>海澜之家旗舰店</a></span>
	<span class='idel'></span>
	</div>
	<div class='itemleft' style='height:159px;'>
	<div class='igoods'>
	<span class='iimg'></span>
	<span class='ititle'><a href=''>HLA海澜之家短袖T恤男基础款简约圆领HNTBJ2E153A藏青(F3)175/92A(50)</a></span>
	<span class='iattr'>粉色;XL</span>
	<span class='iprice'><i>￥</i><i class='p'>58.00</i></span>
	<span class='inum'>2</span>
	</div>
	<div class='igoods'>
	<span class='iimg'></span>
	<span class='ititle'><a href=''>HLA海澜之家短袖T恤男基础款简约圆领HNTBJ2E153A藏青(F3)175/92A(50)</a></span>
	<span class='iattr'>粉色;XL</span>
	<span class='iprice'><i>￥</i><i class='p'>58.00</i></span>
	<span class='inum'>1</span>
	</div>
	</div>
	<div class='itemright' style='margin-top:42px'>
	<span class='it_p'><i>￥</i><i class='p'>174.00</i></span>
	</div>
</div>

<div class='oitem' style='height:180px;'>
	<div class='itemtitle'>
	<span class='it_i'><input type="checkbox" value="Bike" /></span>
	<span class='it_n'>订单号:dd1212323323</span>
	<span class='it_t'>2018/03/21</span>
	<span class='it_sn'><a href=''>海澜之家旗舰店</a></span>
	<span class='idel'></span>
	</div>
	<div class='itemleft' style='height:159px;'>
	<div class='igoods'>
	<span class='iimg'></span>
	<span class='ititle'><a href=''>HLA海澜之家短袖T恤男基础款简约圆领HNTBJ2E153A藏青(F3)175/92A(50)</a></span>
	<span class='iattr'>粉色;XL</span>
	<span class='iprice'><i>￥</i><i class='p'>58.00</i></span>
	<span class='inum'>2</span>
	</div>
	<div class='igoods'>
	<span class='iimg'></span>
	<span class='ititle'><a href=''>HLA海澜之家短袖T恤男基础款简约圆领HNTBJ2E153A藏青(F3)175/92A(50)</a></span>
	<span class='iattr'>粉色;XL</span>
	<span class='iprice'><i>￥</i><i class='p'>58.00</i></span>
	<span class='inum'>1</span>
	</div>
	</div>
	<div class='itemright' style='margin-top:42px'>
	<span class='it_p'><i>￥</i><i class='p'>174.00</i></span>
	</div>
</div>
</div>
<div class='pageturn'>
<span class='totalpage'>总页数:<i>10<i></span>
<span class='currentpage'>当前页:<i>1<i></span>
<span class='next'>下一页></span>
<span class='last'><上一页</span>
</div>
</div>
</div>

<div id='allfix'>
<div class='del'>
<div class='desp'>
	<img src='/web/image/user/warning.png'/>
	<span class='msg'>确认删除？</span>
</div>
<input type='button' class='yes' value='确认'/>
<input type='button' class='no' value='取消'/>
</div>
</div>
</body>
<script>
$('.oitem .itemtitle .idel').click(function(){
	$('#allfix').css('display','block');
});
$('#allfix .yes').click(function(){
	$('#allfix').css('display','none');
});
$('#allfix .no').click(function(){
	$('#allfix').css('display','none');
});
</script>
</html>