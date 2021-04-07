#!/bin/bash

if [ "$1" = "ASD" ] || [ "$1" = "XSD" ] || [ "$1" = "YSD" ]; then
	aType="homing"
fi
if [ "$1" = "AXS" ] || [ "$1" = "YXS" ] || [ "$1" = "CRS" ]; then
	aType="shredder"
fi
echo $aType