#=========================================================================
# addi
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

    csrr x1, mngr2proc, < 5
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    addi x3, x1, 0x0004
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 > 9
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
  """

# ''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Define additional directed and random test cases.
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def gen_alu_use_bypass_X():
  # Bypass from X due to a RAW ALU-use hazard
  # The base design should experience 3 stalls
  # Alternative design should not experience stalls
  return """

    csrr x10, mngr2proc, < 5
    csrr x11, mngr2proc, < 7
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    addi x2, x11, 0x01
    addi x1, x2,  0x01
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x1 > 9
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
  """

def gen_alu_use_bypass_priority():
  # This test has two RAW ALU-use hazards in X and M
  # It should correctly bypass from X instead of M
  # The base design should experience 3 stalls
  # Alternative design should not experience stalls
  return """

    csrr x10, mngr2proc, < 5
    csrr x11, mngr2proc, < 7
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    addi x2, x10, 0x01
    addi x2, x11, 0x01
    addi x1, x2,  0x01
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x1 > 9
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
  """

def gen_alu_load_use_double_bypass():
  # This test has two ALU use and one Load-Use hazards.
  # In the third stage of the second add instruction, 
  # the D stage has to get bypass from both the W and M stage
  # In the Base design, there are 3 stalls after the first addi instruction and 3 stalls after load instruction
  # In the Alt design, there is only 1 stall after the lw instruction
  return """
    csrr x10, mngr2proc < 0x00001FFF
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    addi x1, x10, 0x01
    lw   x2, 0(x1)
    add  x4, x2, x1
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x4 > 0x01022304

    .data
    .word 0x01020304
  """

def gen_alu_use_bypass_M():
  # This builds upon the previous test case
  # This tests for bypass from M to D for ALU-use RAW dependency
  # The base design should experience 2 stalls
  # Alternative design should not experience stalls
  return """

    csrr x10, mngr2proc, < 5
    csrr x11, mngr2proc, < 7
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    addi x2, x10, 0x01
    addi x2, x11, 0x01
    addi x1, x10,  0x02
    addi x3, x2,  0x05
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 > 13
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
  """

def gen_alu_use_bypass_W():
  # This builds upon the previous test case
  # This tests for bypass from W to D for ALU-use RAW dependency
  # The base design should experience 1 stall
  # Alternative design should not experience stalls
  return """

    csrr x10, mngr2proc, < 5
    csrr x11, mngr2proc, < 7
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    addi x2, x10, 0x01
    addi x2, x11, 0x01
    addi x1, x10,  0x01
    addi x3, x11,  0x05
    addi x4, x2,  0x08
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x4 > 16
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
  """
