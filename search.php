<?php
require_once "./function/common.fun.php";

ob_start();

$response = [
	'success'=> null,
	'data'   => null
];

$type = isset($_GET['type'])?$_GET['type']:false ;
if( !in_array($type, array('job','farm')) ){
	exit(json_encode(['success'=>0, 'data'=> '参数错误!'] ));
}

$kw = isset($_GET['kw'])?$_GET['kw']:false ;
if( $kw ){
	$res_json = file_get_contents('http://localhost:8080/search?keywords='.urlencode($kw).'&type='.$type);
	$res = json_decode($res_json,true);
	if(isset($res['success']) && $res['success']===1){
		$response['success'] = 1;
	}else{
		$response['success'] = 0;
	}
	$response['data']    = $res['data'];
}else{
	$response['success'] = 0;
	$response['data']    = '非法参数！';

}

exit(json_encode($response));
?>