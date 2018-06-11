<?php
require_once "./function/common.fun.php";




if(isset($_FILES['audioData'])){
	$up_file = $_FILES['audioData'];
	if( $path = save_upload_file($up_file) ){
		exit(('文件保存在：'.$path));
	}else{
		exit('保存失败！');
	}
}else{
	echo '没有任何数据！';
}
print_r($_FILES);
?>