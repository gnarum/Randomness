#!/bin/bash

export PATH=$PATH:/root/.Scripts:/root/.bin
alias ls='ls --color=auto'
alias dir='dir --color=auto'
alias vdir='vdir --color=auto'
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'
alias diff='diff --color=auto'
alias ip='ip --color=auto'
alias oscp='openvpn /root/OS-548530-PWK.ovpn'
alias dirs='function _dirs(){ dirsearch -u $1 w /usr/share/seclists/Web-Content/directory-list-2.3-big.txt;} ;_dirs'
alias start-script='script --log-io `date +%F_%T`_log.txt'
alias get-sploits='function _get-sploits(){ for e in $(searchsploit $@ -w -t | grep http | cut -f 2 -d "|"); do exp_name=$(echo $e | cut -d "/" -f 5) && url=$(echo $e | sed 's/exploits/raw/') && wget -q --no-check-certificate $url -O $exp_name; done; }; _get-sploits'
# some more ls aliases
alias ll='ls -l'
alias la='ls -A'
alias l='ls -CF'
