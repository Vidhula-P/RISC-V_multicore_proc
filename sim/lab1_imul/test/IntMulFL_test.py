#=========================================================================
# IntMulFL_test
#=========================================================================

import pytest

from random import randint

from pymtl3 import *
from pymtl3.stdlib.test_utils import mk_test_case_table, run_sim
from pymtl3.stdlib.stream import StreamSourceFL, StreamSinkFL

from lab1_imul.IntMulFL import IntMulFL

#-------------------------------------------------------------------------
# TestHarness
#-------------------------------------------------------------------------

class TestHarness( Component ):

  def construct( s, imul ):

    # Instantiate models

    s.src  = StreamSourceFL( Bits64 )
    s.sink = StreamSinkFL( Bits32 )
    s.imul = imul

    # Connect

    s.src.ostream  //= s.imul.istream
    s.imul.ostream //= s.sink.istream

  def done( s ):
    return s.src.done() and s.sink.done()

  def line_trace( s ):
    return s.src.line_trace() + " > " + s.imul.line_trace() + " > " + s.sink.line_trace()

#-------------------------------------------------------------------------
# mk_imsg/mk_omsg
#-------------------------------------------------------------------------

# Make input message, truncate ints to ensure they fit in 32 bits.

def mk_imsg( a, b ):
  return concat( Bits32( a, trunc_int=True ), Bits32( b, trunc_int=True ) )

# Make output message, truncate ints to ensure they fit in 32 bits.

def mk_omsg( a ):
  return Bits32( a, trunc_int=True )

def perform_lmask(a, num_bits_to_mask):
  mask = ((1<<32) -1) << num_bits_to_mask
  return Bits32( ( a & mask ), trunc_int=True)

def mk_imsg_lmask(a, b, num_bits_to_mask): # modified mk_imsg to accomodate masking of lower bits
  return concat( perform_lmask(a, num_bits_to_mask), perform_lmask(b, num_bits_to_mask) )

def perform_mmask(a, start_bit, end_bit):
  mask = ~ (((1 << (end_bit - start_bit + 1)) - 1) << start_bit)
  return Bits32( ( a & mask ), trunc_int=True)

def mk_imsg_mmask(a, b, start_bit, end_bit): # modified mk_imsg to accomodate masking of middle bits
  return concat( perform_mmask(a, start_bit, end_bit), perform_mmask(b, start_bit, end_bit) )

#----------------------------------------------------------------------
# Test Case: small positive * positive
#----------------------------------------------------------------------

small_pos_pos_msgs = [
  mk_imsg(  2,  3 ), mk_omsg(   6 ),
  mk_imsg(  4,  5 ), mk_omsg(  20 ),
  mk_imsg(  3,  4 ), mk_omsg(  12 ),
  mk_imsg( 10, 13 ), mk_omsg( 130 ),
  mk_imsg(  8,  7 ), mk_omsg(  56 ),
]

# ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Define additional lists of input/output messages to create
# additional directed and random test cases.
# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

#----------------------------------------------------------------------
# Test Case: basic 0, 1, -1
#----------------------------------------------------------------------

basic_msgs = [
  mk_imsg(  0,  0 ), mk_omsg(  0 ),
  mk_imsg(  1,  1 ), mk_omsg(  1 ),
  mk_imsg( -1, -1 ), mk_omsg(  1 ),

  mk_imsg(  0,  1 ), mk_omsg(  0 ),
  mk_imsg(  1,  0 ), mk_omsg(  0 ),

  mk_imsg(  0, -1 ), mk_omsg(  0 ),
  mk_imsg( -1,  0 ), mk_omsg(  0 ),

  mk_imsg(  1, -1 ), mk_omsg( -1 ),
  mk_imsg( -1,  1 ), mk_omsg( -1 ),
]

#----------------------------------------------------------------------
# Test Case: small positive * negative
#----------------------------------------------------------------------

small_pos_neg_msgs = [
  mk_imsg(  2,  -3 ), mk_omsg(   -6 ),
  mk_imsg(  4,  -5 ), mk_omsg(  -20 ),
  mk_imsg(  3,  -4 ), mk_omsg(  -12 ),
  mk_imsg( 10, -13 ), mk_omsg( -130 ),
  mk_imsg(  8,  -7 ), mk_omsg(  -56 ),
]

#----------------------------------------------------------------------
# Test Case: small negative * positive
#----------------------------------------------------------------------

small_neg_pos_msgs = [
  mk_imsg(  -2,  3 ), mk_omsg(   -6 ),
  mk_imsg(  -4,  5 ), mk_omsg(  -20 ),
  mk_imsg(  -3,  4 ), mk_omsg(  -12 ),
  mk_imsg( -10, 13 ), mk_omsg( -130 ),
  mk_imsg(  -8,  7 ), mk_omsg(  -56 ),
]

#----------------------------------------------------------------------
# Test Case: small negative * negative
#----------------------------------------------------------------------

small_neg_neg_msgs = [
  mk_imsg(  -2,  -3 ), mk_omsg(   6 ),
  mk_imsg(  -4,  -5 ), mk_omsg(  20 ),
  mk_imsg(  -3,  -4 ), mk_omsg(  12 ),
  mk_imsg( -10, -13 ), mk_omsg( 130 ),
  mk_imsg(  -8,  -7 ), mk_omsg(  56 ),
]

#----------------------------------------------------------------------
# Test Case: large positive * positive
#----------------------------------------------------------------------

large_pos_pos_msgs = [
  # Tests that do not cause output to overflow (input up to 16 bits)


  # Tests that cause output to overflow (input more than 16 bits)
  mk_imsg(  2000000000,  3141592653 ), mk_omsg(  6283185306000000000 ),
  mk_imsg(  4294967295,  1000000000 ), mk_omsg(  4294967295000000000 ),
  mk_imsg(  5000000000,  6000000000 ), mk_omsg(  30000000000000000000 ),
  mk_imsg(  7000000000,  8000000000 ), mk_omsg(  56000000000000000000 ),
  mk_imsg(  9000000000,  1234567890 ), mk_omsg(  11111111010000000000 ),

  # Maximum 16 bit and 32 bit positive values
]

#----------------------------------------------------------------------
# Test Case: large positive * negative
#----------------------------------------------------------------------

large_pos_neg_msgs = [
  mk_imsg(  2000000000,  -3141592653 ), mk_omsg(  -6283185306000000000 ),
  mk_imsg(  4294967295,  -1000000000 ), mk_omsg(  -4294967295000000000 ),
  mk_imsg(  5000000000,  -6000000000 ), mk_omsg(  -30000000000000000000 ),
  mk_imsg(  7000000000,  -8000000000 ), mk_omsg(  -56000000000000000000 ),
  mk_imsg(  9000000000,  -1234567890 ), mk_omsg(  -11111111010000000000 ),
]

#----------------------------------------------------------------------
# Test Case: large negative * positive
#----------------------------------------------------------------------

large_neg_pos_msgs = [
  mk_imsg(  -2000000000,  3141592653 ), mk_omsg(  -6283185306000000000 ),
  mk_imsg(  -4294967295,  1000000000 ), mk_omsg(  -4294967295000000000 ),
  mk_imsg(  -5000000000,  6000000000 ), mk_omsg(  -30000000000000000000 ),
  mk_imsg(  -7000000000,  8000000000 ), mk_omsg(  -56000000000000000000 ),
  mk_imsg(  -9000000000,  1234567890 ), mk_omsg(  -11111111010000000000 ),
]

#----------------------------------------------------------------------
# Test Case: large negative * negative
#----------------------------------------------------------------------

large_neg_neg_msgs = [
  mk_imsg(  -2000000000,  -3141592653 ), mk_omsg(  6283185306000000000 ),
  mk_imsg(  -4294967295,  -1000000000 ), mk_omsg(  4294967295000000000 ),
  mk_imsg(  -5000000000,  -6000000000 ), mk_omsg(  30000000000000000000 ),
  mk_imsg(  -7000000000,  -8000000000 ), mk_omsg(  56000000000000000000 ),
  mk_imsg(  -9000000000,  -1234567890 ), mk_omsg(  11111111010000000000 ),
]

#----------------------------------------------------------------------
# Test Case: lower bits masked
#----------------------------------------------------------------------

low_mask_msgs = [
  mk_imsg_lmask(  239,        453,         2 ), mk_omsg(              106672 ),
  mk_imsg_lmask(  8920,       15502,       8 ), mk_omsg(          133693440  ),
  mk_imsg_lmask(  47847382,   739006219,   15), mk_omsg(  35353937397678080  ),
]

#----------------------------------------------------------------------
# Test Case: middle bits masked
#----------------------------------------------------------------------

mid_mask_msgs = [
  mk_imsg_mmask(  239,        453,         2,    4 ),  mk_omsg(            101923 ),
  mk_imsg_mmask(  8920,       15502,       4,    11 ), mk_omsg(         100876400 ),
  mk_imsg_mmask(  47847382,   739006219,   7,    19),  mk_omsg( 34832592371975090 ),
]

#----------------------------------------------------------------------
# Test Case: sparse numbers
#----------------------------------------------------------------------

sparse_msgs = [
  mk_imsg(  4294967296,         65536),  mk_omsg( 281474976710656 ),
  mk_imsg(  11184640,       279620104),  mk_omsg( 3127450200002560 ),
]

#----------------------------------------------------------------------
# Test Case: dense numbers
#----------------------------------------------------------------------

dense_msgs = [
  mk_imsg(  4294967295,    4294901759 ),  mk_omsg(  18446462590142971905 ),
  mk_imsg(  1605348090,    2142153466),   mk_omsg(  3438901975129979940  ),
]

random_msgs = [
]

for _ in range(30):
  rand_a = randint(-2147483648, 2147483647)
  print("a")
  print(rand_a)
  rand_b = randint(-2147483648, 2147483647)

  # Unmasked
  random_msgs.extend([mk_imsg(rand_a, rand_b),  mk_omsg(rand_a * rand_b)])

  # Low Mask
  num_bits_to_mask = randint(0, 32)
  masked_rand_a = perform_lmask(rand_a, num_bits_to_mask)
  masked_rand_b = perform_lmask(rand_b, num_bits_to_mask)
  random_msgs.extend([mk_imsg_lmask(rand_a, rand_b, num_bits_to_mask), mk_omsg(masked_rand_a * masked_rand_b)])

  # Middle Mask
  start_bit = randint(0, 31)
  end_bit = randint(start_bit, 31)
  masked_rand_a = perform_mmask(rand_a, start_bit, end_bit)
  masked_rand_b = perform_mmask(rand_b, start_bit, end_bit)
  random_msgs.extend([mk_imsg_mmask(rand_a, rand_b, start_bit, end_bit), mk_omsg(masked_rand_a * masked_rand_b)])

#-------------------------------------------------------------------------
# Test Case Table
#-------------------------------------------------------------------------

test_case_table = mk_test_case_table([
  (                      "msgs                   src_delay sink_delay"),
  [ "small_pos_pos",     small_pos_pos_msgs,     0,        0          ],
  [ "small_pos_pos",     small_pos_pos_msgs,     0,        1          ],

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to leverage the additional lists
  # of request/response messages defined above, but also to test
  # different source/sink random delays.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  [ "basic",             basic_msgs,             0,        0          ],
  [ "basic",             basic_msgs,             1,        0          ],

  [ "small_pos_neg",     small_pos_neg_msgs,     0,        0          ],
  [ "small_pos_neg",     small_pos_neg_msgs,     0,        2          ],

  [ "small_neg_pos",     small_neg_pos_msgs,     0,        0          ],
  [ "small_neg_pos",     small_neg_pos_msgs,     2,        0          ],

  [ "small_neg_neg",     small_neg_neg_msgs,     0,        0          ],
  [ "small_neg_neg",     small_neg_neg_msgs,     2,        1          ],

  [ "large_pos_pos",     large_pos_pos_msgs,     0,        0          ],
  [ "large_pos_pos",     large_pos_pos_msgs,     1,        2          ],

  [ "large_pos_neg",     large_pos_neg_msgs,     0,        0          ],
  [ "large_pos_neg",     large_pos_neg_msgs,     0,        3          ],

  [ "large_neg_pos",     large_neg_pos_msgs,     0,        0          ],
  [ "large_neg_pos",     large_neg_pos_msgs,     3,        0          ],

  [ "large_neg_neg",     large_neg_neg_msgs,     0,        0          ],
  [ "large_neg_neg",     large_neg_neg_msgs,     3,        5          ],

  [ "lower_bits_mask",   low_mask_msgs,          0,        0          ],
  [ "lower_bits_mask",   low_mask_msgs,          0,       10          ],

  [ "middle_bits_mask",  mid_mask_msgs,          0,        0          ],
  [ "middle_bits_mask",  mid_mask_msgs,         10,        0          ],

  [ "sparse_bits",       sparse_msgs,            0,        0          ],
  [ "sparse_bits",       sparse_msgs,            2,        7          ],

  [ "dense_bits",        dense_msgs,             0,        0          ],
  [ "dense_bits",        dense_msgs,             9,        1          ],

  [ "random_tests",      random_msgs,            0,        0          ],
  [ "random_tests",      random_msgs,            2,        6          ],
])

#-------------------------------------------------------------------------
# TestHarness
#-------------------------------------------------------------------------

@pytest.mark.parametrize( **test_case_table )
def test( test_params, cmdline_opts ):

  th = TestHarness( IntMulFL() )

  th.set_param("top.src.construct",
    msgs=test_params.msgs[::2],
    initial_delay=test_params.src_delay+3,
    interval_delay=test_params.src_delay )

  th.set_param("top.sink.construct",
    msgs=test_params.msgs[1::2],
    initial_delay=test_params.sink_delay+3,
    interval_delay=test_params.sink_delay )

  run_sim( th, cmdline_opts, duts=['imul'] )

