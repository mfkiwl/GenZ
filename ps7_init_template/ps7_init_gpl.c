/******************************************************************************
* (c) Copyright 2010-2018 Xilinx, Inc. All rights reserved.
*
*    This program is free software; you can redistribute it and/or modify
*    it under the terms of the GNU General Public License as published by
*    the Free Software Foundation; either version 2 of the License, or
*    (at your option) any later version.
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
* @file ps7_init_gpl.c
*
* This file is automatically generated
*
*****************************************************************************/

#include "ps7_init_gpl.h"

unsigned long ps7_pll_init_data_3_0[] = {
PS7_PLL_INIT_DATA_TBD
};

unsigned long ps7_clock_init_data_3_0[] = {
PS7_CLOCK_INIT_DATA_TBD
};

unsigned long ps7_ddr_init_data_3_0[] = {
PS7_DDR_INIT_DATA_TBD
};

unsigned long ps7_mio_init_data_3_0[] = {
PS7_MIO_INIT_DATA_TBD
};

unsigned long ps7_peripherals_init_data_3_0[] = {
PS7_PERIPHERALS_INIT_DATA_TBD
};

unsigned long ps7_post_config_3_0[] = {
PS7_POST_CONFIG_TBD
};

unsigned long ps7_debug_3_0[] = {
};

#include "xil_io.h"
#define PS7_MASK_POLL_TIME 100000000

char*
getPS7MessageInfo(unsigned key) {

  char* err_msg = "";
  switch (key) {
    case PS7_INIT_SUCCESS:                  err_msg = "PS7 initialization successful"; break;
    case PS7_INIT_CORRUPT:                  err_msg = "PS7 init Data Corrupted"; break;
    case PS7_INIT_TIMEOUT:                  err_msg = "PS7 init mask poll timeout"; break;
    case PS7_POLL_FAILED_DDR_INIT:          err_msg = "Mask Poll failed for DDR Init"; break;
    case PS7_POLL_FAILED_DMA:               err_msg = "Mask Poll failed for PLL Init"; break;
    case PS7_POLL_FAILED_PLL:               err_msg = "Mask Poll failed for DMA done bit"; break;
    default:                                err_msg = "Undefined error status"; break;
  }

  return err_msg;
}

unsigned long
ps7GetSiliconVersion () {
  // Read PS version from MCTRL register [31:28]
  unsigned long mask = 0xF0000000;
  unsigned long *addr = (unsigned long*) 0XF8007080;
  unsigned long ps_version = (*addr & mask) >> 28;
  return ps_version;
}

void mask_write (unsigned long add , unsigned long  mask, unsigned long val ) {
        volatile unsigned long *addr = (volatile unsigned long*) add;
        *addr = ( val & mask ) | ( *addr & ~mask);
        //xil_printf("MaskWrite : 0x%x--> 0x%x \n \r" ,add, *addr);
}


int mask_poll(unsigned long add , unsigned long mask ) {
        volatile unsigned long *addr = (volatile unsigned long*) add;
        int i = 0;
        while (!(*addr & mask)) {
          if (i == PS7_MASK_POLL_TIME) {
            return -1;
          }
          i++;
        }
     return 1;
        //xil_printf("MaskPoll : 0x%x --> 0x%x \n \r" , add, *addr);
}

unsigned long mask_read(unsigned long add , unsigned long mask ) {
        volatile unsigned long *addr = (volatile unsigned long*) add;
        unsigned long val = (*addr & mask);
        //xil_printf("MaskRead : 0x%x --> 0x%x \n \r" , add, val);
        return val;
}



int
ps7_config(unsigned long * ps7_config_init)
{
    unsigned long *ptr = ps7_config_init;

    unsigned long  opcode;            // current instruction ..
    unsigned long  args[16];           // no opcode has so many args ...
    int  numargs;           // number of arguments of this instruction
    int  j;                 // general purpose index

    volatile unsigned long *addr;         // some variable to make code readable
    unsigned long  val,mask;              // some variable to make code readable

    int finish = -1 ;           // loop while this is negative !
    int i = 0;                  // Timeout variable

    while( finish < 0 ) {
        numargs = ptr[0] & 0xF;
        opcode = ptr[0] >> 4;

        for( j = 0 ; j < numargs ; j ++ )
            args[j] = ptr[j+1];
        ptr += numargs + 1;


        switch ( opcode ) {

        case OPCODE_EXIT:
            finish = PS7_INIT_SUCCESS;
            break;

        case OPCODE_CLEAR:
            addr = (unsigned long*) args[0];
            *addr = 0;
            break;

        case OPCODE_WRITE:
            addr = (unsigned long*) args[0];
            val = args[1];
            *addr = val;
            break;

        case OPCODE_MASKWRITE:
            addr = (unsigned long*) args[0];
            mask = args[1];
            val = args[2];
            *addr = ( val & mask ) | ( *addr & ~mask);
            break;

        case OPCODE_MASKPOLL:
            addr = (unsigned long*) args[0];
            mask = args[1];
            i = 0;
            while (!(*addr & mask)) {
                if (i == PS7_MASK_POLL_TIME) {
                    finish = PS7_INIT_TIMEOUT;
                    break;
                }
                i++;
            }
            break;
        case OPCODE_MASKDELAY:
            addr = (unsigned long*) args[0];
            mask = args[1];
            int delay = get_number_of_cycles_for_delay(mask);
            perf_reset_and_start_timer();
            while ((*addr < delay)) {
            }
            break;
        default:
            finish = PS7_INIT_CORRUPT;
            break;
        }
    }
    return finish;
}

unsigned long *ps7_mio_init_data = ps7_mio_init_data_3_0;
unsigned long *ps7_pll_init_data = ps7_pll_init_data_3_0;
unsigned long *ps7_clock_init_data = ps7_clock_init_data_3_0;
unsigned long *ps7_ddr_init_data = ps7_ddr_init_data_3_0;
unsigned long *ps7_peripherals_init_data = ps7_peripherals_init_data_3_0;

int
ps7_post_config()
{
  // Get the PS_VERSION on run time
  unsigned long si_ver = ps7GetSiliconVersion ();
  int ret = -1;
  if (si_ver == PCW_SILICON_VERSION_1) {
	  while (1);
	  /*ret = ps7_config (ps7_post_config_1_0);*/
	  /*if (ret != PS7_INIT_SUCCESS) return ret;*/
  } else if (si_ver == PCW_SILICON_VERSION_2) {
	  while (1);
	  /*ret = ps7_config (ps7_post_config_2_0);*/
	  /*if (ret != PS7_INIT_SUCCESS) return ret;*/
  } else {
	  ret = ps7_config (ps7_post_config_3_0);
	  if (ret != PS7_INIT_SUCCESS) return ret;
  }
  return PS7_INIT_SUCCESS;
}

int
ps7_debug()
{
  /*// Get the PS_VERSION on run time*/
  /*unsigned long si_ver = ps7GetSiliconVersion ();*/
  /*int ret = -1;*/
  /*if (si_ver == PCW_SILICON_VERSION_1) {*/
      /*ret = ps7_config (ps7_debug_1_0);*/
      /*if (ret != PS7_INIT_SUCCESS) return ret;*/
  /*} else if (si_ver == PCW_SILICON_VERSION_2) {*/
      /*ret = ps7_config (ps7_debug_2_0);*/
      /*if (ret != PS7_INIT_SUCCESS) return ret;*/
  /*} else {*/
      /*ret = ps7_config (ps7_debug_3_0);*/
      /*if (ret != PS7_INIT_SUCCESS) return ret;*/
  /*}*/
  return PS7_INIT_SUCCESS;
}

int
ps7_init()
{
  // Get the PS_VERSION on run time
  unsigned long si_ver = ps7GetSiliconVersion ();
  xil_printf ("\n Silicon Version : %d.0, only 3 will be supported!!", si_ver);
  int ret;
  //int pcw_ver = 0;

  if (si_ver == PCW_SILICON_VERSION_1) {
	  while (1);
    /*ps7_mio_init_data = ps7_mio_init_data_1_0;*/
    /*ps7_pll_init_data = ps7_pll_init_data_1_0;*/
    /*ps7_clock_init_data = ps7_clock_init_data_1_0;*/
    /*ps7_ddr_init_data = ps7_ddr_init_data_1_0;*/
    /*ps7_peripherals_init_data = ps7_peripherals_init_data_1_0;*/
    //pcw_ver = 1;

  } else if (si_ver == PCW_SILICON_VERSION_2) {
	  while (1);
    /*ps7_mio_init_data = ps7_mio_init_data_2_0;*/
    /*ps7_pll_init_data = ps7_pll_init_data_2_0;*/
    /*ps7_clock_init_data = ps7_clock_init_data_2_0;*/
    /*ps7_ddr_init_data = ps7_ddr_init_data_2_0;*/
    /*ps7_peripherals_init_data = ps7_peripherals_init_data_2_0;*/
    //pcw_ver = 2;

  } else {
    ps7_mio_init_data = ps7_mio_init_data_3_0;
    ps7_pll_init_data = ps7_pll_init_data_3_0;
    ps7_clock_init_data = ps7_clock_init_data_3_0;
    ps7_ddr_init_data = ps7_ddr_init_data_3_0;
    ps7_peripherals_init_data = ps7_peripherals_init_data_3_0;
    //pcw_ver = 3;
  }

  // MIO init
  ret = ps7_config (ps7_mio_init_data);
  if (ret != PS7_INIT_SUCCESS) return ret;

  // PLL init
  ret = ps7_config (ps7_pll_init_data);
  if (ret != PS7_INIT_SUCCESS) return ret;

  // Clock init
  ret = ps7_config (ps7_clock_init_data);
  if (ret != PS7_INIT_SUCCESS) return ret;

  // DDR init
  ret = ps7_config (ps7_ddr_init_data);
  if (ret != PS7_INIT_SUCCESS) return ret;



  // Peripherals init
  ret = ps7_config (ps7_peripherals_init_data);
  if (ret != PS7_INIT_SUCCESS) return ret;
  //xil_printf ("\n PCW Silicon Version : %d.0", pcw_ver);
  return PS7_INIT_SUCCESS;
}




/* For delay calculation using global timer */

/* start timer */
 void perf_start_clock(void)
{
	*(volatile unsigned int*)SCU_GLOBAL_TIMER_CONTROL = ((1 << 0) | // Timer Enable
						      (1 << 3) | // Auto-increment
						      (0 << 8) // Pre-scale
	);
}

/* stop timer and reset timer count regs */
 void perf_reset_clock(void)
{
	perf_disable_clock();
	*(volatile unsigned int*)SCU_GLOBAL_TIMER_COUNT_L32 = 0;
	*(volatile unsigned int*)SCU_GLOBAL_TIMER_COUNT_U32 = 0;
}

/* Compute mask for given delay in milliseconds*/
int get_number_of_cycles_for_delay(unsigned int delay)
{
  // GTC is always clocked at 1/2 of the CPU frequency (CPU_3x2x)
  return (APU_FREQ*delay/(2*1000));

}

/* stop timer */
 void perf_disable_clock(void)
{
	*(volatile unsigned int*)SCU_GLOBAL_TIMER_CONTROL = 0;
}

void perf_reset_and_start_timer()
{
  	    perf_reset_clock();
	    perf_start_clock();
}




