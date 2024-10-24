#=========================================================================
# jalr
#=========================================================================

import random

# Fix the random seed so results are reproducible
random.seed(0xdeadbeef)

from pymtl3 import *
from lab2_proc.test.inst_utils import *

#-------------------------------------------------------------------------
# gen_basic_test
#-------------------------------------------------------------------------

def gen_basic_test():
  return """

    # Use r3 to track the control flow pattern
    addi  x3, x0, 0           # 0x0200
                              #
    lui x1,      %hi[label_a] # 0x0204
    addi x1, x1, %lo[label_a] # 0x0208
                              #
    nop                       # 0x020c
    nop                       # 0x0210
    nop                       # 0x0214
    nop                       # 0x0218
    nop                       # 0x021c
    nop                       # 0x0220
    nop                       # 0x0224
    nop                       # 0x0228
                              #
    jalr  x31, x1, 0          # 0x022c
    addi  x3, x3, 0b01        # 0x0230

    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop

  label_a:
    addi  x3, x3, 0b10

    # Check the link address
    csrw  proc2mngr, x31 > 0x0230

    # Only the second bit should be set if jump was taken
    csrw  proc2mngr, x3  > 0b10

  """

#-------------------------------------------------------------------------
# gen_jalr_imm_test
# Test the passing of an immediate operand
#-------------------------------------------------------------------------

def gen_jalr_imm_test():
  return """

    # Use r3 to track the control flow pattern
    addi  x3, x0, 0           # 0x0200
                              #
    lui x1,      %hi[label_a] # 0x0204
    addi x1, x1, %lo[label_a] # 0x0208
                              #
    nop                       # 0x020c
    nop                       # 0x0210
    nop                       # 0x0214
    nop                       # 0x0218
    nop                       # 0x021c
    nop                       # 0x0220
    nop                       # 0x0224
    nop                       # 0x0228
                              #
    jalr  x31, x1, 0x08          # 0x022c
    addi  x3, x3, 0b01        # 0x0230

    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop

  label_a:
    addi  x3, x3, 0b10
    addi  x3, x3, 0b100
    addi  x3, x3, 0b1000


    # Check the link address
    csrw  proc2mngr, x31 > 0x0230

    # Only the second bit should be set if jump was taken
    csrw  proc2mngr, x3  > 0b1000

  """


#-------------------------------------------------------------------------
# gen_jalr_nested_test
# Test nested jalr instructions
#-------------------------------------------------------------------------

def gen_jalr_nested_test():
  return """
    # Test nested jumps using JALR

    lui x1,      %hi[label_e]
    addi x1, x1, %lo[label_e]
    lui x2,      %hi[label_f]
    addi x2, x2, %lo[label_f]
    lui x3,      %hi[label_g]
    addi x3, x3, %lo[label_g]
    lui x4,      %hi[label_h]
    addi x4, x4, %lo[label_h]
    lui  x14,      %hi[label_end]
    addi x14, x14, %lo[label_end]

    addi  x10, x0, 0

    jalr   x5, x1, 0x00

    nop
    nop
    nop
    nop

  label_e:
    addi  x10, x3, 0b0001
    addi  x10, x3, 0b0010
    jalr  x6, x3, 0x01

  label_f:
    addi  x10, x3, 0b0100
    addi  x10, x3, 0b1000
    jalr  x7, x4, 0x00

  label_g:
    addi  x10, x3, 0b10000
    addi  x10, x3, 0b100000
    jalr  x8, x14, 0x00

  label_h:
    addi  x10, x3, 0b1000000
    addi  x10, x3, 0b10000000
    jalr  x9, x14, 0x00

  label_end:
    csrw  proc2mngr, x10 > 0b01001111000
    csrw  proc2mngr, x6 > 0x024c
    csrw  proc2mngr, x7 > 0x0000
    csrw  proc2mngr, x8 > 0x0264
    csrw  proc2mngr, x9 > 0x0000
  """

#-------------------------------------------------------------------------
# gen_jalr_no_return_test
# Test a jalr instruction that writes to x0
#-------------------------------------------------------------------------

def gen_jalr_no_return_test():
  return """
    # Test if JALR behaves correctly with x0 as link register (no return)

    lui x1,      %hi[label_a]
    addi x1, x1, %lo[label_a]
    jalr   x0, x1, 0x00        # Jump to label_l, but don't save return address

    # Instruction that would have been executed if no jump occurred
    addi  x3, x3, 0b01       # This should not be executed

    nop
    nop

  label_a:
    addi  x3, x0, 0b10       # This should be executed after jump

    # Ensure that no link is saved, and x3 is updated correctly
    csrw  proc2mngr, x3 > 0b10
  """

#-------------------------------------------------------------------------
# gen_jalr_with_branch_not_taken_test
# Test a jalr instruction that comes after a branch not taken instruction.
#-------------------------------------------------------------------------

def gen_jalr_with_branch_not_taken_test():
  return """
    # Test JAL with conditional branches

    lui x10,      %hi[label_m]
    addi x10, x10, %lo[label_m]

    addi  x3, x0, 0b00001      # Set x3 to 0b01

    beq   x3, x0, skip_jal  # If x3 == 0, skip the jump (should not happen)
    jalr   x1, x10, 0x00       # Jump to label_m

    addi  x3, x3, 0b00010      # This should not be executed due to the jump

  skip_jal:
    addi  x3, x3, 0b00100      # Should not be executed since x3 is not zero

  label_m:
    addi  x3, x3, 0b01000     # Executed after the jump

    # Check the link address
    csrw  proc2mngr, x1 > 0x0214

    # Ensure x3 is correctly updated after the jump
    csrw  proc2mngr, x3 > 0b01001
  """

#-------------------------------------------------------------------------
# gen_jalr_with_branch_taken_test
# Test a jalr instruction that comes after a branch taken instruction.
# The bypass should correctly priroritise branch over the jalr
#-------------------------------------------------------------------------

def gen_jalr_with_branch_taken_test():
  return """
    # Test JALR with conditional branches

    lui x10,      %hi[label_m]
    addi x10, x10, %lo[label_m]

    addi  x3, x0, 0b0      # Set x3 to 0b0

    beq   x3, x0, skip_jal  # If x3 == 0, skip the jump (should not happen)
    jalr   x1, x10, 0x00       # Jump to label_m

    addi  x3, x3, 0b00010      # This should not be executed due to the jump

  skip_jal:
    addi  x3, x3, 0b00100      # Should not be executed since x3 is not zero

  label_m:
    addi  x3, x3, 0b01000     # Executed after the jump

    # Ensure x3 is correctly updated after the jump
    csrw  proc2mngr, x3 > 0b01100
  """

#-------------------------------------------------------------------------
# gen_jalr_function_call_test
# Simulate a function call using jalr
#-------------------------------------------------------------------------

def gen_jalr_function_call_test():
  return """
    # Simulate function call using JALR

    lui x10,      %hi[label_m]
    addi x10, x10, %lo[label_m]

    jalr   x1, x10, 0x00     # Jump to function_a

  label_m:
    addi  x3, x3, 0b100      # Continue after returning from function

    # Check if link register is correct after returning from the function
    csrw  proc2mngr, x1 > 0x020c
    csrw  proc2mngr, x3 > 0b100

  function_a:
    addi  x3, x0, 0b01       # Set x3 inside the function
    jalr  x1, x1, 0          # Return to caller
  """