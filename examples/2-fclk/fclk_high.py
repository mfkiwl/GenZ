#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
from zynq7000 import *

z7000_ps_param_fclk_on = {
    'freq'  : { 'crystal'  : 33.333333333,
                'fclk0'    : 50,
                'fclk1'    : 250,
                'fclk2'    : 300,
                'fclk3'    : 400
               }
    }

if __name__ == '__main__':
    z7 = Zynq7000()
    z7.param_load(z7000_ps_param_fclk_on)
    z7.ps7_init_gen(zynq7_allregisters)
    z7.ps7_init_filewrite('./ps7_init_fclk_high/')
