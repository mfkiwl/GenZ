#!/bin/bash
arm-none-eabi-gcc -mcpu=cortex-a9 -mfpu=vfpv3 -mfloat-abi=hard -Wl,-T -Wl,lscript.ld emio.c -o emio -nostdlib
