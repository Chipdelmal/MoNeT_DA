#!/bin/bash

PTH=$1 # '/Users/sanchez.hmsc/Desktop/QLD/year4/'

inkscape --export-type=png --export-dpi=250 "${PTH}QLD_panel_1e-06.svg" --export-filename="${PTH}1e-06"
inkscape --export-type=png --export-dpi=250 "${PTH}QLD_panel_1e-07.svg" --export-filename="${PTH}1e-07"
inkscape --export-type=png --export-dpi=250 "${PTH}QLD_panel_1e-08.svg" --export-filename="${PTH}1e-08"
inkscape --export-type=png --export-dpi=250 "${PTH}QLD_panel_1e-09.svg" --export-filename="${PTH}1e-09"
inkscape --export-type=png --export-dpi=250 "${PTH}QLD_panel_1e-10.svg" --export-filename="${PTH}1e-10"