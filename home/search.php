<html>
<head>
<meta charset='utf-8'/>
<title>Welcome to UBUY!</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0"/>
<link rel="shortcut icon" href="/web/image/bitbug_favicon.ico" /> 
<link rel="stylesheet" href="/web/home/css/index.css?ver=300" type="text/css"/>
<link rel="stylesheet" href="/web/home/css/search.css?ver=1640" type="text/css"/>
<script src='/jquery/jquery-1.7.2.min.js'></script>
<script src='/web/home/js/basic.js?ver=1.2'></script>
<script src='/web/home/js/pro.js?var=1.0'></script>
<script src='/web/home/js/searchbasic.js?var=1.1' charset='utf-8'></script>
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
<div id='allgoods'>
<span>所选分类 ></span><!--
<span class='condit' ty='颜色'>颜色:红色<i></i></span>
<span class='condit' ty='尺寸'>尺寸:XXXL<i></i></span>
<span class='condit' ty='材质'>材质:棉<i></i></span>-->
</div>
<div id='allkinds'>
<div class='kinds' ty ='颜色'>
	<span>颜色:</span><span>红色</span><span>绿色</span><span>蓝色</span>
</div>
<div class='kinds' ty='尺寸'>
	<span>尺寸:</span><span>XXS</span><span>XS</span><span>S</span><span>M</span>
	<span>均码</span><span>L</span><span>XL</span><span>XXL</span><span>XXXL</span>
</div>
<div class='kinds' ty='材质'>
	<span>材质:</span><span>腈纶</span><span>涤纶</span>
	<span>锦纶</span><span>棉氨</span><span>棉麻</span>
	<span>棉</span>
</div>
</div>

<div id='sort'>
	<span class='general' status='0'>综合<i></i></span>
	<span class='sales' status='0'>销量<i></i></span>
	<span class='price' status='0'>价格<i></i></span>
	<span class='range'><input placeholder='￥' class='start'/> - <input placeholder='￥' class='end'/><span class='ok'>确认</span></span>
	</span>
	<div class='place'>发货地<i></i>
	<div class='detail_place'></div>
	</div>
</div>
<div id='commodity'>
	<div class='goods'>
		<a href='/web/index.php?type=detail&pid=p01'><img alt='' src='/web/image/products/0002.jpg'/></a>
		<div class='desp'>
			<span class='price'><i>￥</i><span>59.00</span></span>
			<span class='sales'>销量:300</span>
			<p class='name'><a href=''>HLA海澜之家短袖T恤男基础款简约圆领HNTBJ2E153A藏青(F3)175/92A(50)</a></p>
			<p class='shop'><i></i><a href="">海澜之家官方旗舰店</a></p>
			<span class='district'>广州</span>
		</div>
	</div>
</div>
<div id='pageTurn'><!--
<a class='lastpage' href=''><上一页</a>
<a class='page' href=''>1</a>
<a class='page' href=''>2</a>
<a class='page' href=''>3</a>
<a class='omit'>...</a>
<a class='page' href=''>5</a>
<a class='nextpage' href="">下一页></a>
<span>到第<input type='number' min="1" max="5"/>页<input class='yes' type='button' value='确定'/></span>
<span class='totalPage'>共10页</span>-->
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
<script>

$('#allkinds .kinds span:first-child').siblings().click(function(){
	s = "<span' class='condit' ty="+$(this).parent().attr('ty')+">"+$($(this).siblings()[0]).text()+$(this).text()+"<i></i></span>"
	$('#allgoods').append(s);
	$(this).parent().css('display','none');
	$('#allgoods .condit').click(conditclick);
});
function changeheight(p){
	$('#allkinds').css('height',$('#allkinds').height()+p)
}
function conditclick(){
	$('#allkinds .kinds[ty='+$(this).attr('ty')+']').css('display','block');
	$(this).remove();
}

/*窗口滚动动态显示顶部的搜索框及加载网页下部的动态信息*/
$(window).scroll(function(){
	if($(document).scrollTop() >= 350){
		//alert();
		$('#fix_top_bg').css('top','0px');
		if (isLoadEnd == 0 && $(document).scrollTop() >= 600){
		}
	} else {
		$('#fix_top_bg').css('top','-48px');
		$('#autoComplt2').slideUp();
	}
});
loadEnd();
for (var i = 0; i < 19; i++){
	$('#commodity').append($($('#commodity .goods')[0]).clone());
}
console.log('没有考虑分类名字过长导致分类框溢出问题');

var currentPage = GetQueryString('page')? parseInt(GetQueryString('page')):1;
var totalPage = 20;
var queryPage = new RegExp("(^|&)page=([^&]*)(&|$)");
function getGoods(page){
	$.ajax({
		url:"/web/index.php",
		data:{'page':page},
		type:"POST",
		success:function(data){
			//修改商品列表 现在测试返回20
			totalPage = parseInt(data);
			//currentPage = parseInt(GetQueryString('page'));
			createPage(currentPage, totalPage);
			setTimeout("turnPage()",200);
		}
	});
}

window.onload = function(){
	$('#top_search .search .input').val(GetQueryString('q'));
	$('.fix_search .input').val(GetQueryString('q'));
	getGoods(currentPage);
	basic();
	searchbasic();
}

</script>

</html>