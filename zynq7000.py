#!/usr/bin/env python3
from zynq7000_register_names import *
# from pathlib import Path
import os
import math

# This file handles the real, detailed configuration of a PS7
# User provides a z7000_ps_param_demo configuring all the peripherals used and parameters (zynq7000_user.py),
# the Zynq7000 class derives all ps7_init register writes, and BSP files

# The ps7_init is usually made of the following parts:
# pll, clock: for all the clocks and frequencies.
#  This is tedious as each peripheral has their own frequency values and ranges, and clock sources
# mio: for each MIO pins used
# peripherals: for register configuration of each peripheral, like UART at 0xe0000000/0xe0000100
# ddr: DDR3, unsupported yet
# post_config: some fixed sequences (PS-to-PL level shifter, etc, not user-visible). Called separately

class Clock:
    def __init__(self, name, requested, lower, upper,
                 oc=0, auto=0, source='default', disable=0, has_div1=0, tolerance=1):
        self.name = name
        self.freq = requested
        self.actual = 0
        self.lower = lower
        self.upper = upper
        self.oc = oc # allow overclocking
        self.auto = auto # allow any frequency in range
        self.source = source
        self.disable = disable
        self.div0 = -1
        self.div1 = -1
        self.has_div1 = has_div1
        self.tolerance = tolerance # weight when doing optmization

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
    print("FDIV (PLL multiplier)", fdiv, "invalid!")
    return (-1, -1, -1)
# Peripheral configuration and MIO configuration is kind separated
# Peripherals can be without MIO pins -- will be accessible only to EMIO then
# EMIO GPIO and peripherals are seen as always enabled
# mios_defaults = {'TRI_ENABLE': disable,
                 # 'Speed': slow,
                 # 'IO_Type': lvcmos33,
                 # 'PULLUP': enable,
                 # 'DisableRcvr': disable}
# Boot Mode MIO pins, pullup is not available. 
mios_nopullup = [2, 3, 4, 5, 6, 7, 8]
# Eyecandies...
_=0
x=''
# some user-friendly macros
unlock_key = 0xdf0d
lock_key = 0x767b
enable = 1
disable = 0
assert_ = 1
deassert = 0
# PLL selection for APU
ARM_ARM_PLL = 0b00
ARM_DDR_PLL = 0b10
ARM_IO_PLL = 0b11
# PLL selection for IO
IO_IO_PLL = 0b00
IO_ARM_PLL = 0b10
IO_DDR_PLL = 0b11
# MIO IO type
lvcmos18 = 0b001
lvcmos25 = 0b010
lvcmos33 = 0b011
hstl = 0b100
slow = 0
fast = 1

# Return L0_SEL, L1_SEL, L2_SEL, L3_SEL
def z7000_ps_param_L_sel(arr):
    idx = arr.index(next(filter(lambda x: x!='', arr)))
    idx_arr = [[0b1, 0b0, 0b00, 0b000],
               [0b0, 0b1, 0b00, 0b000],
               [0b0, 0b0, 0b01, 0b000],
               [0b0, 0b0, 0b10, 0b000],
               [0b0, 0b0, 0b11, 0b000],
               [0b0, 0b0, 0b00, 0b000],
               [0b0, 0b0, 0b00, 0b001],
               [0b0, 0b0, 0b00, 0b010],
               [0b0, 0b0, 0b00, 0b011],
               [0b0, 0b0, 0b00, 0b100],
               [0b0, 0b0, 0b00, 0b101],
               [0b0, 0b0, 0b00, 0b110],
               [0b0, 0b0, 0b00, 0b111]]
    return idx_arr[idx]

# input: input frequency, output frequecy, multiplier range, divisor0 range, divisor1 range
# output: mul, div0, div1, frequency diff in percentage
# ordinary calc: returns mul, div, abs deviation
# in range only: fin should be (requested, fmin, fmax) returns mul, div, freq (-1 for impossible), dev (from requested freq)
# prioritize multiplier in order as specified in mulrange
# Unit: MHz
def calc_pll_muldiv(fin, fout, mulrange, div0range, div1range,
                    freq_range=(0, 9e9), pll_range=(900, 1600),
                    opt='mul', tolerance=1):
    # print(freq_range)
    fin = fin # this controls our accuracy!
    fout = fout
    drange = []
    for d0 in div0range:
        for d1 in div1range:
            drange.append(d0 * d1)
    # if not optdiv: # don't need sort actually, just repeat...
        # drange = list(set(drange)) # automatically sorted
    # print(mulrange)
    # print(drange)
    mbest = -1
    dbest = -1
    devmin = 9e9
    if opt == 'div':
        for d in drange:
            devsmall = 9e9
            mgood = -1
            for m in mulrange:
                if not in_range(fin*m, pll_range):
                    continue
                f = fin * m / d
                dev = abs(f - fout) / fout
                if dev < devsmall and in_range(f, freq_range):
                    devsmall = dev
                    mgood = m
            if devsmall < devmin:
                devmin = devsmall
                dbest = d
                mbest = mgood
    elif opt == 'mul':
        for m in mulrange:
            if not in_range(fin*m, pll_range):
                continue
            devsmall = 9e9
            dgood = -1
            for d in drange:
                f = fin * m / d
                dev = abs(f - fout) / fout
                if dev < devsmall and in_range(f, freq_range):
                    devsmall = dev
                    dgood = d
            if devsmall < devmin:
                devmin = devsmall
                mbest = m
                dbest = dgood
    d0best = -1
    d1best = -1
    for d0 in div0range[::-1]: # prefer large d0, small d1
        for d1 in div1range:
            if d0*d1 == dbest:
                d0best = d0
                d1best = d1
                break
        if d0best != -1:
            break
    # print(fin, 'MHz ->', fout, '(', fin*mbest/(d0best*d1best) , ')MHz:', mbest, d0best, d1best, devmin)
    # in_range_only gives much more tolerance for deviation from "expected" freq
    # we don't need a special in_range_only parameter, it's done automatically
    return (mbest, d0best, d1best, devmin / tolerance)

def r_l_h(l, h):
    return [i for i in range(l, h+1)]
def in_range(f, frange):
    return f >= frange[0] and f <= frange[1]

class Zynq7000:
    def __init__(self):
        print("Zynq7000: Init default")
        # ALL DEFAULT CLOCKS AND RANGES
        self.CRYSTAL_FREQ = Clock('CRYSTAL', 33.333333333, 30, 60)
        self.APU_FREQ = Clock('APU', 666.666666, 50, 667, oc=1999) # default from ARM PLL
        self.APU_CLK_RATIO = '6:2:1' # or 4:2:1
        self.DDR_FREQ = Clock('DDR', 533.333333, 200, 534, oc=1999) # default from DDR PLL
        self.FCLK0_FREQ = Clock('FPGA0', 50, 0.1, 250, disable=1, has_div1=1, oc=999) # FCLK and peripheral default from IO PLL
        self.FCLK1_FREQ = Clock('FPGA1', 50, 0.1, 250, disable=1, has_div1=1, oc=999)
        self.FCLK2_FREQ = Clock('FPGA2', 50, 0.1, 250, disable=1, has_div1=1, oc=999)
        self.FCLK3_FREQ = Clock('FPGA3', 50, 0.1, 250, disable=1, has_div1=1, oc=999)
        # Note: some devices, like uart0/uart1, shares one Clock
        self.QSPI_FREQ = Clock('QSPI', 200, 10, 200, disable=1)
        self.SMC_FREQ = Clock('SMC', 100, 10, 100, disable=1) # static memory controller
        self.ENET0_FREQ = Clock('ENET0', 125, 0.1, 125, disable=1)
        self.ENET1_FREQ = Clock('ENET1', 125, 0.1, 125, disable=1)
        self.SDIO_FREQ = Clock('SDIO', 100, 10, 125, disable=1)
        self.SPI_FREQ = Clock('SPI', 170, 0, 200, disable=1, tolerance=100)
        self.UART_FREQ = Clock('UART', 100, 10, 100, disable=1)
        self.CAN_FREQ = Clock('CAN', 100, 0.1, 100, disable=1)
        self.PCAP_FREQ = Clock('PCAP', 200, 10, 200, tolerance=10) # processor configuration access point, for loading bitstream from PS
        self.DCI_FREQ = Clock('DCI', 10.1, 0.1, 177, has_div1=1) # digital controlled impedance, for DDR PHY calibration, default from DDR PLL

        self.pll_mul_min = 13
        self.pll_mul_max = 48
        self.pll_muldiv_min_abs = 1
        self.pll_muldiv_max_abs = 63

        self.uart0_baud = 115200
        self.uart1_baud = 115200

        self.volt_bank0 = lvcmos33
        self.volt_bank1 = lvcmos33

        self.warning_thres = 0.005 # 0.5%
        # We load param and calculate params separately, so user has chance to override
        self.param_calculated = False
        self.param = None

    # can check with e.g. uart0, uart1, uart
    def check_param_enabled(self, name):
        try:
            p = self.param[name]
            # Explicitly enabled
            return True
        except KeyError:
            pass
        try:
            p = self.param['freq'][name]
            # FCLK frequency specified
            return True
        except KeyError:
            pass
        for i in range(0, 53+1):
            mio_pin = 'MIO_PIN_%02d' % i
            try:
                if ''.join(self.param[mio_pin]).find(name) != -1:
                    # Specified in MIO
                    return True
            except KeyError:
                continue
        return False

    def param_load(self, param):
        print("Zynq7000: Param load")
        self.param = param

    def param_calc(self):
        print("Zynq7000: Param calc")

        # TODO: if this part is done in param_load, then user setting parameters seems not working (Python memory copy problem?)
        # Don't allow customizing peripheral clk freq yet

        try:
            self.volt_bank0 = self.param['volt']['bank0']
        except KeyError: pass
        try:
            self.volt_bank1 = self.param['volt']['bank1']
        except KeyError: pass

        self.UART_FREQ.disable = not self.check_param_enabled('uart')
        self.QSPI_FREQ.disable = not self.check_param_enabled('qspi')
        self.SPI_FREQ.disable = not self.check_param_enabled('spi')
        self.SDIO_FREQ.disable = not self.check_param_enabled('sd')
        try:
            self.CRYSTAL_FREQ.freq = self.param['freq']['crystal']
        except KeyError: pass
        try:
            self.APU_FREQ.freq = self.param['freq']['apu']
        except KeyError: pass
        try:
            self.DDR_FREQ.freq = self.param['freq']['ddr']
        except KeyError: pass
        if self.check_param_enabled('fclk0'):
            self.FCLK0_FREQ.disable = 0
            self.FCLK0_FREQ.freq = self.param['freq']['fclk0']
        if self.check_param_enabled('fclk1'):
            self.FCLK1_FREQ.disable = 0
            self.FCLK1_FREQ.freq = self.param['freq']['fclk1']
        if self.check_param_enabled('fclk2'):
            self.FCLK2_FREQ.disable = 0
            self.FCLK2_FREQ.freq = self.param['freq']['fclk2']
        if self.check_param_enabled('fclk3'):
            self.FCLK3_FREQ.disable = 0
            self.FCLK3_FREQ.freq = self.param['freq']['fclk3']

        xtal = self.CRYSTAL_FREQ.freq
        print("ZYNQ PS XTAL", xtal, 'MHz')
        # absolute range of divisors/multipliers
        r_l_h_abs = r_l_h(self.pll_muldiv_min_abs, self.pll_muldiv_max_abs)
        r_l_h_mut = r_l_h(self.pll_mul_min, self.pll_mul_max)

        # ARM PLL
        m, d0, d1, dev = calc_pll_muldiv(xtal, self.APU_FREQ.freq,
                        r_l_h_mut, [2] + r_l_h_abs, [1], opt='div',
                        freq_range=(self.APU_FREQ.lower, self.APU_FREQ.oc + self.APU_FREQ.upper))
        self.arm_pll_mul = m
        self.APU_FREQ.div0 = d0 # usually 2
        self.APU_FREQ.actual = xtal*m/d0
        print("ARM PLL:", xtal, '*', m, '=', xtal*m, 'MHz')
        print("\tAPU:", '/', d0, '=', self.APU_FREQ.actual, 'MHz (requested', self.APU_FREQ.freq, 'MHz)')
        if dev > self.warning_thres:
            print("\tWarning: ARM PLL deviation is large!")

        # DDR PLL
        m, d0, d1, dev = calc_pll_muldiv(xtal, self.DDR_FREQ.freq,
                        r_l_h_mut, [2], [1], opt='div', 
                        freq_range=(self.DDR_FREQ.lower, self.DDR_FREQ.oc + self.DDR_FREQ.upper))
        self.ddr_pll_mul = m
        self.DDR_FREQ.div0 = d0 # now fixed to 2
        self.DDR_FREQ.actual = xtal*m/d0
        print("DDR PLL:", xtal, '*', m, '=', xtal*m, 'MHz')
        print("\tDDR:", '/', d0, '=', self.DDR_FREQ.actual, 'MHz (requested', self.DDR_FREQ.freq, 'MHz)')
        if dev > self.warning_thres:
            print("\tWarning: DDR PLL deviation is large!")
        m, d0, d1, dev = calc_pll_muldiv(xtal, self.DCI_FREQ.freq,
                        [self.ddr_pll_mul], r_l_h_abs, r_l_h_abs, opt='div')
        self.DCI_FREQ.div0 = d0
        self.DCI_FREQ.div1 = d1
        self.DCI_FREQ.actual = xtal*m/(d0*d1)
        print("\tDCI:", '/', d0, '/', d1, '=', self.DCI_FREQ.actual, 'MHz (requested', self.DCI_FREQ.freq, 'MHz)')
        if dev > 0.1:
            print("\tWarning: DCI freq deviation is large!")
        # IO PLL
        periph_list = [self.FCLK0_FREQ, self.FCLK1_FREQ, self.FCLK2_FREQ, self.FCLK3_FREQ, 
                       self.QSPI_FREQ, self.SMC_FREQ, self.ENET0_FREQ, self.ENET1_FREQ, 
                       self.SDIO_FREQ, self.SPI_FREQ, self.UART_FREQ, self.CAN_FREQ,
                       self.PCAP_FREQ]
        # Find best IO multiplier
        dev_sum_min = 9e9
        mbest = -1
        for m in r_l_h_mut:
            dev_sum = 0
            for CLOCK in [p for p in periph_list if not p.disable]:
                x, d0, d1, dev = calc_pll_muldiv(xtal, CLOCK.freq,
                                 [m], r_l_h_abs, r_l_h_abs if CLOCK.has_div1 else [1],
                                 freq_range=(CLOCK.lower, CLOCK.oc + CLOCK.upper),
                                 tolerance=CLOCK.tolerance)
                dev_sum += dev
            if dev_sum < dev_sum_min:
                dev_sum_min = dev_sum
                mbest = m
        self.io_pll_mul = mbest
        print("IO PLL:", xtal, '*', mbest, '=', xtal*mbest, 'MHz')
        # Find each peripheral's divisor with the best m deterimined
        for CLOCK in periph_list:
            x, d0, d1, x = calc_pll_muldiv(xtal, CLOCK.freq,
                             [mbest], r_l_h_abs, r_l_h_abs if CLOCK.has_div1 else [1],
                             freq_range=(CLOCK.lower, CLOCK.oc + CLOCK.upper),
                             tolerance=CLOCK.tolerance)
            CLOCK.actual = xtal*mbest/(d0*d1)
            CLOCK.div0 = d0
            CLOCK.div1 = d1
            if not CLOCK.disable:
                print('\t', CLOCK.name, ':', '/', d0, ('/ ' + str(d1)) if CLOCK.has_div1 else '',
                      '=', CLOCK.actual, 'MHz (requested', CLOCK.freq, 'MHz)',
                      'OVERCLOCKED!' if CLOCK.actual > CLOCK.upper else '')

        # UART baud rate calc, just use PLL calc tool
        if self.check_param_enabled('uart0'):
            # print(self.UART_FREQ.actual)
            # print(self.UART_FREQ.div0)
            # print(self.UART_FREQ.div1)
            try: self.uart0_baud = self.param['uart0']['baud']
            except KeyError: pass
            # print(self.uart0_baud)
            x, self.uart0_cd, self.uart0_bdiv, dev = calc_pll_muldiv(
                    self.UART_FREQ.actual*1e6, self.uart0_baud,
                    [1], r_l_h(1, 65535), r_l_h(4+1, 255+1), pll_range=(0,9e9))
            self.uart0_bdiv -= 1
        if self.check_param_enabled('uart1'):
            try: self.uart1_baud = self.param['uart1']['baud']
            except KeyError: pass
            x, self.uart1_cd, self.uart1_bdiv, dev = calc_pll_muldiv(
                    self.UART_FREQ.actual*1e6, self.uart1_baud,
                    [1], r_l_h(1, 65535), r_l_h(4+1, 255+1), pll_range=(0,9e9))
            self.uart1_bdiv -= 1
            # print(self.uart0_cd, self.uart0_bdiv, dev)


        self.param_calculated = True

    def ps7_init_gen(self, zar):
        print("Zynq7000: ps7_init gen")
        if not self.param_calculated:
            self.param_calc()
        # 5 arrays of init date required for ZYNQ7
        pll = PS7_InitData('pll')
        clock = PS7_InitData('clock')
        mio = PS7_InitData('mio')
        peripherals = PS7_InitData('peripherals')
        ddr = PS7_InitData('ddr')
        post_config = PS7_InitData('post_config')

        # PLL, Input crystal is fed into 3 PLLs and multipled: ARM, DDR, and IO
        # Then, the 3 PLLs divided and generate all the clocks
        # frequency multiplers are set here
        # Procedures are the same -- set params, reset, wait for lock, set derived info
        pll.add(zar, 'slcr', 'slcr_unlock', 'unlock_key', unlock_key)
        # ARM PLL
        cp, res, cnt = get_pll_cp_res_cnt(self.arm_pll_mul)
        pll.add(zar, 'slcr', 'arm_pll_cfg', 'pll_res', res)
        pll.add(zar, 'slcr', 'arm_pll_cfg', 'pll_cp', cp)
        pll.add(zar, 'slcr', 'arm_pll_cfg', 'lock_cnt', cnt)
        pll.add(zar, 'slcr', 'arm_pll_ctrl', 'pll_fdiv', self.arm_pll_mul)
        pll.add(zar, 'slcr', 'arm_pll_ctrl', 'pll_bypass_force', enable)
        pll.add(zar, 'slcr', 'arm_pll_ctrl', 'pll_reset', assert_)
        pll.add(zar, 'slcr', 'arm_pll_ctrl', 'pll_reset', deassert)
        pll.add(zar, 'slcr', 'pll_status', 'arm_pll_lock', 1, poll=1)
        pll.add(zar, 'slcr', 'arm_pll_ctrl', 'pll_bypass_force', disable)
        pll.add(zar, 'slcr', 'arm_clk_ctrl', 'srcsel', ARM_ARM_PLL)
        pll.add(zar, 'slcr', 'arm_clk_ctrl', 'divisor', self.APU_FREQ.div0)
        pll.add(zar, 'slcr', 'arm_clk_ctrl', 'cpu_6or4xclkact', enable)
        pll.add(zar, 'slcr', 'arm_clk_ctrl', 'cpu_3or2xclkact', enable)
        pll.add(zar, 'slcr', 'arm_clk_ctrl', 'cpu_1xclkact', enable)
        pll.add(zar, 'slcr', 'arm_clk_ctrl', 'cpu_peri_clkact', enable)
        # DDR PLL
        cp, res, cnt = get_pll_cp_res_cnt(self.ddr_pll_mul)
        pll.add(zar, 'slcr', 'ddr_pll_cfg', 'pll_res', res)
        pll.add(zar, 'slcr', 'ddr_pll_cfg', 'pll_cp', cp)
        pll.add(zar, 'slcr', 'ddr_pll_cfg', 'lock_cnt', cnt)
        pll.add(zar, 'slcr', 'ddr_pll_ctrl', 'pll_fdiv', self.ddr_pll_mul)
        pll.add(zar, 'slcr', 'ddr_pll_ctrl', 'pll_bypass_force', enable)
        pll.add(zar, 'slcr', 'ddr_pll_ctrl', 'pll_reset', assert_)
        pll.add(zar, 'slcr', 'ddr_pll_ctrl', 'pll_reset', deassert)
        pll.add(zar, 'slcr', 'pll_status', 'ddr_pll_lock', 1, poll=1)
        pll.add(zar, 'slcr', 'ddr_pll_ctrl', 'pll_bypass_force', disable)
        pll.add(zar, 'slcr', 'ddr_clk_ctrl', 'ddr_3xclkact', enable) 
        pll.add(zar, 'slcr', 'ddr_clk_ctrl', 'ddr_2xclkact', enable)
        pll.add(zar, 'slcr', 'ddr_clk_ctrl', 'ddr_3xclk_divisor', 0x2) # only this was seen, yet
        pll.add(zar, 'slcr', 'ddr_clk_ctrl', 'ddr_2xclk_divisor', 0x3)
        # IO PLL
        cp, res, cnt = get_pll_cp_res_cnt(self.io_pll_mul)
        pll.add(zar, 'slcr', 'io_pll_cfg', 'pll_res', res)
        pll.add(zar, 'slcr', 'io_pll_cfg', 'pll_cp', cp)
        pll.add(zar, 'slcr', 'io_pll_cfg', 'lock_cnt', cnt)
        pll.add(zar, 'slcr', 'io_pll_ctrl', 'pll_fdiv', self.io_pll_mul)
        pll.add(zar, 'slcr', 'io_pll_ctrl', 'pll_bypass_force', enable)
        pll.add(zar, 'slcr', 'io_pll_ctrl', 'pll_reset', assert_)
        pll.add(zar, 'slcr', 'io_pll_ctrl', 'pll_reset', deassert)
        pll.add(zar, 'slcr', 'pll_status', 'io_pll_lock', 1, poll=1)
        pll.add(zar, 'slcr', 'io_pll_ctrl', 'pll_bypass_force', disable)

        pll.add(zar, 'slcr', 'slcr_lock', 'lock_key', lock_key)

        # Clock, PLL output drives various clocks
        # frequency divisors are set here, some have 2, some have only 1
        # clock enables for each of each PS peripheral kinds (eg. UART0-1, FCLK0-3) are also set here
        clock.add(zar, 'slcr', 'slcr_unlock', 'unlock_key', unlock_key)
        clock.add(zar, 'slcr', 'dci_clk_ctrl', 'clkact', enable)
        clock.add(zar, 'slcr', 'dci_clk_ctrl', 'divisor0', self.DCI_FREQ.div0)
        clock.add(zar, 'slcr', 'dci_clk_ctrl', 'divisor1', self.DCI_FREQ.div1)

        clock.add(zar, 'slcr', 'sdio_clk_ctrl', 'clkact0', enable)
        clock.add(zar, 'slcr', 'sdio_clk_ctrl', 'clkact1', enable)
        clock.add(zar, 'slcr', 'sdio_clk_ctrl', 'srcsel', IO_IO_PLL)
        clock.add(zar, 'slcr', 'sdio_clk_ctrl', 'divisor', self.SDIO_FREQ.div0)

        clock.add(zar, 'slcr', 'uart_clk_ctrl', 'clkact0', enable)
        clock.add(zar, 'slcr', 'uart_clk_ctrl', 'clkact1', enable)
        clock.add(zar, 'slcr', 'uart_clk_ctrl', 'srcsel', IO_IO_PLL)
        clock.add(zar, 'slcr', 'uart_clk_ctrl', 'divisor', self.SDIO_FREQ.div0)

        clock.add(zar, 'slcr', 'pcap_clk_ctrl', 'clkact', enable)
        clock.add(zar, 'slcr', 'pcap_clk_ctrl', 'srcsel', IO_IO_PLL)
        clock.add(zar, 'slcr', 'pcap_clk_ctrl', 'divisor', self.PCAP_FREQ.div0)
        # TODO: more peripherals to support
        clock.add(zar, 'slcr', 'fpga0_clk_ctrl', 'srcsel', IO_IO_PLL)
        clock.add(zar, 'slcr', 'fpga0_clk_ctrl', 'divisor0', self.FCLK0_FREQ.div0)
        clock.add(zar, 'slcr', 'fpga0_clk_ctrl', 'divisor1', self.FCLK0_FREQ.div1)
        clock.add(zar, 'slcr', 'fpga1_clk_ctrl', 'srcsel', IO_IO_PLL)
        clock.add(zar, 'slcr', 'fpga1_clk_ctrl', 'divisor0', self.FCLK1_FREQ.div0)
        clock.add(zar, 'slcr', 'fpga1_clk_ctrl', 'divisor1', self.FCLK1_FREQ.div1)
        clock.add(zar, 'slcr', 'fpga2_clk_ctrl', 'srcsel', IO_IO_PLL)
        clock.add(zar, 'slcr', 'fpga2_clk_ctrl', 'divisor0', self.FCLK2_FREQ.div0)
        clock.add(zar, 'slcr', 'fpga2_clk_ctrl', 'divisor1', self.FCLK2_FREQ.div1)
        clock.add(zar, 'slcr', 'fpga3_clk_ctrl', 'srcsel', IO_IO_PLL)
        clock.add(zar, 'slcr', 'fpga3_clk_ctrl', 'divisor0', self.FCLK3_FREQ.div0)
        clock.add(zar, 'slcr', 'fpga3_clk_ctrl', 'divisor1', self.FCLK3_FREQ.div1)
        clock.add(zar, 'slcr', 'clk_621_true', 'clk_621_true', enable if self.APU_CLK_RATIO == '6:2:1' else disable)
        # AMBA peripheral clocks, unsupported parts are disabled now
        clock.add(zar, 'slcr', 'aper_clk_ctrl', 'dma_cpu_2xclkact', enable)
        clock.add(zar, 'slcr', 'aper_clk_ctrl', 'usb0_cpu_1xclkact', disable)
        clock.add(zar, 'slcr', 'aper_clk_ctrl', 'usb1_cpu_1xclkact', disable)
        clock.add(zar, 'slcr', 'aper_clk_ctrl', 'gem0_cpu_1xclkact', disable)
        clock.add(zar, 'slcr', 'aper_clk_ctrl', 'gem1_cpu_1xclkact', disable)
        clock.add(zar, 'slcr', 'aper_clk_ctrl', 'sdi0_cpu_1xclkact', not self.SDIO_FREQ.disable)
        clock.add(zar, 'slcr', 'aper_clk_ctrl', 'sdi1_cpu_1xclkact', not self.SDIO_FREQ.disable)
        clock.add(zar, 'slcr', 'aper_clk_ctrl', 'spi0_cpu_1xclkact', disable)
        clock.add(zar, 'slcr', 'aper_clk_ctrl', 'spi1_cpu_1xclkact', disable)
        clock.add(zar, 'slcr', 'aper_clk_ctrl', 'can0_cpu_1xclkact', disable)
        clock.add(zar, 'slcr', 'aper_clk_ctrl', 'can1_cpu_1xclkact', disable)
        clock.add(zar, 'slcr', 'aper_clk_ctrl', 'i2c0_cpu_1xclkact', disable)
        clock.add(zar, 'slcr', 'aper_clk_ctrl', 'i2c1_cpu_1xclkact', disable)
        clock.add(zar, 'slcr', 'aper_clk_ctrl', 'uart0_cpu_1xclkact', not self.UART_FREQ.disable)
        clock.add(zar, 'slcr', 'aper_clk_ctrl', 'uart1_cpu_1xclkact', not self.UART_FREQ.disable)
        clock.add(zar, 'slcr', 'aper_clk_ctrl', 'gpio_cpu_1xclkact', enable)
        clock.add(zar, 'slcr', 'aper_clk_ctrl', 'lqspi_cpu_1xclkact', disable)
        clock.add(zar, 'slcr', 'aper_clk_ctrl', 'smc_cpu_1xclkact', disable)
        clock.add(zar, 'slcr', 'slcr_lock', 'lock_key', lock_key)

        # MIOs and Peripherals
        # TODO: more granular checking
        mio.add(zar, 'slcr', 'slcr_unlock', 'unlock_key', unlock_key)
        peripherals.add(zar, 'slcr', 'slcr_unlock', 'unlock_key', unlock_key)
        for i in range(0, 53+1):
            mio_pin = 'MIO_PIN_%02d' % i
            try:
                used = 13 - self.param[mio_pin].count('') 
            except KeyError:
                continue
            if used == 0:
                continue
            if used > 1:
                print('Error: MIO %02d used multiple times!' % i)
                return # TODO: abort
            print(mio_pin, ''.join(self.param[mio_pin]))
            # MIO pin mux function select
            l0_sel, l1_sel, l2_sel, l3_sel = z7000_ps_param_L_sel(self.param[mio_pin])
            mio.add(zar, 'slcr', mio_pin, 'L0_SEL', l0_sel)
            mio.add(zar, 'slcr', mio_pin, 'L1_SEL', l1_sel)
            mio.add(zar, 'slcr', mio_pin, 'L2_SEL', l2_sel)
            mio.add(zar, 'slcr', mio_pin, 'L3_SEL', l3_sel)
            # MIO default pin properties
            mio.add(zar, 'slcr', mio_pin, 'TRI_ENABLE', disable)
            mio.add(zar, 'slcr', mio_pin, 'Speed', slow)
            mio.add(zar, 'slcr', mio_pin, 'IO_Type', self.volt_bank0 if i <= 15 else self.volt_bank1) # corresponding bank voltage
            mio.add(zar, 'slcr', mio_pin, 'PULLUP', disable if i in mios_nopullup else enable)
            mio.add(zar, 'slcr', mio_pin, 'DisableRcvr', disable)

        # SD
        # no special reg conf needed, just select (or not select) WP and CD pins
        for i in ['0', '1']:
            if self.check_param_enabled('sd'+i):
                mio.add(zar, 'slcr', 'sd'+i+'_wp_cd_sel', 'sdio'+i+'_wp_sel', 55) # EMIO by default
                mio.add(zar, 'slcr', 'sd'+i+'_wp_cd_sel', 'sdio'+i+'_cd_sel', 56) # EMIO by default

        # UART
        for i in ['0', '1']:
            if self.check_param_enabled('uart'+i):
                peripherals.add(zar, 'uart'+i, 'baud_rate_divider_reg0', 'bdiv', self.uart0_bdiv if i=='0' else self.uart1_bdiv)
                peripherals.add(zar, 'uart'+i, 'xuartps_baudgen_offset', 'cd', self.uart0_cd if i=='0' else self.uart1_cd)
                peripherals.add(zar, 'uart'+i, 'xuartps_cr_offset', 'txen', 1)
                peripherals.add(zar, 'uart'+i, 'xuartps_cr_offset', 'rxen', 1)
                peripherals.add(zar, 'uart'+i, 'xuartps_cr_offset', 'txdis', 0)
                peripherals.add(zar, 'uart'+i, 'xuartps_cr_offset', 'rxdis', 0)
                peripherals.add(zar, 'uart'+i, 'xuartps_cr_offset', 'stpbrk', 0)
                peripherals.add(zar, 'uart'+i, 'xuartps_cr_offset', 'sttbrk', 0)
                peripherals.add(zar, 'uart'+i, 'xuartps_cr_offset', 'rstto', 0) # torst, receiver timeout counter, self-clearing
                peripherals.add(zar, 'uart'+i, 'xuartps_cr_offset', 'txres', 1) # self-clearing reset
                peripherals.add(zar, 'uart'+i, 'xuartps_cr_offset', 'rxres', 1)
                peripherals.add(zar, 'uart'+i, 'xuartps_mr_offset', 'chmode', 0) # normal, 01: auto echo, 10: local lpbk, 11: remote lpbk
                peripherals.add(zar, 'uart'+i, 'xuartps_mr_offset', 'nbstop', 0) # 1 stop bit
                peripherals.add(zar, 'uart'+i, 'xuartps_mr_offset', 'par', 0b100) # no parity, this resets to 0 (even parity)!!
                peripherals.add(zar, 'uart'+i, 'xuartps_mr_offset', 'chrl', 0) # 8 bits char
                peripherals.add(zar, 'uart'+i, 'xuartps_mr_offset', 'clks', 0) # 0: uart_ref_clk, 1: uart_ref_clk/8
        # QSPI
        peripherals.add(zar, 'qspi', 'xqspips_cr_offset', 'holdb_dr', 1) # Holdb/WPn drive, set in all cases
        # devcfg
        peripherals.add(zar, 'devcfg', 'xdcfg_ctrl_offset', 'pcfg_por_cnt_4k', 0) # 4k instead of 64k, faster startup, optional
        mio.add(zar, 'slcr', 'slcr_lock', 'lock_key', lock_key)
        peripherals.add(zar, 'slcr', 'slcr_lock', 'lock_key', lock_key)

        post_config.add(zar, 'slcr', 'slcr_unlock', 'unlock_key', unlock_key)
        post_config.add(zar, 'slcr', 'lvl_shftr_en', '', 0xF, fullreg=1)
        post_config.add(zar, 'slcr', 'fpga_rst_ctrl', '', 0x0, fullreg=1)
        post_config.add(zar, 'slcr', 'slcr_lock', 'lock_key', lock_key)

        # pll.merge()
        clock.merge()
        mio.merge()
        peripherals.merge()
        post_config.merge()

        self.pll = pll
        self.clock = clock
        self.mio = mio
        self.peripherals = peripherals
        self.ddr = ddr
        self.post_config = post_config

        # print(pll.emit())
        # print(clock.emit())
        # print(mio.emit())
        # print(peripherals.emit(fmt='TCL'))
        # print(ddr.emit())
        # print(post_config.emit())

    def ps7_init_filewrite(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), './ps7_init_template/')
        for name in ['ps7_init.c', 'ps7_init.h', 'ps7_init.tcl', 'xparameters.h']:
            iname = os.path.join(template_path, name)
            oname = os.path.join(path, name)
            with open(iname, 'r') as fi, open(oname, 'w') as fo:
                # Emit register writes
                di = fi.read()
                di = di.replace('PS7_PLL_INIT_DATA_TBD', self.pll.emit(fmt='TCL' if name.lower().endswith('.tcl') else 'C'))
                di = di.replace('PS7_CLOCK_INIT_DATA_TBD', self.clock.emit(fmt='TCL' if name.lower().endswith('.tcl') else 'C'))
                di = di.replace('PS7_MIO_INIT_DATA_TBD', self.mio.emit(fmt='TCL' if name.lower().endswith('.tcl') else 'C'))
                di = di.replace('PS7_PERIPHERALS_INIT_DATA_TBD', self.peripherals.emit(fmt='TCL' if name.lower().endswith('.tcl') else 'C'))
                di = di.replace('PS7_DDR_INIT_DATA_TBD', self.ddr.emit(fmt='TCL' if name.lower().endswith('.tcl') else 'C'))
                di = di.replace('PS7_POST_CONFIG_TBD', self.post_config.emit(fmt='TCL' if name.lower().endswith('.tcl') else 'C'))
                
                # Update macros in .h, most are unused, actually
                periph_list = [self.FCLK0_FREQ, self.FCLK1_FREQ, self.FCLK2_FREQ, self.FCLK3_FREQ, 
                               self.QSPI_FREQ, self.SMC_FREQ, self.ENET0_FREQ, self.ENET1_FREQ, 
                               self.SDIO_FREQ, self.SPI_FREQ, self.UART_FREQ, self.CAN_FREQ,
                               self.PCAP_FREQ, self.APU_FREQ, self.DDR_FREQ, self.DCI_FREQ]
                for PERIPH in periph_list:
                    pn = PERIPH.name
                    pf = PERIPH.actual
                    di = di.replace(pn+'_FREQ_TBD', str(round(pf * 1e6)))
                unsupported_list = ['USB0', 'USB1', 'I2C', 'WDT', 'TTC', 'TPIU']
                for u in unsupported_list:
                    di = di.replace(u+'_FREQ_TBD', '10000000')

                # Peripheral address BASEADDR/HIGHADDR in xparameters.h
                # We target to correctly compile embeddedsw FSBL and HelloWorld, 
                #  these designes use at most 1 peripheral per type.
                #  More advanced usages are left to users to handle. 
                # QSPI, unsupported for now
                di = di.replace('QSPI_NUM_TBD', '0')
                di = di.replace('QSPI_FREQ_TBD', str(self.QSPI_FREQ.actual))
                # SDIO
                if self.check_param_enabled('sd'):
                    di = di.replace('SDIO_NUM_TBD', '1')
                    di = di.replace('SDIO_FREQ_TBD', str(self.SDIO_FREQ.actual))
                    if self.check_param_enabled('sd0'):
                        di = di.replace('SDIO_BASEADDR_TBD', hex(sdio.baseaddrs[0]))
                        di = di.replace('SDIO_HIGHADDR_TBD', hex(sdio.baseaddrs[0] + uart.highaddr))
                    elif self.check_param_enabled('sd1'):
                        di = di.replace('SDIO_BASEADDR_TBD', hex(sdio.baseaddrs[1]))
                        di = di.replace('SDIO_HIGHADDR_TBD', hex(sdio.baseaddrs[1] + uart.highaddr))
                # UART
                if self.check_param_enabled('uart'):
                    di = di.replace('UART_NUM_TBD', '1')
                    di = di.replace('UART_FREQ_TBD', str(self.UART_FREQ.actual))
                    if self.check_param_enabled('uart0'):
                        di = di.replace('UART_BASEADDR_TBD', hex(uart.baseaddrs[0]))
                        di = di.replace('UART_HIGHADDR_TBD', hex(uart.baseaddrs[0] + uart.highaddr))
                    elif self.check_param_enabled('uart1'):
                        di = di.replace('UART_BASEADDR_TBD', hex(uart.baseaddrs[1]))
                        di = di.replace('UART_HIGHADDR_TBD', hex(uart.baseaddrs[1] + uart.highaddr))


                di = di.replace(u+'_FREQ_TBD', '10000000')
                fo.write(di)

if __name__ == '__main__':
    for sample in ['noddr-0-uart', 'noddr-0-sd', 'noddr-0-uart-elsegpio']:
        parse_ps7_init_entries_fields("./tcl_fuzz/hdf/" + sample + "/ps7_init_gpl.c")
    zynq7_allregisters.show()
    z7 = Zynq7000()
    z7.param_load(z7000_ps_param_demo)
    z7.ps7_init_gen(zynq7_allregisters)
    z7.ps7_init_filewrite('./ps7_init_test/')
    # calc_pll_muldiv(33.333333, 50, [i for i in range(z7.pll_mul_min, z7.pll_mul_max+1)], [i for i in range(1, 63+1)], [1])
    # calc_pll_muldiv(33.333333, 666.666667, [i for i in range(z7.pll_mul_min, z7.pll_mul_max+1)], [2], [1])
    # calc_pll_muldiv(33.333333, 1966.666667, [i for i in range(z7.pll_mul_min, z7.pll_mul_max+1)], [2] + [i for i in range(z7.pll_muldiv_min_abs, z7.pll_muldiv_max_abs+1)], [1], opt='div')

