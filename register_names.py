#!/usr/bin/env python3
import re
import sys
import copy

# Register -> Entry -> Field
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

    def show():
        print(f"{self.name}, 0x{self.addr:08x}")
        for f in self.fields:
            print(f"\t{f}, 0x{self.fields[f]:08x}")


class Register:
    def __init__(self, name, baseaddr, entries):
        self.name = name
        # self.baseaddr = baseaddr
        self.entries = copy.deepcopy(entries)

    def update_entry_field(self, entryaddr, fieldname, fieldmask):
        pass

    def n2a(self, name, absolute=False):
        addr = -1
        for e in self.entries:
            if e.name.lower() == name.lower():
                addr = e.addr;
        if addr == -1:
            raise Exception("Entry ", name, " not found in Register ", self.name, " !")
        # if absolute:
            # addr += self.baseaddr
        return addr

    def a2n(self, addr):
        name = ''
        for e in self.entries:
            if e.addr == addr:
                name = e.name()
        if name == '':
            raise Exception("Entry ", hex(addr), " not found in Register ", self.name, " !")
        return name
    
    def show(self):
        print(f"{self.name}")
        for e in self.entries:
            e.show()
            


# From UG585, ZYNQ 7000 TRM, Page 1632
# Register Name, Address, Width, Type, Reset Value, Description
slcr = Register('slcr', 0xf8000000, [
    Entry("SCL",0xf8000000,32,"rw",0x00000000,"Secure Configuration Lock"),
    Entry("SLCR_LOCK",0xf8000004,32,"wo",0x00000000,"SLCR Write Protection Lock"),
    Entry("SLCR_UNLOCK",0xf8000008,32,"wo",0x00000000,"SLCR Write Protection Unlock"),
    Entry("SLCR_LOCKSTA",0xf800000C,32,"ro",0x00000001,"SLCR Write Protection Status"),
    Entry("ARM_PLL_CTRL",0xf8000100,32,"rw",0x0001A008,"Arm PLL Control"),
    Entry("DDR_PLL_CTRL",0xf8000104,32,"rw",0x0001A008,"DDR PLL Control"),
    Entry("IO_PLL_CTRL",0xf8000108,32,"rw",0x0001A008,"IO PLL Control"),
    Entry("PLL_STATUS",0xf800010C,32,"ro",0x0000003F,"PLL Status"),
    Entry("ARM_PLL_CFG",0xf8000110,32,"rw",0x00177EA0,"Arm PLL Configuration"),
    Entry("DDR_PLL_CFG",0xf8000114,32,"rw",0x00177EA0,"DDR PLL Configuration"),
    Entry("IO_PLL_CFG",0xf8000118,32,"rw",0x00177EA0,"IO PLL Configuration"),
    Entry("ARM_CLK_CTRL",0xf8000120,32,"rw",0x1F000400,"CPU Clock Control"),
    Entry("DDR_CLK_CTRL",0xf8000124,32,"rw",0x18400003,"DDR Clock Control"),
    Entry("DCI_CLK_CTRL",0xf8000128,32,"rw",0x01E03201,"DCI clock control"),
    Entry("APER_CLK_CTRL",0xf800012C,32,"rw",0x01FFCCCD,"AMBA Peripheral Clock Control"),
    Entry("USB0_CLK_CTRL",0xf8000130,32,"rw",0x00101941,"USB 0 ULPI Clock Control"),
    Entry("USB1_CLK_CTRL",0xf8000134,32,"rw",0x00101941,"USB 1 ULPI Clock Control"),
    Entry("GEM0_RCLK_CTRL",0xf8000138,32,"rw",0x00000001,"GigE 0 Rx Clock and Rx Signals Select"),
    Entry("GEM1_RCLK_CTRL",0xf800013C,32,"rw",0x00000001,"GigE 1 Rx Clock and Rx Signals Select"),
    Entry("GEM0_CLK_CTRL",0xf8000140,32,"rw",0x00003C01,"GigE 0 Ref Clock Control"),
    Entry("GEM1_CLK_CTRL",0xf8000144,32,"rw",0x00003C01,"GigE 1 Ref Clock Control"),
    Entry("SMC_CLK_CTRL",0xf8000148,32,"rw",0x00003C21,"SMC Ref Clock Control"),
    Entry("LQSPI_CLK_CTRL",0xf800014C,32,"rw",0x00002821,"Quad SPI Ref Clock Control"),
    Entry("SDIO_CLK_CTRL",0xf8000150,32,"rw",0x00001E03,"SDIO Ref Clock Control"),
    Entry("UART_CLK_CTRL",0xf8000154,32,"rw",0x00003F03,"UART Ref Clock Control"),
    Entry("SPI_CLK_CTRL",0xf8000158,32,"rw",0x00003F03,"SPI Ref Clock Control"),
    Entry("CAN_CLK_CTRL",0xf800015C,32,"rw",0x00501903,"CAN Ref Clock Control"),
    Entry("CAN_MIOCLK_CTRL",0xf8000160,32,"rw",0x00000000,"CAN MIO Clock Control"),
    Entry("DBG_CLK_CTRL",0xf8000164,32,"rw",0x00000F03,"SoC Debug Clock Control"),
    Entry("PCAP_CLK_CTRL",0xf8000168,32,"rw",0x00000F01,"PCAP Clock Control"),
    Entry("TOPSW_CLK_CTRL",0xf800016C,32,"rw",0x00000000,"Central Interconnect Clock Control"),
    Entry("FPGA0_CLK_CTRL",0xf8000170,32,"rw",0x00101800,"PL Clock 0 Output control"),
    Entry("FPGA0_THR_CTRL",0xf8000174,32,"rw",0x00000000,"PL Clock 0 Throttle control"),
    Entry("FPGA0_THR_CNT",0xf8000178,32,"rw",0x00000000,"PL Clock 0 Throttle Count control"),
    Entry("FPGA0_THR_STA",0xf800017C,32,"ro",0x00010000,"PL Clock 0 Throttle Status read"),
    Entry("FPGA1_CLK_CTRL",0xf8000180,32,"rw",0x00101800,"PL Clock 1 Output control"),
    Entry("FPGA1_THR_CTRL",0xf8000184,32,"rw",0x00000000,"PL Clock 1 Throttle control"),
    Entry("FPGA1_THR_CNT",0xf8000188,32,"rw",0x00000000,"PL Clock 1 Throttle Count"),
    Entry("FPGA1_THR_STA",0xf800018C,32,"ro",0x00010000,"PL Clock 1 Throttle Status control"),
    Entry("FPGA2_CLK_CTRL",0xf8000190,32,"rw",0x00101800,"PL Clock 2 output control"),
    Entry("FPGA2_THR_CTRL",0xf8000194,32,"rw",0x00000000,"PL Clock 2 Throttle Control"),
    Entry("FPGA2_THR_CNT",0xf8000198,32,"rw",0x00000000,"PL Clock 2 Throttle Count"),
    Entry("FPGA2_THR_STA",0xf800019C,32,"ro",0x00010000,"PL Clock 2 Throttle Status"),
    Entry("FPGA3_CLK_CTRL",0xf80001A0,32,"rw",0x00101800,"PL Clock 3 output control"),
    Entry("FPGA3_THR_CTRL",0xf80001A4,32,"rw",0x00000000,"PL Clock 3 Throttle Control"),
    Entry("FPGA3_THR_CNT",0xf80001A8,32,"rw",0x00000000,"PL Clock 3 Throttle Count"),
    Entry("FPGA3_THR_STA",0xf80001AC,32,"ro",0x00010000,"PL Clock 3 Throttle Status"),
    Entry("CLK_621_TRUE",0xf80001C4,32,"rw",0x00000001,"CPU Clock Ratio Mode select"),
    Entry("PSS_RST_CTRL",0xf8000200,32,"rw",0x00000000,"PS Software Reset Control"),
    Entry("DDR_RST_CTRL",0xf8000204,32,"rw",0x00000000,"DDR Software Reset Control"),
    Entry("TOPSW_RST_CTRL",0xf8000208,32,"rw",0x00000000,"Central Interconnect Reset Control"),
    Entry("DMAC_RST_CTRL",0xf800020C,32,"rw",0x00000000,"DMAC Software Reset Control"),
    Entry("USB_RST_CTRL",0xf8000210,32,"rw",0x00000000,"USB Software Reset Control"),
    Entry("GEM_RST_CTRL",0xf8000214,32,"rw",0x00000000,"Gigabit Ethernet SW Reset Control"),
    Entry("SDIO_RST_CTRL",0xf8000218,32,"rw",0x00000000,"SDIO Software Reset Control"),
    Entry("SPI_RST_CTRL",0xf800021C,32,"rw",0x00000000,"SPI Software Reset Control"),
    Entry("CAN_RST_CTRL",0xf8000220,32,"rw",0x00000000,"CAN Software Reset Control"),
    Entry("I2C_RST_CTRL",0xf8000224,32,"rw",0x00000000,"I2C Software Reset Control"),
    Entry("UART_RST_CTRL",0xf8000228,32,"rw",0x00000000,"UART Software Reset Control"),
    Entry("GPIO_RST_CTRL",0xf800022C,32,"rw",0x00000000,"GPIO Software Reset Control"),
    Entry("LQSPI_RST_CTRL",0xf8000230,32,"rw",0x00000000,"Quad SPI Software Reset Control"),
    Entry("SMC_RST_CTRL",0xf8000234,32,"rw",0x00000000,"SMC Software Reset Control"),
    Entry("OCM_RST_CTRL",0xf8000238,32,"rw",0x00000000,"OCM Software Reset Control"),
    Entry("FPGA_RST_CTRL",0xf8000240,32,"rw",0x01F33F0F,"FPGA Software Reset Control"),
    Entry("A9_CPU_RST_CTRL",0xf8000244,32,"rw",0x00000000,"CPU Reset and Clock control"),
    Entry("RS_AWDT_CTRL",0xf800024C,32,"rw",0x00000000,"Watchdog Timer Reset Control"),
    Entry("REBOOT_STATUS",0xf8000258,32,"rw",0x00400000,"Reboot Status, persistent"),
    Entry("BOOT_MODE",0xf800025C,32,"mixed","x", "Boot Mode Strapping Pins"),
    Entry("APU_CTRL",0xf8000300,32,"rw",0x00000000,"APU Control"),
    Entry("WDT_CLK_SEL",0xf8000304,32,"rw",0x00000000,"SWDT clock source select"),
    Entry("TZ_DMA_NS",0xf8000440,32,"rw",0x00000000,"DMAC TrustZone Config"),
    Entry("TZ_DMA_IRQ_NS",0xf8000444,32,"rw",0x00000000,"DMAC TrustZone Config for Interrupts"),
    Entry("TZ_DMA_PERIPH_NS",0xf8000448,32,"rw",0x00000000,"DMAC TrustZone Config for Peripherals"),
    Entry("PSS_IDCODE",0xf8000530,32,"ro","x", "PS IDCODE"),
    Entry("DDR_URGENT",0xf8000600,32,"rw",0x00000000,"DDR Urgent Control"),
    Entry("DDR_CAL_START",0xf800060C,32,"mixed",0x00000000,"DDR Calibration Start Triggers"),
    Entry("DDR_REF_START",0xf8000614,32,"mixed",0x00000000,"DDR Refresh Start Triggers"),
    Entry("DDR_CMD_STA",0xf8000618,32,"mixed",0x00000000,"DDR Command Store Status"),
    Entry("DDR_URGENT_SEL",0xf800061C,32,"rw",0x00000000,"DDR Urgent Select"),
    Entry("DDR_DFI_STATUS",0xf8000620,32,"mixed",0x00000000,"DDR DFI status"),
    Entry("MIO_PIN_00",0xf8000700,32,"rw",0x00001601,"MIO Pin 0 Control"),
    Entry("MIO_PIN_01",0xf8000704,32,"rw",0x00001601,"MIO Pin 1 Control"),
    Entry("MIO_PIN_02",0xf8000708,32,"rw",0x00000601,"MIO Pin 2 Control"),
    Entry("MIO_PIN_03",0xf800070C,32,"rw",0x00000601,"MIO Pin 3 Control"),
    Entry("MIO_PIN_04",0xf8000710,32,"rw",0x00000601,"MIO Pin 4 Control"),
    Entry("MIO_PIN_05",0xf8000714,32,"rw",0x00000601,"MIO Pin 5 Control"),
    Entry("MIO_PIN_06",0xf8000718,32,"rw",0x00000601,"MIO Pin 6 Control"),
    Entry("MIO_PIN_07",0xf800071C,32,"rw",0x00000601,"MIO Pin 7 Control"),
    Entry("MIO_PIN_08",0xf8000720,32,"rw",0x00000601,"MIO Pin 8 Control"),
    Entry("MIO_PIN_09",0xf8000724,32,"rw",0x00001601,"MIO Pin 9 Control"),
    Entry("MIO_PIN_10",0xf8000728,32,"rw",0x00001601,"MIO Pin 10 Control"),
    Entry("MIO_PIN_11",0xf800072C,32,"rw",0x00001601,"MIO Pin 11 Control"),
    Entry("MIO_PIN_12",0xf8000730,32,"rw",0x00001601,"MIO Pin 12 Control"),
    Entry("MIO_PIN_13",0xf8000734,32,"rw",0x00001601,"MIO Pin 13 Control"),
    Entry("MIO_PIN_14",0xf8000738,32,"rw",0x00001601,"MIO Pin 14 Control"),
    Entry("MIO_PIN_15",0xf800073C,32,"rw",0x00001601,"MIO Pin 15 Control"),
    Entry("MIO_PIN_16",0xf8000740,32,"rw",0x00001601,"MIO Pin 16 Control"),
    Entry("MIO_PIN_17",0xf8000744,32,"rw",0x00001601,"MIO Pin 17 Control"),
    Entry("MIO_PIN_18",0xf8000748,32,"rw",0x00001601,"MIO Pin 18 Control"),
    Entry("MIO_PIN_19",0xf800074C,32,"rw",0x00001601,"MIO Pin 19 Control"),
    Entry("MIO_PIN_20",0xf8000750,32,"rw",0x00001601,"MIO Pin 20 Control"),
    Entry("MIO_PIN_21",0xf8000754,32,"rw",0x00001601,"MIO Pin 21 Control"),
    Entry("MIO_PIN_22",0xf8000758,32,"rw",0x00001601,"MIO Pin 22 Control"),
    Entry("MIO_PIN_23",0xf800075C,32,"rw",0x00001601,"MIO Pin 23 Control"),
    Entry("MIO_PIN_24",0xf8000760,32,"rw",0x00001601,"MIO Pin 24 Control"),
    Entry("MIO_PIN_25",0xf8000764,32,"rw",0x00001601,"MIO Pin 25 Control"),
    Entry("MIO_PIN_26",0xf8000768,32,"rw",0x00001601,"MIO Pin 26 Control"),
    Entry("MIO_PIN_27",0xf800076C,32,"rw",0x00001601,"MIO Pin 27 Control"),
    Entry("MIO_PIN_28",0xf8000770,32,"rw",0x00001601,"MIO Pin 28 Control"),
    Entry("MIO_PIN_29",0xf8000774,32,"rw",0x00001601,"MIO Pin 29 Control"),
    Entry("MIO_PIN_30",0xf8000778,32,"rw",0x00001601,"MIO Pin 30 Control"),
    Entry("MIO_PIN_31",0xf800077C,32,"rw",0x00001601,"MIO Pin 31 Control"),
    Entry("MIO_PIN_32",0xf8000780,32,"rw",0x00001601,"MIO Pin 32 Control"),
    Entry("MIO_PIN_33",0xf8000784,32,"rw",0x00001601,"MIO Pin 33 Control"),
    Entry("MIO_PIN_34",0xf8000788,32,"rw",0x00001601,"MIO Pin 34 Control"),
    Entry("MIO_PIN_35",0xf800078C,32,"rw",0x00001601,"MIO Pin 35 Control"),
    Entry("MIO_PIN_36",0xf8000790,32,"rw",0x00001601,"MIO Pin 36 Control"),
    Entry("MIO_PIN_37",0xf8000794,32,"rw",0x00001601,"MIO Pin 37 Control"),
    Entry("MIO_PIN_38",0xf8000798,32,"rw",0x00001601,"MIO Pin 38 Control"),
    Entry("MIO_PIN_39",0xf800079C,32,"rw",0x00001601,"MIO Pin 39 Control"),
    Entry("MIO_PIN_40",0xf80007A0,32,"rw",0x00001601,"MIO Pin 40 Control"),
    Entry("MIO_PIN_41",0xf80007A4,32,"rw",0x00001601,"MIO Pin 41 Control"),
    Entry("MIO_PIN_42",0xf80007A8,32,"rw",0x00001601,"MIO Pin 42 Control"),
    Entry("MIO_PIN_43",0xf80007AC,32,"rw",0x00001601,"MIO Pin 43 Control"),
    Entry("MIO_PIN_44",0xf80007B0,32,"rw",0x00001601,"MIO Pin 44 Control"),
    Entry("MIO_PIN_45",0xf80007B4,32,"rw",0x00001601,"MIO Pin 45 Control"),
    Entry("MIO_PIN_46",0xf80007B8,32,"rw",0x00001601,"MIO Pin 46 Control"),
    Entry("MIO_PIN_47",0xf80007BC,32,"rw",0x00001601,"MIO Pin 47 Control"),
    Entry("MIO_PIN_48",0xf80007C0,32,"rw",0x00001601,"MIO Pin 48 Control"),
    Entry("MIO_PIN_49",0xf80007C4,32,"rw",0x00001601,"MIO Pin 49 Control"),
    Entry("MIO_PIN_50",0xf80007C8,32,"rw",0x00001601,"MIO Pin 50 Control"),
    Entry("MIO_PIN_51",0xf80007CC,32,"rw",0x00001601,"MIO Pin 51 Control"),
    Entry("MIO_PIN_52",0xf80007D0,32,"rw",0x00001601,"MIO Pin 52 Control"),
    Entry("MIO_PIN_53",0xf80007D4,32,"rw",0x00001601,"MIO Pin 53 Control"),
    Entry("MIO_LOOPBACK",0xf8000804,32,"rw",0x00000000,"Loopback function within MIO"),
    Entry("MIO_MST_TRI0",0xf800080C,32,"rw",0xFFFFFFFF,"MIO pin Tri-state Enables, 31:0"),
    Entry("MIO_MST_TRI1",0xf8000810,32,"rw",0x003FFFFF,"MIO pin Tri-state Enables, 53:32"),
    Entry("SD0_WP_CD_SEL",0xf8000830,32,"rw",0x00000000,"SDIO 0 WP CD select"),
    Entry("SD1_WP_CD_SEL",0xf8000834,32,"rw",0x00000000,"SDIO 1 WP CD select"),
    Entry("LVL_SHFTR_EN",0xf8000900,32,"rw",0x00000000,"Level Shifters Enable"),
    Entry("OCM_CFG",0xf8000910,32,"rw",0x00000000,"OCM Address Mapping"),
    Entry("Reserved",0xf8000A1C,32,"rw",0x00010101,"Reserved"),
    Entry("GPIOB_CTRL",0xf8000B00,32,"rw",0x00000000,"PS IO Buffer Control"),
    Entry("GPIOB_CFG_CMOS18",0xf8000B04,32,"rw",0x00000000,"MIO GPIOB CMOS 1.8V config"),
    Entry("GPIOB_CFG_CMOS25",0xf8000B08,32,"rw",0x00000000,"MIO GPIOB CMOS 2.5V config"),
    Entry("GPIOB_CFG_CMOS33",0xf8000B0C,32,"rw",0x00000000,"MIO GPIOB CMOS 3.3V config"),
    Entry("GPIOB_CFG_HSTL",0xf8000B14,32,"rw",0x00000000,"MIO GPIOB HSTL config"),
    Entry("GPIOB_DRVR_BIAS_CTRL",0xf8000B18,32,"mixed",0x00000000,"MIO GPIOB Driver Bias Control"),
    Entry("DDRIOB_ADDR0",0xf8000B40,32,"rw",0x00000800,"DDR IOB Config for ARegister(14:0), CKE and DRST_B"),
    Entry("DDRIOB_ADDR1",0xf8000B44,32,"rw",0x00000800,"DDR IOB Config for BARegister(2:0), ODT, CS_B, WE_B, RAS_B and CAS_B"),
    Entry("DDRIOB_DATA0",0xf8000B48,32,"rw",0x00000800,"DDR IOB Config for Data 15:0"),
    Entry("DDRIOB_DATA1",0xf8000B4C,32,"rw",0x00000800,"DDR IOB Config for Data 31:16"),
    Entry("DDRIOB_DIFF0",0xf8000B50,32,"rw",0x00000800,"DDR IOB Config for DQS 1:0"),
    Entry("DDRIOB_DIFF1",0xf8000B54,32,"rw",0x00000800,"DDR IOB Config for DQS 3:2"),
    Entry("DDRIOB_CLOCK",0xf8000B58,32,"rw",0x00000800,"DDR IOB Config for Clock Output"),
    Entry("DDRIOB_DRIVE_SLEW_ADDR",0xf8000B5C,32,"rw",0x00000000,"Drive and Slew controls for Address and Command pins of the DDR Interface"),
    Entry("DDRIOB_DRIVE_SLEW_DATA",0xf8000B60,32,"rw",0x00000000,"Drive and Slew controls for DQ pins of the DDR Interface"),
    Entry("DDRIOB_DRIVE_SLEW_DIFF",0xf8000B64,32,"rw",0x00000000,"Drive and Slew controls for DQS pins of the DDR Interface"),
    Entry("DDRIOB_DRIVE_SLEW_CLOCK",0xf8000B68,32,"rw",0x00000000,"Drive and Slew controls for Clock pins of the DDR Interface"),
    Entry("DDRIOB_DDR_CTRL",0xf8000B6C,32,"rw",0x00000000,"DDR IOB Buffer Control"),
    Entry("DDRIOB_DCI_CTRL",0xf8000B70,32,"rw",0x00000020,"DDR IOB DCI Config"),
    Entry("DDRIOB_DCI_STATUS",0xf8000B74,32,"mixed",0x00000000,"DDR IO Buffer DCI Status") 
])

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
                print(m_entry_addr.group(1), m_field_name.group(1), m_field_mask.group(1))
                # slcr.update_entry_field(m_entry_addr.group(1), m_field_name.group(1), m_field_mask.group(1))
                # break



if __name__ == "__main__":
    parse_slcr_entries_fields("./hdf/1/ps7_init.c")
    # print(slcr)
