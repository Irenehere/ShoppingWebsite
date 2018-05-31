<?php
session_start();
if(request() =='POST'){
	if (post('user') && post('passwd')){ /*请求登录*/
		include('login.php');
		$log = new Login($_POST['user'],$_POST['passwd']);
		if ($log->check()){ /*成功登陆*/
			$_SESSION['cname'] = $_POST['user'];
			$_SESSION['cid'] = '00001';
			echo 'success';
		} else {
			echo 'failure';
		}
	} else if(post('type') && $_POST['type'] == 'headline'){
		include('headline.php');
		$hL = new HL();
		echo $hL->getHL();
	} else if(post('type') && $_POST['type'] == 'popularItem'){
		include('recommend/popularItem.php');
		$pI = new PI();
		//sleep(5);
		echo $pI->getPI();
	} else if(post('type') && $_POST['type'] == 'recommend'){
		if(isLogin()){
			include('recommend/recommend.php');
			$rcd = new RCD($_SESSION['cname']);
			echo $rcd->getRCD();
		} else {
			echo "";
		}
	} else if(post('type') && $_POST['type'] == 'end'){
		include('end.php');
	} else {
		echo '10';
	}
} else if (request() =='GET'){
	if (get('type') && $_GET['type']=='exit'){
		$_SESSION = array();
		echo 'exit';
	} else if(get('q')){
		include('./home/search.php');
	} else if(get('type') && $_GET['type'] == 'detail'){
		include('./home/goodsDetail.php');
	} else if(get('type') && $_GET['type'] == 'myubuy'){
		include('./home/orderMana.php');
	} else {
		include('./home/index.php');
		//include('./home/html/index.html');
		//showLogin();
	}
} else {
	echo '非法请求';
}





function request(){
	return $_SERVER['REQUEST_METHOD'];
}
function post($s){
	return array_key_exists($s,$_POST);
}
function get($s){
	return array_key_exists($s,$_GET);
}
function isLogin(){
	return isset($_SESSION['cname']) && isset($_SESSION['cid']);
}
function showLogin(){
	if (isLogin()){/*判断是否登录*/
		echo "<script>$('#a1').replaceWith('<a>欢迎来到ubuy！</a><a class=".'"cname" href="/web/myubuy.php?item=basicdata">'.$_SESSION['cname']."</a>');</script>";
		echo "<script>$('#a2').replaceWith('<a href=".'""'.' id="exit"'.">退出登录</a>');</script>";
	} else {
		echo "<script>$('#a1').replaceWith('<a href=".'""'."class=".'"login"'.">登陆</a>');</script>";
		echo "<script>$('#a2').replaceWith('<a href=".'"/web/register.html?redirectURL=/web/index.php"'.'class="'.'regisiter"'.">注册</a>');</script>";
	}
}