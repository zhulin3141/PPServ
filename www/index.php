<?php
/**
 *  PPServ index.php
 *  @author zhulin3141@gmail.com
 */


$configFile = '../conf/conf.json';
$config = (preg_replace('#(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|([\s\t](//).*)#','',file_get_contents($configFile)));
$config = json_decode($config);

$act = isset($_GET['act']) ? $_GET['act'] : '';
if($act == 'phpinfo'){
  phpinfo();
}else if($act == 'mem'){
  mem_status();
}else{
  default_page();
}

function default_page()
{
  global $config;
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
    <h2>Tools</h2>
    <dl>
        <dd><a href='/?act=phpinfo'>phpinfo</a></dd>
    </dl>
    <dl>
        <dd><a href='/?act=mem'>Memcache status</a></dd>
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
}

function mem_status()
{
  $mem = new Memcache;
  $host = "127.0.0.1";
  $port = 11211;
  $mem->connect($host, $port);

  print "<table style='border: 1px solid #D9D9D9;'>";
  print "<thead><th>Memcache Status</th></thead>";
  foreach($mem->getstats() as $key=>$value)
      print "<tr><td style='background: #E3E3F1;'>$key</td> <td>$value</td></tr>\n";
  print "</table>";

  print "<p>";
  $mem->set('test', 'This is a test value', 0, 60);
  print $mem->get('test');
  print "</p>";

  $mem->flush();
}
