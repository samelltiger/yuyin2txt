<?php
require_once "./function/common.fun.php";




ob_start();

// print_r($_FILES);

		// wxupload();

// print_r($arr);
// $content = ob_get_contents();

// ob_clean();
// exit(json_encode(['result'=> $content ]));


if(isset($_FILES['audioData'])){
	$up_file = $_FILES['audioData'];
	if( $path = save_upload_file($up_file) ){
		// exit(json_encode(['result'=>'文件保存在：'.$path]));
		$res = yuyin2txt($path);
		$content = ob_get_contents();

		ob_clean();
		exit(json_encode(['result'=> $content.$res ]));
	}else{
		exit(json_encode(['result'=>'保存失败！']));
	}
}else{
		exit(json_encode(['result'=>'没有任何数据！']));
}
?>