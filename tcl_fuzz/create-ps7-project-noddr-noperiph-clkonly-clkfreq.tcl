set PROJ_DIR .
set PROJ_NAME ps_project_auto_noddr
set HDF_DIR ./hdf
set HDF_FILE noddr-0-clkfreq.hdf
create_project -force ${PROJ_NAME} ${PROJ_DIR}/${PROJ_NAME} -part xc7z020clg400-1
create_bd_design "design_1"
create_bd_cell -type ip -vlnv xilinx.com:ip:processing_system7:5.5 processing_system7_0
apply_bd_automation -rule xilinx.com:bd_rule:processing_system7 -config {make_external "FIXED_IO, DDR" Master "Disable" Slave "Disable" }  [get_bd_cells processing_system7_0]
connect_bd_net [get_bd_pins processing_system7_0/FCLK_CLK0] [get_bd_pins processing_system7_0/M_AXI_GP0_ACLK]
set_property -dict [list CONFIG.PCW_EN_CLK1_PORT {1} CONFIG.PCW_EN_CLK2_PORT {1} CONFIG.PCW_EN_CLK3_PORT {1} CONFIG.PCW_PRESET_BANK1_VOLTAGE {LVCMOS 1.8V} CONFIG.PCW_UIPARAM_DDR_ENABLE {0}] [get_bd_cells processing_system7_0]
set_property -dict [list CONFIG.PCW_USE_M_AXI_GP1 {1} CONFIG.PCW_USE_S_AXI_GP0 {1} CONFIG.PCW_USE_S_AXI_GP1 {1} CONFIG.PCW_USE_S_AXI_ACP {1} CONFIG.PCW_USE_S_AXI_HP0 {1} CONFIG.PCW_USE_S_AXI_HP1 {1} CONFIG.PCW_USE_S_AXI_HP2 {1} CONFIG.PCW_USE_S_AXI_HP3 {1} CONFIG.PCW_USE_DMA0 {1} CONFIG.PCW_USE_DMA1 {1} CONFIG.PCW_USE_DMA2 {1} CONFIG.PCW_USE_DMA3 {1} CONFIG.PCW_USE_FABRIC_INTERRUPT {0} ] [get_bd_cells processing_system7_0]
delete_bd_objs [get_bd_intf_nets processing_system7_0_DDR]
connect_bd_net [get_bd_pins processing_system7_0/FCLK_CLK0] [get_bd_pins processing_system7_0/M_AXI_GP1_ACLK]
connect_bd_net [get_bd_pins processing_system7_0/FCLK_CLK0] [get_bd_pins processing_system7_0/S_AXI_GP0_ACLK]
connect_bd_net [get_bd_pins processing_system7_0/FCLK_CLK0] [get_bd_pins processing_system7_0/S_AXI_GP1_ACLK]
connect_bd_net [get_bd_pins processing_system7_0/FCLK_CLK0] [get_bd_pins processing_system7_0/S_AXI_ACP_ACLK]
connect_bd_net [get_bd_pins processing_system7_0/FCLK_CLK0] [get_bd_pins processing_system7_0/S_AXI_HP0_ACLK]
connect_bd_net [get_bd_pins processing_system7_0/FCLK_CLK0] [get_bd_pins processing_system7_0/S_AXI_HP1_ACLK]
connect_bd_net [get_bd_pins processing_system7_0/FCLK_CLK0] [get_bd_pins processing_system7_0/S_AXI_HP2_ACLK]
connect_bd_net [get_bd_pins processing_system7_0/FCLK_CLK0] [get_bd_pins processing_system7_0/S_AXI_HP3_ACLK]
connect_bd_net [get_bd_pins processing_system7_0/FCLK_CLK0] [get_bd_pins processing_system7_0/DMA0_ACLK]
connect_bd_net [get_bd_pins processing_system7_0/FCLK_CLK0] [get_bd_pins processing_system7_0/DMA1_ACLK]
connect_bd_net [get_bd_pins processing_system7_0/FCLK_CLK0] [get_bd_pins processing_system7_0/DMA2_ACLK]
connect_bd_net [get_bd_pins processing_system7_0/FCLK_CLK0] [get_bd_pins processing_system7_0/DMA3_ACLK]

set_property -dict [list CONFIG.PCW_CRYSTAL_PERIPHERAL_FREQMHZ {40} CONFIG.PCW_APU_PERIPHERAL_FREQMHZ {620} CONFIG.PCW_FPGA0_PERIPHERAL_FREQMHZ {20} CONFIG.PCW_FPGA1_PERIPHERAL_FREQMHZ {30} CONFIG.PCW_FPGA2_PERIPHERAL_FREQMHZ {40} CONFIG.PCW_FPGA3_PERIPHERAL_FREQMHZ {50}] [get_bd_cells processing_system7_0]


validate_bd_design
save_bd_design
make_wrapper -files [get_files ${PROJ_DIR}/${PROJ_NAME}/${PROJ_NAME}.srcs/sources_1/bd/design_1/design_1.bd] -top
add_files -norecurse ${PROJ_DIR}/${PROJ_NAME}/${PROJ_NAME}.srcs/sources_1/bd/design_1/hdl/design_1_wrapper.v
update_compile_order -fileset sources_1
generate_target all [get_files  ${PROJ_DIR}/${PROJ_NAME}/${PROJ_NAME}.srcs/sources_1/bd/design_1/design_1.bd]
file mkdir ${HDF_DIR}
write_hwdef -force -file ${HDF_DIR}/${HDF_FILE}
file mkdir ${HDF_DIR}
file mkdir ${HDF_DIR}/[file rootname ${HDF_FILE}]
exec unzip ${HDF_DIR}/${HDF_FILE} -d ${HDF_DIR}/[file rootname ${HDF_FILE}]

