/* SPDX-License-Identifier: MIT */

SECTIONS
{
. = 0xFFFF0000;
.text : { *(.text) }
.data : { *(.data) }
.bss : { *(.bss) }
}
