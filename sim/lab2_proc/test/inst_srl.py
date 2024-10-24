#=========================================================================
# srl
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
    csrr x2, mngr2proc < 0x00000003
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    srl x3, x1, x2
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
    gen_rr_dest_dep_test( 7, "srl",    1, 1,  0 ), #truncate 0.5 to 0
    gen_rr_dest_dep_test( 5, "srl",   16, 2,  4 ),
    gen_rr_dest_dep_test( 3, "srl", 3328, 8, 13 ),
  ]

#-------------------------------------------------------------------------
# gen_src0_dep_test
#-------------------------------------------------------------------------

def gen_src0_dep_test():
  return [
    gen_rr_src0_dep_test( 8, "srl",    336,  4,  21 ),
    gen_rr_src0_dep_test( 6, "srl",   7168, 10,  7 ),
    gen_rr_src0_dep_test( 4, "srl", 753664, 15, 23 ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_test
#-------------------------------------------------------------------------

def gen_src1_dep_test():
  return [
    gen_rr_src1_dep_test( 2, "srl",  90112, 13, 11 ),
    gen_rr_src1_dep_test( 1, "srl", 180224, 14, 11 ),
    gen_rr_src1_dep_test( 0, "srl", 360448, 15, 11 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_test
#-------------------------------------------------------------------------

def gen_srcs_dep_test():
  return [
    gen_rr_srcs_dep_test( 5, "srl", 12, 2, 3 ),
    gen_rr_srcs_dep_test( 4, "srl", 24, 3, 3 ),
    gen_rr_srcs_dep_test( 3, "srl", 48, 4, 3 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rr_src0_eq_dest_test( "srl", 26, 1, 13 ),
    gen_rr_src1_eq_dest_test( "srl", 28, 1, 14 ),
    gen_rr_src0_eq_src1_test( "srl", 12, 0 ),
    gen_rr_srcs_eq_dest_test( "srl", 16, 0 ), 
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [
    gen_rr_value_test( "srl", 0x10001000, 0x00000000, 0x10001000 ), #shift by 0
    gen_rr_value_test( "srl", 0xffff8000, 0x00500000, 0xffff8000 ), #takes only last 5 bits of 2nd parameter
    gen_rr_value_test( "srl", 0x7fff8000, 0x00000002,  0x1fffe000),
    gen_rr_value_test( "srl", 0x00f01a000, 0x00000014, 0x000000f0 ), 
  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in range(100):
    src0 = b32( random.randint(0,0xffffffff) )
    src1 = b32( random.randint(0,0x0000001f) )
    dest = src0 >> src1
    asm_code.append( gen_rr_value_test( "srl", src0.uint(), src1.uint(), dest.uint() ) )
  return asm_code
