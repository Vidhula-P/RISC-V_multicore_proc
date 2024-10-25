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

#-------------------------------------------------------------------------
# gen_dest_dep_test
#-------------------------------------------------------------------------

def gen_dest_dep_test():
  return [
    gen_rimm_dest_dep_test( 5, "addi", 1, 1, 2 ),
    gen_rimm_dest_dep_test( 4, "addi", 2, 1, 3 ),
    gen_rimm_dest_dep_test( 3, "addi", 3, 1, 4 ),
    gen_rimm_dest_dep_test( 2, "addi", 4, 1, 5 ),
    gen_rimm_dest_dep_test( 1, "addi", 5, 1, 6 ),
    gen_rimm_dest_dep_test( 0, "addi", 6, 1, 7 ),
  ]

#-------------------------------------------------------------------------
# gen_src_dep_test
#-------------------------------------------------------------------------

def gen_src_dep_test():
  return [
    gen_rimm_src_dep_test( 5, "addi",  7, 1,  8 ),
    gen_rimm_src_dep_test( 4, "addi",  8, 1,  9 ),
    gen_rimm_src_dep_test( 3, "addi",  9, 1, 10 ),
    gen_rimm_src_dep_test( 2, "addi", 1, 10, 11 ),
    gen_rimm_src_dep_test( 1, "addi", 1, 11, 12 ),
    gen_rimm_src_dep_test( 0, "addi", 1, 12, 13 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rimm_src_eq_dest_test( "addi", 25, 1, 26 ),
    gen_rimm_src_eq_dest_test( "addi", 7832, 34, 7866 ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [

    gen_rimm_value_test( "addi", 0x00000000, 0x00000000, 0x00000000 ),
    gen_rimm_value_test( "addi", 0x00000001, 0x00000001, 0x00000002 ),
    gen_rimm_value_test( "addi", 0x00000003, 0x00000007, 0x0000000a ),
    gen_rimm_value_test( "addi", 0x80000000, 0x00000000, 0x80000000 ),
    gen_rimm_value_test( "addi", 0xffffffff, 0x00000001, 0x00000000 ), #overflow
    gen_rimm_value_test( "addi", 0x7fffffff, 0x00000000, 0x7fffffff ),

    gen_rimm_value_test( "addi", 0x80000000, 0x000007FF, 0x800007ff ),
    #gen_rimm_value_test( "addi", 0x80000000, 0x000027ff, 0x800007ff ), #immediate value expected to be 12-bit --> causes an assertion error
    gen_rimm_value_test( "addi", 0x7fffffff, 0x000007FF, 0x800007fe ),
  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in range(100):
    src0 = b32( random.randint(0,0xffffffff) )
    src1 = b32( random.randint(-2048, 2047 ) )
    dest = b32(src0.int() + src1.int())
    asm_code.append( gen_rimm_value_test( "addi", src0.int(), src1.int(), dest.int() ) )
  return asm_code

#-------------------------------------------------------------------------
# gen_alu_use_bypass_X
#-------------------------------------------------------------------------

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
#-------------------------------------------------------------------------
# gen_alu_use_bypass_priority
#-------------------------------------------------------------------------

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
#-------------------------------------------------------------------------
# gen_alu_load_use_double_bypass
#-------------------------------------------------------------------------

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
#-------------------------------------------------------------------------
# gen_alu_use_bypass_M
#-------------------------------------------------------------------------

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
#-------------------------------------------------------------------------
# gen_alu_use_bypass_W
#-------------------------------------------------------------------------

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
