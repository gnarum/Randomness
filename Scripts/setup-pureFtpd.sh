#!/bin/bash
apt install -y pure-ftpd
groupadd ftpgroup
useradd -g ftpgroup -d /dev/null -s /etc ftpuser
pure-pw useradd offsec -u ftpuser -d /opt/ftphome
pure-pw mkdb
cd /etc/pure-ftpd/auth/
ln -s ../conf/PureDB 60pdb
mkdir -p /opt/ftphome
chown -R ftpuser:ftpgroup /opt/ftphome/
systemctl restart pure-ftpd
