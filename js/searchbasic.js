function searchbasic(){
$('#allgoods .condit').hover(function(){
	//$(this).children('i').css('background','url("/web/image/search/del_red.png")');
	$(this).children('i').css('backgroundPosition','-15px 0px')
	}, function(){
	$(this).children('i').css('backgroundPosition','0px 0px')
	});
$('#sort .range').hover(function(){
	$(this).children('.ok').css({'display':'inline'});
}, function(){
	$(this).children('.ok').css({'display':'none'});	
});
$('#sort .price').click(function(){
	if($(this).attr('status') != '-1'){//降
		$(this).children('i').css('backgroundPosition','0px 0px');
		$(this).attr('status','-1');
		$(this).css({'background':'#FFFFFF','color':'red'});
	} else if($(this).attr('status') == '-1'){//升
		$(this).children('i').css('backgroundPosition','-15px 0px');
		$(this).attr('status','1');
		$(this).css({'background':'#FFFFFF','color':'red'});
	}
	$(this).siblings('.general').attr('status','0').css({'background':'transparent','color':'#6c6c6c'});
});
$('#sort .general').click(function(){
	$(this).siblings('.price').attr('status','0').css({'background':'transparent','color':'#6c6c6c'});
	$(this).siblings('.sales').attr('status','0').css({'background':'transparent','color':'#6c6c6c'});
	$(this).attr('status','1');
	$(this).css({'background':'#FFFFFF','color':'red'});
});
$('#sort .sales').click(function(){
	$(this).siblings('.general').attr('status','0').css({'background':'transparent','color':'#6c6c6c'});
	$(this).siblings('.sales').attr('status','0').css({'background':'transparent','color':'#6c6c6c'});
	$(this).attr('status','1');
	$(this).css({'background':'#FFFFFF','color':'red'});
});
$("#sort .place").hover(function(){
	$(this).children('.detail_place').slideDown('fast');
},function(){
	$(this).children('.detail_place').slideUp('fast');
})
}
/*创造底部翻页*/
function createPage(currentPage,totalPage){
var intv = 5;//中间预留页数
var s1 = '';
if (totalPage == 1){
} else if (totalPage <= intv+2){
	s1 =  "<a class='lastpage' href=''><上一页</a>";
	for (var i=0; i<totalPage; i++){
		s1 += "<a class='page' num='"+(i+1)+"' href=''>"+(i+1)+"</a>";
	}
} else {
	if (currentPage < (intv+1)/2+1){
		//1,2,3,4,5,...10
		s1 =  "<a class='lastpage' href=''><上一页</a>";
		for (var i=0; i<intv; i++){
			s1 += "<a class='page' num='"+(i+1)+"' href=''>"+(i+1)+"</a>";
		}
		s1 +="<a class='omit'>...</a><a class='page' num='"+totalPage+"' href=''>"+totalPage+"</a>";
	} else if (currentPage == (intv+1)/2+1){
		//1,2,3,4,5,6,...,10
		s1 =  "<a class='lastpage' href=''><上一页</a>";
		for (var i=0; i<intv+1; i++){
			s1 += "<a class='page' num='"+(i+1)+"' href=''>"+(i+1)+"</a>";
		}
		s1 +="<a class='omit'>...</a><a class='page' num='"+totalPage+"' href=''>"+totalPage+"</a>";
	} else if (currentPage > totalPage-(intv+1)/2){
		//1,...,6,7,8,9,10
		s1 =  "<a class='lastpage' href=''><上一页</a><a class='page' num='1' href=''>1</a><a class='omit'>...</a>";
		for (var i=0; i<intv; i++){
			s1 += "<a class='page' num='"+(totalPage-intv+i+1)+"' href=''>"+(totalPage-intv+i+1)+"</a>";
		}
	} else if (currentPage == totalPage-(intv+1)/2){
		//1,...,5,6,7,8,9,10
		s1 =  "<a class='lastpage' href=''><上一页</a><a class='page' num='1' href=''>1</a><a class='omit'>...</a>";
		for (var i=0; i<intv+1; i++){
			s1 += "<a class='page' num='"+(totalPage-intv+i)+"' href=''>"+(totalPage-intv+i)+"</a>";
		}
	} else {
		//1,...2,3,4,5,6 .. ,10
		s1 =  "<a class='lastpage' href=''><上一页</a><a class='page' num='1' href=''>1</a><a class='omit'>...</a>";
		for (var i=0; i<intv; i++){
			s1 += "<a class='page' num='"+(currentPage+i-(intv-1)/2)+"' href=''>"+(currentPage+i-(intv-1)/2)+"</a>";
		}
		s1 +="<a class='omit'>...</a><a class='page' num='"+totalPage+"' href=''>"+totalPage+"</a>";
	}
}
	if (s1){
		s1 += "<a class='nextpage' href=''>下一页></a>";
		s1 += "<span>到第<input type='number' min='1' max='"+totalPage+"'/>页<input class='yes' type='button' value='确定'/></span><span class='totalPage'>共"+totalPage+"页</span>";
		$("#pageTurn").append(s1);
	}
}
/*翻页应有的功能*/
function turnPage(){
	$(".page[num="+currentPage+"]").addClass("currentpage").removeClass('page').removeAttr('href');
	var jqarr = $(".page:not([num="+currentPage+"])");
	for (var i = 0; i<jqarr.length; i++){
		$(jqarr[i]).attr('href',setUrlPage($(jqarr[i]).attr('num')));
	}
	if (currentPage==1){
		$('#pageTurn .lastpage').css('color','#ededed').removeAttr('href').addClass('noclick');
	} else {
		$('#pageTurn .lastpage').attr('href',setUrlPage(currentPage-1));
	}
	if (currentPage == totalPage){
		$('#pageTurn .nextpage').css('color','#ededed').removeAttr('href').addClass('noclick');
	} else {
		$('#pageTurn .nextpage').attr('href',setUrlPage(currentPage+1))
	}
	$('#pageTurn .yes').click(function(){
		var page = $("#pageTurn input[type=number]").val();
		if( page && parseInt(page) != currentPage && parseInt(page)>0 && parseInt(page) <= totalPage){
			location.href=setUrlPage(parseInt(page));
		}
	})
	$('#pageTurn input[type=number]').keyup(function(e){
		var key_num = e.keyCode;
		if (13 == key_num) {
			$('#pageTurn .yes').click();		
		}
	})
	//$(".page:not([num="+currentPage+"])").attr('href',setUrlPage($(this).attr('num')));
}
/*暂时无用*/
function pushURL(jqObj){
	var stateObject = {"currentPage": jqObj.attr('num')};
	var title = $('title').text();
	var newUrl = setUrlPage(jqObj.attr('num'))
	history.pushState(stateObject,title,newUrl);
}

/*
window.addEventListener('popstate', function(event) {
	getGoods(event.state.currentPage);
});
*/
/*  (^|&)page==([^&]*)(&|$)
^&page=.+&$
var stateObject = {};
var title = "Wow Title";
var newUrl = "/my/awesome/url";
history.pushState(stateObject,title,newUrl);

for(i=0;i<5;i++){
	var stateObject = {currentPage: i};
	var title = "Wow Title "+i;
	var newUrl = "/my/awesome/url/"+i;
	history.pushState(stateObject,title,newUrl);
}
*/
/*根据传入的页码返回带页面的url*/
function setUrlPage(i){
	var reg = /[?&]page=[^&]+(&|$)/;
	var r = window.location.search.match(reg);
	if (r != null){
		var s = r[0].replace(/[&?]/g,'');
		return window.location.href.replace(s,'page='+i);
	} else {
		return window.location.href+"&page="+i;
	}
}
/*从链接中提取查询的字段信息*/
function GetQueryString(name){
    var reg = new RegExp("(^|&)"+name+"=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if(r!= null) return unescape(r[2]); return null;
}
/*
翻页设计
1,总页数小于等于7 直接全显示
2,否则如(10页)
如果当前页<=3 
	1,2,3,4,5...10
如果当前页 >=5 && <= 6 例如6
	1...4,5,6,7,8,...10
如果当前页 >= 7 例如 8
	1...6,7,8,9,10
				例如 7
	1...5,6,7,8,9,10
<div id='pageTurn'>
<a class='lastpage' href=''><上一页</a>
<a class='page' href=''>1</a>
<a class='page' href=''>2</a>
<a class='page' href=''>3</a>
<a class='omit'>...</a>
<a class='page' href=''>5</a>
<a class='nextpage' href="">下一页></a>
<span>到第<input type='number' min='1' max='5'/>页<input class='yes' type='button' value='确定'/></span>
<span class='totalPage'>共10页</span>
</div>
*/