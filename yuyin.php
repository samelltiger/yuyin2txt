<?php 
// silk是webm格式通过base64编码后的结果，我们解码后需要将webm转换成pcm、wav

// file_put_contents('./upload/bbb.silk',base64_decode(file_get_contents('./upload/aaa.mp3')));


require_once "./function/common.fun.php";

// yuyin2txt('./upload/CqVnQXmlrW.mp3');
// echo dirname("/Applications/MAMP/htdocs/yuyin2txt/function/common.fun.php");
// echo dirname(dirname("/Applications/MAMP/htdocs/yuyin2txt/function/common.fun.php"));
// echo "<br>".$BASE_DIR;
echo exec('whoami');
?>