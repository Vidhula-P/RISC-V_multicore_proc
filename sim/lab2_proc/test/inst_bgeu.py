#=========================================================================
# bgeu
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
    csrr  x2, mngr2proc < 2

    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop

    # This branch should be taken
    bgeu   x1, x2, label_a
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
    gen_br2_src0_dep_test( 5, "bgeu ", 1, 7, False ),
    gen_br2_src0_dep_test( 4, "bgeu ", 2, 7, False ),
    gen_br2_src0_dep_test( 3, "bgeu ", 3, 7, False ),
    gen_br2_src0_dep_test( 2, "bgeu ", 4, 7, False ),
    gen_br2_src0_dep_test( 1, "bgeu ", 5, 7, False ),
    gen_br2_src0_dep_test( 0, "bgeu ", 6, 7, False ),
  ]

#-------------------------------------------------------------------------
# gen_src0_dep_nottaken_test
#-------------------------------------------------------------------------

def gen_src0_dep_nottaken_test():
  return [
    gen_br2_src0_dep_test( 5, "bgeu ", 1, 1, True ),
    gen_br2_src0_dep_test( 4, "bgeu ", 2, 2, True ),
    gen_br2_src0_dep_test( 3, "bgeu ", 3, 3, True ),
    gen_br2_src0_dep_test( 2, "bgeu ", 4, 4, True ),
    gen_br2_src0_dep_test( 1, "bgeu ", 5, 5, True ),
    gen_br2_src0_dep_test( 0, "bgeu ", 6, 6, True ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_taken_test
#-------------------------------------------------------------------------

def gen_src1_dep_taken_test():
  return [
    gen_br2_src1_dep_test( 5, "bgeu ", 7, 1, True ),
    gen_br2_src1_dep_test( 4, "bgeu ", 7, 2, True ),
    gen_br2_src1_dep_test( 3, "bgeu ", 7, 3, True ),
    gen_br2_src1_dep_test( 2, "bgeu ", 7, 4, True ),
    gen_br2_src1_dep_test( 1, "bgeu ", 7, 5, True ),
    gen_br2_src1_dep_test( 0, "bgeu ", 7, 6, True ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_nottaken_test
#-------------------------------------------------------------------------

def gen_src1_dep_nottaken_test():
  return [
    gen_br2_src1_dep_test( 5, "bgeu ", 1, 1, True ),
    gen_br2_src1_dep_test( 4, "bgeu ", 2, 2, True ),
    gen_br2_src1_dep_test( 3, "bgeu ", 3, 3, True ),
    gen_br2_src1_dep_test( 2, "bgeu ", 4, 4, True ),
    gen_br2_src1_dep_test( 1, "bgeu ", 5, 5, True ),
    gen_br2_src1_dep_test( 0, "bgeu ", 6, 6, True ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_taken_test
#-------------------------------------------------------------------------

def gen_srcs_dep_taken_test():
  return [
    gen_br2_srcs_dep_test( 5, "bgeu ", 1, 2, False ),
    gen_br2_srcs_dep_test( 4, "bgeu ", 2, 3, False ),
    gen_br2_srcs_dep_test( 3, "bgeu ", 3, 4, False ),
    gen_br2_srcs_dep_test( 2, "bgeu ", 4, 5, False ),
    gen_br2_srcs_dep_test( 1, "bgeu ", 5, 6, False ),
    gen_br2_srcs_dep_test( 0, "bgeu ", 6, 7, False ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_nottaken_test
#-------------------------------------------------------------------------

def gen_srcs_dep_nottaken_test():
  return [
    gen_br2_srcs_dep_test( 5, "bgeu ", 1, 1, True ),
    gen_br2_srcs_dep_test( 4, "bgeu ", 2, 2, True ),
    gen_br2_srcs_dep_test( 3, "bgeu ", 3, 3, True ),
    gen_br2_srcs_dep_test( 2, "bgeu ", 4, 4, True ),
    gen_br2_srcs_dep_test( 1, "bgeu ", 5, 5, True ),
    gen_br2_srcs_dep_test( 0, "bgeu ", 6, 6, True ),
  ]

#-------------------------------------------------------------------------
# gen_src0_eq_src1_nottaken_test
#-------------------------------------------------------------------------

def gen_src0_eq_src1_test():
  return [
    gen_br2_src0_eq_src1_test( "bgeu ", 1, True ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [
    gen_br2_value_test( "bgeu ",  0,  0, True  ),
    gen_br2_value_test( "bgeu ",  0,  1, False   ),
    gen_br2_value_test( "bgeu ",  1,  0, True  ),
    gen_br2_value_test( "bgeu ",  1,  1, True  ),

    # would be different for signed and unsigned
    gen_br2_value_test( "bgeu ", 0xfffffff7, 0xfffffff7, True ),
    gen_br2_value_test( "bgeu ", 0x7fffffff, 0x7fffffff, True ),
    gen_br2_value_test( "bgeu ", 0xfffffff7, 0x7fffffff, True ), # 4,294,967,287 < 2,147,483,647 --> True
    gen_br2_value_test( "bgeu ", 0x7fffffff, 0xfffffff7, False  ),

    gen_br2_value_test( "bgeu ", 0xa09fff7f, 0xfa09fff7, False  ), # 2,694,840,191 < 4,194,959,351 --> False
    gen_br2_value_test( "bgeu ", 0xfa09fff7, 0xa09fff7f, True ), 

    gen_br2_value_test( "bgeu ", 0x6ed6321a, 0x78fa9c32, False ), # 1,859,531,290 < 2,029,689,906 --> False
    gen_br2_value_test( "bgeu ", 0x78fa9c32, 0x6ed6321a, True  ),

    gen_br2_value_test( "bgeu ", 0x7fecab70, 0x98fa9c32, False  ), # 2,146,216,816 < 2,566,560,818 --> False
    gen_br2_value_test( "bgeu ", 0x98fa9c32, 0x7fecab70, True   ), 
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
      # Branch taken, src0 >= src1
      src1 = b32( random.randint(0, src0) )
      
    else:
      # Branch not taken, src0 < src1
      src1 = b32( random.randint( src0, 0xffffffff) )
      if src0 == src1:
        src1 = src0 + 1
    asm_code.append( gen_br2_value_test( "bgeu ", src0.uint(), src1.uint(), taken ) )
  return asm_code

#-------------------------------------------------------------------------
# gen_back_to_back_test
#-------------------------------------------------------------------------

def gen_back_to_back_test():
  return """
     # test backwards walk (back to back branch taken)

     csrr x3, mngr2proc < 2
     csrr x1, mngr2proc < 1

     bgeu  x3, x0, x0        # branch taken as x3 >= x0  --> line 1
     csrw proc2mngr, x0
     nop
     a0:
     csrw proc2mngr, x1 > 1
     bgeu  x3, x0, y0        # branch taken as x3 >= x0  --> line 11
     b0:
     bgeu  x3, x0, a0        # branch taken as x3 >= x0  --> line 10
     c0:
     bgeu  x3, x0, b0        # branch taken as x3 >= x0  --> line 9
     d0:
     bgeu  x3, x0, c0        # branch taken as x3 >= x0  --> line 8
     e0:
     bgeu  x3, x0, d0        # branch taken as x3 >= x0  --> line 7
     f0:
     bgeu  x3, x0, e0        # branch taken as x3 >= x0  --> line 6
     g0:
     bgeu  x3, x0, f0        # branch taken as x3 >= x0  --> line 5
     h0:
     bgeu  x3, x0, g0        # branch taken as x3 >= x0  --> line 4
     i0:
     bgeu  x3, x0, h0        # branch taken as x3 >= x0  --> line 3
     x0:
     bgeu  x3, x0, i0        # branch taken as x3 >= x0  --> line 2
     y0:

     bgeu  x3, x0, x1        # branch taken as x3 >= x0  --> line 12
     csrw proc2mngr, x0
     nop
     a1:
     csrw proc2mngr, x1 > 1
     bgeu  x3, x0, y1        # branch taken as x3 >= x0  --> line 22
     b1:
     bgeu  x3, x0, a1        # branch taken as x3 >= x0  --> line 21
     c1:
     bgeu  x3, x0, b1        # branch taken as x3 >= x0  --> line 20
     d1:
     bgeu  x3, x0, c1        # branch taken as x3 >= x0  --> line 19
     e1:
     bgeu  x3, x0, d1        # branch taken as x3 >= x0  --> line 18
     f1:
     bgeu  x3, x0, e1        # branch taken as x3 >= x0  --> line 17
     g1:
     bgeu  x3, x0, f1        # branch taken as x3 >= x0  --> line 16
     h1:
     bgeu  x3, x0, g1        # branch taken as x3 >= x0  --> line 15
     i1:
     bgeu  x3, x0, h1        # branch taken as x3 >= x0  --> line 14
     x1:
     bgeu  x3, x0, i1        # branch taken as x3 >= x0  --> line 13
     y1:

     bgeu  x3, x0, x2        # branch taken as x3 >= x0  --> line 23
     csrw proc2mngr, x0
     nop
     a2:
     csrw proc2mngr, x1 > 1
     bgeu  x3, x0, y2        # branch taken as x3 >= x0  --> line 33
     b2:
     bgeu  x3, x0, a2        # branch taken as x3 >= x0  --> line 32
     c2:
     bgeu  x3, x0, b2        # branch taken as x3 >= x0  --> line 31
     d2:
     bgeu  x3, x0, c2        # branch taken as x3 >= x0  --> line 30
     e2:
     bgeu  x3, x0, d2        # branch taken as x3 >= x0  --> line 29
     f2:
     bgeu  x3, x0, e2        # branch taken as x3 >= x0  --> line 28
     g2:
     bgeu  x3, x0, f2        # branch taken as x3 >= x0  --> line 27
     h2:
     bgeu  x3, x0, g2        # branch taken as x3 >= x0  --> line 26
     i2:
     bgeu  x3, x0, h2        # branch taken as x3 >= x0  --> line 25
     x2:
     bgeu  x3, x0, i2        # branch taken as x3 >= x0  --> line 24
     y2:

     bgeu  x3, x0, x3        # branch taken as x3 >= x0  --> line 34
     csrw proc2mngr, x0
     nop
     a3:
     csrw proc2mngr, x1 > 1
     bgeu  x3, x0, y3        # branch taken as x3 >= x0  --> line 42
     b3:
     bgeu  x3, x0, a3        # branch taken as x3 >= x0  --> line 41
     c3:
     bgeu  x3, x0, b3        # branch taken as x3 >= x0  --> line 41
     d3:
     bgeu  x3, x0, c3        # branch taken as x3 >= x0  --> line 40
     e3:
     bgeu  x3, x0, d3        # branch taken as x3 >= x0  --> line 39
     f3:
     bgeu  x3, x0, e3        # branch taken as x3 >= x0  --> line 38
     g3:
     bgeu  x3, x0, f3        # branch taken as x3 >= x0  --> line 37
     h3:
     bgeu  x3, x0, g3        # branch taken as x3 >= x0  --> line 36
     i3:
     bgeu  x3, x0, h3        # branch taken as x3 >= x0  --> line 35
     x3:
     bgeu  x3, x0, i3        # branch taken as x3 >= x0  --> line 34
     y3:
     nop                    # ends here
     nop
     nop
     nop
     nop
     nop
     nop
  """