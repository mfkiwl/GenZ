#!/usr/bin/env python3
from register_names import *

class Clock:
    def __init__(self, requested, lower, upper, oc=0, source='default'):
        self.requested = requested
        self.actual = 0
        self.lower = lower
        self.upper = upper
        self.oc = oc
        self.source = source

# UG585, Page 744
# PLL frequency control settings
# PLL_FDIV (multipler) L/H, PLL CP, PLL RES, LOCK CNT
def get_pll_cp_res_cnt(fdiv):
    for entry in [[13, 13, 2, 6 , 750],
                [14, 14, 2, 6 , 700],
                [15, 15, 2, 6 , 650],
                [16, 16, 2, 10, 625],
                [17, 17, 2, 10, 575],
                [18, 18, 2, 10, 550],
                [19, 19, 2, 10, 525],
                [20, 20, 2, 12, 500],
                [21, 21, 2, 12, 475],
                [22, 22, 2, 12, 450],
                [23, 23, 2, 12, 425],
                [24, 25, 2, 12, 400],
                [26, 26, 2, 12, 375],
                [27, 28, 2, 12, 350],
                [29, 30, 2, 12, 325],
                [31, 33, 2, 2 , 300],
                [34, 36, 2, 2 , 275],
                [37, 40, 2, 2 , 250],
                [41, 47, 3, 12, 250],
                [48, 66, 2, 4 , 250]]:
        if fdiv >= entry[0] and fdiv <= entry[1]:
            return (entry[2], entry[3], entry[4])
    print("FDIV", fdiv, "invalid!")
    return (-1, -1, -1)

class Zynq7000:
    def __init__(self):
        self.CRYSTAL_FREQ = Clock(33.333333, 30, 60)
        self.APU_FREQ = Clock(666.666666, 50, 667, oc=1)
        self.APU_CLK_RATIO = '6:2:1' # or 4:2:1
        self.DDR_FREQ = Clock(533.333333, 200, 534, oc=1)
        self.FCLK0_FREQ = Clock(50, 0.1, 250)
        self.FCLK1_FREQ = Clock(50, 0.1, 250)
        self.FCLK2_FREQ = Clock('disable', 0.1, 250)
        self.FCLK3_FREQ = Clock('disable', 0.1, 250)
        self.PCAP_FREQ = Clock('auto', 10, 200)
        self.UART_FREQ = Clock('auto', 10, 100)

        pass
        self.CAN_FREQ = Clock('auto', 0.1, 100)
        self.SDIO_FREQ = Clock('auto', 10, 125)
        self.QSPI_FREQ = Clock('auto', 10, 200)
        self.ENET0_FREQ = Clock('disable', 0.1, 125)
        self.ENET1_FREQ = Clock('disable', 0.1, 125)
        self.DCI_FREQ = Clock('auto', 0.1, 177) # digital controlled impedance, for DDR PHY calibration
    def ps7_init_gen(self, zar):
        # 5 arrays of init date required for ZYNQ7
        pll = PS7_InitData('pll')
        clock = PS7_InitData('clock')
        mio = PS7_InitData('mio')
        peripherals = PS7_InitData('peripherals')
        ddr = PS7_InitData('ddr')

        # PLL, Input crystal is fed into 3 PLLs and multipled: ARM, DDR, and IO
        # Then, the 3 PLLs divided and generate all the clocks
        # frequency multiplers are set here
        # Procedures are the same -- set params, reset, wait for lock, set derived info
        pll.add(zar, 'slcr', 'slcr_unlock', 'unlock_key', unlock_key)
        # ARM PLL
        pll.add(zar, 'slcr', 'arm_pll_cfg', 'pll_res', -1)
        pll.add(zar, 'slcr', 'arm_pll_cfg', 'pll_cp', -1)
        pll.add(zar, 'slcr', 'arm_pll_cfg', 'lock_cnt', -1)
        pll.add(zar, 'slcr', 'arm_pll_ctrl', 'pll_fdiv', -1)
        pll.add(zar, 'slcr', 'arm_pll_ctrl', 'pll_bypass_force', 1)
        pll.add(zar, 'slcr', 'arm_pll_ctrl', 'pll_reset', 1)
        pll.add(zar, 'slcr', 'arm_pll_ctrl', 'pll_reset', 0)
        pll.add(zar, 'slcr', 'pll_status', 'arm_pll_lock', 1, poll=1)
        pll.add(zar, 'slcr', 'arm_pll_ctrl', 'pll_bypass_force', 0)
        pll.add(zar, 'slcr', 'arm_clk_ctrl', 'srcsel', -1)
        pll.add(zar, 'slcr', 'arm_clk_ctrl', 'divisor', -1)
        pll.add(zar, 'slcr', 'arm_clk_ctrl', 'cpu_6or4xclkact', 1)
        pll.add(zar, 'slcr', 'arm_clk_ctrl', 'cpu_3or2xclkact', 1)
        pll.add(zar, 'slcr', 'arm_clk_ctrl', 'cpu_1xclkact', 1)
        pll.add(zar, 'slcr', 'arm_clk_ctrl', 'cpu_peri_clkact', 1)
        # DDR PLL
        pll.add(zar, 'slcr', 'ddr_pll_cfg', 'pll_res', -1)
        pll.add(zar, 'slcr', 'ddr_pll_cfg', 'pll_cp', -1)
        pll.add(zar, 'slcr', 'ddr_pll_cfg', 'lock_cnt', -1)
        pll.add(zar, 'slcr', 'ddr_pll_ctrl', 'pll_fdiv', -1)
        pll.add(zar, 'slcr', 'ddr_pll_ctrl', 'pll_bypass_force', 1)
        pll.add(zar, 'slcr', 'ddr_pll_ctrl', 'pll_reset', 1)
        pll.add(zar, 'slcr', 'ddr_pll_ctrl', 'pll_reset', 0)
        pll.add(zar, 'slcr', 'pll_status', 'ddr_pll_lock', 1, poll=1)
        pll.add(zar, 'slcr', 'ddr_pll_ctrl', 'pll_bypass_force', 0)
        pll.add(zar, 'slcr', 'ddr_clk_ctrl', 'ddr_3xclkact', 1)
        pll.add(zar, 'slcr', 'ddr_clk_ctrl', 'ddr_2xclkact', 1)
        pll.add(zar, 'slcr', 'ddr_clk_ctrl', 'ddr_3xclk_divisor', -1)
        pll.add(zar, 'slcr', 'ddr_clk_ctrl', 'ddr_2xclk_divisor', -1)
        # IO PLL
        pll.add(zar, 'slcr', 'io_pll_cfg', 'pll_res', -1)
        pll.add(zar, 'slcr', 'io_pll_cfg', 'pll_cp', -1)
        pll.add(zar, 'slcr', 'io_pll_cfg', 'lock_cnt', -1)
        pll.add(zar, 'slcr', 'io_pll_ctrl', 'pll_fdiv', -1)
        pll.add(zar, 'slcr', 'io_pll_ctrl', 'pll_bypass_force', 1)
        pll.add(zar, 'slcr', 'io_pll_ctrl', 'pll_reset', 1)
        pll.add(zar, 'slcr', 'io_pll_ctrl', 'pll_reset', 0)
        pll.add(zar, 'slcr', 'pll_status', 'io_pll_lock', 1, poll=1)
        pll.add(zar, 'slcr', 'io_pll_ctrl', 'pll_bypass_force', 0)

        pll.add(zar, 'slcr', 'slcr_lock', 'lock_key', lock_key)

        # Clock, PLL output drives various clocks, frequency divisors are set here
        clock.add(zar, 'slcr', 'slcr_unlock', 'unlock_key', unlock_key)
        clock.add(zar, 'slcr', 'clk_621_true', 'clk_621_true', 1 if self.APU_CLK_RATIO == '6:2:1' else 0)
        clock.add(zar, 'slcr', 'slcr_lock', 'lock_key', lock_key)
        print(pll.emit())

    def xparameter_h_gen(self):
        pass

if __name__ == '__main__':
    parse_ps7_init_entries_fields("./hdf/noddr-0-uart/ps7_init_gpl.c")
    z7 = Zynq7000()
    z7.ps7_init_gen(zynq7_allregisters)
