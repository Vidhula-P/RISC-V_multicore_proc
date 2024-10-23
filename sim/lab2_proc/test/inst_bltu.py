#=========================================================================
# bltu
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

    # Use x3 to track the control flow pattern
    addi  x3, x0, 0

    csrr  x1, mngr2proc < 2
    csrr  x2, mngr2proc < 1

    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop

    # This branch should be taken
    bltu   x2, x1, label_a
    addi  x3, x3, 0b01

    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop

  label_a:
    addi  x3, x3, 0b10

    # Only the second bit should be set if branch was taken
    csrw proc2mngr, x3 > 0b10

  """

# ''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Define additional directed and random test cases.
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

#-------------------------------------------------------------------------
# gen_src0_dep_taken_test
#-------------------------------------------------------------------------

def gen_src0_dep_taken_test():
  return [
    gen_br2_src0_dep_test( 5, "bltu ", 1, 7, True ),
    gen_br2_src0_dep_test( 4, "bltu ", 2, 7, True ),
    gen_br2_src0_dep_test( 3, "bltu ", 3, 7, True ),
    gen_br2_src0_dep_test( 2, "bltu ", 4, 7, True ),
    gen_br2_src0_dep_test( 1, "bltu ", 5, 7, True ),
    gen_br2_src0_dep_test( 0, "bltu ", 6, 7, True ),
  ]

#-------------------------------------------------------------------------
# gen_src0_dep_nottaken_test
#-------------------------------------------------------------------------

def gen_src0_dep_nottaken_test():
  return [
    gen_br2_src0_dep_test( 5, "bltu ", 1, 1, False ),
    gen_br2_src0_dep_test( 4, "bltu ", 2, 2, False ),
    gen_br2_src0_dep_test( 3, "bltu ", 3, 3, False ),
    gen_br2_src0_dep_test( 2, "bltu ", 4, 4, False ),
    gen_br2_src0_dep_test( 1, "bltu ", 5, 5, False ),
    gen_br2_src0_dep_test( 0, "bltu ", 6, 6, False ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_taken_test
#-------------------------------------------------------------------------

def gen_src1_dep_taken_test():
  return [
    gen_br2_src1_dep_test( 5, "bltu ", 7, 1, False ),
    gen_br2_src1_dep_test( 4, "bltu ", 7, 2, False ),
    gen_br2_src1_dep_test( 3, "bltu ", 7, 3, False ),
    gen_br2_src1_dep_test( 2, "bltu ", 7, 4, False ),
    gen_br2_src1_dep_test( 1, "bltu ", 7, 5, False ),
    gen_br2_src1_dep_test( 0, "bltu ", 7, 6, False ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_nottaken_test
#-------------------------------------------------------------------------

def gen_src1_dep_nottaken_test():
  return [
    gen_br2_src1_dep_test( 5, "bltu ", 1, 1, False ),
    gen_br2_src1_dep_test( 4, "bltu ", 2, 2, False ),
    gen_br2_src1_dep_test( 3, "bltu ", 3, 3, False ),
    gen_br2_src1_dep_test( 2, "bltu ", 4, 4, False ),
    gen_br2_src1_dep_test( 1, "bltu ", 5, 5, False ),
    gen_br2_src1_dep_test( 0, "bltu ", 6, 6, False ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_taken_test
#-------------------------------------------------------------------------

def gen_srcs_dep_taken_test():
  return [
    gen_br2_srcs_dep_test( 5, "bltu ", 1, 2, True ),
    gen_br2_srcs_dep_test( 4, "bltu ", 2, 3, True ),
    gen_br2_srcs_dep_test( 3, "bltu ", 3, 4, True ),
    gen_br2_srcs_dep_test( 2, "bltu ", 4, 5, True ),
    gen_br2_srcs_dep_test( 1, "bltu ", 5, 6, True ),
    gen_br2_srcs_dep_test( 0, "bltu ", 6, 7, True ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_nottaken_test
#-------------------------------------------------------------------------

def gen_srcs_dep_nottaken_test():
  return [
    gen_br2_srcs_dep_test( 5, "bltu ", 1, 1, False ),
    gen_br2_srcs_dep_test( 4, "bltu ", 2, 2, False ),
    gen_br2_srcs_dep_test( 3, "bltu ", 3, 3, False ),
    gen_br2_srcs_dep_test( 2, "bltu ", 4, 4, False ),
    gen_br2_srcs_dep_test( 1, "bltu ", 5, 5, False ),
    gen_br2_srcs_dep_test( 0, "bltu ", 6, 6, False ),
  ]

#-------------------------------------------------------------------------
# gen_src0_eq_src1_nottaken_test
#-------------------------------------------------------------------------

def gen_src0_eq_src1_test():
  return [
    gen_br2_src0_eq_src1_test( "bltu ", 1, False ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [
    gen_br2_value_test( "bltu ",  0,  0, False  ),
    gen_br2_value_test( "bltu ",  0,  1, True   ),
    gen_br2_value_test( "bltu ",  1,  0, False  ),
    gen_br2_value_test( "bltu ",  1,  1, False  ),

    # would be different for signed and unsigned
    gen_br2_value_test( "bltu ", 0xfffffff7, 0xfffffff7, False ),
    gen_br2_value_test( "bltu ", 0x7fffffff, 0x7fffffff, False ),
    gen_br2_value_test( "bltu ", 0xfffffff7, 0x7fffffff, False ), # 4,294,967,287 < 2,147,483,647 --> False
    gen_br2_value_test( "bltu ", 0x7fffffff, 0xfffffff7, True  ),

    gen_br2_value_test( "bltu ", 0xa09fff7f, 0xfa09fff7, True  ), # 2,694,840,191 < 4,194,959,351 --> True
    gen_br2_value_test( "bltu ", 0xfa09fff7, 0xa09fff7f, False ), 

    gen_br2_value_test( "bltu ", 0x6ed6321a, 0x78fa9c32, True ), # 1,859,531,290 < 2,029,689,906 --> True
    gen_br2_value_test( "bltu ", 0x78fa9c32, 0x6ed6321a, False  ),

    gen_br2_value_test( "bltu ", 0x7fecab70, 0x98fa9c32, True  ), # 2,146,216,816 < 2,566,560,818 --> True
    gen_br2_value_test( "bltu ", 0x98fa9c32, 0x7fecab70, False   ), 
  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in range(25):
    taken = random.choice([True, False])
    src0  = b32( random.randint(0,0xfffffffe) )
    if taken:
      # Branch taken, src0 < src1
      src1 = b32( random.randint( src0, 0xffffffff) )
      if src0 == src1:
        src1 = src0 + 1
    else:
      # Branch not taken, src0 >= src1
      src1 = b32( random.randint(0, src0) )
    asm_code.append( gen_br2_value_test( "bltu ", src0.uint(), src1.uint(), taken ) )
  return asm_code

#-------------------------------------------------------------------------
# gen_back_to_back_test
#-------------------------------------------------------------------------

def gen_back_to_back_test():
  return """
     # Test backwards walk (back to back branch taken)

     csrr x3, mngr2proc < 1
     csrr x1, mngr2proc < 1

     bltu  x0, x3, X0        # Branch taken as x3 < x0  --> Line 1
     csrw proc2mngr, x0
     nop
     a0:
     csrw proc2mngr, x1 > 1
     bltu  x0, x3, y0        # Branch taken as x3 < x0  --> Line 11
     b0:
     bltu  x0, x3, a0        # Branch taken as x3 < x0  --> Line 10
     c0:
     bltu  x0, x3, b0        # Branch taken as x3 < x0  --> Line 9
     d0:
     bltu  x0, x3, c0        # Branch taken as x3 < x0  --> Line 8
     e0:
     bltu  x0, x3, d0        # Branch taken as x3 < x0  --> Line 7
     f0:
     bltu  x0, x3, e0        # Branch taken as x3 < x0  --> Line 6
     g0:
     bltu  x0, x3, f0        # Branch taken as x3 < x0  --> Line 5
     h0:
     bltu  x0, x3, g0        # Branch taken as x3 < x0  --> Line 4
     i0:
     bltu  x0, x3, h0        # Branch taken as x3 < x0  --> Line 3
     X0:
     bltu  x0, x3, i0        # Branch taken as x3 < x0  --> Line 2
     y0:

     bltu  x0, x3, X1        # Branch taken as x3 < x0  --> Line 12
     csrw proc2mngr, x0
     nop
     a1:
     csrw proc2mngr, x1 > 1
     bltu  x0, x3, y1        # Branch taken as x3 < x0  --> Line 22
     b1:
     bltu  x0, x3, a1        # Branch taken as x3 < x0  --> Line 21
     c1:
     bltu  x0, x3, b1        # Branch taken as x3 < x0  --> Line 20
     d1:
     bltu  x0, x3, c1        # Branch taken as x3 < x0  --> Line 19
     e1:
     bltu  x0, x3, d1        # Branch taken as x3 < x0  --> Line 18
     f1:
     bltu  x0, x3, e1        # Branch taken as x3 < x0  --> Line 17
     g1:
     bltu  x0, x3, f1        # Branch taken as x3 < x0  --> Line 16
     h1:
     bltu  x0, x3, g1        # Branch taken as x3 < x0  --> Line 15
     i1:
     bltu  x0, x3, h1        # Branch taken as x3 < x0  --> Line 14
     X1:
     bltu  x0, x3, i1        # Branch taken as x3 < x0  --> Line 13
     y1:

     bltu  x0, x3, X2        # Branch taken as x3 < x0  --> Line 23
     csrw proc2mngr, x0
     nop
     a2:
     csrw proc2mngr, x1 > 1
     bltu  x0, x3, y2        # Branch taken as x3 < x0  --> Line 33
     b2:
     bltu  x0, x3, a2        # Branch taken as x3 < x0  --> Line 32
     c2:
     bltu  x0, x3, b2        # Branch taken as x3 < x0  --> Line 31
     d2:
     bltu  x0, x3, c2        # Branch taken as x3 < x0  --> Line 30
     e2:
     bltu  x0, x3, d2        # Branch taken as x3 < x0  --> Line 29
     f2:
     bltu  x0, x3, e2        # Branch taken as x3 < x0  --> Line 28
     g2:
     bltu  x0, x3, f2        # Branch taken as x3 < x0  --> Line 27
     h2:
     bltu  x0, x3, g2        # Branch taken as x3 < x0  --> Line 26
     i2:
     bltu  x0, x3, h2        # Branch taken as x3 < x0  --> Line 25
     X2:
     bltu  x0, x3, i2        # Branch taken as x3 < x0  --> Line 24
     y2:

     bltu  x0, x3, X3        # Branch taken as x3 < x0  --> Line 34
     csrw proc2mngr, x0
     nop
     a3:
     csrw proc2mngr, x1 > 1
     bltu  x0, x3, y3        # Branch taken as x3 < x0  --> Line 42
     b3:
     bltu  x0, x3, a3        # Branch taken as x3 < x0  --> Line 41
     c3:
     bltu  x0, x3, b3        # Branch taken as x3 < x0  --> Line 41
     d3:
     bltu  x0, x3, c3        # Branch taken as x3 < x0  --> Line 40
     e3:
     bltu  x0, x3, d3        # Branch taken as x3 < x0  --> Line 39
     f3:
     bltu  x0, x3, e3        # Branch taken as x3 < x0  --> Line 38
     g3:
     bltu  x0, x3, f3        # Branch taken as x3 < x0  --> Line 37
     h3:
     bltu  x0, x3, g3        # Branch taken as x3 < x0  --> Line 36
     i3:
     bltu  x0, x3, h3        # Branch taken as x3 < x0  --> Line 35
     X3:
     bltu  x0, x3, i3        # Branch taken as x3 < x0  --> Line 34
     y3:
     nop                    # Ends here
     nop
     nop
     nop
     nop
     nop
     nop
  """