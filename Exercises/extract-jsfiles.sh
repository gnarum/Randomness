#!/bin/bash

[ -e $1 ] && cat $1 | awk '{print $7}' | grep -o -E '[a-zA-Z0-9\.]+\.js$' | sort | uniq || echo 'Usage:  $0 <filename>'
