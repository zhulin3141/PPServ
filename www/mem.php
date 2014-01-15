<?php
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
