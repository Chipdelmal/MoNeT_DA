#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import path
import compress_pickle as pkl
import EPI_aux as aux


def landSelector(LND, USR='lab'):
    if (LND=='PAN'):
        PAN = ([0], )
        return PAN
    else:
        PAN = ([0], )
        return PAN


def landRelSelector(LND):
    if LND=='PAN':
        relStart = 5
    else:
        relStart = 100
    return relStart
