<?php
require_once "./speech/AipSpeech.php";
require_once './config/config.local.php';

// 创建客户端对象
$client = new AipSpeech(APP_ID, API_KEY, SECRET_KEY);

echo "<pre>";
// 识别本地文件
$res_json = $client->asr(file_get_contents('16k.pcm'), 'pcm', 16000, array(
    'dev_pid' => 1536,
)) ;

print_r($res_json);
  ?>