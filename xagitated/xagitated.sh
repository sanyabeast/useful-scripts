#!/bin/bash
SCRIPT=$(readlink -f $0)
SCRIPT_DIR=`dirname $SCRIPT`
sleep 2
python3 "$SCRIPT_DIR/xagitated.py"