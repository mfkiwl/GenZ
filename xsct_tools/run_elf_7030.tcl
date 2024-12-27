#!xsct
puts "$argc $argv"
connect -url tcp:127.0.0.1:3121
if {$argc > 0} {
	source [lindex $argv 0]
} else {
	source ../ps7_init_fclk/ps7_init.tcl
}
# We program bitstream by hand
if {$argc > 1} {
	if {[lindex $argv 1] != "x"}
	rst -system
	after 3000
	fpga -file [lindex $argv 1]
}
configparams force-mem-access 1
targets -set -nocase -filter {name =~"APU*"} -index 0
stop
# The config is for generic Zynq7000, and even works on a 7030!
ps7_init
ps7_post_config
targets -set -nocase -filter {name =~ "ARM*#0"} -index 0
rst -processor
if {$argc > 2} {
	dow [lindex $argv 2]
}
# The PS really has no peripherals...
#dow /home/petergu/PTP/zynq-openxc7/embeddedsw/lib/sw_apps/hello_world/src/hello-world.elf
#dow /home/petergu/PTP/zynq-openxc7/embeddedsw/lib/sw_apps/zynq_fsbl/src/fsbl.elf
configparams force-mem-access 0
con
