#=========================================================================
# sltiu
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
    sltiu x3, x1, 6
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
    gen_rimm_dest_dep_test( 5, "sltiu", 1, 1, 0 ),
    gen_rimm_dest_dep_test( 4, "sltiu", 2, 1, 0 ),
    gen_rimm_dest_dep_test( 3, "sltiu", 3, 1, 0 ),
    gen_rimm_dest_dep_test( 2, "sltiu", 4, 1, 0 ),
    gen_rimm_dest_dep_test( 1, "sltiu", 5, 1, 0 ),
    gen_rimm_dest_dep_test( 0, "sltiu", 6, 1, 0 ),
  ]

#-------------------------------------------------------------------------
# gen_src0_dep_test
#-------------------------------------------------------------------------

def gen_src_dep_test():
  return [
    gen_rimm_src_dep_test( 5, "sltiu", 7, 1,  0 ),
    gen_rimm_src_dep_test( 4, "sltiu", 8, 1,  0 ),
    gen_rimm_src_dep_test( 3, "sltiu", 9, 1,  0 ),
    gen_rimm_src_dep_test( 2, "sltiu", 1, 16, 1 ),
    gen_rimm_src_dep_test( 1, "sltiu", 1, 17, 1 ),
    gen_rimm_src_dep_test( 0, "sltiu", 1, 18, 1 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rimm_src_eq_dest_test( "sltiu", 1, 25, 1  ),
    gen_rimm_src_eq_dest_test( "sltiu", 27, 1, 0),
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
    src0 = b32( random.randint(0,0xffffffff) )
    src1 = b32( random.randint(0,0x0000001f) )
    if (src0<src1):
      dest = b32(1)
    else:
      dest = b32(0)
    asm_code.append( gen_rimm_value_test( "sltiu", src0.uint(), src1.uint(), dest.uint() ) )
  return asm_code