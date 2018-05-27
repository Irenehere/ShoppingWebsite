function basic(){
/*首页*/
$('#top .login').attr('href','/web/login.html?redirectURL='+window.location.href)
$('#top .register').attr('href','/web/register.html?redirectURL='+window.location.href)

/*进入下拉分类项*/
$('#center li').hover(function(){
	var index=$(this).index("#center li");
	$(this).addClass('lihover').siblings().removeClass('lihover');
	$(this).children('span').addClass('arrow');
	$(this).siblings().children('span').removeClass("arrow");
	$(this).children('i').addClass('onhover');
	$(this).siblings().children('i').removeClass("onhover");
	$($('#center .detail')[index]).stop().fadeIn().siblings().stop().fadeOut();
	}, function (){
});
/*下拉分类离开*/
$('#center .left').mouseleave(function (){
	$('#center .left li').removeClass('lihover');
	$('#center .left i').removeClass('onhover');
	$('#center .left span').removeClass('arrow');
	$("#center .detail").stop().fadeOut();
});
/*顶部我的下拉*/
$('#top .my').hover(function(){
	$('#top .mylist').stop().slideDown(200);
	$('#top .my span').css('transform','rotate(180deg)');
	$('#top .my span').css('top','7.5px');
	},function(){
	$('#top .mylist').stop().slideUp(200);
	$('#top .my span').css('transform','rotate(0deg)');
	$('#top .my span').css('top','13.5px');
});
/*搜索类型选择:店铺,商品*/
$('#top_search .search .choose div').click(function(){
	$(this).attr('class','ched').siblings().attr('class','alter');
});
/*搜索回车*/
$('.input').keydown(function(e){
	var key_num = event.keyCode;
    if (13 == key_num) {
        $('#top_search .search .submit').click();
    }
});
/*搜索输入动态补全事件*/
$('#top_search .search .input').keyup(function(){
	$('#fix_top .input').val($(this).val());
	if ($('#top_search .search .input').val()){
	$.ajax({
		url:'/session/autoComplete.php',
		type:'get',
		data:{code:'utf-8', q:$('#top_search .search .input').val(),area:'c2c'},
		success: function(data){
			var result='';
			try{
			result = JSON.parse(data)['result'];
			} catch(e){}
			var autoComplt = $('#autoComplt');
			if (result.length){
				autoComplt.empty();
				for (var i =0; i< result.length; i++){
					autoComplt.append('<li>'+result[i][0]+'</li>');
				}
				autoComplt.css('height',result.length*30+'px');
				autoComplt.children().click(function(){
					$('#top_search .search .input').val($(this).text());
					$('#fix_top .input').val($(this).text());
					$('#top_search .search .submit').click();
					autoComplt.stop().slideUp();
				});
				autoComplt.stop().slideDown();
			} else {
				autoComplt.stop().slideUp();
			}
		}
	})
	} else {
		$('#autoComplt').stop().slideUp();
	}
});
/*搜索按钮点击事件*/
$('#top_search .submit').click(function(){
	var keyword= $('#top_search .input').val();
	if (keyword){
		window.location.href='/web/index.php?q='+keyword;
	}
});
/*顶部登录后退出登录事件*/
$('#exit').click(function(){
	$.ajax({
		url:'/web/index.php',
		type:'GET',
		data:{"type":"exit"},
		success:function(data){
			if(data){
				location.href='/web/index.php';
			}
		}
	});
});
/*悬浮于网页上方搜索类别鼠标悬浮事件*/
$('.chos').hover(function(){
	$('.fix_search .c2').stop().slideDown(50);
	$('.fix_search .kinds').css('borderRadius','5px 0px 0px 0px');
},function(){
	$('.fix_search .c2').stop().slideUp(50);
	$('.fix_search .kinds').css('borderRadius','5px 0px 0px 5px');
});
/*悬浮于网页上方搜索类别鼠标点击事件:店铺 商品*/
$('.chos').click(function(){
	var s1 = $('.fix_search .kinds').val();
	var s2 = $('.fix_search .c2').text();
	$('.fix_search .kinds').val(s2);
	$('.fix_search .c2').text(s1);
});
/*悬浮于网页上方搜索框输入动态补全事件*/
$('#fix_top .input').keyup(function(){
	$('#top_search .search .input').val($(this).val());
	if ($('#fix_top .input').val()){
	$.ajax({
		url:'/session/autoComplete.php',
		type:'get',
		data:{code:'utf-8', q:$('#fix_top .input').val(),area:'c2c'},
		success: function(data){
			var result='';
			try{
			result = JSON.parse(data)['result'];
			} catch(e){}
			var autoComplt = $('#autoComplt2');
			if (result.length){
				autoComplt.empty();
				for (var i =0; i< result.length; i++){
					autoComplt.append('<li>'+result[i][0]+'</li>');
				}
				autoComplt.css('height',result.length*30+'px');
				autoComplt.children().click(function(){
					$('#top_search .search .input').val($(this).text());
					$('#fix_top .input').val($(this).text());
					$('#top_search .search .submit').click();
					autoComplt.stop().slideUp();
				});
				autoComplt.stop().slideDown();
			} else {
				autoComplt.stop().slideUp();
			}
		}
	})
	} else {
		$('#autoComplt2').stop().slideUp();
	}
});
/*悬浮于网页上方搜索框失去焦点事件（用户点击别处，自动补全框缩回）*/
$('#fix_top .input').blur(function(){
	setTimeout("$('#autoComplt2').css('display','none')",300);//延时为了让用户选中li
});
/*搜索框失去焦点事件（用户点击别处，自动补全框缩回）*/
$('#top_search .search .input').blur(function(){
	setTimeout("$('#autoComplt').css('display','none')",300);
});
/*悬浮于网页上方搜索按钮点击事件*/
$('#fix_top .submit').click(function(){
	var keyword= $('#fix_top .input').val();
	if (keyword){
		window.location.href='/web/index.php?q='+keyword;
	}
});
}
