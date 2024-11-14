// Modified for GenZ
/******************************************************************************
* Copyright (c) 2021 - 2022 Xilinx, Inc.  All rights reserved.
* Copyright (C) 2024 Advanced Micro Devices, Inc. All Rights Reserved.
* SPDX-License-Identifier: MIT
******************************************************************************/
#ifndef XPARAMETERS_H
#define XPARAMETERS_H

/* Definition for CPU ID */
#define XPAR_CPU_ID 0U

/* Canonical definitions for peripheral PS7_CORTEXA9_0 */
#define XPAR_CPU_CORTEXA9_0_CPU_CLK_FREQ_HZ APU_FREQ_TBD

#include "xparameters_ps.h"

#define STDIN_BASEADDRESS UART_BASEADDR_TBD
#define STDOUT_BASEADDRESS UART_BASEADDR_TBD

/* Platform specific definitions */
#define PLATFORM_ZYNQ
 
/* Definitions for sleep timer configuration */
#define XSLEEP_TIMER_IS_DEFAULT_TIMER

/* Definitions for driver DEVCFG */
#define XPAR_XDCFG_NUM_INSTANCES 1U
/* Canonical definitions for peripheral PS7_DEV_CFG_0 */
#define XPAR_XDCFG_0_DEVICE_ID 0
#define XPAR_XDCFG_0_BASEADDR 0xF8007000U
#define XPAR_XDCFG_0_HIGHADDR 0xF80070FFU

/* Definitions for driver DMAPS */
#define XPAR_XDMAPS_NUM_INSTANCES 2
/* Canonical definitions for peripheral PS7_DMA_NS */
#define XPAR_XDMAPS_0_DEVICE_ID 0
#define XPAR_XDMAPS_0_BASEADDR 0xF8004000
#define XPAR_XDMAPS_0_HIGHADDR 0xF8004FFF
/* Canonical definitions for peripheral PS7_DMA_S */
#define XPAR_XDMAPS_1_DEVICE_ID 1
#define XPAR_XDMAPS_1_BASEADDR 0xF8003000
#define XPAR_XDMAPS_1_HIGHADDR 0xF8003FFF


/* Definitions for driver GPIOPS */
#define XPAR_XGPIOPS_NUM_INSTANCES 1
/* Canonical definitions for peripheral PS7_GPIO_0 */
#define XPAR_XGPIOPS_0_DEVICE_ID 0
#define XPAR_XGPIOPS_0_BASEADDR 0xE000A000
#define XPAR_XGPIOPS_0_HIGHADDR 0xE000AFFF

// QSPI not supported by GenZ for now
/* Definitions for driver QSPIPS */
#define XPAR_XQSPIPS_NUM_INSTANCES QSPI_NUM_TBD
/* Canonical definitions for peripheral PS7_QSPI_0 */
#define XPAR_XQSPIPS_0_DEVICE_ID 0
#define XPAR_XQSPIPS_0_BASEADDR 0xE000D000
#define XPAR_XQSPIPS_0_HIGHADDR 0xE000DFFF
#define XPAR_XQSPIPS_0_QSPI_CLK_FREQ_HZ QSPI_FREQ_TBD
#define XPAR_XQSPIPS_0_QSPI_MODE 0
#define XPAR_XQSPIPS_0_QSPI_BUS_WIDTH 2

/* Definitions for driver SCUGIC */
#define XPAR_XSCUGIC_NUM_INSTANCES 1U
/* Canonical definitions for peripheral PS7_SCUGIC_0 */
#define XPAR_SCUGIC_0_DEVICE_ID 0U
#define XPAR_SCUGIC_0_CPU_BASEADDR 0xF8F00100U
#define XPAR_SCUGIC_0_CPU_HIGHADDR 0xF8F001FFU
#define XPAR_SCUGIC_0_DIST_BASEADDR 0xF8F01000U

/* Definitions for driver SCUTIMER */
#define XPAR_XSCUTIMER_NUM_INSTANCES 1
/* Canonical definitions for peripheral PS7_SCUTIMER_0 */
#define XPAR_XSCUTIMER_0_DEVICE_ID 0
#define XPAR_XSCUTIMER_0_BASEADDR 0xF8F00600
#define XPAR_XSCUTIMER_0_HIGHADDR 0xF8F0061F

/* Definitions for driver SCUWDT */
#define XPAR_XSCUWDT_NUM_INSTANCES 1
/* Canonical definitions for peripheral PS7_SCUWDT_0 */
#define XPAR_SCUWDT_0_DEVICE_ID 0
#define XPAR_SCUWDT_0_BASEADDR 0xF8F00620
#define XPAR_SCUWDT_0_HIGHADDR 0xF8F006FF

/* Definitions for driver SDPS */
#define XPAR_XSDPS_NUM_INSTANCES SDIO_NUM_TBD
// We just directly generate to XPAR_X....
/* Definitions for peripheral PS7_SD_0 */
#define XPAR_PS7_SD_0_IS_CACHE_COHERENT 0
/* Canonical definitions for peripheral PS7_SD_0 */
#define XPAR_XSDPS_0_DEVICE_ID 0
#define XPAR_XSDPS_0_BASEADDR SDIO_BASEADDR_TBD
#define XPAR_XSDPS_0_HIGHADDR SDIO_HIGHADDR_TBD
#define XPAR_XSDPS_0_SDIO_CLK_FREQ_HZ SDIO_FREQ_TBD
#define XPAR_XSDPS_0_HAS_CD 0
#define XPAR_XSDPS_0_HAS_WP 0
#define XPAR_XSDPS_0_BUS_WIDTH 0
#define XPAR_XSDPS_0_MIO_BANK 0 // unused, don't care
#define XPAR_XSDPS_0_HAS_EMIO 0 // unused, don't care  
#define XPAR_XSDPS_0_SLOT_TYPE 0 // unused, don't care
#define XPAR_XSDPS_0_IS_CACHE_COHERENT 0
#define XPAR_XSDPS_0_CLK_50_SDR_ITAP_DLY 0
#define XPAR_XSDPS_0_CLK_50_SDR_OTAP_DLY 0
#define XPAR_XSDPS_0_CLK_50_DDR_ITAP_DLY 0
#define XPAR_XSDPS_0_CLK_50_DDR_OTAP_DLY 0
#define XPAR_XSDPS_0_CLK_100_SDR_OTAP_DLY 0
#define XPAR_XSDPS_0_CLK_200_SDR_OTAP_DLY 0
#define XPAR_XSDPS_0_CLK_200_DDR_OTAP_DLY 0

/* Definitions for driver UARTPS */
#define XPAR_XUARTPS_NUM_INSTANCES UART_NUM_TBD
#define XPAR_XUARTPS_0_DEVICE_ID 0
#define XPAR_XUARTPS_0_BASEADDR UART_BASEADDR_TBD
#define XPAR_XUARTPS_0_HIGHADDR UART_HIGHADDR_TBD
#define XPAR_XUARTPS_0_UART_CLK_FREQ_HZ UART_FREQ_TBD
#define XPAR_XUARTPS_0_HAS_MODEM 0

/* Definitions for driver XADCPS */
#define XPAR_XADCPS_NUM_INSTANCES 1
#define XPAR_XADCPS_0_DEVICE_ID 0
#define XPAR_XADCPS_0_BASEADDR 0xF8007100
#define XPAR_XADCPS_0_HIGHADDR 0xF8007120

/* Xilinx FAT File System Library (XilFFs) User Settings */
#define FILE_SYSTEM_INTERFACE_SD
#define FILE_SYSTEM_USE_MKFS
#define FILE_SYSTEM_NUM_LOGIC_VOL 2
#define FILE_SYSTEM_USE_STRFUNC 0
#define FILE_SYSTEM_SET_FS_RPATH 0
#define FILE_SYSTEM_WORD_ACCESS
#endif
