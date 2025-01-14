### 4. Using AXI: Gateway to real applications

Using the M_AXI_GP ports from ARM. Minimal AXI device is implemented in the PL, to test AXI transactions emitted by the ARM core as a host. If your complex AXI device doesn't work, this is the basics to check with! 

It's made of 3 parts:
- Bitstream contains two minimal AXI devices for M_AXI_GP0 and M_AXI_GP1 -- one reads back the writen data, and one reads back a constant. 
- GenZ configures the ARM cores (PLL, FCLK, EMIO, etc.). 
- A ELF file running in ARM cores, that interacts with the AXI devices in PL -- at 0x40000000 and 0x80000000 (UG585, chap. 4.1). 

```
$ ./run_caas.sh
$ export PYTHONPATH=../..
$ python3 axi.py
$ arm-none-eabi-gcc -mcpu=cortex-a9 -mfpu=vfpv3 -mfloat-abi=hard -Wl,-T -Wl,lscript.ld axi.c -o axi -nostdlib
(Using XSCT) 
$ source /opt/Xilinx/Vivado/2019.1/settings64.sh
$ ../../xsct_tools/run_elf_7030.tcl ps7_init_axi/ps7_init.tcl build/top.bit axi
```

The upper (left) two LEDs should be on, indication EMIO is working and AXI transactions have finished. 
The lower (right) two LEDs should be off, indicating no error. If 4 LEDs are all on, then probably an AXI transaction hung the ARM cores. In this case, a reset to the ARM cores or a powercycle is needed. 
