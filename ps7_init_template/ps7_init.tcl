proc ps7_pll_init_data_3_0 {} {
PS7_PLL_INIT_DATA_TBD
}
proc ps7_clock_init_data_3_0 {} {
PS7_CLOCK_INIT_DATA_TBD
}
proc ps7_mio_init_data_3_0 {} {
PS7_MIO_INIT_DATA_TBD
}
proc ps7_ddr_init_data_3_0 {} {
PS7_DDR_INIT_DATA_TBD
}
proc ps7_peripherals_init_data_3_0 {} {
PS7_PERIPHERALS_INIT_DATA_TBD
}
proc ps7_post_config_3_0 {} {
PS7_POST_CONFIG_TBD
}

proc mask_poll { addr mask } {
    set cnt 1
	set val 0
    while { $val == 0 } {
        set val "0x[string range [mrd $addr] end-8 end]"
        set val [expr $val & $mask]
		incr cnt
        if { $cnt == 100000 } {
          puts "MASKPOLL FAILED AT ADDRESS: $addr MASK: $mask"
          break
        }
    }
}

proc ps7_post_config {} {
    set saved_mode [configparams force-mem-accesses]
    configparams force-mem-accesses 1
	ps7_post_config_3_0
	configparams force-mem-accesses $saved_mode
}

proc ps7_init {} {
	ps7_mio_init_data_3_0
	ps7_pll_init_data_3_0
	ps7_clock_init_data_3_0
	ps7_ddr_init_data_3_0
	ps7_peripherals_init_data_3_0
}
