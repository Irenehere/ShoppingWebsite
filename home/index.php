<html>
<head>
<meta charset='utf-8'/>
<title>Welcome to UBUY!</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0"/>
<link rel="shortcut icon" href="/web/image/bitbug_favicon.ico" /> 
<link rel="stylesheet" href="/web/home/css/index.css?ver=431" type="text/css"/>
<script src='/jquery/jquery-1.7.2.min.js'></script>
<script src='/web/home/js/basic.js?ver=10'></script>
<script src='/web/home/js/banner.js?var=1.2'></script>
<script src='/web/home/js/pro.js?var=1.1'></script>
<script>
/*页面加载完毕执行操作*/
$.ready(ready());
function ready(){
	createBanner();
	//setTimeout("default_animation()",100);
}
window.onload= function(){
	basic();
	default_animation();
}
/*窗口滚动动态显示顶部的搜索框及加载网页下部的动态信息*/
$(window).scroll(function(){
	if($(document).scrollTop() >= 200){
		//alert();
		$('#fix_top_bg').css('top','0px');
		if(isLoadRecommend== 0 && $('.recommend').width() != null&&1!==0){
			loadRecommend();
		}
		if (isLoadPopular == 0 &&1!==0){
			loadPopular();
		}
		if (isLoadEnd == 0 && $(document).scrollTop() >= 600){
			loadEnd();
		}
	} else {
		$('#fix_top_bg').css('top','-48px');
		$('#autoComplt2').slideUp();
	}
});
</script>
</head>
<body>
<div id='top_bg'>
<div id='top'>
<?php 
	if (isLogin()){/*判断是否登录*/
		echo "<a>欢迎来到ubuy！</a><a class='cname' href='/web/myubuy.php?item=basicdata'>".$_SESSION['cname']."</a>";
		echo "<a href='' id='exit'>退出登录</a>";
	} else {
		echo "<a href='' class='login'>登陆</a>";
		echo "<a href='/web/register.html?redirectURL=/web/index.php' class='regisiter'>注册</a>";
	}
?>
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
<div id='top_search'>
	<div class='logo'></div>
	<div class='search'>
		<div class="choose">
			<div class='ched'><span>商品</span></div>
			<div class='alter'><span>店铺</span></div>
		</div>
		<div class='search_input'>
		<input type='text' class='input'/>
		<input type='button'class='submit'/>
		<ul id='autoComplt'>
		</ul><!--自动补全的div-->
		</div>
	</div>
</div>
	
<div id='navi_bg'>
	<div id='navi'></div>
</div>

<div id='center'>
	<div class='left'>
	<ul>
		<li><i class='clothes'></i><a href='#'>男装</a> / <a href='#'>女装</a><span></span></li>
		<li><i class='cosmetic'></i><a href='#'>美妆</a> / <a href='#'>个人护理</a><span ></span></li>
		<li><i class='jewllery'></i><a href='#'>腕表</a> / <a href='#'>珠宝饰品</a><span ></span></li>
		<li><i class='maternal'></i><a href='#'>母婴用品</a><span ></span></li>
		<li><i class='snacks'></i><a href='#'>零食</a> / <a href='#'>茶酒</a><span ></span></li>
		<li><i class='furniture'></i><a href='#'>家具</a> / <a href='#'>建材</a>/ <a href='#'>装修</a><span ></span></li>
		<li><i class='appliances'></i><a href='#'>大家电</a> / <a href='#'>生活电器</a><span ></span></li>
		<li><i class='textile'></i><a href='#'>家纺</a> / <a href='#'>家饰</a><span ></span></li>
		<li><i class='book'></i><a href='#'>图书</a> / <a href='#'>音像</a><span ></span></li>
		<li><i class='shoes'></i><a href='#'>女鞋</a>/ <a href='#'>男鞋</a>/ <a href='#'>箱包</a><span ></span></li>
		<li><i class='medicine'></i><a href='#'>医药</a> / <a href='#'>保健</a><span ></span></li>
		<li><i class='utensils'></i><a href='#'>收纳</a> / <a href='#'>厨具</a><span ></span></li>
		<li><i class='car'></i><a href='#'>汽车</a> / <a href='#'>二手车</a><span ></span></li>
	</ul>
	<div>
		<div class='detail'>1</div>
		<div class='detail'>2</div>
		<div class='detail'>3</div>
		<div class='detail'>4</div>
		<div class='detail'>5</div>
		<div class='detail'>6</div>
		<div class='detail'>7</div>
		<div class='detail'>8</div>
		<div class='detail'>9</div>
		<div class='detail'>10</div>
		<div class='detail'>11</div>
		<div class='detail'>12</div>
		<div class='detail'>13</div>
	</div>
	</div>
	<div class='right'>
		<div id='banner'>
			<ul class="bannerAllPic"></ul>
			<div class="arrow">
				<a href="javascript:void(0)" class="aLeft">&lt;</a>
				<a href="javascript:void(0)" class="aRight">&gt;</a>
			</div>
			<ol class="circleAll"></ol>
		</div>
		<div class='head2'><a href="#"><img src="/web/image/img1.jpg" alt=""></a></div>
		<div class='head2'><a href="#"><img src="/web/image/img3.jpg" alt=""></a></div>
		<div class='head2 head2end'><a href="#"><img src="/web/image/img5.jpg" alt=""></a></div>
	</div>
</div>

<?php 
	if (isLogin()){/*判断是否登录*/
		echo "<div class='recommend'><div class='slogen'><i class='star'></i><span>为您推荐</span></div><div class='line'></div>
		<div class='item'></div>
		<div class='item'></div>
		<div class='item'></div>
		<div class='item'></div>
		<div class='item'></div>
		</div>";
	}
?>

<div class='popularItem'>
	<div class='slogen'>
		<i class='star'></i>
		<span>热门单品</span>
	</div>
	<div class='line'></div>
	<a class='item' href=''></a>
	<a class='item' href=''></a>
	<a class='item' href=''></a>
	<a class='item' href=''></a>
	<a class='item' href=''></a>
	<a class='item' href=''></a>
	<a class='item' href=''></a>
	<a class='item' href=''></a>
	<a class='item' href=''></a>
	<a class='item' href=''></a>	
</div>

<div id='end'>
	<div class='line'></div>
	<div class='endLine'>
		<span>END</span>
	</div>
</div>

<div id='fix_top_bg'>
	<div id='fix_top'>
	<div class='fix_logo'></div>
	<div class='fix_search'>
		<div class='chos'>
		<input type='button' class='kinds' value='商品'/>
		<div class='c2'>店铺</div>
		</div>
		<input type='text' class='input'/>
		<input type='button'class='submit'/>
		<ul id='autoComplt2'></ul>
		<i></i>
	</div>
	</div>
</div>
</body>
</html>