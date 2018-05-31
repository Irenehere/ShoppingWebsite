<?php

$from = $_POST['from'];
$to = $_POST['to'];

//$from = 'm00001';
//$to = 'c00001';


$query = "
	select chatid, [from], chatRecord from chat 
	where [from] in ('$from','$to') and [to] in ('$from','$to') and [time] > (getdate()-3) 
	order by time asc";
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
	$stmt = sqlsrv_query($conn,$query);
	if ($stmt === false) { #查询出错控制
		echo "error";
		die(sqlsrv_close($conn));
	} else { #查询成功处理
		$jsons = Array();
		while ($row = sqlsrv_fetch_array($stmt,SQLSRV_FETCH_ASSOC)){
			if ($row['from'] == $from){
				$row['type'] = 'other';
			} else {
				$row['type'] = 'me';
			}
			unset($row['from']);
			unset($row['to']);
			array_push($jsons, $row);
		}
		print json_encode($jsons);
	}
	if ($conn){
		sqlsrv_close($conn);
	}
}
?>
