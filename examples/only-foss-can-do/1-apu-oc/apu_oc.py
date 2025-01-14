#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
from zynq7000 import *

z7000_ps_param_50 = {
    'freq'  : { 'crystal'  : 33.333333333,
                'apu'      : 50.0
               }
    }
z7000_ps_param_667 = {
    'freq'  : { 'crystal'  : 33.333333333,
                'apu'      : 667.0
               }
    }
z7000_ps_param_900 = {
    'freq'  : { 'crystal'  : 33.333333333,
                'apu'      : 900.0
               }
    }
z7000_ps_param_1200 = {
    'freq'  : { 'crystal'  : 33.333333333,
                'apu'      : 1200.0
               }
    }

if __name__ == '__main__':
    z7 = Zynq7000()
    z7.param_load(z7000_ps_param_667)
    z7.ps7_init_gen(zynq7_allregisters)
    z7.ps7_init_filewrite('./ps7_init_apu_oc/')
