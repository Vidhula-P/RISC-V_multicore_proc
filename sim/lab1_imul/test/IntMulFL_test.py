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

def mk_imsg_lmask(a, b, num_bits_to_mask): # modified mk_imsg to accomodate masking of lower bits
  mask = ((1<<32) -1) << num_bits_to_mask
  return concat( Bits32( ( a & mask ), trunc_int=True ), Bits32( ( b & mask ), trunc_int=True ) )

def mk_imsg_mmask(a, b, start_bit, end_bit): # modified mk_imsg to accomodate masking of middle bits
  mask = ~((1 << (end_bit - start_bit + 1)) - 1) << start_bit
  return concat( Bits32( ( a & mask ), trunc_int=True ), Bits32( ( b & mask ), trunc_int=True ) )

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
  mk_imsg(  2000000000,  3141592653 ), mk_omsg(  6283185306000000000 ),
  mk_imsg(  4294967295,  1000000000 ), mk_omsg(  4294967295000000000 ),
  mk_imsg(  5000000000,  6000000000 ), mk_omsg(  30000000000000000000 ),
  mk_imsg(  7000000000,  8000000000 ), mk_omsg(  56000000000000000000 ),
  mk_imsg(  9000000000,  1234567890 ), mk_omsg(  11111111010000000000 ),
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

#-------------------------------------------------------------------------
# Test Case Table
#-------------------------------------------------------------------------

test_case_table = mk_test_case_table([
  (                      "msgs                   src_delay sink_delay"),
  [ "small_pos_pos",     small_pos_pos_msgs,     0,        0          ],

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to leverage the additional lists
  # of request/response messages defined above, but also to test
  # different source/sink random delays.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  [ "basic",             basic_msgs,             0,        0          ],
  [ "small_pos_neg",     small_pos_neg_msgs,     0,        0          ],
  [ "small_neg_pos",     small_neg_pos_msgs,     0,        0          ],
  [ "small_neg_neg",     small_neg_neg_msgs,     0,        0          ],
  [ "large_pos_pos",     large_pos_pos_msgs,     0,        0          ],
  [ "large_pos_neg",     large_pos_neg_msgs,     0,        0          ],
  [ "large_neg_pos",     large_neg_pos_msgs,     0,        0          ],
  [ "large_neg_neg",     large_neg_neg_msgs,     0,        0          ],
  [ "lower_bits_mask",   low_mask_msgs,          0,        0          ],
  [ "middle_bits_mask",  mid_mask_msgs,          0,        0          ],
  [ "sparse_bits",       sparse_msgs,            0,        0          ],
  [ "dense_bits",        dense_msgs,             0,        0          ],
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

