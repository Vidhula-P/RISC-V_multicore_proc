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

#-------------------------------------------------------------------------
# gen_st_src_dep_test
#-------------------------------------------------------------------------

def gen_src_dep_test():
  return [

    gen_st_src_dep_test( 5, "sw", 0x2000, 0x00010203 ),
    gen_st_src_dep_test( 4, "sw", 0x2004, 0x04050607 ),
    gen_st_src_dep_test( 3, "sw", 0x2008, 0x08090a0b ),
    gen_st_src_dep_test( 2, "sw", 0x200c, 0x0c0d0e0f ),
    gen_st_src_dep_test( 1, "sw", 0x2010, 0x10111213 ),
    gen_st_src_dep_test( 0, "sw", 0x2014, 0x14151617 ),
  ]

#-------------------------------------------------------------------------
# gen_base_dep_test
#-------------------------------------------------------------------------

def gen_base_dep_test():
  return [

    gen_st_base_dep_test( 5, "sw", 0x2000, 0x00010203 ),
    gen_st_base_dep_test( 4, "sw", 0x2004, 0x04050607 ),
    gen_st_base_dep_test( 3, "sw", 0x2008, 0x08090a0b ),
    gen_st_base_dep_test( 2, "sw", 0x200c, 0x0c0d0e0f ),
    gen_st_base_dep_test( 1, "sw", 0x2010, 0x10111213 ),
    gen_st_base_dep_test( 0, "sw", 0x2014, 0x14151617 ),

  ]

#-------------------------------------------------------------------------
# gen_base_eq_src_test
#-------------------------------------------------------------------------

def gen_base_eq_src_test():
  return [
    gen_st_base_eq_src_test( "sw", 0x2000, 0x00020304 ),
    gen_word_data([ 0x01020304 ])
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [

    # Test positive offsets

    gen_st_value_test( "sw",   0, 0x00002000, 0xdeadbeef ),
    gen_st_value_test( "sw",   4, 0x00002000, 0x00010203 ),
    gen_st_value_test( "sw",   8, 0x00002000, 0x04050607 ),
    gen_st_value_test( "sw",  12, 0x00002000, 0x08090a0b ),
    gen_st_value_test( "sw",  16, 0x00002000, 0x0c0d0e0f ),
    gen_st_value_test( "sw",  20, 0x00002000, 0xcafecafe ),

    # # Test negative offsets

    gen_st_value_test( "sw", -20, 0x00002014, 0xdeadbeef ),
    gen_st_value_test( "sw", -16, 0x00002014, 0x00010203 ),
    gen_st_value_test( "sw", -12, 0x00002014, 0x04050607 ),
    gen_st_value_test( "sw",  -8, 0x00002014, 0x08090a0b ),
    gen_st_value_test( "sw",  -4, 0x00002014, 0x0c0d0e0f ),
    gen_st_value_test( "sw",   0, 0x00002014, 0xcafecafe ),

    # Test positive offset with unaligned base

    gen_st_value_test( "sw",   1, 0x00001fff, 0xdeadbeef ),
    gen_st_value_test( "sw",   5, 0x00001fff, 0x00010203 ),
    gen_st_value_test( "sw",   9, 0x00001fff, 0x04050607 ),
    gen_st_value_test( "sw",  13, 0x00001fff, 0x08090a0b ),
    gen_st_value_test( "sw",  17, 0x00001fff, 0x0c0d0e0f ),
    gen_st_value_test( "sw",  21, 0x00001fff, 0xcafecafe ),

    # Test negative offset with unaligned base

    gen_st_value_test( "sw", -21, 0x00002015, 0xdeadbeef ),
    gen_st_value_test( "sw", -17, 0x00002015, 0x00010203 ),
    gen_st_value_test( "sw", -13, 0x00002015, 0x04050607 ),
    gen_st_value_test( "sw",  -9, 0x00002015, 0x08090a0b ),
    gen_st_value_test( "sw",  -5, 0x00002015, 0x0c0d0e0f ),
    gen_st_value_test( "sw",  -1, 0x00002015, 0xcafecafe ),

  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():

  # Generate some random data to store

  data = []
  for i in range(128):
    data.append(random.randint(0, 0xffffffff))

  # Generate random store accesses

  asm_code = []
  for i in range(100):

    a = random.randint(0, 127)   # Random index for data array
    b = random.randint(0, 127)   # Random index for base address

    base   = 0x2000 + (4 * b)    # Base address with random offset
    offset = 4 * (a - b)         # Offset to store at a calculated memory location
    src_val = data[a]            # Random value to store

    # Generate the store instruction
    asm_code.append(gen_st_value_test("sw", offset, base, src_val))

  # Add the data section (optional, for checking)
  asm_code.append(gen_word_data(data))

  return asm_code


#-------------------------------------------------------------------------
# unit tests for evaluation
#-------------------------------------------------------------------------

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

