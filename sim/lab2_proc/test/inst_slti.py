#=========================================================================
# slti
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
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    slti x3, x1, 6
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 > 1
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
    gen_rimm_dest_dep_test( 5, "slti", -1,  1, 1 ),
    gen_rimm_dest_dep_test( 4, "slti",  2,  1, 0 ),
    gen_rimm_dest_dep_test( 3, "slti",  3, -1, 0 ),
    gen_rimm_dest_dep_test( 2, "slti",  4,  1, 0 ),
    gen_rimm_dest_dep_test( 1, "slti", -5,  1, 1 ),
    gen_rimm_dest_dep_test( 0, "slti", -6, -1, 1 ),
  ]

#-------------------------------------------------------------------------
# gen_src_dep_test
#-------------------------------------------------------------------------

def gen_src_dep_test():
  return [
    gen_rimm_src_dep_test( 5, "slti",   7, 1,  0 ),
    gen_rimm_src_dep_test( 4, "slti",  -8, 1,  1 ),
    gen_rimm_src_dep_test( 3, "slti",   9, 1,  0 ),
    gen_rimm_src_dep_test( 2, "slti", -1, -16, 0 ),
    gen_rimm_src_dep_test( 1, "slti",  1,  17, 1 ),
    gen_rimm_src_dep_test( 0, "slti",  1,  18, 1 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rimm_src_eq_dest_test( "slti", 1, 25, 1  ),
    gen_rimm_src_eq_dest_test( "slti", 27, 1, 0),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [
    gen_rimm_value_test( "slti", 0x00000000, 0x00000000, 0 ),
    gen_rimm_value_test( "slti", 0xfffffff0, 0x00000000, 1 ),
    gen_rimm_value_test( "slti", 0xffffffff, 0x00000001, 1 ),

    gen_rimm_value_test( "slti", 0x0000001e, 0x0000041f, 1 ),
    gen_rimm_value_test( "slti", 0x00007fff, 0x00000fca, 0 ),
    gen_rimm_value_test( "slti", 0x00000003, 0x00000007, 1 ),
    gen_rimm_value_test( "slti", 0x80000000, 0x000007ff, 1 ),
    gen_rimm_value_test( "slti", 0x7fffffff, 0x00000064, 0 ),
  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in range(100):
    src0 = b32( random.randint(-2147483648, 2147483645) )
    src1 = b32( random.randint(-64, 63) )
    if (src0.int()<src1.int()):
      dest = b32(1)
    else:
      dest = b32(0)
    asm_code.append( gen_rimm_value_test( "slti", src0.int(), src1.int(), dest.int() ) )
  return asm_code