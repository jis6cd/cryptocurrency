#!/bin/bash

case "$1" in
    name) echo "Gimli Buck"
	  #no additional parameters
	  ;;
    genesis) python3 cmoney.py genesis block_0.txt
	     #no additional parameters
	     ;;
    generate) python3 cmoney.py generate $2
	      #no additional parameters
	      ;;
    address) python3 cmoney.py address $2
	     ;;
    fund) python3 cmoney.py fund $2 $3 $4
	  ;;
    transfer) python3 cmoney.py transfer $2 $3 $4 $5
	      ;;
    balance) python3 cmoney.py balance $2
	     ;;
    verify) python3 cmoney.py verify $2 $3
	    ;;
    createblock) python3 cmoney.py createblock
		 ;;
    validate) python3 cmoney.py validate
	      ;;
    *) echo Unknown function: $1
       ;;
esac
