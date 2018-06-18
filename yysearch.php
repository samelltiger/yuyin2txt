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

if(isset($_FILES['audioData'])){
	$up_file = $_FILES['audioData'];
	if( $path = save_upload_file($up_file) ){

		$res = yuyin2txt($path);
		// print_r($res[0]);
		if( $res ){
			$res_json = file_get_contents('http://localhost:8080/search?keywords='.urlencode($res[0]).'&type='.$type) ;
			$res = json_decode($res_json,true);
			if(isset($res['success'])&&$res['success']===1){
				$response['success'] = 1;
			}else{
				$response['success'] = 0;
			}
			$response['data']    = $res['data'];
		}else{
			$response['success'] = 0;
			$response['data']    = '识别失败！';
		}
	}else{
		$response['success'] = 0;
		$response['data']    = '未知错误！';
	}
}else{
		$response['success'] = 0;
		$response['data']    = '您没有传送任何数据！';
}

exit(json_encode($response ));

?>