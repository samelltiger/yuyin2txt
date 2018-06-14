<?php
require_once "./function/common.fun.php";




ob_start();


if(isset($_FILES['audioData'])){
	$up_file = $_FILES['audioData'];
	if( $path = save_upload_file($up_file) ){

		$res = yuyin2txt($path);
		if( $res ){
			print_r($res);
		}else{
			echo '识别失败！';
		}

		$content = ob_get_contents();
		ob_clean();
		exit(json_encode(['result'=> $content ]));
	}else{
		exit(json_encode(['result'=>'保存失败！']));
	}
}else{
		exit(json_encode(['result'=>'没有任何数据！']));
}
?>