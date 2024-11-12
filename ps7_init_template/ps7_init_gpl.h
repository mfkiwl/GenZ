// modifed for GenZ
/******************************************************************************
*
* Copyright (C) 2018 Xilinx, Inc.  All rights reserved.
*
*  This program is free software; you can redistribute it and/or modify
*  it under the terms of the GNU General Public License as published by
*  the Free Software Foundation; either version 2 of the License, or
*  (at your option) any later version.
*
*  This program is distributed in the hope that it will be useful,
*  but WITHOUT ANY WARRANTY; without even the implied warranty of
*  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*  GNU General Public License for more details.
*
*  You should have received a copy of the GNU General Public License along
*  with this program; if not, see <http://www.gnu.org/licenses/>
*
*
******************************************************************************/
/****************************************************************************/
/**
*
* @file ps7_init_gpl.h
*
* This file can be included in FSBL code
* to get prototype of ps7_init() function
* and error codes
*
*****************************************************************************/

#ifdef __cplusplus
extern "C" {
#endif


//typedef unsigned int  u32;


/** do we need to make this name more unique ? **/
//extern u32 ps7_init_data[];
extern unsigned long  * ps7_ddr_init_data;
extern unsigned long  * ps7_mio_init_data;
extern unsigned long  * ps7_pll_init_data;
extern unsigned long  * ps7_clock_init_data;
extern unsigned long  * ps7_peripherals_init_data;



#define OPCODE_EXIT       0U
#define OPCODE_CLEAR      1U
#define OPCODE_WRITE      2U
#define OPCODE_MASKWRITE  3U
#define OPCODE_MASKPOLL   4U
#define OPCODE_MASKDELAY  5U
#define NEW_PS7_ERR_CODE 1

/* Encode number of arguments in last nibble */
#define EMIT_EXIT()                   ( (OPCODE_EXIT      << 4 ) | 0 )
#define EMIT_CLEAR(addr)              ( (OPCODE_CLEAR     << 4 ) | 1 ) , addr
#define EMIT_WRITE(addr,val)          ( (OPCODE_WRITE     << 4 ) | 2 ) , addr, val
#define EMIT_MASKWRITE(addr,mask,val) ( (OPCODE_MASKWRITE << 4 ) | 3 ) , addr, mask, val
#define EMIT_MASKPOLL(addr,mask)      ( (OPCODE_MASKPOLL  << 4 ) | 2 ) , addr, mask
#define EMIT_MASKDELAY(addr,mask)      ( (OPCODE_MASKDELAY << 4 ) | 2 ) , addr, mask

/* Returns codes  of PS7_Init */
#define PS7_INIT_SUCCESS   (0)    // 0 is success in good old C
#define PS7_INIT_CORRUPT   (1)    // 1 the data is corrupted, and slcr reg are in corrupted state now
#define PS7_INIT_TIMEOUT   (2)    // 2 when a poll operation timed out
#define PS7_POLL_FAILED_DDR_INIT (3)    // 3 when a poll operation timed out for ddr init
#define PS7_POLL_FAILED_DMA      (4)    // 4 when a poll operation timed out for dma done bit
#define PS7_POLL_FAILED_PLL      (5)    // 5 when a poll operation timed out for pll sequence init


/* Silicon Versions */
#define PCW_SILICON_VERSION_1 0
#define PCW_SILICON_VERSION_2 1
#define PCW_SILICON_VERSION_3 2

/* This flag to be used by FSBL to check whether ps7_post_config() proc exixts */
#define PS7_POST_CONFIG

/* Freq of all peripherals */

#define APU_FREQ APU_FREQ_TBD
#define DDR_FREQ DDR_FREQ_TBD
#define DCI_FREQ DCI_FREQ_TBD
#define QSPI_FREQ QSPI_FREQ_TBD
#define SMC_FREQ SMC_FREQ_TBD
#define ENET0_FREQ ENET0_FREQ_TBD
#define ENET1_FREQ ENET1_FREQ_TBD
#define USB0_FREQ USB0_FREQ_TBD
#define USB1_FREQ USB1_FREQ_TBD
#define SDIO_FREQ SDIO_FREQ_TBD
#define UART_FREQ UART_FREQ_TBD
#define SPI_FREQ SPI_FREQ_TBD
#define I2C_FREQ I2C_FREQ_TBD
#define WDT_FREQ WDT_FREQ_TBD
#define TTC_FREQ TTC_FREQ_TBD
#define CAN_FREQ CAN_FREQ_TBD
#define PCAP_FREQ PCAP_FREQ_TBD
#define TPIU_FREQ TPIU_FREQ_TBD
#define FPGA0_FREQ FPGA0_FREQ_TBD
#define FPGA1_FREQ FPGA1_FREQ_TBD
#define FPGA2_FREQ FPGA2_FREQ_TBD
#define FPGA3_FREQ FPGA3_FREQ_TBD


/* For delay calculation using global registers*/
#define SCU_GLOBAL_TIMER_COUNT_L32	0xF8F00200
#define SCU_GLOBAL_TIMER_COUNT_U32	0xF8F00204
#define SCU_GLOBAL_TIMER_CONTROL	0xF8F00208
#define SCU_GLOBAL_TIMER_AUTO_INC	0xF8F00218

int ps7_config( unsigned long*);
int ps7_init();
int ps7_post_config();
int ps7_debug();
char* getPS7MessageInfo(unsigned key);

void perf_start_clock(void);
void perf_disable_clock(void);
void perf_reset_clock(void);
void perf_reset_and_start_timer(); 
int get_number_of_cycles_for_delay(unsigned int delay); 
#ifdef __cplusplus
}
#endif

