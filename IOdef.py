#!/usr/bin/python
# -*- coding: utf-8 -*-
def IOdef():
    IOVariables={
    'b_P1_DO': {'Value': 0, 'IOdevice': 2048, 'IOadress': 1, 'Comment': 'Radiator cirk pumpen'},
    'b_SV_OPEN_DO': {'Value': 0, 'IOdevice': 2048, 'IOadress': 2, 'Comment': 'Open heating valve'},
    'b_SV_CLOSE_DO': {'Value': 0, 'IOdevice': 2048, 'IOadress': 3, 'Comment': 'Close heating valve'},
    'b_P2_DO': {'Value': 0, 'IOdevice': 2048, 'IOadress': 4, 'Comment': 'Sunwarming cirk pump'},
    'b_Test': {'Value': 0, 'IOdevice': 2048, 'IOadress': 5, 'Comment': 'Test var'},
    }
    return IOVariables

