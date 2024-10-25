#=========================================================================
# mul
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
    csrr x1, mngr2proc < 5
    csrr x2, mngr2proc < 4
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    mul x3, x1, x2
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 > 20
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
    gen_rr_dest_dep_test( 5, "mul", 1, 1, 1 ),
    gen_rr_dest_dep_test( 4, "mul", 2, 1, 2 ),
    gen_rr_dest_dep_test( 3, "mul", 3, 1, 3 ),
    gen_rr_dest_dep_test( 2, "mul", 4, 1, 4 ),
    gen_rr_dest_dep_test( 1, "mul", 5, 1, 5 ),
    gen_rr_dest_dep_test( 0, "mul", 6, 1, 6 ),
  ]

#-------------------------------------------------------------------------
# gen_src0_dep_test
#-------------------------------------------------------------------------

def gen_src0_dep_test():
  return [
    gen_rr_src0_dep_test( 5, "mul",  7, 1,  7 ),
    gen_rr_src0_dep_test( 4, "mul",  8, 2, 16 ),
    gen_rr_src0_dep_test( 3, "mul",  9, 3, 27 ),
    gen_rr_src0_dep_test( 2, "mul", 10, 4, 40 ),
    gen_rr_src0_dep_test( 1, "mul", 11, 5, 55 ),
    gen_rr_src0_dep_test( 0, "mul", 12, 6, 72 ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_test
#-------------------------------------------------------------------------

def gen_src1_dep_test():
  return [
    gen_rr_src1_dep_test( 5, "mul",  7, 13,  91 ),
    gen_rr_src1_dep_test( 4, "mul",  8, 14, 112 ),
    gen_rr_src1_dep_test( 3, "mul",  9, 15, 135 ),
    gen_rr_src1_dep_test( 2, "mul", 10, 16, 160 ),
    gen_rr_src1_dep_test( 1, "mul", 11, 17, 187 ),
    gen_rr_src1_dep_test( 0, "mul", 12, 18, 216 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_test
#-------------------------------------------------------------------------

def gen_srcs_dep_test():
  return [
    gen_rr_srcs_dep_test( 5, "mul", 12, 2,  24 ),
    gen_rr_srcs_dep_test( 4, "mul", 13, 3,  39 ),
    gen_rr_srcs_dep_test( 3, "mul", 14, 4,  56 ),
    gen_rr_srcs_dep_test( 2, "mul", 15, 5,  75 ),
    gen_rr_srcs_dep_test( 1, "mul", 16, 6,  96 ),
    gen_rr_srcs_dep_test( 0, "mul", 17, 7, 119 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rr_src0_eq_dest_test( "mul", 125, 6,  750 ),
    gen_rr_src1_eq_dest_test( "mul", 226, 5, 1130 ),
    gen_rr_src0_eq_src1_test( "mul", 27, 729 ),
    gen_rr_srcs_eq_dest_test( "mul", 28, 784 ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [
    gen_rr_value_test( "mul", 0x00000000, 0xffff8000, 0x00000000 ),
    gen_rr_value_test( "mul", 0x00000001, 0x00000001, 0x00000001 ),
    gen_rr_value_test( "mul", 0x00000003, 0x00000007, 0x00000015 ),
    gen_rr_value_test( "mul", 0x80000000, 0x0008f100, 0x00000000 ),#overflow

    gen_rr_value_test( "mul", 0x0000111, 0x00000fff, 0x00110eef ),
    gen_rr_value_test( "mul", 0x00000210, 0x0000007f, 0x000105f0 ),
    gen_rr_value_test( "mul", 0x00008000, 0x00007fff, 0x3fff8000 ),

  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in range(100):
    src0 = b32( random.randint(0,0xffffffff) )
    src1 = b32( random.randint(0,0xffffffff) )
    dest = src0 * src1
    asm_code.append( gen_rr_value_test( "mul", src0.uint(), src1.uint(), dest.uint() ) )
  return asm_code

#-------------------------------------------------------------------------
# gen_mul_dependency_check
#-------------------------------------------------------------------------
#RAW dependency due to MUL
# Base design- The addi instruction needs to be stalled when the variable latency iterative multiplier is being excecuted
# Alt design- The addi instruction needs to be stalled, then bypassed from after the variable latency iterative multiplier is excecuted

def gen_mul_dependency_check():
  return """
    csrr x1, mngr2proc < 5
    csrr x2, mngr2proc < 4
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    mul x3, x1, x2
    addi x6, x3, 1
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x6 > 21
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
  """