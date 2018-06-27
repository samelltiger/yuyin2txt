<?php
set_time_limit(0);
$json = file_get_contents('http://localhost:8080/index?type=job');
$json = file_get_contents('http://localhost:8080/index?type=farm');
echo $json;

?>