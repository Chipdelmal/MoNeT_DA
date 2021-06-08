#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import path
import compress_pickle as pkl
import QLD_aux as aux

def landSelector(USR, LND):
    pth = aux.selectGeoPath(USR)
    if(LND=='02'):
        pts = pkl.load(path.join(pth, 'CLS_02.bz'))
    elif(LND=='10'):
        pts = pkl.load(path.join(pth, 'CLS_10.bz'))
    elif(LND=='01'):
        pts = pkl.load(path.join(pth, 'CLS_01.bz'))
    return pts['groups']

