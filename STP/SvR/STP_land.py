#!/usr/bin/python
# -*- coding: utf-8 -*-

import compress_pickle as pkl


def landSelector(land, REL, PT_ROT):
    if land == 'SPA':
        if REL == '265':
            pth = ''.join(PT_ROT.split('/'+REL)).replace('/sim/', '')
            STP = pkl.load(pth+ '/GEO/cluster_1/clusters.bz')
        elif REL == '505':
            pth = ''.join(PT_ROT.split('/'+REL)).replace('/sim/', '')
            STP = pkl.load(pth+ '/GEO/regular/clusters.bz')
        elif REL == '106':
            pth = ''.join(PT_ROT.split('/'+REL)).replace('/sim/', '')
            STP = pkl.load(pth+ '/GEO/cluster_1/clusters.bz')
        return STP
    else:
        PAN = ([0], )
        return PAN
