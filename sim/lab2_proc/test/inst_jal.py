#=========================================================================
# jal
#=========================================================================

from pymtl3 import *
from lab2_proc.test.inst_utils import *
import random

#-------------------------------------------------------------------------
# gen_basic_test
#-------------------------------------------------------------------------

def gen_basic_test():
  return """

    # Use r3 to track the control flow pattern
    addi  x3, x0, 0     # 0x0200
                        #
    nop                 # 0x0204
    nop                 # 0x0208
    nop                 # 0x020c
    nop                 # 0x0210
    nop                 # 0x0214
    nop                 # 0x0218
    nop                 # 0x021c
    nop                 # 0x0220
                        #
    jal   x1, label_a   # 0x0224
    addi  x3, x3, 0b01  # 0x0228

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
    csrw  proc2mngr, x1 > 0x0228

    # Only the second bit should be set if jump was taken
    csrw  proc2mngr, x3 > 0b10

  """

#-------------------------------------------------------------------------
# gen_jal_imm_test
# Test the passing of an immediate operand
#-------------------------------------------------------------------------

def gen_jal_imm_test():
  return """
    # Use r3 to track the control flow pattern
    addi  x3, x0, 0     # 0x0200
                        #
    nop                 # 0x0204
    nop                 # 0x0208
    nop                 # 0x020c
    nop                 # 0x0210
    nop                 # 0x0214
    nop                 # 0x0218
    nop                 # 0x021c
    nop                 # 0x0220
                        #
    jal   x1, 0x00c     # 0x0224
    addi  x3, x3, 0b01  # 0x0228
    nop

    addi  x3, x3, 0b10

    # Check the link address
    csrw  proc2mngr, x1 > 0x0228

    # Only the second bit should be set if jump was taken
    csrw  proc2mngr, x3 > 0b10
  """


#-------------------------------------------------------------------------
# gen_jal_nested_test
# Test nested jal instructions
#-------------------------------------------------------------------------

def gen_jal_nested_test():
  return """
    # Test nested jumps using JAL

    addi  x3, x0, 0     # 0x0200

    jal   x1, label_e   # 0x0204

    nop
    nop
    nop
    nop

  label_e:
    addi  x3, x3, 0b0001
    jal   x2, label_g

  label_f:
    addi  x3, x3, 0b0010
    jal   x4, label_h

  label_g:
    addi  x3, x3, 0b0100
    jal   x5, label_end

  label_h:
    addi  x3, x3, 0b1000
    jal   x6, label_end

  label_end:
    csrw  proc2mngr, x3 > 0b0101
    csrw  proc2mngr, x1 > 0x0208
    csrw  proc2mngr, x2 > 0x0220
    csrw  proc2mngr, x5 > 0x0230
  """


#-------------------------------------------------------------------------
# gen_jal_no_return_test
# Test a jal instruction that writes to x0
#-------------------------------------------------------------------------

def gen_jal_no_return_test():
  return """
    # Test if JAL behaves correctly with x0 as link register (no return)

    jal   x0, label_l        # Jump to label_l, but don't save return address

    # Instruction that would have been executed if no jump occurred
    addi  x3, x3, 0b01       # This should not be executed

    nop
    nop

  label_l:
    addi  x3, x0, 0b10       # This should be executed after jump

    # Ensure that no link is saved, and x3 is updated correctly
    csrw  proc2mngr, x3 > 0b10
  """


#-------------------------------------------------------------------------
# gen_jal_with_branch_not_taken_test
# Test a jal instruction that comes after a branch not taken instruction.
#-------------------------------------------------------------------------

def gen_jal_with_branch_not_taken_test():
  return """
    # Test JAL with conditional branches

    addi  x3, x0, 0b00001      # Set x3 to 0b01

    beq   x3, x0, skip_jal  # If x3 == 0, skip the jump (should not happen)
    jal   x1, label_m       # Jump to label_m

    addi  x3, x3, 0b00010      # This should not be executed due to the jump

  skip_jal:
    addi  x3, x3, 0b00100      # Should not be executed since x3 is not zero

  label_m:
    addi  x3, x3, 0b01000     # Executed after the jump

    # Check the link address
    csrw  proc2mngr, x1 > 0x020c

    # Ensure x3 is correctly updated after the jump
    csrw  proc2mngr, x3 > 0b01001
  """

#-------------------------------------------------------------------------
# gen_jal_with_branch_taken_test
# Test a jal instruction that comes after a branch taken instruction.
# The bypass should correctly priroritise branch over the jal
#-------------------------------------------------------------------------

def gen_jal_with_branch_taken_test():
  return """
    # Test JAL with conditional branches

    addi  x3, x0, 0b0      # Set x3 to 0b0

    beq   x3, x0, skip_jal  # If x3 == 0, skip the jump (should not happen)
    jal   x1, label_m       # Jump to label_m

    addi  x3, x3, 0b00010      # This should not be executed due to the jump

  skip_jal:
    addi  x3, x3, 0b00100      # Should not be executed since x3 is not zero

  label_m:
    addi  x3, x3, 0b01000     # Executed after the jump

    # Ensure x3 is correctly updated after the jump
    csrw  proc2mngr, x3 > 0b01100
  """

#-------------------------------------------------------------------------
# gen_jal_function_call_test
# Simulate a function call using jal
#-------------------------------------------------------------------------

def gen_jal_function_call_test():
  return """
    # Simulate function call using JAL

    jal   x1, function_a     # Jump to function_a

  label_o:
    addi  x3, x3, 0b100      # Continue after returning from function

    # Check if link register is correct after returning from the function
    csrw  proc2mngr, x1 > 0x0218
    csrw  proc2mngr, x3 > 0b101

  function_a:
    addi  x3, x0, 0b01       # Set x3 inside the function
    jalr  x1, x1, 0          # Return to caller
  """

#-------------------------------------------------------------------------
# gen_jal_dep_tests
# Test the bypass paths by varying how many nops are inserted
# between writing the x3 register and reading this register in the instr
# after the jal.
#-------------------------------------------------------------------------

def gen_jal_dep_tests():
  reset_jal_template()
  return [
    gen_jal_dep_test ( 5 ),
    gen_jal_dep_test ( 4 ),
    gen_jal_dep_test ( 3 ),
    gen_jal_dep_test ( 2 ),
    gen_jal_dep_test ( 1 ),
    gen_jal_dep_test ( 0 ),
  ]


#-------------------------------------------------------------------------
# gen_jal_large_offset_tests
# Vary how many nops are between the jal instruction and the jal target
# This tests the jal with large imm offsets.
#-------------------------------------------------------------------------

def gen_jal_large_offset_tests():
  reset_jal_template()
  return [
    gen_jal_large_offset_test ( 500 ),
    gen_jal_large_offset_test ( 400 ),
    gen_jal_large_offset_test ( 335 ),
    gen_jal_large_offset_test ( 221 ),
    gen_jal_large_offset_test ( 106 ),
    gen_jal_large_offset_test ( 0 ),
  ]

#-------------------------------------------------------------------------
# gen_jal_random_tests
#-------------------------------------------------------------------------

def gen_jal_random_tests():
  reset_jal_template()
  asm_code = []
  for _ in range(25):
    num_nops_before = random.randint(0, 500)
    num_nops_after  = random.randint(0, 500)
    asm_code.append( gen_jal_any_nops_test( num_nops_before, num_nops_after) )
  return asm_code