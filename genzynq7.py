#!/usr/bin/env python3
import math
from collections import OrderedDict

class RegisterField:
    def __init__(self, mask = 0xFFFFFFFF, value = math.nan):
        self.mask = mask
        self.value = value

    def update_value(self, new_value):
        self.value = new_value

    def __repr__(self):
        return f"RegisterField(mask=0x{self.mask:08X}, value=0x{self.value:08X})"

class Register:
    def __init__(self, addr=math.nan):
        # Store fields related to this register
        self.fields = {}
        self.addr = addr

    def add_field(self, field_name, mask, value):
        """
        Adds a field (RegisterField) to the register.
        """
        self.fields[field_name] = RegisterField(mask=mask, value=value)

    def emit(self):
        """
        Combines all fields by bitwise OR-ing their masks and values.
        """
        combined_mask = 0
        combined_value = 0

        for field in self.fields.values():
            combined_mask |= field.mask
            combined_value |= field.value

        return self.addr, combined_mask, combined_value

    def __repr__(self):
        return f"Register({self.fields})"

class MMIORegisters:
    def __init__(self):
        self._registers = OrderedDict()

    def add_register(self, reg_name, fields):
        self._registers[reg_name] = fields

    def __getattr__(self, reg_name):
        if reg_name in self._registers:
            return self._registers[reg_name]
        raise AttributeError(f"Register '{reg_name}' not found")

    def write_field(self, reg_name, field_name, value):
        """
        Updates a specific field of a register by applying the mask.
        """
        if reg_name in self._registers:
            register = self._registers[reg_name]
            if field_name in register.fields:
                field = register.fields[field_name]
                field.update_value(value)
            else:
                raise AttributeError(f"Field '{field_name}' not found in register '{reg_name}'")
        else:
            raise AttributeError(f"Register '{reg_name}' not found")

    def emit_all(self):
        """
        Emit all registers in the order they were added.
        :return: A list of tuples, where each tuple contains the register name,
                 the combined mask, and the combined value for that register.
        """
        result = []
        for reg_name, register in self._registers.items():
            addr, combined_mask, combined_value = register.emit()
            result.append((reg_name, addr, combined_mask, combined_value))
        return result

# Initialize the MMIO register handler
registers = MMIORegisters()

# Create a new Register object for 'arm_pll_init'
arm_pll_init = Register(0xf8000000)

# Add fields to the 'arm_pll_init' register
arm_pll_init.add_field('pll_res', 0x000000F0, 0x00000020)  # [7:4]
arm_pll_init.add_field('pll_cp', 0x00000F00, 0x00000200)   # [11:8]
arm_pll_init.add_field('lock_cnt', 0x003FF000, 0x000FA000) # [21:12]

# Add the 'arm_pll_init' register to the MMIO handler
registers.add_register('arm_pll_init', arm_pll_init)

# Add another register for demonstration
some_other_reg = Register(0xf8000004)
some_other_reg.add_field('field1', 0x00FF0000, 0x00110000) # Just another field
registers.add_register('some_other_reg', some_other_reg)

# Accessing register fields
print(f"PLL_RES Mask: {registers.arm_pll_init.fields['pll_res'].mask:X}, Value: {registers.arm_pll_init.fields['pll_res'].value:X}")

# Writing new values to a register field
registers.write_field('arm_pll_init', 'pll_res', 0x00000002)
print(f"Updated PLL_RES Value: {registers.arm_pll_init.fields['pll_res'].value:X}")

# Emit combined mask and value for the 'arm_pll_init' register
addr, combined_mask, combined_value = registers.arm_pll_init.emit()
print(f"Addr: 0x{addr:08X}, Combined Mask: 0x{combined_mask:08X}, Combined Value: 0x{combined_value:08X}")

# Emit all registers in the order they were added
emit_results = registers.emit_all()
for reg_name, addr, mask, value in emit_results:
    print(f"Register: {reg_name}, Addr: 0x{addr:08X}, Combined Mask: 0x{mask:08X}, Combined Value: 0x{value:08X}")

# Output the entire register and fields
# print(registers.arm_pll_init)

# [WRITE, MASKWRITE, MASKPOLL, EXIT]

# ps7_mio_init = []
# ps7_pll_init = []
# ps7_clock_init = []
# ps7_ddr_init = []
# ps7_peripherals_init = []
