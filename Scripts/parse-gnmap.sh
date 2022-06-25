#!/bin/bash

[ "$#" == 2 ] && grep open $1 | awk '{print $2}' | sort -n | uniq > $2 || echo 'Usage: $0 <input gnmap filename> <output ip list filename>'
