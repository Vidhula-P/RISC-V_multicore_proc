#=========================================================================
# slli
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
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    slli x3, x1, 0x03
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
    gen_rimm_dest_dep_test( 5, "slli", 1, 1, 2 ),
    gen_rimm_dest_dep_test( 4, "slli", 2, 1, 4 ),
    gen_rimm_dest_dep_test( 3, "slli", 3, 1, 6 ),
    gen_rimm_dest_dep_test( 2, "slli", 4, 1, 8 ),
    gen_rimm_dest_dep_test( 1, "slli", 5, 1, 10),
    gen_rimm_dest_dep_test( 0, "slli", 6, 1, 12 ),
  ]

#-------------------------------------------------------------------------
# gen_src_dep_test
#-------------------------------------------------------------------------

def gen_src_dep_test():
  return [
    gen_rimm_src_dep_test( 5, "slli",  7, 1, 14 ),
    gen_rimm_src_dep_test( 4, "slli",  8, 1, 16 ),
    gen_rimm_src_dep_test( 3, "slli",  9, 1, 18 ),
    gen_rimm_src_dep_test( 2, "slli", 1, 16, 65536 ),
    gen_rimm_src_dep_test( 1, "slli", 1, 17, 131072),
    gen_rimm_src_dep_test( 0, "slli", 1, 18, 262144 ),
  ]


#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rimm_src_eq_dest_test( "slli", 25, 1, 50 ),
    gen_rimm_src_eq_dest_test( "slli", 26, 1, 52 ),
    ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [
    gen_rimm_value_test( "slli", 0x10001000, 0x00000000, 0x10001000 ),
    gen_rimm_value_test( "slli", 0x00000001, 0x00000001, 0x00000002 ),
    gen_rimm_value_test( "slli", 0x00000003, 0x00000007, 0x0000180 ),

    gen_rimm_value_test( "slli", 0x8fff8000, 0x00000006, 0xffe00000 ),
    gen_rimm_value_test( "slli", 0x80000000, 0x00000000, 0x80000000 ),
    gen_rimm_value_test( "slli", 0x7fff8000, 0x00000002,  0xfffe0000),
    gen_rimm_value_test( "slli", 0x00f01a000, 0x00000014, 0x00000000 ), #overflow
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
    asm_code.append( gen_rimm_value_test( "slli", src0.uint(), src1.uint(), dest.uint() ) )
  return asm_code
