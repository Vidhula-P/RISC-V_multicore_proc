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
  # Tests that do not cause output to overflow (input up to 16 bits twos complement)
  mk_imsg(  25002,  29867 ), mk_omsg(  746734734 ),
  mk_imsg(  28788,  29393 ), mk_omsg(  846165684 ),
  mk_imsg(  25701,  24359 ), mk_omsg(  626050659 ),
  mk_imsg(  13134,  22203 ), mk_omsg(  291614202 ),
  mk_imsg(  18991,  14158 ), mk_omsg(  268874578 ),

  # Tests that cause output to overflow (input more than 16 bits twos complement)
  mk_imsg(  2000000000,   746065439 ), mk_omsg(  1492130878000000000 ),
  mk_imsg(   524811885,  1000000000 ), mk_omsg(   524811885000000000 ),
  mk_imsg(  1178821202,   354137688 ), mk_omsg(   417465015041660976 ),
  mk_imsg(  1523684544,   259862687 ), mk_omsg(   395948759744209728 ),
  mk_imsg(   578894330,  1756184545 ), mk_omsg(  1016645275534129850 ),

  # Maximum 16 bit and 32 bit twos complement positive values
  mk_imsg(  32767,  32767 ), mk_omsg(  1073676289 ),
  mk_imsg(  2147483647,  2147483647 ), mk_omsg(  4611686014132420609 ),
]

#----------------------------------------------------------------------
# Test Case: large positive * negative
#----------------------------------------------------------------------

large_pos_neg_msgs = [
  # Tests that do not cause output to overflow (input up to 16 bits twos complement)
  mk_imsg(  25002,  -29867 ), mk_omsg(  -746734734 ),
  mk_imsg(  28788,  -29393 ), mk_omsg(  -846165684 ),
  mk_imsg(  25701,  -24359 ), mk_omsg(  -626050659 ),
  mk_imsg(  13134,  -22203 ), mk_omsg(  -291614202 ),
  mk_imsg(  18991,  -14158 ), mk_omsg(  -268874578 ),

  # Tests that cause output to overflow (input more than 16 bits twos complement)
  mk_imsg(  2000000000,   -746065439 ), mk_omsg(  -1492130878000000000 ),
  mk_imsg(   524811885,  -1000000000 ), mk_omsg(   -524811885000000000 ),
  mk_imsg(  1178821202,   -354137688 ), mk_omsg(   -417465015041660976 ),
  mk_imsg(  1523684544,   -259862687 ), mk_omsg(   -395948759744209728 ),
  mk_imsg(   578894330,  -1756184545 ), mk_omsg(  -1016645275534129850 ),

  # Maximum 16 bit and 32 bit twos complement positive/negative values
  mk_imsg(  32767,  -32768 ), mk_omsg(  -1073709056 ),
  mk_imsg(  2147483647,  -2147483648 ), mk_omsg(  -4611686016279904256 ),
]

#----------------------------------------------------------------------
# Test Case: large negative * positive
#----------------------------------------------------------------------

large_neg_pos_msgs = [
  # Tests that do not cause output to overflow (input up to 16 bits twos complement)
  mk_imsg(  -25002,  29867 ), mk_omsg(  -746734734 ),
  mk_imsg(  -28788,  29393 ), mk_omsg(  -846165684 ),
  mk_imsg(  -25701,  24359 ), mk_omsg(  -626050659 ),
  mk_imsg(  -13134,  22203 ), mk_omsg(  -291614202 ),
  mk_imsg(  -18991,  14158 ), mk_omsg(  -268874578 ),

  # Tests that cause output to overflow (input more than 16 bits twos complement)
  mk_imsg(  -2000000000,   746065439 ), mk_omsg(  -1492130878000000000 ),
  mk_imsg(   -524811885,  1000000000 ), mk_omsg(   -524811885000000000 ),
  mk_imsg(  -1178821202,   354137688 ), mk_omsg(   -417465015041660976 ),
  mk_imsg(  -1523684544,   259862687 ), mk_omsg(   -395948759744209728 ),
  mk_imsg(   -578894330,  1756184545 ), mk_omsg(  -1016645275534129850 ),

  # Maximum 16 bit and 32 bit twos complement positive/negative values
  mk_imsg(  -32768,  32767 ), mk_omsg(  -1073709056 ),
  mk_imsg(  -2147483648,  2147483647 ), mk_omsg(  -4611686016279904256 ),
]

#----------------------------------------------------------------------
# Test Case: large negative * negative
#----------------------------------------------------------------------

large_neg_neg_msgs = [
  # Tests that do not cause output to overflow (input up to 16 bits twos complement)
  mk_imsg(  -25002,  -29867 ), mk_omsg(  746734734 ),
  mk_imsg(  -28788,  -29393 ), mk_omsg(  846165684 ),
  mk_imsg(  -25701,  -24359 ), mk_omsg(  626050659 ),
  mk_imsg(  -13134,  -22203 ), mk_omsg(  291614202 ),
  mk_imsg(  -18991,  -14158 ), mk_omsg(  268874578 ),

  # Tests that cause output to overflow (input more than 16 bits twos complement)
  mk_imsg(  -2000000000,   -746065439 ), mk_omsg(  1492130878000000000 ),
  mk_imsg(   -524811885,  -1000000000 ), mk_omsg(   524811885000000000 ),
  mk_imsg(  -1178821202,   -354137688 ), mk_omsg(   417465015041660976 ),
  mk_imsg(  -1523684544,   -259862687 ), mk_omsg(   395948759744209728 ),
  mk_imsg(   -578894330,  -1756184545 ), mk_omsg(  1016645275534129850 ),

  # Maximum 16 bit and 32 bit twos complement positive/negative values
  mk_imsg(  -32768,  -32768 ), mk_omsg(  1073741824 ),
  mk_imsg(  -2147483648,  -2147483648 ), mk_omsg(  4611686018427387904 ),

]

#----------------------------------------------------------------------
# Test Case: lower bits masked
#----------------------------------------------------------------------

low_mask_msgs = [
  # Up to 16 bit twos complement
  mk_imsg_lmask(  239,        453,         2 ), mk_omsg(              106672 ),
  mk_imsg_lmask(  985,        1259,        6 ), mk_omsg(             1167360 ),
  mk_imsg_lmask(  8920,       15502,       8 ), mk_omsg(          133693440  ),
  # More than 16 bit twos complement
  mk_imsg_lmask(  47847382,   739006219,   15), mk_omsg(  35353937397678080  ),
]

#----------------------------------------------------------------------
# Test Case: middle bits masked
#----------------------------------------------------------------------

mid_mask_msgs = [
  # Up to 16 bit twos complement
  mk_imsg_mmask(  239,        453,         2,    4 ),  mk_omsg(            101923 ),
  mk_imsg_mmask(  985,        1259,        6,    10 ), mk_omsg(              1075 ),
  mk_imsg_mmask(  8920,       15502,       4,    11 ), mk_omsg(         100876400 ),
  # More than 16 bit twos complement
  mk_imsg_mmask(  47847382,   739006219,   7,    19),  mk_omsg( 34832592371975090 ),
]

#----------------------------------------------------------------------
# Test Case: sparse numbers
#----------------------------------------------------------------------

sparse_msgs = [
  # Up to 16 bit twos complement
  mk_imsg(  32769,  32897),  mk_omsg( 1078001793 ),
  # More than 16 bit twos complement
  mk_imsg(  11184640, 279620104),  mk_omsg( 3127450200002560 ),
]

#----------------------------------------------------------------------
# Test Case: dense numbers
#----------------------------------------------------------------------

dense_msgs = [
  # Up to 16 bit twos complement
  mk_imsg(  31743,  16351 ),  mk_omsg(  519029793 ),
  # More than 16 bit twos complement
  mk_imsg(  1605348090,  2142153466), mk_omsg(  3438901975129979940 ),
]

random_msgs = [
]

for i in range(30):
  rand_a = randint(-2147483648, 2147483647)
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
  [ "small_pos_pos_1",     small_pos_pos_msgs,     0,        0          ],
  [ "small_pos_pos_2",     small_pos_pos_msgs,     0,        50         ],

  [ "basic_1",             basic_msgs,             0,        0          ],
  [ "basic_2",             basic_msgs,             100,      0          ],

  [ "small_pos_neg_1",     small_pos_neg_msgs,     0,        0          ],
  [ "small_pos_neg_2",     small_pos_neg_msgs,     0,        92         ],

  [ "small_neg_pos_1",     small_neg_pos_msgs,     0,        0          ],
  [ "small_neg_pos_2",     small_neg_pos_msgs,     26,       0          ],

  [ "small_neg_neg_1",     small_neg_neg_msgs,     0,        0          ],
  [ "small_neg_neg_2",     small_neg_neg_msgs,     62,       1          ],

  [ "large_pos_pos_1",     large_pos_pos_msgs,     0,        0          ],
  [ "large_pos_pos_2",     large_pos_pos_msgs,     110,      86         ],

  [ "large_pos_neg_1",     large_pos_neg_msgs,     0,        0          ],
  [ "large_pos_neg_2",     large_pos_neg_msgs,     0,        38         ],

  [ "large_neg_pos_1",     large_neg_pos_msgs,     0,        0          ],
  [ "large_neg_pos_2",     large_neg_pos_msgs,     83,       0          ],

  [ "large_neg_neg_1",     large_neg_neg_msgs,     0,        0          ],
  [ "large_neg_neg_2",     large_neg_neg_msgs,     83,       59         ],

  [ "lower_bits_mask_1",   low_mask_msgs,          0,        0          ],
  [ "lower_bits_mask_2",   low_mask_msgs,          0,        120        ],

  [ "middle_bits_mask_1",  mid_mask_msgs,          0,        0          ],
  [ "middle_bits_mask_2",  mid_mask_msgs,          40,       0          ],

  [ "sparse_bits_1",       sparse_msgs,            0,        0          ],
  [ "sparse_bits_2",       sparse_msgs,            60,       47         ],

  [ "dense_bits_1",        dense_msgs,             0,        0          ],
  [ "dense_bits_2",        dense_msgs,             59,       73         ],

  [ "random_tests_1",      random_msgs,            0,        0          ],
  [ "random_tests_2",      random_msgs,            72,       61         ]
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

