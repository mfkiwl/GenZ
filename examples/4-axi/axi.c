/* SPDX-License-Identifier: MIT */

int main()
{
	volatile int* gpio2_dirm = (volatile int*)0xe000a284;
	volatile int* gpio2_oen = (volatile int*)0xe000a288;
	volatile int* gpio2_data_out = (volatile int*)0xe000a048;
	volatile int* gpio2_data_in = (volatile int*)0xe000a068;
	volatile int* m_axi_gp0 = (volatile int*)0x40000000;
	volatile int* m_axi_gp1 = (volatile int*)0x80000000;
	int out_pins_mask = 0xf;
	int in_pins_mask = 0x30;

	*gpio2_dirm = out_pins_mask;
	*gpio2_oen = out_pins_mask;
	*gpio2_data_out = 0xf;
	int i = 0x12341234;
	int err0 = 0;
	int err1 = 0;
	*m_axi_gp0 = i;
	*m_axi_gp1 = i;
	err0 = (*m_axi_gp0 == i);
	err1 = (*m_axi_gp1 == 0xabcdabcd);
    while (1) {
		*gpio2_data_out = (1<<3) + (1<<2) + (!err1<<1) + !err0;
		i++;
    }
    return 0;
}
