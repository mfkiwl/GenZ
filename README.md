## GenZ: the open-source Zynq 7000 BSP generator

![banner](doc/pic/banner.png)

[Awesome through 2035!](https://www.hackster.io/news/product-lifecycle-extension-for-all-7-series-xilinx-devices-through-2035-4b690dac2d42)

GenZ is a FOSS BSP generator for the Zynq 7000 Processing System (PS). It emits the `ps7_init.c`, `ps7_init.h` and `xparameters.h` required for FSBL building and PS software development, from a simple, text-based configuration. 

Together with [OpenXC7](https://github.com/openXC7/), [Xilinx embeddedsw](https://github.com/Xilinx/embeddedsw), and [Antmicro zynq-mkbootimage](https://github.com/antmicro/zynq-mkbootimage), full Zynq 7000 PS/PL development can be done with NO PROPRIETY TOOLS. 

### Get started

There's a bunch of examples! 

[PL only](./examples/1-pl-only) 

[FCLK / 🔥High FCLK](./examplex/2-fclk)  

[EMIO](./examples/3-emio)

[AXI](./examples/4-axi)

[UART / 🔥High-baud UART](./examples/5-uart)

[🕊️No DDR SD Boot, Fully-free](./examples/6-noddr-sdboot)

[🔥ARM overclock](./examples/only-foss-can-do/1-apu-oc)

#### Funding

This project is funded through [NGI0 Entrust](https://nlnet.nl/entrust), a fund established by [NLnet](https://nlnet.nl) with financial support from the European Commission's [Next Generation Internet](https://ngi.eu) program. Learn more at the [NLnet project page](https://nlnet.nl/project/PTP-timingcard-gateware).

[<img src="https://nlnet.nl/logo/banner.png" alt="NLnet foundation logo" width="20%" />](https://nlnet.nl) [<img src="https://nlnet.nl/image/logos/NGI0_tag.svg" alt="NGI Zero Logo" width="20%" />](https://nlnet.nl/entrust)
