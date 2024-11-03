#!/usr/bin/env python3
from register_names import *

class Clock:
    def __init__(self, requested, lower, upper, oc=0, auto=0, source='default'):
        self.requested = requested
        self.actual = 0
        self.lower = lower
        self.upper = upper
        self.oc = oc # allow overclocking
        self.auto = auto # allow any frequency in range
        self.source = source

class Uart:
    def __init__(self, enabled, num, baud=115200):
        self.enabled = enabled
        self.baud = baud

class SD:
    def __init__(self, enabled, num, baud=115200):
        self.enabled = enabled
        self.baud = baud

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
#				TRI_ENABLE	Speed	IO_Type		PULLUP		DisableRcvr
mios_common = [	enable ,	slow ,	lvcmos33,	enable ,	enable 	]
# Boot Mode MIO pins, pullup is not available. 
mios_nopullup = [2, 3, 4, 5, 6, 7, 8]
_=0
z7000_ps_param_demo = {
    #				L0				L1					L2_01				L2_10				L2_11			L3_000		L3_001			L3_010				L3_011			L3_100			L3_101			L3_110			L3_111
    'MIO_PIN_00': [	_*'qspi1 ss_b',	x,					_*'sram/nor cs0',	_*'nand cs0',		_*'sd0 power',	_*'gpio',	x,				x,					x,				x,				x,				x,				'☑ ☐ '],
	'MIO_PIN_01': [	_*'qspi0 ss_b',	x,					_*'sram addr25',	_*'sram/nor cs1',	_*'sd1 power',	_*'gpio',	x,				x,					x,				x,				x,				x,				x],
	'MIO_PIN_02': [	_*'qspi0 io0',	_*'trace data8',	x,					_*'nand alen',		_*'sd0 power',	_*'gpio',	x,				x,					x,				x,				x,				x,				x],
	'MIO_PIN_03': [	_*'qspi0 io1',	_*'trace data9',	_*'sram/nor data0',	_*'nand we_b',		_*'sd1 power',	_*'gpio',	x,				x,					x,				x,				x,				x,				x],
	'MIO_PIN_04': [	_*'qspi0 io2',	_*'trace data10',	_*'sram/nor data1',	_*'nand data2',		_*'sd0 power',	_*'gpio',	x,				x,					x,				x,				x,				x,				x],
	'MIO_PIN_05': [	_*'qspi0 io3',	_*'trace data11',	_*'sram/nor data2',	_*'nand data0',		_*'sd1 power',	_*'gpio',	x,				x,					x,				x,				x,				x,				x],
	'MIO_PIN_06': [	_*'qspi0 sclk',	_*'trace data12',	_*'sram/nor data3',	_*'nand data1',		_*'sd0 power',	_*'gpio',	x,				x,					x,				x,				x,				x,				x],
	'MIO_PIN_07': [	x,				_*'trace data13',	_*'sram/nor oe_b',	_*'nand cle_b',		_*'sd1 power',	_*'gpio',	x,				x,					x,				x,				x,				x,				x],
	'MIO_PIN_08': [	_*'qspi fbclk',	_*'trace data14',	x,					_*'nand rd_b',		_*'sd0 power',	_*'gpio',	_*'can1 tx',	_*'sram/nor bls_b',	x,				x,				x,				x,				_*'uart1 txd'],
	'MIO_PIN_09': [	_*'qspi1 sclk',	_*'trace data15',	_*'sram/nor data6',	_*'nand data4',		_*'sd1 power',	_*'gpio',	_*'can1 rx',	x,					x,				x,				x,				x,				_*'uart1 rxd'],
	'MIO_PIN_10': [	_*'qspi1 io0',	_*'trace data2',	_*'sram/nor data7',	_*'nand data5',		_*'sd0 power',	_*'gpio',	_*'can0 rx',	_*'i2c0 scl',		_*'pjtag tdi',	_*'sd1 data0',	_*'spi1 mosi',	x,				1*'uart0 rxd'],
	'MIO_PIN_11': [	_*'qspi1 io1',	_*'trace data3',	_*'sram/nor data4',	_*'nand data6',		_*'sd1 power',	_*'gpio',	_*'can0 tx',	_*'i2c0 sda',		_*'pjtag tdo',	_*'sd1 cmd',	_*'spi1 miso',	x,				1*'uart0 txd'],
	'MIO_PIN_12': [	_*'qspi1 io2',	_*'trace clk',		x,					_*'nand data7',		_*'sd0 power',	_*'gpio',	_*'can1 tx',	_*'i2c1 scl',		_*'pjtag tck',	_*'sd1 sck',	_*'spi1 sck',	x,				_*'uart1 txd'],
	'MIO_PIN_13': [	_*'qspi1 io3',	_*'trace ctrl',		x,					_*'nand data3',		_*'sd1 power',	_*'gpio',	_*'can1 rx',	_*'i2c1 sda',		_*'pjtag tms',	_*'sd1 data1',	_*'spi1 ss0',	x,				_*'uart1 rxd'],
	'MIO_PIN_14': [	x,				_*'trace data0',	x,					_*'nand busy',		_*'sd0 power',	_*'gpio',	_*'can0 rx',	_*'i2c0 scl',		_*'swdt clk',	_*'sd1 data2',	_*'spi1 ss1',	x,				_*'uart0 rxd'],
	'MIO_PIN_15': [	x,				_*'trace data1',	_*'sram/nor addr0',	x,					_*'sd1 power',	_*'gpio',	_*'can0 tx',	_*'i2c0 sda',		_*'swdt rst',	_*'sd1 data3',	_*'spi1 ss2',	x,				_*'uart0 txd'],
	'MIO_PIN_16': [	_*'gem0 tx_clk',_*'trace data4',	_*'sram/nor addr1',	_*'nand data8',		_*'sd0 power',	_*'gpio',	_*'can1 tx',	_*'i2c1 scl',		x,				1*'sd0 sck',	_*'spi0 sck',	0*'ttc1 wave',	_*'uart1 txd'],
	'MIO_PIN_17': [	_*'gem0 txd0',	_*'trace data5',	_*'sram/nor addr2',	_*'nand data9',		_*'sd1 power',	_*'gpio',	_*'can1 rx',	_*'i2c1 sda',		x,				1*'sd0 cmd',	_*'spi0 miso',	0*'ttc1 clk',	_*'uart1 rxd'],
	'MIO_PIN_18': [	_*'gem0 txd1',	_*'trace data6',	_*'sram/nor addr3',	_*'nand data10',	_*'sd0 power',	_*'gpio',	_*'can0 rx',	_*'i2c0 scl',		x,				1*'sd0 data0',	_*'spi0 ss0',	0*'ttc0 wave',	_*'uart0 rxd'],
	'MIO_PIN_19': [	_*'gem0 txd2',	_*'trace data7',	_*'sram/nor addr4',	_*'nand data11',	_*'sd1 power',	_*'gpio',	_*'can0 tx',	_*'i2c0 sda',		x,				1*'sd0 data1',	_*'spi0 ss1',	0*'ttc0 clk',	_*'uart0 txd'],
	'MIO_PIN_20': [	_*'gem0 txd3',	x,					_*'sram/nor addr5',	_*'nand data12',	_*'sd0 power',	_*'gpio',	_*'can1 tx',	_*'i2c1 scl',		x,				1*'sd0 data2',	_*'spi0 ss2',	x,				_*'uart1 txd'],
	'MIO_PIN_21': [	_*'gem0 tx_ctl',x,					_*'sram/nor addr6',	_*'nand data13',	_*'sd1 power',	_*'gpio',	_*'can1 rx',	_*'i2c1 sda',		x,				1*'sd0 data3',	_*'spi0 mosi',	x,				_*'uart1 rxd'],
	'MIO_PIN_22': [	_*'gem0 rx_clk',_*'trace data2',	_*'sram/nor addr7',	_*'nand data14',	_*'sd0 power',	_*'gpio',	_*'can0 rx',	_*'i2c0 scl',		_*'pjtag tdi',	_*'sd1 data0',	_*'spi1 mosi',	x,				_*'uart0 rxd'],
	'MIO_PIN_23': [	_*'gem0 rxd0',	_*'trace data3',	_*'sram/nor addr8',	_*'nand data15',	_*'sd1 power',	_*'gpio',	_*'can0 tx',	_*'i2c0 sda',		_*'pjtag tdo',	_*'sd1 cmd',	_*'spi1 miso',	x,				_*'uart0 txd'],
	'MIO_PIN_24': [	_*'gem0 rxd1',	_*'trace clk',		_*'sram/nor addr9',	x,					_*'sd0 power',	_*'gpio',	_*'can1 tx',	_*'i2c1 scl',		_*'pjtag tck',	_*'sd1 sck',	_*'spi1 sck',	x,				_*'uart1 txd'],
	'MIO_PIN_25': [	_*'gem0 rxd2',	_*'trace ctrl',		_*'sram/nor addr10',x,					_*'sd1 power',	_*'gpio',	_*'can1 rx',	_*'i2c1 sda',		_*'pjtag tms',	_*'sd1 data1',	_*'spi1 ss0',	x,				_*'uart1 rxd'],
	'MIO_PIN_26': [	_*'gem0 rxd3',	_*'trace data0',	_*'sram/nor addr11',x,					_*'sd0 power',	_*'gpio',	_*'can0 rx',	_*'i2c0 scl',		_*'swdt clk',	_*'sd1 data2',	_*'spi1 ss1',	x,				_*'uart0 rxd'],
	'MIO_PIN_27': [	_*'gem0 rx_clk',_*'trace data1',	_*'sram/nor addr12',x,					_*'sd1 power',	_*'gpio',	_*'can0 tx',	_*'i2c0 sda',		_*'swdt rst',	_*'sd1 data3',	_*'spi1 ss2',	x,				_*'uart0 txd'],
	'MIO_PIN_28': [	_*'gem1 tx_clk',_*'usb0 data4',		_*'sram/nor addr13',x,					_*'sd0 power',	_*'gpio',	_*'can1 tx',	_*'i2c1 scl',		x,				_*'sd0 sck',	_*'spi0 sck',	0*'ttc1 wave',	_*'uart1 txd'],
	'MIO_PIN_29': [	_*'gem1 txd0',	_*'usb0 dir',		_*'sram/nor addr14',x,					_*'sd1 power',	_*'gpio',	_*'can1 rx',	_*'i2c1 sda',		x,				_*'sd0 miso',	_*'spi0 miso',	0*'ttc1 clk',	_*'uart1 rxd'],
	'MIO_PIN_30': [	_*'gem1 txd1',	_*'usb0 stp',		_*'sram/nor addr15',x,					_*'sd0 power',	_*'gpio',	_*'can0 rx',	_*'i2c0 scl',		x,				_*'sd0 data0',	_*'spi0 ss0',	0*'ttc0 wave',	_*'uart0 rxd'],
	'MIO_PIN_31': [	_*'gem1 txd2',	_*'usb0 nxt',		_*'sram/nor addr16',x,					_*'sd1 power',	_*'gpio',	_*'can0 tx',	_*'i2c0 sda',		x,				_*'sd0 data1',	_*'spi0 ss1',	1*'ttc0 clk',	_*'uart0 txd'],
	'MIO_PIN_32': [	_*'gem1 txd3',	_*'usb0 data0',		_*'sram/nor addr17',x,					_*'sd0 power',	_*'gpio',	_*'can1 tx',	_*'i2c1 scl',		x,				_*'sd0 data2',	_*'spi0 ss2',	x,				_*'uart1 txd'],
	'MIO_PIN_33': [	_*'gem1 tx_ctl',_*'usb0 data1',		_*'sram/nor addr18',x,					_*'sd1 power',	_*'gpio',	_*'can1 rx',	_*'i2c1 sda',		x,				_*'sd0 data3',	_*'spi0 mosi',	x,				_*'uart1 rxd'],
	'MIO_PIN_34': [	_*'gem1 rx_clk',_*'usb0 data2',		_*'sram/nor addr19',x,					_*'sd0 power',	_*'gpio',	_*'can0 rx',	_*'i2c0 scl',		_*'pjtag tdi',	_*'sd1 data0',	_*'spi1 mosi',	x,				_*'uart0 rxd'],
	'MIO_PIN_35': [	_*'gem1 rxd0',	_*'usb0 data3',		_*'sram/nor addr20',x,					_*'sd1 power',	_*'gpio',	_*'can0 tx',	_*'i2c0 sda',		_*'pjtag tdo',	_*'sd1 cmd',	_*'spi1 miso',	x,				_*'uart0 txd'],
	'MIO_PIN_36': [	_*'gem1 rxd1',	_*'usb0 clk',		_*'sram/nor addr21',x,					_*'sd0 power',	_*'gpio',	_*'can1 tx',	_*'i2c1 scl',		_*'pjtag tck',	_*'sd1 sck',	_*'spi1 sck',	x,				_*'uart1 txd'],
	'MIO_PIN_37': [	_*'gem1 rxd2',	_*'usb0 data5',		_*'sram/nor addr22',x,					_*'sd1 power',	_*'gpio',	_*'can1 rx',	_*'i2c1 sda',		_*'pjtag tms',	_*'sd1 data1',	_*'spi1 ss0',	x,				_*'uart1 rxd'],
	'MIO_PIN_38': [	_*'gem1 rxd3',	_*'usb0 data6',		_*'sram/nor addr23',x,					_*'sd0 power',	_*'gpio',	_*'can0 rx',	_*'i2c0 scl',		_*'swdt clk',	_*'sd1 data2',	_*'spi1 ss1',	x,				_*'uart0 rxd'],
	'MIO_PIN_39': [	_*'gem1 rx_ctl',_*'usb0 data7',		_*'sram/nor addr24',x,					_*'sd1 power',	_*'gpio',	_*'can0 tx',	_*'i2c0 sda',		_*'swdt rst',	_*'sd1 data3',	_*'spi1 ss2',	x,				_*'uart0 txd'],
	'MIO_PIN_40': [	x,				_*'usb1 data4',		x,					x,					_*'sd0 power',	_*'gpio',	_*'can1 tx',	_*'i2c1 scl',		x,				_*'sd0 sck',	_*'spi0 sck',	0*'ttc1 wave',	_*'uart1 txd'],
	'MIO_PIN_41': [	x,				_*'usb1 dir',		x,					x,					_*'sd1 power',	_*'gpio',	_*'can1 rx',	_*'i2c1 sda',		x,				_*'sd0 miso',	_*'spi0 miso',	0*'ttc1 clk',	_*'uart1 rxd'],
	'MIO_PIN_42': [	x,				_*'usb1 stp',		x,					x,					_*'sd0 power',	_*'gpio',	_*'can0 rx',	_*'i2c0 scl',		x,				_*'sd0 data0',	_*'spi0 ss0',	0*'ttc0 wave',	_*'uart0 rxd'],
	'MIO_PIN_43': [	x,				_*'usb1 nxt',		x,					x,					_*'sd1 power',	_*'gpio',	_*'can0 tx',	_*'i2c0 sda',		x,				_*'sd0 data1',	_*'spi0 ss1',	1*'ttc0 clk',	_*'uart0 txd'],
	'MIO_PIN_44': [	x,				_*'usb1 data0',		x,					x,					_*'sd0 power',	_*'gpio',	_*'can1 tx',	_*'i2c1 scl',		x,				_*'sd0 data2',	_*'spi0 ss2',	x,				_*'uart1 txd'],
	'MIO_PIN_45': [	x,				_*'usb1 data1',		x,					x,					_*'sd1 power',	_*'gpio',	_*'can1 rx',	_*'i2c1 sda',		x,				_*'sd0 data3',	_*'spi0 mosi',	x,				_*'uart1 rxd'],
	'MIO_PIN_46': [	x,				_*'usb1 data2',		x,					x,					_*'sd0 power',	_*'gpio',	_*'can0 rx',	_*'i2c0 scl',		_*'pjtag tdi',	_*'sd1 data0',	_*'spi1 mosi',	x,				_*'uart0 rxd'],
	'MIO_PIN_47': [	x,				_*'usb1 data3',		x,					x,					_*'sd1 power',	_*'gpio',	_*'can0 tx',	_*'i2c0 sda',		_*'pjtag tdo',	_*'sd1 cmd',	_*'spi1 miso',	x,				_*'uart0 txd'],
	'MIO_PIN_48': [	x,				_*'usb1 clk',		x,					x,					_*'sd0 power',	_*'gpio',	_*'can1 tx',	_*'i2c1 scl',		_*'pjtag tck',	_*'sd1 sck',	_*'spi1 sck',	x,				_*'uart1 txd'],
	'MIO_PIN_49': [	x,				_*'usb1 data5',		x,					x,					_*'sd1 power',	_*'gpio',	_*'can1 rx',	_*'i2c1 sda',		_*'pjtag tms',	_*'sd1 data1',	_*'spi1 ss0',	x,				_*'uart1 rxd'],
	'MIO_PIN_50': [	x,				_*'usb1 data6',		x,					x,					_*'sd0 power',	_*'gpio',	_*'can0 rx',	_*'i2c0 scl',		_*'swdt clk',	_*'sd1 data2',	_*'spi1 ss1',	x,				_*'uart0 rxd'],
	'MIO_PIN_51': [	x,				_*'usb1 data7',		x,					x,					_*'sd1 power',	_*'gpio',	_*'can0 tx',	_*'i2c0 sda',		_*'swdt rst',	_*'sd1 data3',	_*'spi1 ss2',	x,				_*'uart0 txd'],
	'MIO_PIN_52': [	x,				x,					x,					x,					_*'sd0 power',	_*'gpio',	_*'can1 tx',	_*'i2c1 scl',		_*'swdt clk',	_*'mdio0 clk',	_*'mdio1 clk',	x,				_*'uart1 txd'],
	'MIO_PIN_53': [	x,				x,					x,					x,					_*'sd1 power',	_*'gpio',	_*'can1 rx',	_*'i2c1 sda',		_*'swdt rst',	_*'mdio0 data',	_*'mdio1 data',	x,				_*'uart1 rxd'],
    'gpio'  : {},
    'uart0' : { 'baud': 115200 },
    'uart1' : { 'baud': 9600 }, 
    'sd0'   : {},
    'freq'  : { 'crystal'  : 33.333333,
                'fclk0'    : 50,
                'fclk1'    : 50}
	}

# input: input frequency, output frequecy, multiplier range, divisor0 range, divisor1 range
# output: mul, div0, div1, frequency diff in percentage
# ordinary calc: returns mul, div, abs deviation
# in range only: returns mul, div, freq (-1 for impossible)
# prioritize multiplier in order as specified in mulrange
def calc_pll_muldiv(fin, fout, mulrange, div0range, div1range, in_range_only=0, opt='mul'):
    fin = fin # this controls our accuracy!
    fout = fout
    drange = []
    for d0 in div0range:
        for d1 in div1range:
            drange.append(d0 * d1)
    # if not optdiv: # don't need sort actually, just repeat...
        # drange = list(set(drange)) # automatically sorted
    print(mulrange)
    print(drange)
    mbest = -1
    dbest = -1
    devmin = 9e9
    if opt == 'div':
        for d in drange:
            devsmall = 9e9
            mgood = -1
            for m in mulrange:
                dev = abs(fin * m / d - fout) / fout
                if dev < devsmall:
                    devsmall = dev
                    mgood = m
            if devsmall < devmin:
                devmin = devsmall
                dbest = d
                mbest = mgood
    elif opt == 'mul':
        for m in mulrange:
            devsmall = 9e9
            dgood = -1
            for d in drange:
                dev = abs(fin * m / d - fout) / fout
                if dev < devsmall:
                    devsmall = dev
                    dgood = d
            if devsmall < devmin:
                devmin = devsmall
                mbest = m
                dbest = dgood

    print(fin, fout, mbest, dbest, devmin)

class Zynq7000:
    def __init__(self, param):
        self.param = param
        self.CRYSTAL_FREQ = Clock(33.333333, 30, 60)
        self.APU_FREQ = Clock(666.666666, 50, 667, oc=1) # default from ARM PLL
        self.APU_CLK_RATIO = '6:2:1' # or 4:2:1
        self.DDR_FREQ = Clock(533.333333, 200, 534, oc=1) # default from DDR PLL
        self.FCLK0_FREQ = Clock('disabled', 0.1, 250) # FCLK and peripheral default from IO PLL
        self.FCLK1_FREQ = Clock('disabled', 0.1, 250)
        self.FCLK2_FREQ = Clock('disabled', 0.1, 250)
        self.FCLK3_FREQ = Clock('disabled', 0.1, 250)
        self.QSPI_FREQ = Clock('disabled', 10, 200)
        self.SMC_FREQ = Clock('disabled', 10, 100) # static memory controller
        self.ENET0_FREQ = Clock('disabled', 0.1, 125)
        self.ENET1_FREQ = Clock('disabled', 0.1, 125)
        self.SDIO_FREQ = Clock('disabled', 10, 125)
        self.SPI_FREQ = Clock('disabled', 0, 200)
        self.UART_FREQ = Clock('disabled', 10, 100)
        self.CAN_FREQ = Clock('disabled', 0.1, 100)
        self.PCAP_FREQ = Clock('auto', 10, 200) # processor configuration access point, for loading bitstream from PS
        self.DCI_FREQ = Clock('auto', 0.1, 177) # digital controlled impedance, for DDR PHY calibration, default from DDR PLL

        self.pll_mul_min = 13
        self.pll_mul_max = 48
        self.pll_muldiv_min_abs = 1
        self.pll_muldiv_max_abs = 63

        self.param_calculated = False


    def param_calc(self):
        self.param_calculated = True
        self.armpll_div0 = 2
        # self.armpll_mul = 

    def ps7_init_gen(self, zar):
        if not self.param_calculated:
            self.param_calc()
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
        pll.add(zar, 'slcr', 'arm_pll_ctrl', 'pll_bypass_force', enable)
        pll.add(zar, 'slcr', 'arm_pll_ctrl', 'pll_reset', assert_)
        pll.add(zar, 'slcr', 'arm_pll_ctrl', 'pll_reset', deassert)
        pll.add(zar, 'slcr', 'pll_status', 'arm_pll_lock', 1, poll=1)
        pll.add(zar, 'slcr', 'arm_pll_ctrl', 'pll_bypass_force', disable)
        pll.add(zar, 'slcr', 'arm_clk_ctrl', 'srcsel', -1)
        pll.add(zar, 'slcr', 'arm_clk_ctrl', 'divisor', -1)
        pll.add(zar, 'slcr', 'arm_clk_ctrl', 'cpu_6or4xclkact', enable)
        pll.add(zar, 'slcr', 'arm_clk_ctrl', 'cpu_3or2xclkact', enable)
        pll.add(zar, 'slcr', 'arm_clk_ctrl', 'cpu_1xclkact', enable)
        pll.add(zar, 'slcr', 'arm_clk_ctrl', 'cpu_peri_clkact', enable)
        # DDR PLL
        pll.add(zar, 'slcr', 'ddr_pll_cfg', 'pll_res', -1)
        pll.add(zar, 'slcr', 'ddr_pll_cfg', 'pll_cp', -1)
        pll.add(zar, 'slcr', 'ddr_pll_cfg', 'lock_cnt', -1)
        pll.add(zar, 'slcr', 'ddr_pll_ctrl', 'pll_fdiv', -1)
        pll.add(zar, 'slcr', 'ddr_pll_ctrl', 'pll_bypass_force', enable)
        pll.add(zar, 'slcr', 'ddr_pll_ctrl', 'pll_reset', assert_)
        pll.add(zar, 'slcr', 'ddr_pll_ctrl', 'pll_reset', deassert)
        pll.add(zar, 'slcr', 'pll_status', 'ddr_pll_lock', 1, poll=1)
        pll.add(zar, 'slcr', 'ddr_pll_ctrl', 'pll_bypass_force', disable)
        pll.add(zar, 'slcr', 'ddr_clk_ctrl', 'ddr_3xclkact', enable)
        pll.add(zar, 'slcr', 'ddr_clk_ctrl', 'ddr_2xclkact', enable)
        pll.add(zar, 'slcr', 'ddr_clk_ctrl', 'ddr_3xclk_divisor', -1)
        pll.add(zar, 'slcr', 'ddr_clk_ctrl', 'ddr_2xclk_divisor', -1)
        # IO PLL
        pll.add(zar, 'slcr', 'io_pll_cfg', 'pll_res', -1)
        pll.add(zar, 'slcr', 'io_pll_cfg', 'pll_cp', -1)
        pll.add(zar, 'slcr', 'io_pll_cfg', 'lock_cnt', -1)
        pll.add(zar, 'slcr', 'io_pll_ctrl', 'pll_fdiv', -1)
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
        clock.add(zar, 'slcr', 'dci_clk_ctrl', 'divisor0', -1)
        clock.add(zar, 'slcr', 'dci_clk_ctrl', 'divisor1', -1)

        clock.add(zar, 'slcr', 'sdio_clk_ctrl', 'clkact0', enable)
        clock.add(zar, 'slcr', 'sdio_clk_ctrl', 'clkact1', enable)
        clock.add(zar, 'slcr', 'sdio_clk_ctrl', 'srcsel', IO_IO_PLL)
        clock.add(zar, 'slcr', 'sdio_clk_ctrl', 'divisor', -1)

        clock.add(zar, 'slcr', 'uart_clk_ctrl', 'clkact0', enable)
        clock.add(zar, 'slcr', 'uart_clk_ctrl', 'clkact1', enable)
        clock.add(zar, 'slcr', 'uart_clk_ctrl', 'srcsel', IO_IO_PLL)
        clock.add(zar, 'slcr', 'uart_clk_ctrl', 'divisor', -1)

        clock.add(zar, 'slcr', 'pcap_clk_ctrl', 'clkact', enable)
        clock.add(zar, 'slcr', 'pcap_clk_ctrl', 'srcsel', IO_IO_PLL)
        clock.add(zar, 'slcr', 'pcap_clk_ctrl', 'divisor', -1)
        # TODO: more peripherals to support
        clock.add(zar, 'slcr', 'fpga0_clk_ctrl', 'srcsel', IO_IO_PLL)
        clock.add(zar, 'slcr', 'fpga0_clk_ctrl', 'divisor0', -1)
        clock.add(zar, 'slcr', 'fpga0_clk_ctrl', 'divisor1', -1)
        clock.add(zar, 'slcr', 'fpga1_clk_ctrl', 'srcsel', IO_IO_PLL)
        clock.add(zar, 'slcr', 'fpga1_clk_ctrl', 'divisor0', -1)
        clock.add(zar, 'slcr', 'fpga1_clk_ctrl', 'divisor1', -1)
        clock.add(zar, 'slcr', 'fpga2_clk_ctrl', 'srcsel', IO_IO_PLL)
        clock.add(zar, 'slcr', 'fpga2_clk_ctrl', 'divisor0', -1)
        clock.add(zar, 'slcr', 'fpga2_clk_ctrl', 'divisor1', -1)
        clock.add(zar, 'slcr', 'fpga3_clk_ctrl', 'srcsel', IO_IO_PLL)
        clock.add(zar, 'slcr', 'fpga3_clk_ctrl', 'divisor0', -1)
        clock.add(zar, 'slcr', 'fpga3_clk_ctrl', 'divisor1', -1)
        clock.add(zar, 'slcr', 'clk_621_true', 'clk_621_true', enable if self.APU_CLK_RATIO == '6:2:1' else disable)
        # AMBA peripheral clocks, enable all for simplicity
        # TODO: disable unused ones
        clock.add(zar, 'slcr', 'aper_clk_ctrl', 'dma_cpu_2xclkact', enable)
        clock.add(zar, 'slcr', 'aper_clk_ctrl', 'usb0_cpu_1xclkact', enable)
        clock.add(zar, 'slcr', 'aper_clk_ctrl', 'usb1_cpu_1xclkact', enable)
        clock.add(zar, 'slcr', 'aper_clk_ctrl', 'gem0_cpu_1xclkact', enable)
        clock.add(zar, 'slcr', 'aper_clk_ctrl', 'gem1_cpu_1xclkact', enable)
        clock.add(zar, 'slcr', 'aper_clk_ctrl', 'sdi0_cpu_1xclkact', enable)
        clock.add(zar, 'slcr', 'aper_clk_ctrl', 'sdi1_cpu_1xclkact', enable)
        clock.add(zar, 'slcr', 'aper_clk_ctrl', 'spi0_cpu_1xclkact', enable)
        clock.add(zar, 'slcr', 'aper_clk_ctrl', 'spi1_cpu_1xclkact', enable)
        clock.add(zar, 'slcr', 'aper_clk_ctrl', 'can0_cpu_1xclkact', enable)
        clock.add(zar, 'slcr', 'aper_clk_ctrl', 'can1_cpu_1xclkact', enable)
        clock.add(zar, 'slcr', 'aper_clk_ctrl', 'i2c0_cpu_1xclkact', enable)
        clock.add(zar, 'slcr', 'aper_clk_ctrl', 'i2c1_cpu_1xclkact', enable)
        clock.add(zar, 'slcr', 'aper_clk_ctrl', 'uart0_cpu_1xclkact', enable)
        clock.add(zar, 'slcr', 'aper_clk_ctrl', 'uart1_cpu_1xclkact', enable)
        clock.add(zar, 'slcr', 'aper_clk_ctrl', 'gpio_cpu_1xclkact', enable)
        clock.add(zar, 'slcr', 'aper_clk_ctrl', 'lqspi_cpu_1xclkact', enable)
        clock.add(zar, 'slcr', 'aper_clk_ctrl', 'smc_cpu_1xclkact', enable)
        clock.add(zar, 'slcr', 'slcr_lock', 'lock_key', lock_key)

        mio.add(zar, 'slcr', 'slcr_unlock', 'unlock_key', unlock_key)
        # mio.add(zar, 'slcr', 'fpga_rst_ctrl', 'unlock_key', unlock_key)
        mio.add(zar, 'slcr', 'slcr_lock', 'lock_key', lock_key)
        # Need tree-like table for MIO functions, and a way to walk the table from python config
        print(pll.emit())
        print(clock.emit())
        print(mio.emit())

    def xparameter_h_gen(self):
        if not self.param_calculated:
            self.param_calc(self)
        pass

if __name__ == '__main__':
    for sample in ['noddr-0-uart', 'noddr-0-sd', 'noddr-0-uart-elsegpio']:
        parse_ps7_init_entries_fields("./hdf/" + sample + "/ps7_init_gpl.c")
    zynq7_allregisters.show()
    z7 = Zynq7000(z7000_ps_param_demo)
    z7.ps7_init_gen(zynq7_allregisters)
    calc_pll_muldiv(33.333333, 50, [i for i in range(z7.pll_mul_min, z7.pll_mul_max+1)], [i for i in range(1, 63+1)], [1])
    calc_pll_muldiv(33.333333, 666.666667, [i for i in range(z7.pll_mul_min, z7.pll_mul_max+1)], [2], [1])
    calc_pll_muldiv(33.333333, 1666.666667, [i for i in range(z7.pll_mul_min, z7.pll_mul_max+1)], [2] + [i for i in range(z7.pll_muldiv_min_abs, z7.pll_muldiv_max_abs+1)], [1], opt='div')

