<html>
<head>
<meta charset='utf-8'/>
<title>Welcome to UBUY!</title>
<link rel="shortcut icon" href="/web/image/bitbug_favicon.ico" /> 
<link rel="stylesheet" href="/web/home/css/index.css?ver=300" type="text/css"/>
<link rel="stylesheet" href="/web/home/css/goodsDetail.css?ver=1309" type="text/css"/>
<link rel="stylesheet" href="/web/home/chat/chat.css?ver=4130" type="text/css"/>
<script src='/jquery/jquery-1.7.2.min.js'></script>
<script src='/web/home/js/basic.js?ver=1.3'></script>
<script src='/web/home/js/pro.js?var=1.0'></script>
<script src='/web/home/chat/chat1.js?var=1.1'></script>
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

<div id='store'>
<span class='storeName'><i></i><a href=''>海澜之家官方旗舰店</a></span>
<span class='allCom'>综合评价:<i>4.8</i></span>
<span class='intoShop'><i></i><a href=''>进店逛逛</a></span>
<span class='chat' title='点此与卖家聊天'><i></i>联系卖家</span>
</div>

<div id='detailP'>
<div id='pic'>
<img id='detPic'src='/web/image/products/0002.jpg'></img>
<div class='mask top1'></div>
<div class='mask left1'></div>
<div class='mask right1'></div>
<div class='mask bottom1'></div>
</div> 
<div id='picHidden'>
<canvas  id='MyCanvas' width='420' height='420'></canvas>
</div>
<div class='rightD'>
<p class='title'>HLA海澜之家短袖T恤男基础款简约圆领HNTBJ2E153A藏青(F3)175/92A(50)</p>
<span class='price'><i>￥</i><span>59.00</span></span><br/>
<span class='secd'>
<span class='sales'>销量:<i>2018<i></span>
<span class='comNum'>累计评论:<i>1200<i></span>
<span class='包邮'></span>
</span>
<div id='allkinds'>
<span class='kinds'>
	<span class='kt'>颜色:</span><span class='dt'><span>红色</span><span>绿色</span><span>蓝色</span>
</span></span>
<span class='kinds'>
	<span class='kt'>尺寸:</span><span class='dt'><span>XXS</span><span>XS</span><span>S</span><span>M</span>
	<span>均码</span><span>L</span><span>XL</span><span>XXL</span><span>XXXL</span>
</span></span>
<span class='kinds'>
	<span class='kt'>材质:</span><span class='dt'><span>腈纶</span><span>涤纶</span>
	<span>锦纶</span><span>棉氨</span><span>棉麻</span>
	<span>棉</span>
</span></span>
</div>
<span class='number'><span class='num'>数量:</span><input id ='inpNum'type="number" value="1" min="1"/><span class='totalNum'>库存:800</span></span>
<input class='but imeBuy' type='button' value='立即购买'/>
<input class='but addCart' type='button' value='加入购物车'/>
</div>
</div>
<div id='detAndCom'>
<span class='cho detailPics'>商品详情</span><span class='ncho comments'>商品评论</span>
<div class='line'></div>
<div class='content'>
<div class='magic_in'>
<div class='detailpic'>
<img src='/web/image/detail/det_img1.jpg'/>
<img src='/web/image/detail/det_img2.jpg' />
<img src='/web/image/detail/det_img3.jpg' />
</div>
<div class='comment'>
<div class='com'>
	<div class='r_com'><span class='u_portrait'><img src='/web/image/detail/up1.jpg'/></span><span class='u_name'>q***0</span></div>
	<div class='l_com'><span class='u_con'>这件衣服挺好的，给商家比心！</span></div>
</div>
<div class='com'>
	<div class='r_com'><span class='u_portrait'><img src='/web/image/detail/up2.jpg'/></span><span class='u_name'>天***忆</span></div>
	<div class='l_com'><span class='u_con'>超级实用的小风扇，这几天郑州真的是热疯了，我们寝室没有安装空调，所以一人买了一个这家的风扇，这的超级好了，很实用，也很凉快，现在我在也不用担心半夜被热醒了，质量也很好。店家很好，耐心耐心的。</span></div>
</div>
<div class='com'>
	<div class='r_com'><span class='u_portrait'><img src='/web/image/detail/up3.jpg'/></span><span class='u_name'>g***k</span></div>
	<div class='l_com'><span class='u_con'>宝贝风很大，声音可以接受蛮小声的，夏天在寝室不开空调应该是可以过了，对着催久了有点头晕，还是小的那个档位。。。。</span></div>
</div>
<div class='com'>
	<div class='r_com'><span class='u_portrait'><img src='/web/image/detail/up3.jpg'/></span><span class='u_name'>g***k</span></div>
	<div class='l_com'><span class='u_con'>宝贝风很大，声音可以接受蛮小声的，夏天在寝室不开空调应该是可以过了，对着催久了有点头晕，还是小的那个档位。。。。</span></div>
</div>
<div class='com'>
	<div class='r_com'><span class='u_portrait'><img src='/web/image/detail/up3.jpg'/></span><span class='u_name'>g***k</span></div>
	<div class='l_com'><span class='u_con'>宝贝风很大，声音可以接受蛮小声的，夏天在寝室不开空调应该是可以过了，对着催久了有点头晕，还是小的那个档位。。。。</span></div>
</div>
<div class='com'>
	<div class='r_com'><span class='u_portrait'><img src='/web/image/detail/up3.jpg'/></span><span class='u_name'>g***k</span></div>
	<div class='l_com'><span class='u_con'>宝贝风很大，声音可以接受蛮小声的，夏天在寝室不开空调应该是可以过了，对着催久了有点头晕，还是小的那个档位。。。。</span></div>
</div>
<div class='com'>
	<div class='r_com'><span class='u_portrait'><img src='/web/image/detail/up3.jpg'/></span><span class='u_name'>g***k</span></div>
	<div class='l_com'><span class='u_con'>宝贝风很大，声音可以接受蛮小声的，夏天在寝室不开空调应该是可以过了，对着催久了有点头晕，还是小的那个档位。。。。</span></div>
</div>
<div class='com'>
	<div class='r_com'><span class='u_portrait'><img src='/web/image/detail/up3.jpg'/></span><span class='u_name'>g***k</span></div>
	<div class='l_com'><span class='u_con'>宝贝风很大，声音可以接受蛮小声的，夏天在寝室不开空调应该是可以过了，对着催久了有点头晕，还是小的那个档位。。。。</span></div>
</div>
<div class='com'>
	<div class='r_com'><span class='u_portrait'><img src='/web/image/detail/up3.jpg'/></span><span class='u_name'>g***k</span></div>
	<div class='l_com'><span class='u_con'>宝贝风很大，声音可以接受蛮小声的，夏天在寝室不开空调应该是可以过了，对着催久了有点头晕，还是小的那个档位。。。。</span></div>
</div>
<div class='pageturn'>
<span class='totalpage'>总页数:<i>10<i></span>
<span class='currentpage'>当前页:<i>1<i></span>
<span class='next'>下一页></span>
<span class='last'><上一页</span>
</div>
</div>
</div>
</div>
</div>

<div id='chat'>
	<div id='frame'>
	<div id='content'>
	</div>
	<div class='scroll'>
	</div>
	</div>
	<div id='textinput'>
		<input type='text' id='input' placeholder='输入内容...'/>
		<input type='button' id='send' value='发送'/>
	</div>
	<div id='more'>
	<span class='smile'></span>
	<span class='more'></span>
	</div>
</div>

<script>
$('#detAndCom>span').click(function(){
	if($(this).hasClass('ncho')){
		$(this).removeClass('ncho').addClass('cho').siblings('.cho').removeClass('cho').addClass('ncho');
	}
	var ma = $('#detAndCom .content .magic_in')
	ma.css('marginLeft',-1*(parseInt(ma.css('marginLeft'))+981)%1962+'px');
})
function ys(){
	var c = document.getElementById('MyCanvas');
	var ctx = c.getContext('2d');
	var img = document.getElementById('detPic');
	img.onmousemove = function(e){
	var nowX = e.clientX-$('#detPic').offset().left+$(document).scrollLeft(), nowY = e.clientY-$('#detPic').offset().top+$(document).scrollTop();;
	var cx = nowX;
	var cy = nowY;
	if (cx < 60){cx = 60} else if(cx > 360) {cx = 360}
	if (cy < 60){cy = 60} else if(cy > 360) {cy = 360}
	ctx.drawImage(img,(cx-60)*460/420,(cy-60)*460/420,120*460/420,120*460/420,0,0,420,420);
	$('#pic .top1').css({'top':(cy-60-120)+'px','left':(cx-60)+'px'});
	$('#pic .left1').css({'top':(cy-60)+'px','left':(cx-60-120)+'px'});
	$('#pic .right1').css({'top':(cy-60)+'px','left':(cx-60+120)+'px'});
	$('#pic .bottom1').css({'top':(cy-60+120)+'px','left':(cx-60)+'px'});
	}
}
$('#pic img').hover(function(){
	$('#picHidden').css('display','block');
	$('.mask').css('display','block');
}, function(){
	$('#picHidden').css('display','none');
	$('.mask').css('display','none');
})
ys()
$('#allkinds .kinds .dt span').click(function(){
	$(this).css('border','1.5px solid red').siblings().css('border','1.5px solid #ededed')
})
window.onload = function(){
	basic();
}
$('#chat').css('display','none');
$('.chat').click(function(){
	$('#chat').stop().slideDown();
	prepareChat();
	getUnRead();//这里已经开始socket了
})
</script>
</html>