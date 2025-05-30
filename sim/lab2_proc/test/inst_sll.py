#=========================================================================
# sll
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
    csrr x1, mngr2proc < 0x80008000
    csrr x2, mngr2proc < 0x00000003
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    sll x3, x1, x2
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 > 0x00040000
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
    gen_rr_dest_dep_test( 5, "sll", 1, 1, 2 ),
    gen_rr_dest_dep_test( 4, "sll", 2, 1, 4 ),
    gen_rr_dest_dep_test( 3, "sll", 3, 1, 6 ),
    gen_rr_dest_dep_test( 2, "sll", 4, 1, 8 ),
    gen_rr_dest_dep_test( 1, "sll", 5, 1, 10),
    gen_rr_dest_dep_test( 0, "sll", 6, 1, 12 ),
  ]

#-------------------------------------------------------------------------
# gen_src0_dep_test
#-------------------------------------------------------------------------

def gen_src0_dep_test():
  return [
    gen_rr_src0_dep_test( 5, "sll",  7, 1, 14 ),
    gen_rr_src0_dep_test( 4, "sll",  8, 1, 16 ),
    gen_rr_src0_dep_test( 3, "sll",  9, 1, 18 ),
    gen_rr_src0_dep_test( 2, "sll", 10, 1, 20 ),
    gen_rr_src0_dep_test( 1, "sll", 11, 1, 22 ),
    gen_rr_src0_dep_test( 0, "sll", 12, 1, 24 ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_test
#-------------------------------------------------------------------------

def gen_src1_dep_test():
  return [
    gen_rr_src1_dep_test( 5, "sll", 1, 13, 8192 ),
    gen_rr_src1_dep_test( 4, "sll", 1, 14, 16384 ),
    gen_rr_src1_dep_test( 3, "sll", 1, 15, 32768 ),
    gen_rr_src1_dep_test( 2, "sll", 1, 16, 65536 ),
    gen_rr_src1_dep_test( 1, "sll", 1, 17, 131072),
    gen_rr_src1_dep_test( 0, "sll", 1, 18, 262144 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_test
#-------------------------------------------------------------------------

def gen_srcs_dep_test():
  return [
    gen_rr_srcs_dep_test( 5, "sll", 12, 2, 48 ),
    gen_rr_srcs_dep_test( 4, "sll", 13, 3, 104 ),
    gen_rr_srcs_dep_test( 3, "sll", 14, 4, 224 ),
    gen_rr_srcs_dep_test( 2, "sll", 15, 5, 480 ),
    gen_rr_srcs_dep_test( 1, "sll", 16, 6, 1024 ),
    gen_rr_srcs_dep_test( 0, "sll", 17, 7, 2176 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rr_src0_eq_dest_test( "sll", 25, 1, 50 ),
    gen_rr_src1_eq_dest_test( "sll", 26, 1, 52 ),
    gen_rr_src0_eq_src1_test( "sll", 27, 3623878656 ), #27 << 27
    gen_rr_srcs_eq_dest_test( "sll", 28, 3221225472 ), #28 << 28 = 7516192768 (33 binary bits) --> truncated to 32 bits- 3221225472
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [
    gen_rr_value_test( "sll", 0x10001000, 0x00000000, 0x10001000 ),
    gen_rr_value_test( "sll", 0x00000001, 0x00000001, 0x00000002 ),
    gen_rr_value_test( "sll", 0x00000003, 0x00000007, 0x0000180 ),

    gen_rr_value_test( "sll", 0xffff8000, 0x00500000, 0xffff8000 ), #takes only last 5 bits of 2nd parameter
    gen_rr_value_test( "sll", 0x80000000, 0x00000000, 0x80000000 ),
    gen_rr_value_test( "sll", 0x7fff8000, 0x00000002,  0xfffe0000),
    gen_rr_value_test( "sll", 0x00f01a000, 0x00000014, 0x00000000 ), #overflow
  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in range(100):
    src0 = b32( random.randint(0,0xffffffff) )
    src1 = b32( random.randint(0,0x0000001f) )
    dest = src0 << src1
    asm_code.append( gen_rr_value_test( "sll", src0.uint(), src1.uint(), dest.uint() ) )
  return asm_code