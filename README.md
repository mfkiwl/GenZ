## GenZ: the open-source Zynq 7000 BSP generator

![banner](doc/pic/banner.png)

[Awesome through 2035!](https://www.hackster.io/news/product-lifecycle-extension-for-all-7-series-xilinx-devices-through-2035-4b690dac2d42)

GenZ is a FOSS BSP generator for the Zynq 7000 Processing System (PS). It emits the `ps7_init.c`, `ps7_init.h` and `xparameters.h` required for FSBL building and PS software development, from a simple, text-based configuration. 

Together with [Xilinx embeddedsw](https://github.com/Xilinx/embeddedsw), [OpenXC7](https://github.com/openXC7/), and [Antmicro zynq-mkbootimage](https://github.com/antmicro/zynq-mkbootimage), full Zynq 7000 PS/PL development can be done with NO PROPRIETY TOOLS. 

### Get started

`python3 zynq7000_user.py` -- you can modify it to fit your board. 

Two sets of BSPs will be generated at `ps7_init_pynqz1` and `ps7_init_muzy4`. 

### FSBL and User App

Use my patched branch for No DDR SDCard boot:

```
git clone https://github.com/regymm/embeddedsw
cd embeddedsw/lib/sw_apps/zynq_fsbl/misc/
```

Prepare new board's target, copy in BSP files, and build (No DDR):

```
cp -a base-genz muzy4-genz
cp -a (GenZ)/ps7_init_muzy4/* ./muzy4-genz/
cd ../src
make clean && make BOARD=muzy4-genz "CFLAGS=-DFSBL_DEBUG_INFO -DNODDR"
```
User App, UART test:

```
cd ../../hello_world/src
make clean && make BOARD=muzy4 #"CFLAGS=-DAXI_TEST" #if has a FPGA AXI GPIO
```

Now, we have `zynq_fsbl/src/fsbl.elf` and `hello_world/src/hello-world.elf`. 

JTAG launch on hardware as a test, now this still requires XSCT from Xilinx: 

```
source /opt/Xilinx/Vivado/2019.1/settings64.sh
cd (GenZ)/xsct_tools
./run_elf.tcl # Need to change this file for your pathes
```

- Can switch between GenZ and Xilinx SDK ps7_init.tcl to compare. 
- When launching via JTAG, ps7_init.tcl is run to configure PS7
  - If FSBL is launched, ps7_init.tcl will configure first, then ps7_init.c (compiled into fsbl.elf) configures PS7 again. 

### FPGA

Bitstream for the PL fabric can be generated with [OpenXC7](https://github.com/openXC7/), with demos at [FPGAOL-CE user-examples](https://github.com/FPGAOL-CE/user-examples/tree/main/zynq7000-demos). Makefiles for various FOSS FPGA toolchains can be generated with the [CaaS Wizard](https://github.com/FPGAOL-CE/caas-wizard). 

### BOOT.BIN

It's the file to put in SD card (or QSPI flash) for startup. 

With a .bif file:

```
the_ROM_image:
{
	[bootloader]/path/to/fsbl.elf
	/path/to/fpga.bit
	/path/to/hello-world.elf
}
```

BOOT.bin ready to boot the Zynq board can be generated with [Antmicro zynq-mkbootimage](https://github.com/antmicro/zynq-mkbootimage):

```
zynq-mkbootimage/mkbootimage output.bif BOOT.bin
```

#### Funding

This project is funded through [NGI0 Entrust](https://nlnet.nl/entrust), a fund established by [NLnet](https://nlnet.nl) with financial support from the European Commission's [Next Generation Internet](https://ngi.eu) program. Learn more at the [NLnet project page](https://nlnet.nl/project/PTP-timingcard-gateware).

[<img src="https://nlnet.nl/logo/banner.png" alt="NLnet foundation logo" width="20%" />](https://nlnet.nl) [<img src="https://nlnet.nl/image/logos/NGI0_tag.svg" alt="NGI Zero Logo" width="20%" />](https://nlnet.nl/entrust)
