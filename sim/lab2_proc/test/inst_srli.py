#=========================================================================
# srli
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
    srli x3, x1, 0x03
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
    gen_rimm_dest_dep_test( 7, "srli",    1, 1,  0 ), #truncate 0.5 to 0
    gen_rimm_dest_dep_test( 5, "srli",   16, 2,  4 ),
    gen_rimm_dest_dep_test( 3, "srli", 3328, 8, 13 ),
  ]

#-------------------------------------------------------------------------
# gen_src_dep_test
#-------------------------------------------------------------------------

def gen_src_dep_test():
  return [
    gen_rimm_src_dep_test( 8, "srli",    336,  4,  21 ),
    gen_rimm_src_dep_test( 6, "srli",   7168, 10,  7 ),
    gen_rimm_src_dep_test( 4, "srli", 753664, 15, 23 ),
    gen_rimm_src_dep_test( 2, "srli",  90112, 13, 11 ),
    gen_rimm_src_dep_test( 1, "srli", 180224, 14, 11 ),
    gen_rimm_src_dep_test( 0, "srli", 360448, 15, 11 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rimm_src_eq_dest_test( "srli", 26, 1, 13 ),
    gen_rimm_src_eq_dest_test( "srli", 28, 1, 14 ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [
    gen_rimm_value_test( "srli", 0x10001000, 0x00000000, 0x10001000 ), #shift by 0
    gen_rimm_value_test( "srli", 0xffff8000, 0x0000001f, 0x00000001 ),
    gen_rimm_value_test( "srli", 0x7fff8000, 0x00000002,  0x1fffe000),
    gen_rimm_value_test( "srli", 0x00f01a000, 0x00000014, 0x000000f0 ), 
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
    asm_code.append( gen_rimm_value_test( "srli", src0.uint(), src1.uint(), dest.uint() ) )
  return asm_code
