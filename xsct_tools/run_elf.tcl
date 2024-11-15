#!xsct
connect -url tcp:127.0.0.1:3121
source /home/petergu/ecptrap/zynq-muzy4-ps/zynq-muzy-ps.sdk/design_1_wrapper_hw_platform_0/ps7_init.tcl
source ../ps7_init_test/ps7_init.tcl
#rst -system
#after 3000
fpga -file /home/petergu/ecptrap/zynq-muzy4-ps/zynq-muzy-ps.sdk/design_1_wrapper_hw_platform_0/design_1_wrapper.bit
configparams force-mem-access 1
targets -set -nocase -filter {name =~"APU*"} -index 0
stop
ps7_init
ps7_post_config
targets -set -nocase -filter {name =~ "ARM*#0"} -index 0
rst -processor
#dow /home/petergu/PTP/zynq-openxc7/embeddedsw/lib/sw_apps/hello_world/src/hello-world.elf
dow /home/petergu/PTP/zynq-openxc7/embeddedsw/lib/sw_apps/zynq_fsbl/src/fsbl.elf
configparams force-mem-access 0
con
