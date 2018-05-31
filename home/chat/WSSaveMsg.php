<?php

$chatid = $_POST['chatid'];
$from = $_POST['from'];
$to = $_POST['to'];
$chatRecord = $_POST['content'];
/*
$chatid = '123qweasd';
$from = 'tfs';
$to = 'dsd';
$chatRecord = 'dsdsdsdsd';
*/
$query = "insert into chat values('$chatid','$from','$to','$chatRecord',CONVERT(varchar, getdate(),21),'0')";

$serverName = "127.0.0.1\EXPRESS"; #serverName\instanceName
$userName = "sa";
$password = "123qwe";
$database = "shop";

$connectionInfo = array("Database"=>$database,"UID"=>$userName, "PWD"=>$password,"CharacterSet"=>"UTF-8");
$conn = sqlsrv_connect( $serverName, $connectionInfo);
if ($conn === false) { #连接出错控制
	print "failed";
	die();
} else {
	$stmt = sqlsrv_query($conn,$query);
	if ($stmt === false) { #查询出错控制
		echo "failed";
	} else {
		print "success";
	}
	if ($conn){
		sqlsrv_close($conn);
	}
}

?>