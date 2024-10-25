#=========================================================================
# lui
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
    lui x1, 0x0001
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x1 > 0x00001000
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
    gen_imm_dest_dep_test( 7, "lui",    1,  4096 ), 
    gen_imm_dest_dep_test( 5, "lui",   16,  65536 ),
    gen_imm_dest_dep_test( 5, "lui",   26, 172032 ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [
    gen_imm_value_test( "lui", 0x00000000, 0x00000000 ),
    gen_imm_value_test( "lui", 0x00000140, 0x00140000 ),
    gen_imm_value_test( "lui", 0x0000001f, 0x0001f000 ),
    gen_imm_value_test( "lui", 0x000007ff, 0x007ff000 ), 
  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in range(100):
    src0 = b32( random.randint(0,0x00000fff) )
    dest = src0 << 12
    asm_code.append( gen_imm_value_test( "lui", src0.uint(), dest.uint() ) )
  return asm_code
