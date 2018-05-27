
function createBanner(){
	$.ajax({
		url:'/web/index.php',
		data:{"type":"headline"},
		type:'POST',
		success:function(data){
			if(data.length > 4){//防止后端出现异常导致js执行出异常
			var hL = $.parseJSON(data);
			for (var i=0; i<hL.length; i++){
				$('#banner .bannerAllPic').append('<li><a href="/web/index.php?type=detail&pid='+hL[i].productid+'"><img src="'+hL[i].pic+'" alt=""></a></li>');
			}
			dynamicMove();
			}
		}
	})
}
function dynamicMove(){
	var banner = $('#banner');
	var bannerUl = $('.bannerAllPic');  
    var aLeft = $('.aLeft');  
    var aRight = $('.aRight');  
    var circleAll = $('.circleAll');  
    var width = parseInt($('#banner').css('width'));  
    var index = 0;    
	var liFirst = $('#banner>.bannerAllPic>li:first').clone();
    bannerUl.append(liFirst);
    var imgNum = $('.bannerAllPic > li').length;
	bannerUl.css('width' , imgNum * width);
    while(index < imgNum-1) {
        circleAll.append("<li></li>");
        index++;
    }
    var firstCircle = $('.circleAll>li:first');
	firstCircle.addClass('now');
	var littleCircle = $('.circleAll>li');
    littleCircle.hover(function() {
		$(this).addClass('now').siblings().removeClass('now'); 
        index = $(this).index();  
        bannerUl.stop().animate({left: -index * width});  
	});
    aRight.click(function() {
        if(index == imgNum-1) {
            index = 0;
            bannerUl.css('left' , 0);
        }
        index++;
        bannerUl.stop().animate({left: -index * width});
        if(index == imgNum-1){
            littleCircle.eq(0).addClass('now').siblings().removeClass('now');
        } else {
            littleCircle.eq(index).addClass('now').siblings().removeClass('now');
        }
    });
    aLeft.click(function() {
        if(index<=0) {
            index = imgNum-1;
            bannerUl.css('left' , -index * width);
        }
        index--;
        bannerUl.stop().animate({left: -index * width});
        littleCircle.eq(index).addClass('now').siblings().removeClass('now');
    });
    var timeId = setInterval(function(){aRight.click()}, 2500);
    banner.hover(function() {
        clearInterval(timeId);
        }, function() {
        timeId = setInterval(function() {
        aRight.click();
        }, 2500);
    });
}