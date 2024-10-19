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

# ''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Define additional directed and random test cases.
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def gen_dest_dep_test():
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
