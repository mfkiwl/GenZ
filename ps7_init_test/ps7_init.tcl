proc ps7_pll_init_data_3_0 {} {
puts "slcr slcr_unlock unlock_key: 0xdf0d"
mask_write 0XF8000008 0x0000FFFF 0x0000DF0D
puts "slcr arm_pll_cfg pll_res: 0x2"
mask_write 0XF8000110 0x000000F0 0x00000020
puts "slcr arm_pll_cfg pll_cp: 0x2"
mask_write 0XF8000110 0x00000F00 0x00000200
puts "slcr arm_pll_cfg lock_cnt: 0xfa"
mask_write 0XF8000110 0x003FF000 0x000FA000
puts "slcr arm_pll_ctrl pll_fdiv: 0x28"
mask_write 0XF8000100 0x0007F000 0x00028000
puts "slcr arm_pll_ctrl pll_bypass_force: 0x1"
mask_write 0XF8000100 0x00000010 0x00000010
puts "slcr arm_pll_ctrl pll_reset: 0x1"
mask_write 0XF8000100 0x00000001 0x00000001
puts "slcr arm_pll_ctrl pll_reset: 0x0"
mask_write 0XF8000100 0x00000001 0x00000000
puts "slcr pll_status arm_pll_lock: 0x1"
mask_poll 0XF800010C 0x00000001
puts "slcr arm_pll_ctrl pll_bypass_force: 0x0"
mask_write 0XF8000100 0x00000010 0x00000000
puts "slcr arm_clk_ctrl srcsel: 0x0"
mask_write 0XF8000120 0x00000030 0x00000000
puts "slcr arm_clk_ctrl divisor: 0x2"
mask_write 0XF8000120 0x00003F00 0x00000200
puts "slcr arm_clk_ctrl cpu_6or4xclkact: 0x1"
mask_write 0XF8000120 0x01000000 0x01000000
puts "slcr arm_clk_ctrl cpu_3or2xclkact: 0x1"
mask_write 0XF8000120 0x02000000 0x02000000
puts "slcr arm_clk_ctrl cpu_1xclkact: 0x1"
mask_write 0XF8000120 0x08000000 0x08000000
puts "slcr arm_clk_ctrl cpu_peri_clkact: 0x1"
mask_write 0XF8000120 0x10000000 0x10000000
puts "slcr ddr_pll_cfg pll_res: 0x2"
mask_write 0XF8000114 0x000000F0 0x00000020
puts "slcr ddr_pll_cfg pll_cp: 0x2"
mask_write 0XF8000114 0x00000F00 0x00000200
puts "slcr ddr_pll_cfg lock_cnt: 0x12c"
mask_write 0XF8000114 0x003FF000 0x0012C000
puts "slcr ddr_pll_ctrl pll_fdiv: 0x20"
mask_write 0XF8000104 0x0007F000 0x00020000
puts "slcr ddr_pll_ctrl pll_bypass_force: 0x1"
mask_write 0XF8000104 0x00000010 0x00000010
puts "slcr ddr_pll_ctrl pll_reset: 0x1"
mask_write 0XF8000104 0x00000001 0x00000001
puts "slcr ddr_pll_ctrl pll_reset: 0x0"
mask_write 0XF8000104 0x00000001 0x00000000
puts "slcr pll_status ddr_pll_lock: 0x1"
mask_poll 0XF800010C 0x00000002
puts "slcr ddr_pll_ctrl pll_bypass_force: 0x0"
mask_write 0XF8000104 0x00000010 0x00000000
puts "slcr ddr_clk_ctrl ddr_3xclkact: 0x1"
mask_write 0XF8000124 0x00000001 0x00000001
puts "slcr ddr_clk_ctrl ddr_2xclkact: 0x1"
mask_write 0XF8000124 0x00000002 0x00000002
puts "slcr ddr_clk_ctrl ddr_3xclk_divisor: 0x2"
mask_write 0XF8000124 0x03F00000 0x00200000
puts "slcr ddr_clk_ctrl ddr_2xclk_divisor: 0x3"
mask_write 0XF8000124 0xFC000000 0x0C000000
puts "slcr io_pll_cfg pll_res: 0xc"
mask_write 0XF8000118 0x000000F0 0x000000C0
puts "slcr io_pll_cfg pll_cp: 0x2"
mask_write 0XF8000118 0x00000F00 0x00000200
puts "slcr io_pll_cfg lock_cnt: 0x145"
mask_write 0XF8000118 0x003FF000 0x00145000
puts "slcr io_pll_ctrl pll_fdiv: 0x1e"
mask_write 0XF8000108 0x0007F000 0x0001E000
puts "slcr io_pll_ctrl pll_bypass_force: 0x1"
mask_write 0XF8000108 0x00000010 0x00000010
puts "slcr io_pll_ctrl pll_reset: 0x1"
mask_write 0XF8000108 0x00000001 0x00000001
puts "slcr io_pll_ctrl pll_reset: 0x0"
mask_write 0XF8000108 0x00000001 0x00000000
puts "slcr pll_status io_pll_lock: 0x1"
mask_poll 0XF800010C 0x00000004
puts "slcr io_pll_ctrl pll_bypass_force: 0x0"
mask_write 0XF8000108 0x00000010 0x00000000
puts "slcr slcr_lock lock_key: 0x767b"
mask_write 0XF8000004 0x0000FFFF 0x0000767B

}
proc ps7_clock_init_data_3_0 {} {
puts "slcr slcr_unlock unlock_key: 0xdf0d"
mask_write 0XF8000008 0x0000FFFF 0x0000DF0D
puts "slcr dci_clk_ctrl clkact: 0x1"
mask_write 0XF8000128 0x00000001 0x00000001
puts "slcr dci_clk_ctrl divisor0: 0x35"
mask_write 0XF8000128 0x00003F00 0x00003500
puts "slcr dci_clk_ctrl divisor1: 0x2"
mask_write 0XF8000128 0x03F00000 0x00200000
puts "slcr sdio_clk_ctrl clkact0: 0x1"
mask_write 0XF8000150 0x00000001 0x00000001
puts "slcr sdio_clk_ctrl clkact1: 0x1"
mask_write 0XF8000150 0x00000002 0x00000002
puts "slcr sdio_clk_ctrl srcsel: 0x0"
mask_write 0XF8000150 0x00000030 0x00000000
puts "slcr sdio_clk_ctrl divisor: 0xa"
mask_write 0XF8000150 0x00003F00 0x00000A00
puts "slcr uart_clk_ctrl clkact0: 0x1"
mask_write 0XF8000154 0x00000001 0x00000001
puts "slcr uart_clk_ctrl clkact1: 0x1"
mask_write 0XF8000154 0x00000002 0x00000002
puts "slcr uart_clk_ctrl srcsel: 0x0"
mask_write 0XF8000154 0x00000030 0x00000000
puts "slcr uart_clk_ctrl divisor: 0xa"
mask_write 0XF8000154 0x00003F00 0x00000A00
puts "slcr pcap_clk_ctrl clkact: 0x1"
mask_write 0XF8000168 0x00000001 0x00000001
puts "slcr pcap_clk_ctrl srcsel: 0x0"
mask_write 0XF8000168 0x00000030 0x00000000
puts "slcr pcap_clk_ctrl divisor: 0x5"
mask_write 0XF8000168 0x00003F00 0x00000500
puts "slcr fpga0_clk_ctrl srcsel: 0x0"
mask_write 0XF8000170 0x00000030 0x00000000
puts "slcr fpga0_clk_ctrl divisor0: 0xa"
mask_write 0XF8000170 0x00003F00 0x00000A00
puts "slcr fpga0_clk_ctrl divisor1: 0x1"
mask_write 0XF8000170 0x03F00000 0x00100000
puts "slcr fpga1_clk_ctrl srcsel: 0x0"
mask_write 0XF8000180 0x00000030 0x00000000
puts "slcr fpga1_clk_ctrl divisor0: 0x14"
mask_write 0XF8000180 0x00003F00 0x00001400
puts "slcr fpga1_clk_ctrl divisor1: 0x1"
mask_write 0XF8000180 0x03F00000 0x00100000
puts "slcr fpga2_clk_ctrl srcsel: 0x0"
mask_write 0XF8000190 0x00000030 0x00000000
puts "slcr fpga2_clk_ctrl divisor0: 0x28"
mask_write 0XF8000190 0x00003F00 0x00002800
puts "slcr fpga2_clk_ctrl divisor1: 0x1"
mask_write 0XF8000190 0x03F00000 0x00100000
puts "slcr fpga3_clk_ctrl srcsel: 0x0"
mask_write 0XF80001A0 0x00000030 0x00000000
puts "slcr fpga3_clk_ctrl divisor0: 0x14"
mask_write 0XF80001A0 0x00003F00 0x00001400
puts "slcr fpga3_clk_ctrl divisor1: 0x1"
mask_write 0XF80001A0 0x03F00000 0x00100000
puts "slcr clk_621_true clk_621_true: 0x1"
mask_write 0XF80001C4 0x00000001 0x00000001
puts "slcr aper_clk_ctrl dma_cpu_2xclkact: 0x1"
mask_write 0XF800012C 0x00000001 0x00000001
puts "slcr aper_clk_ctrl usb0_cpu_1xclkact: 0x0"
mask_write 0XF800012C 0x00000004 0x00000000
puts "slcr aper_clk_ctrl usb1_cpu_1xclkact: 0x0"
mask_write 0XF800012C 0x00000008 0x00000000
puts "slcr aper_clk_ctrl gem0_cpu_1xclkact: 0x0"
mask_write 0XF800012C 0x00000040 0x00000000
puts "slcr aper_clk_ctrl gem1_cpu_1xclkact: 0x0"
mask_write 0XF800012C 0x00000080 0x00000000
puts "slcr aper_clk_ctrl sdi0_cpu_1xclkact: 0x1"
mask_write 0XF800012C 0x00000400 0x00000400
puts "slcr aper_clk_ctrl sdi1_cpu_1xclkact: 0x1"
mask_write 0XF800012C 0x00000800 0x00000800
puts "slcr aper_clk_ctrl spi0_cpu_1xclkact: 0x0"
mask_write 0XF800012C 0x00004000 0x00000000
puts "slcr aper_clk_ctrl spi1_cpu_1xclkact: 0x0"
mask_write 0XF800012C 0x00008000 0x00000000
puts "slcr aper_clk_ctrl can0_cpu_1xclkact: 0x0"
mask_write 0XF800012C 0x00010000 0x00000000
puts "slcr aper_clk_ctrl can1_cpu_1xclkact: 0x0"
mask_write 0XF800012C 0x00020000 0x00000000
puts "slcr aper_clk_ctrl i2c0_cpu_1xclkact: 0x0"
mask_write 0XF800012C 0x00040000 0x00000000
puts "slcr aper_clk_ctrl i2c1_cpu_1xclkact: 0x0"
mask_write 0XF800012C 0x00080000 0x00000000
puts "slcr aper_clk_ctrl uart0_cpu_1xclkact: 0x1"
mask_write 0XF800012C 0x00100000 0x00100000
puts "slcr aper_clk_ctrl uart1_cpu_1xclkact: 0x1"
mask_write 0XF800012C 0x00200000 0x00200000
puts "slcr aper_clk_ctrl gpio_cpu_1xclkact: 0x1"
mask_write 0XF800012C 0x00400000 0x00400000
puts "slcr aper_clk_ctrl lqspi_cpu_1xclkact: 0x0"
mask_write 0XF800012C 0x00800000 0x00000000
puts "slcr aper_clk_ctrl smc_cpu_1xclkact: 0x0"
mask_write 0XF800012C 0x01000000 0x00000000
puts "slcr slcr_lock lock_key: 0x767b"
mask_write 0XF8000004 0x0000FFFF 0x0000767B

}
proc ps7_mio_init_data_3_0 {} {
puts "slcr slcr_unlock unlock_key: 0xdf0d"
mask_write 0XF8000008 0x0000FFFF 0x0000DF0D
puts "slcr MIO_PIN_10 L0_SEL: 0x0"
mask_write 0XF8000728 0x00000002 0x00000000
puts "slcr MIO_PIN_10 L1_SEL: 0x0"
mask_write 0XF8000728 0x00000004 0x00000000
puts "slcr MIO_PIN_10 L2_SEL: 0x0"
mask_write 0XF8000728 0x00000018 0x00000000
puts "slcr MIO_PIN_10 L3_SEL: 0x7"
mask_write 0XF8000728 0x000000E0 0x000000E0
puts "slcr MIO_PIN_10 TRI_ENABLE: 0x0"
mask_write 0XF8000728 0x00000001 0x00000000
puts "slcr MIO_PIN_10 Speed: 0x0"
mask_write 0XF8000728 0x00000100 0x00000000
puts "slcr MIO_PIN_10 IO_Type: 0x3"
mask_write 0XF8000728 0x00000E00 0x00000600
puts "slcr MIO_PIN_10 PULLUP: 0x1"
mask_write 0XF8000728 0x00001000 0x00001000
puts "slcr MIO_PIN_10 DisableRcvr: 0x0"
mask_write 0XF8000728 0x00002000 0x00000000
puts "slcr MIO_PIN_11 L0_SEL: 0x0"
mask_write 0XF800072C 0x00000002 0x00000000
puts "slcr MIO_PIN_11 L1_SEL: 0x0"
mask_write 0XF800072C 0x00000004 0x00000000
puts "slcr MIO_PIN_11 L2_SEL: 0x0"
mask_write 0XF800072C 0x00000018 0x00000000
puts "slcr MIO_PIN_11 L3_SEL: 0x7"
mask_write 0XF800072C 0x000000E0 0x000000E0
puts "slcr MIO_PIN_11 TRI_ENABLE: 0x0"
mask_write 0XF800072C 0x00000001 0x00000000
puts "slcr MIO_PIN_11 Speed: 0x0"
mask_write 0XF800072C 0x00000100 0x00000000
puts "slcr MIO_PIN_11 IO_Type: 0x3"
mask_write 0XF800072C 0x00000E00 0x00000600
puts "slcr MIO_PIN_11 PULLUP: 0x1"
mask_write 0XF800072C 0x00001000 0x00001000
puts "slcr MIO_PIN_11 DisableRcvr: 0x0"
mask_write 0XF800072C 0x00002000 0x00000000
puts "slcr MIO_PIN_40 L0_SEL: 0x0"
mask_write 0XF80007A0 0x00000002 0x00000000
puts "slcr MIO_PIN_40 L1_SEL: 0x0"
mask_write 0XF80007A0 0x00000004 0x00000000
puts "slcr MIO_PIN_40 L2_SEL: 0x0"
mask_write 0XF80007A0 0x00000018 0x00000000
puts "slcr MIO_PIN_40 L3_SEL: 0x4"
mask_write 0XF80007A0 0x000000E0 0x00000080
puts "slcr MIO_PIN_40 TRI_ENABLE: 0x0"
mask_write 0XF80007A0 0x00000001 0x00000000
puts "slcr MIO_PIN_40 Speed: 0x0"
mask_write 0XF80007A0 0x00000100 0x00000000
puts "slcr MIO_PIN_40 IO_Type: 0x3"
mask_write 0XF80007A0 0x00000E00 0x00000600
puts "slcr MIO_PIN_40 PULLUP: 0x1"
mask_write 0XF80007A0 0x00001000 0x00001000
puts "slcr MIO_PIN_40 DisableRcvr: 0x0"
mask_write 0XF80007A0 0x00002000 0x00000000
puts "slcr MIO_PIN_41 L0_SEL: 0x0"
mask_write 0XF80007A4 0x00000002 0x00000000
puts "slcr MIO_PIN_41 L1_SEL: 0x0"
mask_write 0XF80007A4 0x00000004 0x00000000
puts "slcr MIO_PIN_41 L2_SEL: 0x0"
mask_write 0XF80007A4 0x00000018 0x00000000
puts "slcr MIO_PIN_41 L3_SEL: 0x4"
mask_write 0XF80007A4 0x000000E0 0x00000080
puts "slcr MIO_PIN_41 TRI_ENABLE: 0x0"
mask_write 0XF80007A4 0x00000001 0x00000000
puts "slcr MIO_PIN_41 Speed: 0x0"
mask_write 0XF80007A4 0x00000100 0x00000000
puts "slcr MIO_PIN_41 IO_Type: 0x3"
mask_write 0XF80007A4 0x00000E00 0x00000600
puts "slcr MIO_PIN_41 PULLUP: 0x1"
mask_write 0XF80007A4 0x00001000 0x00001000
puts "slcr MIO_PIN_41 DisableRcvr: 0x0"
mask_write 0XF80007A4 0x00002000 0x00000000
puts "slcr MIO_PIN_42 L0_SEL: 0x0"
mask_write 0XF80007A8 0x00000002 0x00000000
puts "slcr MIO_PIN_42 L1_SEL: 0x0"
mask_write 0XF80007A8 0x00000004 0x00000000
puts "slcr MIO_PIN_42 L2_SEL: 0x0"
mask_write 0XF80007A8 0x00000018 0x00000000
puts "slcr MIO_PIN_42 L3_SEL: 0x4"
mask_write 0XF80007A8 0x000000E0 0x00000080
puts "slcr MIO_PIN_42 TRI_ENABLE: 0x0"
mask_write 0XF80007A8 0x00000001 0x00000000
puts "slcr MIO_PIN_42 Speed: 0x0"
mask_write 0XF80007A8 0x00000100 0x00000000
puts "slcr MIO_PIN_42 IO_Type: 0x3"
mask_write 0XF80007A8 0x00000E00 0x00000600
puts "slcr MIO_PIN_42 PULLUP: 0x1"
mask_write 0XF80007A8 0x00001000 0x00001000
puts "slcr MIO_PIN_42 DisableRcvr: 0x0"
mask_write 0XF80007A8 0x00002000 0x00000000
puts "slcr MIO_PIN_43 L0_SEL: 0x0"
mask_write 0XF80007AC 0x00000002 0x00000000
puts "slcr MIO_PIN_43 L1_SEL: 0x0"
mask_write 0XF80007AC 0x00000004 0x00000000
puts "slcr MIO_PIN_43 L2_SEL: 0x0"
mask_write 0XF80007AC 0x00000018 0x00000000
puts "slcr MIO_PIN_43 L3_SEL: 0x4"
mask_write 0XF80007AC 0x000000E0 0x00000080
puts "slcr MIO_PIN_43 TRI_ENABLE: 0x0"
mask_write 0XF80007AC 0x00000001 0x00000000
puts "slcr MIO_PIN_43 Speed: 0x0"
mask_write 0XF80007AC 0x00000100 0x00000000
puts "slcr MIO_PIN_43 IO_Type: 0x3"
mask_write 0XF80007AC 0x00000E00 0x00000600
puts "slcr MIO_PIN_43 PULLUP: 0x1"
mask_write 0XF80007AC 0x00001000 0x00001000
puts "slcr MIO_PIN_43 DisableRcvr: 0x0"
mask_write 0XF80007AC 0x00002000 0x00000000
puts "slcr MIO_PIN_44 L0_SEL: 0x0"
mask_write 0XF80007B0 0x00000002 0x00000000
puts "slcr MIO_PIN_44 L1_SEL: 0x0"
mask_write 0XF80007B0 0x00000004 0x00000000
puts "slcr MIO_PIN_44 L2_SEL: 0x0"
mask_write 0XF80007B0 0x00000018 0x00000000
puts "slcr MIO_PIN_44 L3_SEL: 0x4"
mask_write 0XF80007B0 0x000000E0 0x00000080
puts "slcr MIO_PIN_44 TRI_ENABLE: 0x0"
mask_write 0XF80007B0 0x00000001 0x00000000
puts "slcr MIO_PIN_44 Speed: 0x0"
mask_write 0XF80007B0 0x00000100 0x00000000
puts "slcr MIO_PIN_44 IO_Type: 0x3"
mask_write 0XF80007B0 0x00000E00 0x00000600
puts "slcr MIO_PIN_44 PULLUP: 0x1"
mask_write 0XF80007B0 0x00001000 0x00001000
puts "slcr MIO_PIN_44 DisableRcvr: 0x0"
mask_write 0XF80007B0 0x00002000 0x00000000
puts "slcr MIO_PIN_45 L0_SEL: 0x0"
mask_write 0XF80007B4 0x00000002 0x00000000
puts "slcr MIO_PIN_45 L1_SEL: 0x0"
mask_write 0XF80007B4 0x00000004 0x00000000
puts "slcr MIO_PIN_45 L2_SEL: 0x0"
mask_write 0XF80007B4 0x00000018 0x00000000
puts "slcr MIO_PIN_45 L3_SEL: 0x4"
mask_write 0XF80007B4 0x000000E0 0x00000080
puts "slcr MIO_PIN_45 TRI_ENABLE: 0x0"
mask_write 0XF80007B4 0x00000001 0x00000000
puts "slcr MIO_PIN_45 Speed: 0x0"
mask_write 0XF80007B4 0x00000100 0x00000000
puts "slcr MIO_PIN_45 IO_Type: 0x3"
mask_write 0XF80007B4 0x00000E00 0x00000600
puts "slcr MIO_PIN_45 PULLUP: 0x1"
mask_write 0XF80007B4 0x00001000 0x00001000
puts "slcr MIO_PIN_45 DisableRcvr: 0x0"
mask_write 0XF80007B4 0x00002000 0x00000000
puts "slcr sd0_wp_cd_sel sdio0_wp_sel: 0x37"
mask_write 0XF8000830 0x0000003F 0x00000037
puts "slcr sd0_wp_cd_sel sdio0_cd_sel: 0x38"
mask_write 0XF8000830 0x003F0000 0x00380000
puts "slcr slcr_lock lock_key: 0x767b"
mask_write 0XF8000004 0x0000FFFF 0x0000767B

}
proc ps7_ddr_init_data_3_0 {} {

}
proc ps7_peripherals_init_data_3_0 {} {
puts "slcr slcr_unlock unlock_key: 0xdf0d"
mask_write 0XF8000008 0x0000FFFF 0x0000DF0D
puts "uart0 baud_rate_divider_reg0 bdiv: 0x6"
mask_write 0XE0000034 0x000000FF 0x00000006
puts "uart0 xuartps_baudgen_offset cd: 0x7c"
mask_write 0XE0000018 0x0000FFFF 0x0000007C
puts "uart0 xuartps_cr_offset txen: 0x1"
mask_write 0XE0000000 0x00000010 0x00000010
puts "uart0 xuartps_cr_offset rxen: 0x1"
mask_write 0XE0000000 0x00000004 0x00000004
puts "uart0 xuartps_cr_offset txdis: 0x0"
mask_write 0XE0000000 0x00000020 0x00000000
puts "uart0 xuartps_cr_offset rxdis: 0x0"
mask_write 0XE0000000 0x00000008 0x00000000
puts "uart0 xuartps_cr_offset stpbrk: 0x0"
mask_write 0XE0000000 0x00000100 0x00000000
puts "uart0 xuartps_cr_offset sttbrk: 0x0"
mask_write 0XE0000000 0x00000080 0x00000000
puts "uart0 xuartps_cr_offset rstto: 0x0"
mask_write 0XE0000000 0x00000040 0x00000000
puts "uart0 xuartps_cr_offset txres: 0x1"
mask_write 0XE0000000 0x00000002 0x00000002
puts "uart0 xuartps_cr_offset rxres: 0x1"
mask_write 0XE0000000 0x00000001 0x00000001
puts "uart0 xuartps_mr_offset chmode: 0x0"
mask_write 0XE0000004 0x00000300 0x00000000
puts "uart0 xuartps_mr_offset nbstop: 0x0"
mask_write 0XE0000004 0x000000C0 0x00000000
puts "uart0 xuartps_mr_offset par: 0x4"
mask_write 0XE0000004 0x00000038 0x00000020
puts "uart0 xuartps_mr_offset chrl: 0x0"
mask_write 0XE0000004 0x00000006 0x00000000
puts "uart0 xuartps_mr_offset clks: 0x0"
mask_write 0XE0000004 0x00000001 0x00000000
puts "uart1 baud_rate_divider_reg0 bdiv: 0xa"
mask_write 0XE0001034 0x000000FF 0x0000000A
puts "uart1 xuartps_baudgen_offset cd: 0x3b3"
mask_write 0XE0001018 0x0000FFFF 0x000003B3
puts "uart1 xuartps_cr_offset txen: 0x1"
mask_write 0XE0001000 0x00000010 0x00000010
puts "uart1 xuartps_cr_offset rxen: 0x1"
mask_write 0XE0001000 0x00000004 0x00000004
puts "uart1 xuartps_cr_offset txdis: 0x0"
mask_write 0XE0001000 0x00000020 0x00000000
puts "uart1 xuartps_cr_offset rxdis: 0x0"
mask_write 0XE0001000 0x00000008 0x00000000
puts "uart1 xuartps_cr_offset stpbrk: 0x0"
mask_write 0XE0001000 0x00000100 0x00000000
puts "uart1 xuartps_cr_offset sttbrk: 0x0"
mask_write 0XE0001000 0x00000080 0x00000000
puts "uart1 xuartps_cr_offset rstto: 0x0"
mask_write 0XE0001000 0x00000040 0x00000000
puts "uart1 xuartps_cr_offset txres: 0x1"
mask_write 0XE0001000 0x00000002 0x00000002
puts "uart1 xuartps_cr_offset rxres: 0x1"
mask_write 0XE0001000 0x00000001 0x00000001
puts "uart1 xuartps_mr_offset chmode: 0x0"
mask_write 0XE0001004 0x00000300 0x00000000
puts "uart1 xuartps_mr_offset nbstop: 0x0"
mask_write 0XE0001004 0x000000C0 0x00000000
puts "uart1 xuartps_mr_offset par: 0x4"
mask_write 0XE0001004 0x00000038 0x00000020
puts "uart1 xuartps_mr_offset chrl: 0x0"
mask_write 0XE0001004 0x00000006 0x00000000
puts "uart1 xuartps_mr_offset clks: 0x0"
mask_write 0XE0001004 0x00000001 0x00000000
puts "qspi xqspips_cr_offset holdb_dr: 0x1"
mask_write 0XE000D000 0x00080000 0x00080000
puts "devcfg xdcfg_ctrl_offset pcfg_por_cnt_4k: 0x0"
mask_write 0XF8007000 0x20000000 0x00000000
puts "slcr slcr_lock lock_key: 0x767b"
mask_write 0XF8000004 0x0000FFFF 0x0000767B

}
proc ps7_post_config_3_0 {} {
puts "slcr slcr_unlock unlock_key: 0xdf0d"
mask_write 0XF8000008 0x0000FFFF 0x0000DF0D
puts "slcr lvl_shftr_en fullreg: 0xf"
mwr -force 0XF8000900 0x0000000F
puts "slcr fpga_rst_ctrl fullreg: 0x0"
mwr -force 0XF8000240 0x00000000
puts "slcr slcr_lock lock_key: 0x767b"
mask_write 0XF8000004 0x0000FFFF 0x0000767B

}

proc mask_poll { addr mask } {
    set cnt 1
	set val 0
    while { $val == 0 } {
        set val "0x[string range [mrd $addr] end-8 end]"
        set val [expr $val & $mask]
		incr cnt
        if { $cnt == 100000 } {
          puts "MASKPOLL FAILED AT ADDRESS: $addr MASK: $mask"
          break
        }
    }
}

proc ps7_post_config {} {
    set saved_mode [configparams force-mem-accesses]
    configparams force-mem-accesses 1
	ps7_post_config_3_0
	configparams force-mem-accesses $saved_mode
}

proc ps7_init {} {
	ps7_mio_init_data_3_0
	ps7_pll_init_data_3_0
	ps7_clock_init_data_3_0
	ps7_ddr_init_data_3_0
	ps7_peripherals_init_data_3_0
}
