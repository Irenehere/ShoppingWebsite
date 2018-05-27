/*记录是否已经加载热门商品*/
var isLoadPopular = 0;
/*记录是否已经加载推荐商品*/
var isLoadRecommend = 0;
var isLoadEnd = 0;
/*加载页面底部*/
function loadEnd(){
	isLoadEnd = 1;
	$.ajax({
		url:'/web/index.php',
		data:{"type":"end"},
		type:'POST',
		success:function(data){
			if (data.length > 4){
				$(document.body).append(data);
			}
		}
	})
}
/*加载推荐商品*/
function loadRecommend(){
	//if($('.recommend').width == null)
	isLoadRecommend = 1;
	$.ajax({
		url:'/web/index.php',
		data:{"type":"recommend"},
		type:'POST',
		success:function(data){
			if(data.length > 4){//防止后端出现异常导致js执行出异常
				var items = $.parseJSON(data);
				for (var i=0; i<items.length; i++){
					var s = "<img src='"+items[i].pic+"'/>";
					s += "<div class='desp'><p class='name'>"+items[i].name+"</p><div class='price'><i>￥</i><span>"+items[i].price+"</span></div></div>";
					s += "<div class='attd'><div class='like'></div><div class='like'></div><span class='le1'>喜欢</span><span class='ri2'>不喜欢</span></div></div>";
					$($('.recommend .item')[i]).css('background','#FFFFFF');
					$($('.recommend .item')[i]).empty();
					$($('.recommend .item')[i]).html(s);
					$($('.recommend .item')[i]).attr('id',items[i].id);
				}
				attitude();
			}
		}
	});
}
/*加载热门商品*/
function loadPopular(){
	//if($('.recommend').width == null)
	isLoadPopular = 1;
	$.ajax({
		url:'/web/index.php',
		data:{"type":"popularItem"},
		type:'POST',
		success:function(data){
			if(data.length > 4){//防止后端出现异常导致js执行出异常
				var items = $.parseJSON(data);
				for (var i=0; i<items.length; i++){
					var s = "<img src='"+items[i].pic+"'/>";
					s += "<div class='desp'><p class='name'>"+items[i].name+"</p><div class='price'><i>￥</i><span>"+items[i].price+"</span></div></div></div>";
					$($('.popularItem .item')[i]).css('background','#FFFFFF');
					$($('.popularItem .item')[i]).empty();
					$($('.popularItem .item')[i]).html(s);
					$($('.popularItem .item')[i]).attr('id',items[i].id);
					$($('.popularItem .item')[i]).attr('href','/web/index.php?type=detail&pid='+items[i].id);
				}
			}
		}
	});
}
function dynamic_load(){
	$('.dL').animate({top:'150px'},2000,function(){
		$('.dL').css('top','80px');
	});
}
/*图片未加载默认动画*/
function default_animation(){
	var dynamicLoad = '<div class="dL"></div>'
	$('.item').append(dynamicLoad);
	setInterval('dynamic_load()',2100);
}
/*推荐商品用户态度反馈*/
function attitude(){
$('.item').hover(function(){
	$(this).children('.attd').css('bottom','0px');
},function(){$(this).children('.attd').css('bottom','-90px')});
$('.attd').hover(function(){
	$(this).css('opacity',1);
},function(){$(this).css('opacity',0.8);});
$('.like').click(function(){
	//$(this).parent().parent().css('display','none');
	$(this).parent().css('bottom','-90px');
});
}