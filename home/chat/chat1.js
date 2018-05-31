function prepareChat(){
$('#content').scroll(function(){
	$('#frame .scroll').stop().css('display','block');
	var p = $(this)[0].scrollHeight-$(this).height();
	$('#frame .scroll').css('top',($(this).height()-50)*($(this).scrollTop()/p)+'px');
	$('#frame .scroll').stop().fadeOut(200);
});
$('#input').keydown(function(e){
	var key_num = event.keyCode;
    if (13 == key_num) {
        $('#send').click();
    }
});
$('#getHistory').click(function(){
	getHistory();
});
getId('content').innerHTML = "";
}



var selfId = 'c00001'//用户自己的id
var shopId = 'm00001'//店铺的id

function getHistory(){
	$.ajax({
		url:'/web/home/chat/WSGetHistory.php',
		data:{"to":selfId,"from":shopId},
		type:'POST',
		success:showMsg,
		error:function(){console.log('加载未读失败');}
	});
	function showMsg(data){
		if(data.length > 4){//防止后端出现异常导致js执行出异常
			var msg = $.parseJSON(data);
			var s = '';
			for (var i=0; i<msg.length; i++){
				s+=getMsgStyle(msg[i].chatRecord, msg[i].type);
			}
			getId('content').innerHTML =s+getId('content').innerHTML;
			$('#content').scrollTop($('#content')[0].scrollHeight+1);
		}
	}
}
function getUnRead(){
	$.ajax({
		url:'/web/home/chat/WSGetUnread.php',
		data:{"to":selfId,"from":shopId},
		type:'POST',
		success:showMsg,
		error:function(){console.log('加载未读失败');}
	});
	function showMsg(data){
		if(data.length > 4){//防止后端出现异常导致js执行出异常
			var msg = $.parseJSON(data);
			for (var i=0; i<msg.length; i++){
				getId('content').innerHTML +=getMsgStyle(msg[i].chatRecord, 'other');
			}
			$('#content').scrollTop($('#content')[0].scrollHeight+1);
		}/*防止消息错乱，必须加载完未读才开始聊天*/
		startSocket();
		/*但是有可能可以接收未读和历史消息，但是不支持websocket，导致无法发消息，要先检查websocket支持情况*/
	}
}

/*发送保存到数据库*/
function sendMsg(){ 
	var msg = $('#input').val();
	if (msg){
		$.ajax({
			url:'/web/home/chat/WSSaveMsg.php',
			data:{"from":selfId,"to":shopId,"content":HTMLEnCode(msg),"chatid":uuid(10,64)},
			type:'POST',
			success: deal
		});
	}
	function deal(data){
		if (data != 'success'){/*保存不成功给与警示未同步*/
			
		} else { /*保存成功*/
			
		}
	}
}

function getMsgStyle(msg, type){
	var tmp = document.createElement('div');
	tmp.innerHTML = msg;
	tmp.setAttribute('id','tmp3');
	tmp.style = 'padding:0px 10px;width:200px;word-wrap:break-word;position:absolute;top:0px;left:0px;visibility:hidden';
	//IE不支持直接设置style
	tmp.style.padding = '0px 10px';
	tmp.style.width = '160px';
	tmp.style.wordWrap = 'break-word';
	tmp.style.position = 'absolute';
	tmp.style.top = '0px';
	tmp.style.left = '0px';
	tmp.style.visibility = 'hidden';
	document.body.appendChild(tmp);//先试探性计算出高度，看是否要换行处理
	var height = '';
	height = window.getComputedStyle(document.getElementById('tmp3')).height;
	var heightValue = parseFloat(height); //可直接对像素转换
	document.body.removeChild(tmp);
	if (type =='me'){
		if ( heightValue < 25){
			return "<div class='msg msgR1'><div class='himg'></div><div class='right1'><span>"+msg+"</span></div></div>";
		} else {
			return "<div class='msg msgR2'><div class='himg'></div><div class='right2'>"+msg+"</div></div>";
		}
	} else if (type =='other'){
		if (heightValue < 25){
			return "<div class='msg msgL1'><div class='himg'></div><div class='left1'><span>"+msg+"</span></div></div>";
		} else {
			return "<div class='msg msgL2'><div class='himg'></div><div class='left2'>"+msg+"</div></div>";
		}
	} else {
		return "";
	}
}

/*浏览器支持html5-WebSocket*/
var ws = '';
function startSocket(){
	$('#send').click(send);
	ws = new WebSocket("ws://172.18.38.163:12345");
	ws.onopen = wsopen;
	ws.onmessage = wsmessage;
	ws.onerror = wserror;
	$('#content').scrollTop($('#content')[0].scrollHeight+1);
}
function wsopen(){}
function wsmessage(e){
	var msg = JSON.parse(e.data);
	var data = {'sender':'','content':''};
	var sender, user_name, name_list, change_type;
	switch (msg.type){
        case 'system':
            sender = '系统消息: ';
            break; 
        case 'user':
			data.sender = msg.from;
			data.content = msg.content;
			listMsg(data);
            break;
        case 'handshake':
            var user_info = {'type': 'login', 'content': selfId};//握手消息发给所有人
            wssend(user_info);
		    return;
        case 'login':
		case 'logout':
		    user_name = msg.content;
		    name_list = msg.user_list;
			change_type = msg.type;
			dealUser(user_name, change_type); 
            return;
    }
}
function wserror(){
    var data = "Connection couldn't be established!";
    alert(data);
}
function wssend(msg){
    var data = JSON.stringify(msg);
    ws.send(data);
}
//发送消息
function send(){
	var msg = $('#input').val();
	if (msg){
        var data = {'content': HTMLEnCode(msg), 'type': 'user', 'to':shopId}; //多加一个to 发给谁, allusers代表所有人
        wssend(data);
		sendMsg();
		getId('content').innerHTML += getMsgStyle(HTMLEnCode(msg),'me');
		$('#input').val('').focus();
		$('#content').scrollTop($('#content')[0].scrollHeight+1);
	}
}
/**
 * 将消息内容添加到输出框中,并将滚动条滚动到最下方
*/
function listMsg(data){
	getId('content').innerHTML += getMsgStyle(data.content,'other');
	$('#content').scrollTop($('#content')[0].scrollHeight+1);
}

function dealUser(user_name,change_type){
	if (change_type=='login'){
		
	} else {
	}
}
function confirm(event) {
    var key_num = event.keyCode;
    if (13 == key_num) {
        $('#send').click();
    } else {
        return false;
    }
}

//$('#input').keydown(confirm);


/*获取文件类型*/
function getFileType(fileName){
	return fileName.substring(fileName.lastIndexOf('.')+1);
}
//两个通用便捷函数
function getId(id){
	return document.getElementById(id);
}
function getClass(clsName){
	return document.getElementsByClassName(clsName);
}
function uuid(len, radix) {
	var chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'.split('');
    var uuid = [], i;
    radix = radix || chars.length;
    if (len) {
        for (i = 0; i < len; i++) uuid[i] = chars[0 | Math.random() * radix];
    } else {
        var r;
		uuid[8] = uuid[13] = uuid[18] = uuid[23] = '-';
        uuid[14] = '4';
        for (i = 0; i < 36; i++) {
		    if (!uuid[i]) {
                r = 0 | Math.random() * 16;
                uuid[i] = chars[(i == 19) ? (r & 0x3) | 0x8 : r];
            }
		}
    }
    return uuid.join('');
}
function HTMLEnCode(str) {
	var s = "";
    if (str.length == 0) return "";
    s = str.replace(/&/g, "&gt;");
    s = s.replace(/</g, "&lt;");
    s = s.replace(/>/g, "&gt;");
    s = s.replace(/    /g, "&nbsp;");
    s = s.replace(/\'/g, "'");
    s = s.replace(/\"/g, "&quot;");
    s = s.replace(/\n/g, "<br>");
    return s;
}
function HTMLDeCode(str) {
	var s = "";
	if (str.length == 0) return "";
	s = str.replace(/&amp;/g, "&");
	s = s.replace(/&lt;/g, "<");
	s = s.replace(/&gt;/g, ">");
	s = s.replace(/&nbsp;/g, "    ");
	s = s.replace(/'/g, "\'");
	s = s.replace(/&quot;/g, "\"");
	s = s.replace(/<br>/g, "\n");
	s = s.replace(/&#39;/g, "\'");
	return s;
}