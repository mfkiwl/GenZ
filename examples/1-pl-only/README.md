### 1. PL only bitstream

This only uses the fabric, with no connection to the ARM part. The PS7 instantiation is optional. 

On PYNQ-Z1, two LEDs will show a counter, and the other two are controlled by SW1/SW0. 

Build and program bitstream:

```
$ ./run_caas.sh
$ openFPGALoader --board arty build/top.bit
```

Optionally, build with Vivado:

```
$ source /opt/Xilinx/Vivado/2019.1/settings64.sh
$ make -f Makefile.vivado
```
