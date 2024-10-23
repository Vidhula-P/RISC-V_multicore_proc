#=========================================================================
# blt
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
    blt   x2, x1, label_a
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
    gen_br2_src0_dep_test( 5, "blt", 1, 7, True ),
    gen_br2_src0_dep_test( 4, "blt", 2, 7, True ),
    gen_br2_src0_dep_test( 3, "blt", 3, 7, True ),
    gen_br2_src0_dep_test( 2, "blt", 4, 7, True ),
    gen_br2_src0_dep_test( 1, "blt", 5, 7, True ),
    gen_br2_src0_dep_test( 0, "blt", 6, 7, True ),
  ]

#-------------------------------------------------------------------------
# gen_src0_dep_nottaken_test
#-------------------------------------------------------------------------

def gen_src0_dep_nottaken_test():
  return [
    gen_br2_src0_dep_test( 5, "blt", 1, 1, False ),
    gen_br2_src0_dep_test( 4, "blt", 2, 2, False ),
    gen_br2_src0_dep_test( 3, "blt", 3, 3, False ),
    gen_br2_src0_dep_test( 2, "blt", 4, 4, False ),
    gen_br2_src0_dep_test( 1, "blt", 5, 5, False ),
    gen_br2_src0_dep_test( 0, "blt", 6, 6, False ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_taken_test
#-------------------------------------------------------------------------

def gen_src1_dep_taken_test():
  return [
    gen_br2_src1_dep_test( 5, "blt", 7, 1, False ),
    gen_br2_src1_dep_test( 4, "blt", 7, 2, False ),
    gen_br2_src1_dep_test( 3, "blt", 7, 3, False ),
    gen_br2_src1_dep_test( 2, "blt", 7, 4, False ),
    gen_br2_src1_dep_test( 1, "blt", 7, 5, False ),
    gen_br2_src1_dep_test( 0, "blt", 7, 6, False ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_nottaken_test
#-------------------------------------------------------------------------

def gen_src1_dep_nottaken_test():
  return [
    gen_br2_src1_dep_test( 5, "blt", 1, 1, False ),
    gen_br2_src1_dep_test( 4, "blt", 2, 2, False ),
    gen_br2_src1_dep_test( 3, "blt", 3, 3, False ),
    gen_br2_src1_dep_test( 2, "blt", 4, 4, False ),
    gen_br2_src1_dep_test( 1, "blt", 5, 5, False ),
    gen_br2_src1_dep_test( 0, "blt", 6, 6, False ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_taken_test
#-------------------------------------------------------------------------

def gen_srcs_dep_taken_test():
  return [
    gen_br2_srcs_dep_test( 5, "blt", 1, 2, True ),
    gen_br2_srcs_dep_test( 4, "blt", 2, 3, True ),
    gen_br2_srcs_dep_test( 3, "blt", 3, 4, True ),
    gen_br2_srcs_dep_test( 2, "blt", 4, 5, True ),
    gen_br2_srcs_dep_test( 1, "blt", 5, 6, True ),
    gen_br2_srcs_dep_test( 0, "blt", 6, 7, True ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_nottaken_test
#-------------------------------------------------------------------------

def gen_srcs_dep_nottaken_test():
  return [
    gen_br2_srcs_dep_test( 5, "blt", 1, 1, False ),
    gen_br2_srcs_dep_test( 4, "blt", 2, 2, False ),
    gen_br2_srcs_dep_test( 3, "blt", 3, 3, False ),
    gen_br2_srcs_dep_test( 2, "blt", 4, 4, False ),
    gen_br2_srcs_dep_test( 1, "blt", 5, 5, False ),
    gen_br2_srcs_dep_test( 0, "blt", 6, 6, False ),
  ]

#-------------------------------------------------------------------------
# gen_src0_eq_src1_nottaken_test
#-------------------------------------------------------------------------

def gen_src0_eq_src1_test():
  return [
    gen_br2_src0_eq_src1_test( "blt", 1, False ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [
    gen_br2_value_test( "blt", -1, -1, False ),
    gen_br2_value_test( "blt", -1,  0, True  ),
    gen_br2_value_test( "blt", -1,  1, True  ),

    gen_br2_value_test( "blt",  0, -1, False  ),
    gen_br2_value_test( "blt",  0,  0, False  ),
    gen_br2_value_test( "blt",  0,  1, True   ),

    gen_br2_value_test( "blt",  1, -1, False  ),
    gen_br2_value_test( "blt",  1,  0, False  ),
    gen_br2_value_test( "blt",  1,  1, False  ),

    # would be different for signed and unsigned
    gen_br2_value_test( "blt", 0xfffffff7, 0xfffffff7, False ),
    gen_br2_value_test( "blt", 0x7fffffff, 0x7fffffff, False ),
    gen_br2_value_test( "blt", 0xfffffff7, 0x7fffffff, True  ), # -9 < 2,147,483,647 --> True
    gen_br2_value_test( "blt", 0x7fffffff, 0xfffffff7, False ),

    gen_br2_value_test( "blt ", 0xa09fff7f, 0xfa09fff7, True  ), # -1,600,127,105 < -100,007,945 --> False
    gen_br2_value_test( "blt ", 0xfa09fff7, 0xa09fff7f, False ), 

    gen_br2_value_test( "blt ", 0x6ed6321a, 0x78fa9c32, True ), # 1,859,531,290 < 2,029,689,906 --> True
    gen_br2_value_test( "blt ", 0x78fa9c32, 0x6ed6321a, False  ),

    gen_br2_value_test( "blt ", 0x7fecab70, 0x98fa9c32, False  ), # 2,146,216,816 < -1728406478 --> False
    gen_br2_value_test( "blt ", 0x98fa9c32, 0x7fecab70, True   ),
  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

# def gen_random_test():
#   asm_code = []
#   for i in range(25):
#     taken = random.choice([True, False])
#     src0  = b32( random.randint(0,0xfffffffe) )
#     if taken:
#       # Branch taken, src0 < src1
#       src1 = b32( random.randint( src0, 0xffffffff) )
#       if (src0 == src1):
#         src1 = src0 + 1
#     else:
#       # Branch not taken, src0 >= src1
#       src1 = b32( random.randint(0, src0) )
#     asm_code.append( gen_br2_value_test( "blt", src0.uint(), src1.uint(), taken ) )
#   return asm_code

#-------------------------------------------------------------------------
# gen_back_to_back_test
#-------------------------------------------------------------------------

def gen_back_to_back_test():
  return """
     # Test backwards walk (back to back branch taken)

     csrr x3, mngr2proc <-1
     csrr x1, mngr2proc < 1

     blt  x3, x0, X0        # Branch taken as x3 < x0  --> Line 1
     csrw proc2mngr, x0
     nop
     a0:
     csrw proc2mngr, x1 > 1
     blt  x3, x0, y0        # Branch taken as x3 < x0  --> Line 11
     b0:
     blt  x3, x0, a0        # Branch taken as x3 < x0  --> Line 10
     c0:
     blt  x3, x0, b0        # Branch taken as x3 < x0  --> Line 9
     d0:
     blt  x3, x0, c0        # Branch taken as x3 < x0  --> Line 8
     e0:
     blt  x3, x0, d0        # Branch taken as x3 < x0  --> Line 7
     f0:
     blt  x3, x0, e0        # Branch taken as x3 < x0  --> Line 6
     g0:
     blt  x3, x0, f0        # Branch taken as x3 < x0  --> Line 5
     h0:
     blt  x3, x0, g0        # Branch taken as x3 < x0  --> Line 4
     i0:
     blt  x3, x0, h0        # Branch taken as x3 < x0  --> Line 3
     X0:
     blt  x3, x0, i0        # Branch taken as x3 < x0  --> Line 2
     y0:

     blt  x3, x0, X1        # Branch taken as x3 < x0  --> Line 12
     csrw proc2mngr, x0
     nop
     a1:
     csrw proc2mngr, x1 > 1
     blt  x3, x0, y1        # Branch taken as x3 < x0  --> Line 22
     b1:
     blt  x3, x0, a1        # Branch taken as x3 < x0  --> Line 21
     c1:
     blt  x3, x0, b1        # Branch taken as x3 < x0  --> Line 20
     d1:
     blt  x3, x0, c1        # Branch taken as x3 < x0  --> Line 19
     e1:
     blt  x3, x0, d1        # Branch taken as x3 < x0  --> Line 18
     f1:
     blt  x3, x0, e1        # Branch taken as x3 < x0  --> Line 17
     g1:
     blt  x3, x0, f1        # Branch taken as x3 < x0  --> Line 16
     h1:
     blt  x3, x0, g1        # Branch taken as x3 < x0  --> Line 15
     i1:
     blt  x3, x0, h1        # Branch taken as x3 < x0  --> Line 14
     X1:
     blt  x3, x0, i1        # Branch taken as x3 < x0  --> Line 13
     y1:

     blt  x3, x0, X2        # Branch taken as x3 < x0  --> Line 23
     csrw proc2mngr, x0
     nop
     a2:
     csrw proc2mngr, x1 > 1
     blt  x3, x0, y2        # Branch taken as x3 < x0  --> Line 33
     b2:
     blt  x3, x0, a2        # Branch taken as x3 < x0  --> Line 32
     c2:
     blt  x3, x0, b2        # Branch taken as x3 < x0  --> Line 31
     d2:
     blt  x3, x0, c2        # Branch taken as x3 < x0  --> Line 30
     e2:
     blt  x3, x0, d2        # Branch taken as x3 < x0  --> Line 29
     f2:
     blt  x3, x0, e2        # Branch taken as x3 < x0  --> Line 28
     g2:
     blt  x3, x0, f2        # Branch taken as x3 < x0  --> Line 27
     h2:
     blt  x3, x0, g2        # Branch taken as x3 < x0  --> Line 26
     i2:
     blt  x3, x0, h2        # Branch taken as x3 < x0  --> Line 25
     X2:
     blt  x3, x0, i2        # Branch taken as x3 < x0  --> Line 24
     y2:

     blt  x3, x0, X3        # Branch taken as x3 < x0  --> Line 34
     csrw proc2mngr, x0
     nop
     a3:
     csrw proc2mngr, x1 > 1
     blt  x3, x0, y3        # Branch taken as x3 < x0  --> Line 42
     b3:
     blt  x3, x0, a3        # Branch taken as x3 < x0  --> Line 41
     c3:
     blt  x3, x0, b3        # Branch taken as x3 < x0  --> Line 41
     d3:
     blt  x3, x0, c3        # Branch taken as x3 < x0  --> Line 40
     e3:
     blt  x3, x0, d3        # Branch taken as x3 < x0  --> Line 39
     f3:
     blt  x3, x0, e3        # Branch taken as x3 < x0  --> Line 38
     g3:
     blt  x3, x0, f3        # Branch taken as x3 < x0  --> Line 37
     h3:
     blt  x3, x0, g3        # Branch taken as x3 < x0  --> Line 36
     i3:
     blt  x3, x0, h3        # Branch taken as x3 < x0  --> Line 35
     X3:
     blt  x3, x0, i3        # Branch taken as x3 < x0  --> Line 34
     y3:
     nop                    # Ends here
     nop
     nop
     nop
     nop
     nop
     nop
  """