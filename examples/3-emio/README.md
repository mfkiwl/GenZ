### 3. Using EMIO: The simplest PS/PL communication

On PYNQ-Z1, use switches to control LEDs, but by the ARM cores (PS), via the EMIO interface. This is a PS/PL communication! The 64-bit EMIO is enough for many low-speed purposes. 

It's made of 3 parts:
- Bitstream wires EMIO port directly to SW/LEDs, in the PL fabric. 
- GenZ configures the ARM cores (PLL, etc.). 
- A ELF file, compiled by the ordinary GCC toolchain, that periodically assigns LEDs to SWs, is loaded to the ARM cores. 

```
$ ./run_caas.sh
$ export PYTHONPATH=../..
$ python3 emio.py
$ arm-none-eabi-gcc -mcpu=cortex-a9 -mfpu=vfpv3 -mfloat-abi=hard -Wl,-T -Wl,lscript.ld emio.c -o emio -nostdlib
(Using XSCT) 
$ source /opt/Xilinx/Vivado/2019.1/settings64.sh
$ ../../xsct_tools/run_elf_7030.tcl ps7_init_emio/ps7_init.tcl build/top.bit emio
```

After configuring everything, the two switches will control two LEDs (LD0, LD1) with a small time delay. 

Also, all `PS7` ports are shown in `top.v`. 
