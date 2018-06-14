<?php 
require_once "./extr/speech/AipSpeech.php";
require_once './config/config.local.php';

/**
生成指定长度的随机字符串
@param  $length  生成字符长度
@param  $specialChars  是否使用特殊字符
*/
function randString($length=10, $specialChars = false) {
    $chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    if ($specialChars) {
        $chars .= '!@#$%^&*()';
    }

    $result = '';
    $max = strlen($chars) - 1;
    for ($i = 0; $i < $length; $i++) {
        $result .= $chars[rand(0, $max)];
    }
    return $result;
}

function save_upload_file($file, $save_dir='./upload')
{
	 // 取得上传文件信息
    $fileName = $file['name'];
    $fileType = $file['type'];
    $fileError = $file['error'];
    $fileSize = $file['size'];
    $tempName = $file['tmp_name'];
    
    // 定义上传文件类型
    // $typeList = array('audio/wave', 'audio/wav', 'audio/x-wav', 'audio/x-pn-wav', 'audio/mpeg', 'audio/mp3');  //定义允许的类型
    $typeList = array(
    	'wav' => ['audio/wave', 'audio/wav', 'audio/x-wav', 'audio/x-pn-wav'],
    	'mp3' => ['audio/mpeg', 'audio/mp3'],
    	'aac' => ['audio/x-aac']
	);

    if ($fileError > 0) {
            // 上传文件错误编号判断
            switch ($fileError) {
                case 1:
                    $message = "上传的文件超过了php.ini 中 upload_max_filesize 选项限制的值。"; 
                    break;
                case 2:
                    $message = "上传文件的大小超过了 HTML 表单中 MAX_FILE_SIZE 选项指定的值。"; 
                    break;
                case 3:
                    $message = "文件只有部分被上传。"; 
                    break;
                case 4:
                    $message = "没有文件被上传。";
                    break;
                case 6:
                    $message = "找不到临时文件夹。"; 
                    break;
                case 7:
                    $message = "文件写入失败"; 
                    break;
                case 8:
                    $message = "由于PHP的扩展程序中断了文件上传";
                    break;
            }
            exit("文件上传失败：".$message);
    }
    if (!is_uploaded_file($tempName)) {
        exit("不是通过HTTP POST方式上传上来的");
    }
    $extr_name = null;
    foreach ($typeList as $key => $value) {
    	if( in_array( $fileType, $value ) ){
    		$extr_name = $key;
    	}
    }
   
    if ($fileSize > 100000) {
        exit("上传文件超出限制大小");                                 // 对特定表单的上传文件限制大小
    } else {
    	if( !file_exists($save_dir) ){
    		mkdir($save_dir);
    		chmod($save_dir,0777);
    	}
        $fileName = $save_dir.'/'.randString().'.'.$extr_name;
        if (move_uploaded_file($tempName, $fileName)) {
            return $fileName;
        } else {
            return false;
        }
    }

}



// 转换音频格式到允许的格式
function convert_to_allow($path, $to= 'wav')
{
    global $BASE_DIR;

    $path = ltrim($path,'.');
    $extra  = explode('.', $path);
    $extra_name  = array_pop( $extra );
    $all_name = join( '.', $extra );

    // 如果现在的扩展名与转换后扩展名一样，则直接返回
    if( $extra_name && $extra_name === $to ){
        return $path;
    }

    $new_name = $BASE_DIR.$all_name.'.'.$to;
    if( file_exists( $new_name ) ){
        $new_name = $BASE_DIR.$all_name.randString(6).'.'.$to;
    }
    $cmd_templat = '%s -y -i %s %s 2>&1';
    $cmd = sprintf( $cmd_templat, FFMPEG_DIR, $BASE_DIR.$path, $new_name );
    $info = null;
    $status = null;
    exec($cmd, $info, $status);
    sleep(1);

    print_r($status);
    echo 'new_name is: '.$new_name;
    chmod($new_name, 0777);
    // echo $cmd;die;
    if ( $status == 0 ) {
        return $new_name;
    }

	return false;
}

function yuyin2txt($path)
{

    if(!file_exists($path)){
        return false;
    }
    $new_file = convert_to_allow($path);
    if( !$new_file ){
        return false;
    }
	// 创建客户端对象
	$client = new AipSpeech(APP_ID, API_KEY, SECRET_KEY);
    $extra  = explode('.', $new_file);
    $extra  = end( $extra );
    echo  $extra;
	

    // 识别本地文件
    $res_json = $client->asr( file_get_contents($new_file), $extra, 16000, array(
        'dev_pid' => 1536,
    )) ;

    print_r($res_json);
    // print_r($res_json['result']);

}

 ?>