### 2. Using PS FCLK

The crystal oscillator on many ZYNQ boards only goes to the ARM cores (PS). The FPGA (PL) part uses FCLKs driven by the PS. 

On PYNQ-Z1, four LEDs shows blinky driven by the 4 FCLKs. 

Build and program bitstream:

```
$ ./run_caas.sh
$ openFPGALoader --board arty build/top.bit
```

Probably, you can't see blinky after programming bitstream, this means FCLKs are not turned on, which is the default behaviour after power-on. Also, Linux will disable unused FCLKs ([reference](https://xilinx-wiki.atlassian.net/wiki/spaces/A/pages/18841795/Controlling+FCLKs+in+Linux)). 

[GenZ](https://github.com/regymm/GenZ) can then be used to turn the FCLKs on:

```
$ export PYTHONPATH=../..
$ python3 fclk.py
(Using XSCT) 
$ source /opt/Xilinx/Vivado/2019.1/settings64.sh
$ ../../xsct_tools/run_elf_7030.tcl ps7_init_fclk/ps7_init.tcl
(Using OpenOCD)
TODO
```

After configuring the PS FCLKs, 4 LEDs will blinky at different paces (50, 100, 150, and 200 MHz). 

In Vivado, the maximum FCLK frequency is 250 MHz. With Genz, the frequency can be higher (e.g. 400 MHz on 7010/7020, 600 MHz on 7030). `fclk_high.py` generates higher frequencies. 
