#=========================================================================
# sw
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
    csrr x1, mngr2proc < 0x00002000
    csrr x2, mngr2proc < 0xdeadbeef
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    sw   x2, 8(x1)
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    lw   x3, 8(x1)
    csrw proc2mngr, x3 > 0xdeadbeef

    .data
    .word 0x01020304
  """

# ''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Define additional directed and random test cases.
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def gen_long_test():
  return """
    csrr x1, mngr2proc < 0x00002000
    csrr x2, mngr2proc < 0xdeadbeef
    csrr x3, mngr2proc < 0xdea00eef
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    sw   x2, 0(x1)
    sw   x2, 4(x1)
    sw   x3, 8(x1)
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    lw   x4, 4(x1)
    lw   x5, 8(x1)
    lw   x8, 0(x1)
    csrw proc2mngr, x4 > 0xdeadbeef
    csrw proc2mngr, x5 > 0xdea00eef
    csrw proc2mngr, x8 > 0xdeadbeef

    .data
    .word 0x01020304
  """

def gen_long_test_from_eval():
  return """
    csrr  x1, mngr2proc < 100
    csrr x6, mngr2proc < 0x2000
    csrr x7, mngr2proc < 0x3000
    csrr x8, mngr2proc < 0x4000
    csrr x9, mngr2proc < 0x5000
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    sw   x6, 0(x1)
    sw   x7, 4(x1)
    sw   x8, 8(x1)
    sw   x9, 12(x1)
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    lw   x3, 0(x1)
    lw   x4, 4(x1)
    lw   x5, 8(x1)
    lw   x10, 12(x1)
    csrw proc2mngr, x3 > 0x2000
    csrw proc2mngr, x4 > 0x3000
    csrw proc2mngr, x5 > 0x4000
    csrw proc2mngr, x10 > 0x5000

    .data
    .word 0x01020304
  """

def gen_long_complex_check():

    # text section

    return """
    # load array pointers
    csrr  x1, mngr2proc < 100
    csrr  x2, mngr2proc < 0x2000
    csrr  x3, mngr2proc < 0x3000
    csrr  x4, mngr2proc < 0x4000
    add   x5, x0, x1

    # main loop
  loop:
    lw    x6,   0(x2)
    lw    x7,   4(x2)
    lw    x8,   8(x2)
    lw    x9,  12(x2)
    lw    x10,  0(x3)
    lw    x11,  4(x3)
    lw    x12,  8(x3)
    lw    x13, 12(x3)
    add   x6, x6, x10
    add   x7, x7, x11
    add   x8, x8, x12
    add   x9, x9, x13
    sw    x6,   0(x4)
    sw    x7,   4(x4)
    sw    x8,   8(x4)
    sw    x9,  12(x4)
    addi  x5, x5, -4
    addi  x2, x2, 16
    addi  x3, x3, 16
    addi  x4, x4, 16
    # bne   x5, x0, loop

    # end of the program
    csrw  proc2mngr, x0 > 0
    nop
    nop
    nop
    nop
    nop
    nop
"""

    # mem_image = assemble( text )

    # # load data by manually create data sections using binutils

    # src0_section = mk_section( ".data", c_vvadd_src0_ptr, src0 )

    # src1_section = mk_section( ".data", c_vvadd_src1_ptr, src1 )

    # # load data

    # mem_image.add_section( src0_section )
    # mem_image.add_section( src1_section )

    # return mem_image
