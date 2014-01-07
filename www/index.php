<?php
/**
 *  PPServ index.php
 *  @author zhulin3141@gmail.com
 */

$configFile = '../conf/conf.json';
$config = (preg_replace('#(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|([\s\t](//).*)#','',file_get_contents($configFile)));
$config = json_decode($config);

$moduleStr = $projectStr = '';

foreach (array_keys((array)$config->module) as $name) {
    $moduleStr .= "<dd>$name</dd>";
}

$projectIgnore = array ('.','..');
$handle = opendir(".");
while ($file = readdir($handle)) {
    if (is_dir($file) && !in_array($file, $projectIgnore)) {
        $projectStr .= '<dd><a href="'.$file.'">'.$file.'</a></dd>';
    }
}
closedir($handle);
$content = <<< PAGE
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>PPServ</title>
<style type="text/css">
  *{margin: 0; padding: 0;}
  h2{margin: 0.8em 0 0 0;}
  a{color: #69C; text-decoration: none;}
  dl{padding-left: 1em;}
  body {margin: 1em 10%; padding: 1em 3em; font: 80%/1.4 tahoma, arial, sans-serif; border: 1px solid #999;}
  #footer{margin: 3em 10% 3px 10%; text-align: center;}
</style>
</head>
<body>
  <h1>PPServ</h1>
  <hr/>
  <h2>Module</h2>
  <dl>
      $moduleStr
  </dl>
  <h2>Project</h2>
  <dl>
      $projectStr
  </dl>
  <p id="footer">
      <a href="https://github.com/zhulin3141/PPServ">PPServ</a>
  </p>
</body>
</html>
PAGE;

echo $content;
