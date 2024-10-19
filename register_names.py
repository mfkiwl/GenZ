#!/usr/bin/env python3
import re
import sys
import copy

# BaseRegister -> Entry -> Field
# No data is stored here: only skeleton registers/masks

class Entry:
    def __init__(self, name, addr, width, tp, reset, description):
        self.name = name
        self.addr = addr
        self.width = width
        self.tp = tp
        self.reset = reset
        self.description = description
        self.fields = {}

    def name(self):
        return self.name

    def addr(self):
        return self.addr

    def add_field(self, field, mask):
        self.fields[field] = mask

    def get_field_mask(self, field):
        return self.fields[field]

    def show(self):
        print(f"{self.name}, 0x{self.addr:08x}")
        for f in self.fields:
            print(f"\t{f}, 0x{self.fields[f]:08x}")


class BaseRegister:
    def __init__(self, baseaddr, entries, name=""):
        self.name = name
        self.baseaddr = baseaddr
        self.entries = entries

    def update_entry_field(self, entryaddr, fieldname, fieldmask):
        # todo: check if belong!
        e = self.a2e(entryaddr - self.baseaddr)
        if e:
            e.add_field(fieldname, fieldmask)
            return True
        return False

    def n2a(self, name, absolute=False):
        addr = -1
        for e in self.entries:
            if e.name.lower() == name.lower():
                addr = e.addr;
        if addr == -1:
            raise Exception("Entry ", name, " not found in BaseRegister ", self.name, " !")
        # if absolute:
            # addr += self.baseaddr
        return addr

    def a2e(self, addr):
        for e in self.entries:
            if e.addr == addr:
                return e
        print(hex(addr + self.baseaddr), ' not found in BaseRegister ', self.name, '!')
        return None
        # raise Exception("Entry ", hex(addr), " not found in Register ", self.name, " !")

    def a2n(self, addr):
        name = ''
        for e in self.entries:
            if e.addr == addr:
                name = e.name()
        if name == '':
            raise Exception("Entry ", hex(addr), " not found in BaseRegister ", self.name, "!")
        return name
    
    def show(self):
        # print(f"{self.name}")
        for e in self.entries:
            e.show()
            


# From UG585, ZYNQ 7000 TRM, Page 1632
# Register Name, Address, Width, Type, Reset Value, Description
# Page 832: all base register list
# periperals like uart, gem, usb, sd, etc has 0 and 1, and address of these are maintained by software.
uart0 = 0xe0000000
uart1 = 0xe0001000
slcr = BaseRegister(0xf8000000, [
    Entry("SCL",0x00000000,32,"rw",0x00000000,"Secure Configuration Lock"),
    Entry("SLCR_LOCK",0x00000004,32,"wo",0x00000000,"SLCR Write Protection Lock"),
    Entry("SLCR_UNLOCK",0x00000008,32,"wo",0x00000000,"SLCR Write Protection Unlock"),
    Entry("SLCR_LOCKSTA",0x0000000C,32,"ro",0x00000001,"SLCR Write Protection Status"),
    Entry("ARM_PLL_CTRL",0x00000100,32,"rw",0x0001A008,"Arm PLL Control"),
    Entry("DDR_PLL_CTRL",0x00000104,32,"rw",0x0001A008,"DDR PLL Control"),
    Entry("IO_PLL_CTRL",0x00000108,32,"rw",0x0001A008,"IO PLL Control"),
    Entry("PLL_STATUS",0x0000010C,32,"ro",0x0000003F,"PLL Status"),
    Entry("ARM_PLL_CFG",0x00000110,32,"rw",0x00177EA0,"Arm PLL Configuration"),
    Entry("DDR_PLL_CFG",0x00000114,32,"rw",0x00177EA0,"DDR PLL Configuration"),
    Entry("IO_PLL_CFG",0x00000118,32,"rw",0x00177EA0,"IO PLL Configuration"),
    Entry("ARM_CLK_CTRL",0x00000120,32,"rw",0x1F000400,"CPU Clock Control"),
    Entry("DDR_CLK_CTRL",0x00000124,32,"rw",0x18400003,"DDR Clock Control"),
    Entry("DCI_CLK_CTRL",0x00000128,32,"rw",0x01E03201,"DCI clock control"),
    Entry("APER_CLK_CTRL",0x0000012C,32,"rw",0x01FFCCCD,"AMBA Peripheral Clock Control"),
    Entry("USB0_CLK_CTRL",0x00000130,32,"rw",0x00101941,"USB 0 ULPI Clock Control"),
    Entry("USB1_CLK_CTRL",0x00000134,32,"rw",0x00101941,"USB 1 ULPI Clock Control"),
    Entry("GEM0_RCLK_CTRL",0x00000138,32,"rw",0x00000001,"GigE 0 Rx Clock and Rx Signals Select"),
    Entry("GEM1_RCLK_CTRL",0x0000013C,32,"rw",0x00000001,"GigE 1 Rx Clock and Rx Signals Select"),
    Entry("GEM0_CLK_CTRL",0x00000140,32,"rw",0x00003C01,"GigE 0 Ref Clock Control"),
    Entry("GEM1_CLK_CTRL",0x00000144,32,"rw",0x00003C01,"GigE 1 Ref Clock Control"),
    Entry("SMC_CLK_CTRL",0x00000148,32,"rw",0x00003C21,"SMC Ref Clock Control"),
    Entry("LQSPI_CLK_CTRL",0x0000014C,32,"rw",0x00002821,"Quad SPI Ref Clock Control"),
    Entry("SDIO_CLK_CTRL",0x00000150,32,"rw",0x00001E03,"SDIO Ref Clock Control"),
    Entry("UART_CLK_CTRL",0x00000154,32,"rw",0x00003F03,"UART Ref Clock Control"),
    Entry("SPI_CLK_CTRL",0x00000158,32,"rw",0x00003F03,"SPI Ref Clock Control"),
    Entry("CAN_CLK_CTRL",0x0000015C,32,"rw",0x00501903,"CAN Ref Clock Control"),
    Entry("CAN_MIOCLK_CTRL",0x00000160,32,"rw",0x00000000,"CAN MIO Clock Control"),
    Entry("DBG_CLK_CTRL",0x00000164,32,"rw",0x00000F03,"SoC Debug Clock Control"),
    Entry("PCAP_CLK_CTRL",0x00000168,32,"rw",0x00000F01,"PCAP Clock Control"),
    Entry("TOPSW_CLK_CTRL",0x0000016C,32,"rw",0x00000000,"Central Interconnect Clock Control"),
    Entry("FPGA0_CLK_CTRL",0x00000170,32,"rw",0x00101800,"PL Clock 0 Output control"),
    Entry("FPGA0_THR_CTRL",0x00000174,32,"rw",0x00000000,"PL Clock 0 Throttle control"),
    Entry("FPGA0_THR_CNT",0x00000178,32,"rw",0x00000000,"PL Clock 0 Throttle Count control"),
    Entry("FPGA0_THR_STA",0x0000017C,32,"ro",0x00010000,"PL Clock 0 Throttle Status read"),
    Entry("FPGA1_CLK_CTRL",0x00000180,32,"rw",0x00101800,"PL Clock 1 Output control"),
    Entry("FPGA1_THR_CTRL",0x00000184,32,"rw",0x00000000,"PL Clock 1 Throttle control"),
    Entry("FPGA1_THR_CNT",0x00000188,32,"rw",0x00000000,"PL Clock 1 Throttle Count"),
    Entry("FPGA1_THR_STA",0x0000018C,32,"ro",0x00010000,"PL Clock 1 Throttle Status control"),
    Entry("FPGA2_CLK_CTRL",0x00000190,32,"rw",0x00101800,"PL Clock 2 output control"),
    Entry("FPGA2_THR_CTRL",0x00000194,32,"rw",0x00000000,"PL Clock 2 Throttle Control"),
    Entry("FPGA2_THR_CNT",0x00000198,32,"rw",0x00000000,"PL Clock 2 Throttle Count"),
    Entry("FPGA2_THR_STA",0x0000019C,32,"ro",0x00010000,"PL Clock 2 Throttle Status"),
    Entry("FPGA3_CLK_CTRL",0x000001A0,32,"rw",0x00101800,"PL Clock 3 output control"),
    Entry("FPGA3_THR_CTRL",0x000001A4,32,"rw",0x00000000,"PL Clock 3 Throttle Control"),
    Entry("FPGA3_THR_CNT",0x000001A8,32,"rw",0x00000000,"PL Clock 3 Throttle Count"),
    Entry("FPGA3_THR_STA",0x000001AC,32,"ro",0x00010000,"PL Clock 3 Throttle Status"),
    Entry("CLK_621_TRUE",0x000001C4,32,"rw",0x00000001,"CPU Clock Ratio Mode select"),
    Entry("PSS_RST_CTRL",0x00000200,32,"rw",0x00000000,"PS Software Reset Control"),
    Entry("DDR_RST_CTRL",0x00000204,32,"rw",0x00000000,"DDR Software Reset Control"),
    Entry("TOPSW_RST_CTRL",0x00000208,32,"rw",0x00000000,"Central Interconnect Reset Control"),
    Entry("DMAC_RST_CTRL",0x0000020C,32,"rw",0x00000000,"DMAC Software Reset Control"),
    Entry("USB_RST_CTRL",0x00000210,32,"rw",0x00000000,"USB Software Reset Control"),
    Entry("GEM_RST_CTRL",0x00000214,32,"rw",0x00000000,"Gigabit Ethernet SW Reset Control"),
    Entry("SDIO_RST_CTRL",0x00000218,32,"rw",0x00000000,"SDIO Software Reset Control"),
    Entry("SPI_RST_CTRL",0x0000021C,32,"rw",0x00000000,"SPI Software Reset Control"),
    Entry("CAN_RST_CTRL",0x00000220,32,"rw",0x00000000,"CAN Software Reset Control"),
    Entry("I2C_RST_CTRL",0x00000224,32,"rw",0x00000000,"I2C Software Reset Control"),
    Entry("UART_RST_CTRL",0x00000228,32,"rw",0x00000000,"UART Software Reset Control"),
    Entry("GPIO_RST_CTRL",0x0000022C,32,"rw",0x00000000,"GPIO Software Reset Control"),
    Entry("LQSPI_RST_CTRL",0x00000230,32,"rw",0x00000000,"Quad SPI Software Reset Control"),
    Entry("SMC_RST_CTRL",0x00000234,32,"rw",0x00000000,"SMC Software Reset Control"),
    Entry("OCM_RST_CTRL",0x00000238,32,"rw",0x00000000,"OCM Software Reset Control"),
    Entry("FPGA_RST_CTRL",0x00000240,32,"rw",0x01F33F0F,"FPGA Software Reset Control"),
    Entry("A9_CPU_RST_CTRL",0x00000244,32,"rw",0x00000000,"CPU Reset and Clock control"),
    Entry("RS_AWDT_CTRL",0x0000024C,32,"rw",0x00000000,"Watchdog Timer Reset Control"),
    Entry("REBOOT_STATUS",0x00000258,32,"rw",0x00400000,"Reboot Status, persistent"),
    Entry("BOOT_MODE",0x0000025C,32,"mixed","x", "Boot Mode Strapping Pins"),
    Entry("APU_CTRL",0x00000300,32,"rw",0x00000000,"APU Control"),
    Entry("WDT_CLK_SEL",0x00000304,32,"rw",0x00000000,"SWDT clock source select"),
    Entry("TZ_DMA_NS",0x00000440,32,"rw",0x00000000,"DMAC TrustZone Config"),
    Entry("TZ_DMA_IRQ_NS",0x00000444,32,"rw",0x00000000,"DMAC TrustZone Config for Interrupts"),
    Entry("TZ_DMA_PERIPH_NS",0x00000448,32,"rw",0x00000000,"DMAC TrustZone Config for Peripherals"),
    Entry("PSS_IDCODE",0x00000530,32,"ro","x", "PS IDCODE"),
    Entry("DDR_URGENT",0x00000600,32,"rw",0x00000000,"DDR Urgent Control"),
    Entry("DDR_CAL_START",0x0000060C,32,"mixed",0x00000000,"DDR Calibration Start Triggers"),
    Entry("DDR_REF_START",0x00000614,32,"mixed",0x00000000,"DDR Refresh Start Triggers"),
    Entry("DDR_CMD_STA",0x00000618,32,"mixed",0x00000000,"DDR Command Store Status"),
    Entry("DDR_URGENT_SEL",0x0000061C,32,"rw",0x00000000,"DDR Urgent Select"),
    Entry("DDR_DFI_STATUS",0x00000620,32,"mixed",0x00000000,"DDR DFI status"),
    Entry("MIO_PIN_00",0x00000700,32,"rw",0x00001601,"MIO Pin 0 Control"),
    Entry("MIO_PIN_01",0x00000704,32,"rw",0x00001601,"MIO Pin 1 Control"),
    Entry("MIO_PIN_02",0x00000708,32,"rw",0x00000601,"MIO Pin 2 Control"),
    Entry("MIO_PIN_03",0x0000070C,32,"rw",0x00000601,"MIO Pin 3 Control"),
    Entry("MIO_PIN_04",0x00000710,32,"rw",0x00000601,"MIO Pin 4 Control"),
    Entry("MIO_PIN_05",0x00000714,32,"rw",0x00000601,"MIO Pin 5 Control"),
    Entry("MIO_PIN_06",0x00000718,32,"rw",0x00000601,"MIO Pin 6 Control"),
    Entry("MIO_PIN_07",0x0000071C,32,"rw",0x00000601,"MIO Pin 7 Control"),
    Entry("MIO_PIN_08",0x00000720,32,"rw",0x00000601,"MIO Pin 8 Control"),
    Entry("MIO_PIN_09",0x00000724,32,"rw",0x00001601,"MIO Pin 9 Control"),
    Entry("MIO_PIN_10",0x00000728,32,"rw",0x00001601,"MIO Pin 10 Control"),
    Entry("MIO_PIN_11",0x0000072C,32,"rw",0x00001601,"MIO Pin 11 Control"),
    Entry("MIO_PIN_12",0x00000730,32,"rw",0x00001601,"MIO Pin 12 Control"),
    Entry("MIO_PIN_13",0x00000734,32,"rw",0x00001601,"MIO Pin 13 Control"),
    Entry("MIO_PIN_14",0x00000738,32,"rw",0x00001601,"MIO Pin 14 Control"),
    Entry("MIO_PIN_15",0x0000073C,32,"rw",0x00001601,"MIO Pin 15 Control"),
    Entry("MIO_PIN_16",0x00000740,32,"rw",0x00001601,"MIO Pin 16 Control"),
    Entry("MIO_PIN_17",0x00000744,32,"rw",0x00001601,"MIO Pin 17 Control"),
    Entry("MIO_PIN_18",0x00000748,32,"rw",0x00001601,"MIO Pin 18 Control"),
    Entry("MIO_PIN_19",0x0000074C,32,"rw",0x00001601,"MIO Pin 19 Control"),
    Entry("MIO_PIN_20",0x00000750,32,"rw",0x00001601,"MIO Pin 20 Control"),
    Entry("MIO_PIN_21",0x00000754,32,"rw",0x00001601,"MIO Pin 21 Control"),
    Entry("MIO_PIN_22",0x00000758,32,"rw",0x00001601,"MIO Pin 22 Control"),
    Entry("MIO_PIN_23",0x0000075C,32,"rw",0x00001601,"MIO Pin 23 Control"),
    Entry("MIO_PIN_24",0x00000760,32,"rw",0x00001601,"MIO Pin 24 Control"),
    Entry("MIO_PIN_25",0x00000764,32,"rw",0x00001601,"MIO Pin 25 Control"),
    Entry("MIO_PIN_26",0x00000768,32,"rw",0x00001601,"MIO Pin 26 Control"),
    Entry("MIO_PIN_27",0x0000076C,32,"rw",0x00001601,"MIO Pin 27 Control"),
    Entry("MIO_PIN_28",0x00000770,32,"rw",0x00001601,"MIO Pin 28 Control"),
    Entry("MIO_PIN_29",0x00000774,32,"rw",0x00001601,"MIO Pin 29 Control"),
    Entry("MIO_PIN_30",0x00000778,32,"rw",0x00001601,"MIO Pin 30 Control"),
    Entry("MIO_PIN_31",0x0000077C,32,"rw",0x00001601,"MIO Pin 31 Control"),
    Entry("MIO_PIN_32",0x00000780,32,"rw",0x00001601,"MIO Pin 32 Control"),
    Entry("MIO_PIN_33",0x00000784,32,"rw",0x00001601,"MIO Pin 33 Control"),
    Entry("MIO_PIN_34",0x00000788,32,"rw",0x00001601,"MIO Pin 34 Control"),
    Entry("MIO_PIN_35",0x0000078C,32,"rw",0x00001601,"MIO Pin 35 Control"),
    Entry("MIO_PIN_36",0x00000790,32,"rw",0x00001601,"MIO Pin 36 Control"),
    Entry("MIO_PIN_37",0x00000794,32,"rw",0x00001601,"MIO Pin 37 Control"),
    Entry("MIO_PIN_38",0x00000798,32,"rw",0x00001601,"MIO Pin 38 Control"),
    Entry("MIO_PIN_39",0x0000079C,32,"rw",0x00001601,"MIO Pin 39 Control"),
    Entry("MIO_PIN_40",0x000007A0,32,"rw",0x00001601,"MIO Pin 40 Control"),
    Entry("MIO_PIN_41",0x000007A4,32,"rw",0x00001601,"MIO Pin 41 Control"),
    Entry("MIO_PIN_42",0x000007A8,32,"rw",0x00001601,"MIO Pin 42 Control"),
    Entry("MIO_PIN_43",0x000007AC,32,"rw",0x00001601,"MIO Pin 43 Control"),
    Entry("MIO_PIN_44",0x000007B0,32,"rw",0x00001601,"MIO Pin 44 Control"),
    Entry("MIO_PIN_45",0x000007B4,32,"rw",0x00001601,"MIO Pin 45 Control"),
    Entry("MIO_PIN_46",0x000007B8,32,"rw",0x00001601,"MIO Pin 46 Control"),
    Entry("MIO_PIN_47",0x000007BC,32,"rw",0x00001601,"MIO Pin 47 Control"),
    Entry("MIO_PIN_48",0x000007C0,32,"rw",0x00001601,"MIO Pin 48 Control"),
    Entry("MIO_PIN_49",0x000007C4,32,"rw",0x00001601,"MIO Pin 49 Control"),
    Entry("MIO_PIN_50",0x000007C8,32,"rw",0x00001601,"MIO Pin 50 Control"),
    Entry("MIO_PIN_51",0x000007CC,32,"rw",0x00001601,"MIO Pin 51 Control"),
    Entry("MIO_PIN_52",0x000007D0,32,"rw",0x00001601,"MIO Pin 52 Control"),
    Entry("MIO_PIN_53",0x000007D4,32,"rw",0x00001601,"MIO Pin 53 Control"),
    Entry("MIO_LOOPBACK",0x00000804,32,"rw",0x00000000,"Loopback function within MIO"),
    Entry("MIO_MST_TRI0",0x0000080C,32,"rw",0xFFFFFFFF,"MIO pin Tri-state Enables, 31:0"),
    Entry("MIO_MST_TRI1",0x00000810,32,"rw",0x003FFFFF,"MIO pin Tri-state Enables, 53:32"),
    Entry("SD0_WP_CD_SEL",0x00000830,32,"rw",0x00000000,"SDIO 0 WP CD select"),
    Entry("SD1_WP_CD_SEL",0x00000834,32,"rw",0x00000000,"SDIO 1 WP CD select"),
    Entry("LVL_SHFTR_EN",0x00000900,32,"rw",0x00000000,"Level Shifters Enable"),
    Entry("OCM_CFG",0x00000910,32,"rw",0x00000000,"OCM Address Mapping"),
    Entry("Reserved",0x00000A1C,32,"rw",0x00010101,"Reserved"),
    Entry("GPIOB_CTRL",0x00000B00,32,"rw",0x00000000,"PS IO Buffer Control"),
    Entry("GPIOB_CFG_CMOS18",0x00000B04,32,"rw",0x00000000,"MIO GPIOB CMOS 1.8V config"),
    Entry("GPIOB_CFG_CMOS25",0x00000B08,32,"rw",0x00000000,"MIO GPIOB CMOS 2.5V config"),
    Entry("GPIOB_CFG_CMOS33",0x00000B0C,32,"rw",0x00000000,"MIO GPIOB CMOS 3.3V config"),
    Entry("GPIOB_CFG_HSTL",0x00000B14,32,"rw",0x00000000,"MIO GPIOB HSTL config"),
    Entry("GPIOB_DRVR_BIAS_CTRL",0x00000B18,32,"mixed",0x00000000,"MIO GPIOB Driver Bias Control"),
    Entry("DDRIOB_ADDR0",0x00000B40,32,"rw",0x00000800,"DDR IOB Config for ARegister(14:0), CKE and DRST_B"),
    Entry("DDRIOB_ADDR1",0x00000B44,32,"rw",0x00000800,"DDR IOB Config for BARegister(2:0), ODT, CS_B, WE_B, RAS_B and CAS_B"),
    Entry("DDRIOB_DATA0",0x00000B48,32,"rw",0x00000800,"DDR IOB Config for Data 15:0"),
    Entry("DDRIOB_DATA1",0x00000B4C,32,"rw",0x00000800,"DDR IOB Config for Data 31:16"),
    Entry("DDRIOB_DIFF0",0x00000B50,32,"rw",0x00000800,"DDR IOB Config for DQS 1:0"),
    Entry("DDRIOB_DIFF1",0x00000B54,32,"rw",0x00000800,"DDR IOB Config for DQS 3:2"),
    Entry("DDRIOB_CLOCK",0x00000B58,32,"rw",0x00000800,"DDR IOB Config for Clock Output"),
    Entry("DDRIOB_DRIVE_SLEW_ADDR",0x00000B5C,32,"rw",0x00000000,"Drive and Slew controls for Address and Command pins of the DDR Interface"),
    Entry("DDRIOB_DRIVE_SLEW_DATA",0x00000B60,32,"rw",0x00000000,"Drive and Slew controls for DQ pins of the DDR Interface"),
    Entry("DDRIOB_DRIVE_SLEW_DIFF",0x00000B64,32,"rw",0x00000000,"Drive and Slew controls for DQS pins of the DDR Interface"),
    Entry("DDRIOB_DRIVE_SLEW_CLOCK",0x00000B68,32,"rw",0x00000000,"Drive and Slew controls for Clock pins of the DDR Interface"),
    Entry("DDRIOB_DDR_CTRL",0x00000B6C,32,"rw",0x00000000,"DDR IOB Buffer Control"),
    Entry("DDRIOB_DCI_CTRL",0x00000B70,32,"rw",0x00000020,"DDR IOB DCI Config"),
    Entry("DDRIOB_DCI_STATUS",0x00000B74,32,"mixed",0x00000000,"DDR IO Buffer DCI Status") ], name='slrc')
ddrc = BaseRegister(0xf8006000, [
    Entry("ddrc_ctrl", 0x00000000, 32, "rw", 0x00000200, "DDRC Control"),
    Entry("Two_rank_cfg", 0x00000004, 29, "rw", 0x000C1076, "Two Rank Configuration"),
    Entry("HPR_reg", 0x00000008, 26, "rw", 0x03C0780F, "HPR Queue control"),
    Entry("LPR_reg", 0x0000000C, 26, "rw", 0x03C0780F, "LPR Queue control"),
    Entry("WR_reg", 0x00000010, 26, "rw", 0x0007F80F, "WR Queue control"),
    Entry("DRAM_param_reg0", 0x00000014, 21, "rw", 0x00041016, "DRAM Parameters 0"),
    Entry("DRAM_param_reg1", 0x00000018, 32, "rw", 0x351B48D9, "DRAM Parameters 1"),
    Entry("DRAM_param_reg2", 0x0000001C, 32, "rw", 0x83015904, "DRAM Parameters 2"),
    Entry("DRAM_param_reg3", 0x00000020, 32, "mixed", 0x250882D0, "DRAM Parameters 3"),
    Entry("DRAM_param_reg4", 0x00000024, 28, "mixed", 0x0000003C, "DRAM Parameters 4"),
    Entry("DRAM_init_param", 0x00000028, 14, "rw", 0x00002007, "DRAM Initialization Parameters"),
    Entry("DRAM_EMR_reg", 0x0000002C, 32, "rw", 0x00000008, "DRAM EMR2, EMR3 access"),
    Entry("DRAM_EMR_MR_reg", 0x00000030, 32, "rw", 0x00000940, "DRAM EMR, MR access"),
    Entry("DRAM_burst8_rdwr", 0x00000034, 29, "mixed", 0x00020034, "DRAM Burst 8 read/write"),
    Entry("DRAM_disable_DQ", 0x00000038, 13, "mixed", 0x00000000, "DRAM Disable DQ"),
    Entry("DRAM_addr_map_bank", 0x0000003C, 20, "rw", 0x00000F77, "Row/Column address bits"),
    Entry("DRAM_addr_map_col", 0x00000040, 32, "rw", 0xFFF00000, "Column address bits"),
    Entry("DRAM_addr_map_row", 0x00000044, 28, "rw", 0x0FF55555, "Select DRAM row address bits"),
    Entry("DRAM_ODT_reg", 0x00000048, 30, "rw", 0x00000249, "DRAM ODT control"),
    Entry("phy_dbg_reg", 0x0000004C, 20, "ro", 0x00000000, "PHY debug"),
    Entry("phy_cmd_timeout_rddata_cpt", 0x00000050, 32, "mixed", 0x00010200, "PHY command time out and read data capture FIFO"),
    Entry("mode_sts_reg", 0x00000054, 21, "ro", 0x00000000, "Controller operation mode status"),
    Entry("DLL_calib", 0x00000058, 17, "rw", 0x00000101, "DLL calibration"),
    Entry("ODT_delay_hold", 0x0000005C, 16, "rw", 0x00000023, "ODT delay and ODT hold"),
    Entry("ctrl_reg1", 0x00000060, 13, "mixed", 0x0000003E, "Controller 1"),
    Entry("ctrl_reg2", 0x00000064, 18, "mixed", 0x00020000, "Controller 2"),
    Entry("ctrl_reg3", 0x00000068, 26, "rw", 0x00284027, "Controller 3"),
    Entry("ctrl_reg4", 0x0000006C, 16, "rw", 0x00001610, "Controller 4"),
    Entry("ctrl_reg5", 0x00000078, 32, "mixed", 0x00455111, "Controller register 5"),
    Entry("ctrl_reg6", 0x0000007C, 32, "mixed", 0x00032222, "Controller register 6"),
    Entry("CHE_REFRESH_TIMER01", 0x000000A0, 24, "rw", 0x00008000, "CHE_REFRESH_TIMER01"),
    Entry("CHE_T_ZQ", 0x000000A4, 32, "rw", 0x10300802, "ZQ parameters"),
    Entry("CHE_T_ZQ_Short_Interval_Reg", 0x000000A8, 28, "rw", 0x0020003A, "Misc parameters"),
    Entry("deep_pwrdwn_reg", 0x000000AC, 9, "rw", "0x00000000", "Deep powerdown (LPDDR2)"),
    Entry("reg_2c", 0x000000B0, 29, "mixed", 0x00000000, "Training control"),
    Entry("reg_2d", 0x000000B4, 11, "rw", 0x00000200, "Misc Debug"),
    Entry("dfi_timing", 0x000000B8, 25, "rw", 0x00200067, "DFI timing"),
    Entry("CHE_ECC_CONTROL_REG_OFFSET", 0x000000C4, 2, "rw", 0x00000000 , "ECCerror clear"),
    Entry("CHE_CORR_ECC_LOG_REG_OFFSET", 0x000000C8, 8, "mixed", 0x00000000 , "ECCerror correction"),
    Entry("CHE_CORR_ECC_ADDR_REG_OFFSET", 0x000000CC, 31, "ro", 0x00000000, "ECC error correction address log"),
    Entry("CHE_CORR_ECC_DATA_31_0_REG_OFFSET", 0x000000D0, 32, "ro", 0x00000000, "ECC error correction data log low"),
    Entry("CHE_CORR_ECC_DATA_63_32_REG_OFFSET", 0x000000D4, 32, "ro", 0x00000000, "ECC error correction data log mid"),
    Entry("CHE_CORR_ECC_DATA_71_64_REG_OFFSET", 0x000000D8, 8, "ro", 0x00000000, "ECCerror correction data log high"),
    Entry("CHE_UNCORR_ECC_LOG_REG_OFFSET", 0x000000DC, 1, "clronwr", 0x00000000, "ECC unrecoverable error status"),
    Entry("CHE_UNCORR_ECC_ADDR_REG_OFFSET", 0x000000E0, 31, "ro", 0x00000000, "ECC unrecoverable error address"),
    Entry("CHE_UNCORR_ECC_DATA_31_0_REG_OFFSET", 0x000000E4, 32, "ro", 0x00000000, "ECC unrecoverable error data low"),
    Entry("CHE_UNCORR_ECC_DATA_63_32_REG_OFFSET", 0x000000E8, 32, "ro", 0x00000000, "ECC unrecoverable error data middle"),
    Entry("CHE_UNCORR_ECC_DATA_71_64_REG_OFFSET", 0x000000EC, 8, "ro", 0x00000000, "ECC unrecoverable error data high"),
    Entry("CHE_ECC_STATS_REG_OFFSET", 0x000000F0, 16, "clron wr", 0x00000000, "ECC error count"),
    Entry("ECC_scrub", 0x000000F4, 4, "rw", 0x00000008, "ECC mode/scrub"),
    Entry("CHE_ECC_CORR_BIT_MASK_31_0_REG_OFFSET", 0x000000F8, 32, "ro", 0x00000000, "ECC data mask low"),
    Entry("CHE_ECC_CORR_BIT_MASK_63_32_REG_OFFSET", 0x000000FC, 32, "ro", 0x00000000, "ECC data mask high"),
    Entry("phy_rcvr_enable", 0x00000114, 8, "rw", 0x00000000, "Phyreceiver enable register"),
    Entry("PHY_Config0", 0x00000118, 31, "rw", 0x40000001, "PHY configuration register for data slice 0."),
    Entry("PHY_Config1", 0x0000011C, 31, "rw", 0x40000001, "PHY configuration register for data slice 1."),
    Entry("PHY_Config2", 0x00000120, 31, "rw", 0x40000001, "PHY configuration register for data slice 2."),
    Entry("PHY_Config3", 0x00000124, 31, "rw", 0x40000001, "PHY configuration register for data slice 3."),
    Entry("phy_init_ratio0", 0x0000012C, 20, "rw", 0x00000000, "PHY init ratio register for data slice 0."),
    Entry("phy_init_ratio1", 0x00000130, 20, "rw", 0x00000000, "PHY init ratio register for data slice 1."),
    Entry("phy_init_ratio2", 0x00000134, 20, "rw", 0x00000000, "PHY init ratio register for data slice 2."),
    Entry("phy_init_ratio3", 0x00000138, 20, "rw", 0x00000000, "PHY init ratio register for data slice 3."),
    Entry("phy_rd_dqs_cfg0", 0x00000140, 20, "rw", 0x00000040, "PHY read DQS configuration register for data slice 0."),
    Entry("phy_rd_dqs_cfg1", 0x00000144, 20, "rw", 0x00000040, "PHY read DQS configuration register for data slice 1."),
    Entry("phy_rd_dqs_cfg2", 0x00000148, 20, "rw", 0x00000040, "PHY read DQS configuration register for data slice 2."),
    Entry("phy_rd_dqs_cfg3", 0x0000014C, 20, "rw", 0x00000040, "PHY read DQS configuration register for data slice 3."),
    Entry("phy_wr_dqs_cfg0", 0x00000154, 20, "rw", 0x00000000, "PHY write DQS configuration register for data slice 0."),
    Entry("phy_wr_dqs_cfg1", 0x00000158, 20, "rw", 0x00000000, "PHY write DQS configuration register for data slice 1."),
    Entry("phy_wr_dqs_cfg2", 0x0000015C, 20, "rw", 0x00000000, "PHY write DQS configuration register for data slice 2."),
    Entry("phy_wr_dqs_cfg3", 0x00000160, 20, "rw", 0x00000000, "PHY write DQS configuration register for data slice 3."),
    Entry("phy_we_cfg0", 0x00000168, 21, "rw", 0x00000040, "PHY FIFO write enable configuration for data slice 0."),
    Entry("phy_we_cfg1", 0x0000016C, 21, "rw", 0x00000040, "PHY FIFO write enable configuration for data slice 1."),
    Entry("phy_we_cfg2", 0x00000170, 21, "rw", 0x00000040, "PHY FIFO write enable configuration for data slice 2."),
    Entry("phy_we_cfg3", 0x00000174, 21, "rw", 0x00000040, "PHY FIFO write enable configuration for data slice 3."),
    Entry("wr_data_slv0", 0x0000017C, 20, "rw", 0x00000080, "PHY write data slave ratio config for data slice 0."),
    Entry("wr_data_slv1", 0x00000180, 20, "rw", 0x00000080, "PHY write data slave ratio config for data slice 1."),
    Entry("wr_data_slv2", 0x00000184, 20, "rw", 0x00000080, "PHY write data slave ratio config for data slice 2."),
    Entry("wr_data_slv3", 0x00000188, 20, "rw", 0x00000080, "PHY write data slave ratio config for data slice 3."),
    Entry("reg_64", 0x00000190, 32, "rw", 0x10020000, "Training control 2"),
    Entry("reg_65", 0x00000194, 20, "rw", 0x00000000, "Training control 3"),
    Entry("reg69_6a0", 0x000001A4, 29, "ro", 0x00070000, "Training results for data slice 0."),
    Entry("reg69_6a1", 0x000001A8, 29, "ro", 0x00060200, "Training results for data slice 1."),
    Entry("reg6c_6d2", 0x000001B0, 28, "ro", 0x00040600, "Training results for data slice 2."),
    Entry("reg6c_6d3", 0x000001B4, 28, "ro", 0x00000E00, "Training results for data slice 3."),
    Entry("reg6e_710", 0x000001B8, 30, "ro", "xx", "Training results (2) for data slice 0."),
    Entry("reg6e_711", 0x000001BC, 30, "ro", "xx", "Training results (2) for data slice 1."),
    Entry("reg6e_712", 0x000001C0, 30, "ro", "xx", "Training results (2) for data slice 2."),
    Entry("reg6e_713", 0x000001C4, 30, "ro", "xx", "Training results (2) for data slice 3."),
    Entry("phy_dll_sts0", 0x000001CC, 27, "ro", 0x00000000, "Slave DLL results for data slice 0."),
    Entry("phy_dll_sts1", 0x000001D0, 27, "ro", 0x00000000, "Slave DLL results for data slice 1."),
    Entry("phy_dll_sts2", 0x000001D4, 27, "ro", 0x00000000, "Slave DLL results for data slice 2."),
    Entry("phy_dll_sts3", 0x000001D8, 27, "ro", 0x00000000, "Slave DLL results for data slice 3."),
    Entry("dll_lock_sts", 0x000001E0, 24, "ro", 0x00F00000, "DLL Lock Status, read"),
    Entry("phy_ctrl_sts", 0x000001E4, 30, "ro", "xx", "PHY Control status, read"),
    Entry("phy_ctrl_sts_reg2", 0x000001E8, 27, "ro", 0x00000013, "PHY Control status (2), read"),
    Entry("axi_id", 0x00000200, 26, "ro", 0x00153042, "ID and revision information"),
    Entry("page_mask", 0x00000204, 32, "rw", 0x00000000, "Page mask"),
    Entry("axi_priority_wr_port0", 0x00000208, 20, "mixed", 0x000803FF, "AXI Priority control for write port 0."),
    Entry("axi_priority_wr_port1", 0x0000020C, 20, "mixed", 0x000803FF, "AXI Priority control for write port 1."),
    Entry("axi_priority_wr_port2", 0x00000210, 20, "mixed", 0x000803FF, "AXI Priority control for write port 2."),
    Entry("axi_priority_wr_port3", 0x00000214, 20, "mixed", 0x000803FF, "AXI Priority control for write port 3."),
    Entry("axi_priority_rd_port0", 0x00000218, 20, "mixed", 0x000003FF, "AXI Priority control for read port 0."),
    Entry("axi_priority_rd_port1", 0x0000021C, 20, "mixed", 0x000003FF, "AXI Priority control for read port 1."),
    Entry("axi_priority_rd_port2", 0x00000220, 20, "mixed", 0x000003FF, "AXI Priority control for read port 2."),
    Entry("axi_priority_rd_port3", 0x00000224, 20, "mixed", 0x000003FF, "AXI Priority control for read port 3."),
    Entry("excl_access_cfg0", 0x00000294, 18, "rw", 0x00000000, "Exclusive access configuration for port 0."),
    Entry("excl_access_cfg1", 0x00000298, 18, "rw", 0x00000000, "Exclusive access configuration for port 1."),
    Entry("excl_access_cfg2", 0x0000029C, 18, "rw", 0x00000000, "Exclusive access configuration for port 2."),
    Entry("excl_access_cfg3", 0x000002A0, 18, "rw", 0x00000000, "Exclusive access configuration for port 3."),
    Entry("mode_reg_read", 0x000002A4, 32, "ro", 0x00000000, "Mode register read data"),
    Entry("lpddr_ctrl0", 0x000002A8, 12, "rw", 0x00000000, "LPDDR2 Control 0"),
    Entry("lpddr_ctrl1", 0x000002AC, 32, "rw", 0x00000000, "LPDDR2 Control 1"),
    Entry("lpddr_ctrl2", 0x000002B0, 22, "rw", 0x003C0015, "LPDDR2 Control 2"),
    Entry("lpddr_ctrl3", 0x000002B4, 18, "rw", 0x00000601, "LPDDR2 Control 3")], name='ddrc')
devcfg = BaseRegister(0xf8007000, [
    Entry("XDCFG_CTRL_OFFSET", 0xf8007000, 32, "mixed", 0x0C006000, "Control Register"),
    Entry("XDCFG_LOCK_OFFSET", 0xf8007004, 32, "mixed", 0x00000000, "Locks for the Control Register."),
    Entry("XDCFG_CFG_OFFSET", 0xf8007008, 32, "rw", 0x00000508, "Configuration Register: This register contains configuration information for the AXI transfers, and other general setup."),
    Entry("XDCFG_INT_STS_OFFSET", 0xf800700C, 32, "mixed", 0x00000000, "Interrupt Status"),
    Entry("XDCFG_INT_MASK_OFFSET", 0xf8007010, 32, "rw", 0xFFFFFFFF, "Interrupt Mask."),
    Entry("XDCFG_STATUS_OFFSET", 0xf8007014, 32, "mixed", 0x40000820, "Miscellaneous Status."),
    Entry("XDCFG_DMA_SRC_ADDR_OFFSET", 0xf8007018, 32, "rw", 0x00000000, "DMA Source Address."),
    Entry("XDCFG_DMA_DEST_ADDR_OFFSET", 0xf800701C, 32, "rw", 0x00000000, "DMA Destination Address."),
    Entry("XDCFG_DMA_SRC_LEN_OFFSET", 0xf8007020, 32, "rw", 0x00000000, "DMA Source Transfer Length."),
    Entry("XDCFG_DMA_DEST_LEN_OFFSET", 0xf8007024, 32, "rw", 0x00000000, "DMA Destination Transfer Length."),
    Entry("XDCFG_MULTIBOOT_ADDR_OFFSET", 0xf800702C, 13, "rw", 0x00000000, "Multi-Boot Address Pointer."),
    Entry("XDCFG_UNLOCK_OFFSET", 0xf8007034, 32, "rw", 0x00000000, "Unlock Control."),
    Entry("XDCFG_MCTRL_OFFSET", 0xf8007080, 32, "mixed", "x", "Miscellaneous Control."),
    Entry("XADCIF_CFG", 0xf8007100, 32, "rw", 0x00001114, "XADC Interface Configuration."),
    Entry("XADCIF_INT_STS", 0xf8007104, 32, "mixed", 0x00000200, "XADC Interface Interrupt Status."),
    Entry("XADCIF_INT_MASK", 0xf8007108, 32, "rw", 0xFFFFFFFF, "XADC Interface Interrupt Mask."),
    Entry("XADCIF_MSTS", 0xf800710C, 32, "ro", 0x00000500, "XADC Interface Miscellaneous Status."),
    Entry("XADCIF_CMDFIFO", 0xf8007110, 32, "wo", 0x00000000, "XADC Interface Command FIFO Data Port"),
    Entry("XADCIF_RDFIFO", 0xf8007114, 32, "ro", 0x00000000, "XADC Interface Data FIFO Data Port"),
    Entry("XADCIF_MCTL", 0xf8007118, 32, "rw", 0x00000010, "XADC Interface Miscellaneous Control.")], name='devcfg')
uart0 = BaseRegister(0xe0000000, [
    Entry("XUARTPS_CR_OFFSET", 0x00000000, 32, "mixed", 0x00000128, "UART Control Register"),
    Entry("XUARTPS_MR_OFFSET", 0x00000004, 32, "mixed", 0x00000000, "UART Mode Register"),
    Entry("XUARTPS_IER_OFFSET", 0x00000008, 32, "mixed", 0x00000000, "Interrupt Enable Register"),
    Entry("XUARTPS_IDR_OFFSET", 0x0000000C, 32, "mixed", 0x00000000, "Interrupt Disable Register"),
    Entry("XUARTPS_IMR_OFFSET", 0x00000010, 32, "ro", 0x00000000, "Interrupt Mask Register"),
    Entry("XUARTPS_ISR_OFFSET", 0x00000014, 32, "wtc", 0x00000000, "Channel Interrupt Status Register"),
    Entry("XUARTPS_BAUDGEN_OFFSET", 0x00000018, 32, "mixed", 0x0000028B, "Baud Rate Generator Register."),
    Entry("XUARTPS_RXTOUT_OFFSET", 0x0000001C, 32, "mixed", 0x00000000, "Receiver Timeout Register"),
    Entry("XUARTPS_RXWM_OFFSET", 0x00000020, 32, "mixed", 0x00000020, "Receiver FIFO Trigger Level Register"),
    Entry("XUARTPS_MODEMCR_OFFSET", 0x00000024, 32, "mixed", 0x00000000, "Modem Control Register"),
    Entry("XUARTPS_MODEMSR_OFFSET", 0x00000028, 32, "mixed", "x", "Modem Status Register"),
    Entry("XUARTPS_SR_OFFSET", 0x0000002C, 32, "ro", 0x00000000, "Channel Status Register"),
    Entry("XUARTPS_FIFO_OFFSET", 0x00000030, 32, "mixed", 0x00000000, "Transmit and Receive FIFO"),
    Entry("Baud_rate_divider_reg0", 0x00000034, 32, "mixed", 0x0000000F, "Baud Rate Divider Register"),
    Entry("Flow_delay_reg0", 0x00000038, 32, "mixed", 0x00000000, "Flow Control Delay Register"),
    Entry("Tx_FIFO_trigger_level0", 0x00000044, 32, "mixed", 0x00000020, "Transmitter FIFO Trigger Level Register")], name='uart0')

# def zynq7000_name2addr(n):
    # addr = -1
    # for i in slcr:
        # if n.lower() == i[0].
    # return 0
# def zynq7000_addr2name(a):
    # return 0

def parse_slcr_entries_fields(ps7_init):
    with open(ps7_init, "r") as ps7_init_f:
        ps7_init_lines = ps7_init_f.readlines()

        ln_cut = 0
        for ln, l in enumerate(ps7_init_lines):
            if 'unsigned long ps7_pll_init_data_2_0' in l:
                ln_cut = ln
                break
        ps7_init_lines = ps7_init_lines[:ln_cut]

        # print(ps7_init_lines)
        # print('---')
        r_entry_addr = re.compile(r'.*==> (0X[0-9A-F]+)\[.*\] = 0x([0-9A-F]+)U')
        r_field_name = re.compile(r'.*\.\. (.*) = [0-9].*')
        r_field_mask = re.compile(r'.*==> MASK : (0x[0-9A-F]+)U.*')
        for ln, l in enumerate(ps7_init_lines):
            m_entry_addr = r_entry_addr.match(l)
            if m_entry_addr:
                m_field_name = r_field_name.match(ps7_init_lines[ln - 1])
                m_field_mask = r_field_mask.match(ps7_init_lines[ln + 1])
                if not m_field_name:
                    print('Err: name syntax incorrect in ps7_init.c!')
                if not m_field_mask:
                    print('Err: MASK syntax incorrect in ps7_init.c!')
                # print(m_entry_addr.group(1), m_field_name.group(1), m_field_mask.group(1))
                slcr.update_entry_field(int(m_entry_addr.group(1), 16), m_field_name.group(1), int(m_field_mask.group(1), 16))
                # break



if __name__ == "__main__":
    parse_slcr_entries_fields("./hdf/noddr-0-uart/ps7_init.c")
    slcr.show()
    # print(slcr)
