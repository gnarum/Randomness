#!/bin/bash

nikto

## ESTSABLISH DIFF LISTS between the different sizes so that words are not repeated.
ffuf small (directories)
gobuster medium (files)
grep for wp in the output
wpscan
ffuf medium
gobuster medium
ffuf large
gobuster large

