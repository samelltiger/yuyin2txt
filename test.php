<?php
require_once "./function/common.fun.php";




ob_start();

$response = [
	'success'=> null,
	'data'   => null
];

if(isset($_FILES['audioData'])){
	$up_file = $_FILES['audioData'];
	if( $path = save_upload_file($up_file) ){

		$res = yuyin2txt($path);
		if( $res ){
			$response['success'] = 1;
			$response['data']    = $res;
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