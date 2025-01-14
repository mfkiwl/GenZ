/* SPDX-License-Identifier: MIT */

int main()
{
	volatile int* gpio2_dirm = (volatile int*)0xe000a284;
	volatile int* gpio2_oen = (volatile int*)0xe000a288;
	volatile int* gpio2_data_out = (volatile int*)0xe000a048;
	volatile int* gpio2_data_in = (volatile int*)0xe000a068;
	int out_pins_mask = 0xf;
	int in_pins_mask = 0x30;

	*gpio2_dirm = out_pins_mask;
	*gpio2_oen = out_pins_mask;
    while (1) {
		for (int i = 0; i < 20000000; i++);
        /**gpio2_data_out = 0x5;*/
		*gpio2_data_out = *gpio2_data_in >> 4;
    }
    return 0;
}
