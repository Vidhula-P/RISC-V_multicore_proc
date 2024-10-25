#=========================================================================
# srai
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
    csrr x1, mngr2proc < 0x00008000
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    srai x3, x1, 0x03
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 > 0x00001000
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
    gen_rimm_dest_dep_test( 7, "srai",   16, 2,  4 ),
    gen_rimm_dest_dep_test( 5, "srai", 3328, 8, 13 ),
    gen_rimm_dest_dep_test( 2, "srai",  -20, 2, -5 ), #signed bit accounted for
  ]

#-------------------------------------------------------------------------
# gen_src_dep_test
#-------------------------------------------------------------------------

def gen_src_dep_test():
  return [
    gen_rimm_src_dep_test( 8, "srai",  -336,  4,  -21 ),
    gen_rimm_src_dep_test( 6, "srai",   7168, 10,   7 ),
    gen_rimm_src_dep_test( 4, "srai",-753664, 15, -23 ),
    gen_rimm_src_dep_test( 8, "srai",   90112, 13,  11 ),
    gen_rimm_src_dep_test( 7, "srai", -180224, 14, -11 ),
    gen_rimm_src_dep_test( 4, "srai", -360448, 15, -11 ),
  ]


#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rimm_src_eq_dest_test( "srai", -14680064, 20, -14 ),
    gen_rimm_src_eq_dest_test( "srai",       -28, 1, -14 ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [
    gen_rimm_value_test( "srai", 0x10001000, 0x00000000, 0x10001000 ), #shift by 0
    gen_rimm_value_test( "srai", 0xffff8000, 0x000001f, 0xffffffff ),
    gen_rimm_value_test( "srai", 0x7fff8000, 0x00000002,  0x1fffe000),
    gen_rimm_value_test( "srai", 0x00f01a000, 0x00000014, 0x000000f0 ), 
  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in range(100):
    src0 = b32(random.randint(-2147483648, 2147483647))
    src1 = b32(random.randint(0, 31))
    
    # Perform arithmetic right shift
    if src0.int() < 0:  # If src0 is negative
      dest = b32((src0.int() >> src1.uint()) | (0xffffffff << (32 - src1.uint())))  # Perform shift and mask result to 32-bit
    else:
      dest = b32(src0.int() >> src1.uint())  # For positive numbers, just use right shift
    
    asm_code.append(gen_rimm_value_test("srai", src0.uint(), src1.uint(), dest.int()))
  
  return asm_code