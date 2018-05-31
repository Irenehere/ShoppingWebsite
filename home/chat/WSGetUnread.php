<?php

$from = $_POST['from'];
$to = $_POST['to'];


#获取未读
$query = "select chatid, chatRecord, time from chat where [from]='$from' and [to]='$to' and chatState = '0' order by time asc";
$serverName = "127.0.0.1\EXPRESS"; #serverName\instanceName
$userName = "sa";
$password = "123qwe";
$database = "shop";

$connectionInfo = array("Database"=>$database,"UID"=>$userName, "PWD"=>$password,"CharacterSet"=>"UTF-8");
$conn = sqlsrv_connect( $serverName, $connectionInfo);
if ($conn === false) { #连接出错控制
	echo "conn_error";
	die();
} else {
	if (sqlsrv_begin_transaction($conn) === false){ //开启事务
		print "error";
		die(sqlsrv_close($conn));
	}
	$stmt = sqlsrv_query($conn,$query);
	if ($stmt === false) { #查询出错控制
		echo "error";
		die(sqlsrv_close($conn));
	} else { #查询成功处理
		$jsons = Array();
		while ($row = sqlsrv_fetch_array($stmt,SQLSRV_FETCH_ASSOC)){
			$row['type'] = 'other';
			array_push($jsons, $row);
		}
		$js = json_encode($jsons);
		$chatids = "'s'";
		for($i = 0; $i < count($jsons); $i++){
			$chatids = $chatids." ,'".$jsons[$i]['chatid']."'";
		}
		$query = "update chat set chatstate = '1' where chatid in ($chatids)";
		$stmt = sqlsrv_query($conn,$query);
		if ($stmt === false){
			sqlsrv_rollback( $conn);
			die(sqlsrv_close($conn));
			print '[]';
		} else {
			sqlsrv_commit($conn);
			print $js;
		}
	}
	if ($conn){
		sqlsrv_close($conn);
	}
}
?>
