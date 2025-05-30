#=========================================================================
# NetRouterSwitchUnit_test
#=========================================================================

import pytest

from pymtl3 import *
from pymtl3.stdlib.test_utils import mk_test_case_table, run_sim
from pymtl3.stdlib.stream import StreamSourceFL, StreamSinkFL

from lab4_sys.NetMsg import mk_net_msg
from lab4_sys.NetRouterSwitchUnit import NetRouterSwitchUnit

import random

#-------------------------------------------------------------------------
# Message Types
#-------------------------------------------------------------------------

NetMsgType = mk_net_msg( 32 )

#-------------------------------------------------------------------------
# TestHarness
#-------------------------------------------------------------------------

class TestHarness( Component ):

  def construct( s ):

    # Instantiate models

    s.srcs  = [ StreamSourceFL( NetMsgType ) for _ in range(3) ]
    s.sunit = NetRouterSwitchUnit( p_msg_nbits=44 )
    s.sink  = StreamSinkFL( NetMsgType )

    # Connect

    s.srcs[0].ostream //= s.sunit.istream[0]
    s.srcs[1].ostream //= s.sunit.istream[1]
    s.srcs[2].ostream //= s.sunit.istream[2]
    s.sunit.ostream   //= s.sink.istream

  def done( s ):
    return s.srcs[0].done() and s.srcs[1].done() and s.srcs[2].done() and s.sink.done()

  def line_trace( s ):
    return s.srcs[0].line_trace()  + "|" + \
           s.srcs[1].line_trace()  + "|" + \
           s.srcs[2].line_trace()  + " > (" + \
           s.sunit.line_trace() + ") > " + \
           s.sink.line_trace()

#-------------------------------------------------------------------------
# test_basic
#-------------------------------------------------------------------------
# These is an example of a basic test. This tests may not be valid
# depending on your arbitration algorithm. You are free to change this
# test. We will not test your switch unit since its functionality depends
# on the chosen arbitration algorithm.

def test_basic( cmdline_opts ):

  th = TestHarness()

  msgs = [
    #           src  dest opaq  payload
    NetMsgType( 1,   0,   0x11, 0x11111111 ),
    NetMsgType( 2,   0,   0x12, 0x12121212 ),
    NetMsgType( 0,   0,   0x10, 0x10101010 ),
  ]

  th.set_param("top.srcs[0].construct", msgs=[ m for m in msgs if m.src == 0 ] )
  th.set_param("top.srcs[1].construct", msgs=[ m for m in msgs if m.src == 1 ] )
  th.set_param("top.srcs[2].construct", msgs=[ m for m in msgs if m.src == 2 ] )
  th.set_param("top.sink.construct", msgs=msgs  )

  th.elaborate()

  run_sim( th, cmdline_opts, duts=['sunit'] )

#-------------------------------------------------------------------------
# Test Cases: Very Simple
#-------------------------------------------------------------------------
# These are examples of a simple tests using a test case table. These
# tests may not be valid depending on your arbitration algorithm. You are
# free to change these tests. We will not test your switch unit since its
# functionality depends on the chosen arbitration algorithm.

one = [
  #           src  dest opaq  payload
  NetMsgType( 0,   0,   0x10, 0x10101010 ),
]

three = [
  #           src  dest opaq  payload
  NetMsgType( 1,   0,   0x11, 0x11111111 ),
  NetMsgType( 2,   0,   0x12, 0x12121212 ),
  NetMsgType( 0,   0,   0x10, 0x10101010 ),
]

three_diff_dest = [
  #           src  dest opaq  payload
  NetMsgType( 1,   2,   0x11, 0x11111111 ),
  NetMsgType( 2,   1,   0x12, 0x12121212 ),
  NetMsgType( 0,   3,   0x10, 0x10101010 ),
]

# Tests with rotated order of destinations

three_diff_dest_rotated0 = [
  #           src  dest opaq  payload
  NetMsgType( 1,   1,   0x11, 0x11111111 ),
  NetMsgType( 2,   3,   0x12, 0x12121212 ),
  NetMsgType( 0,   2,   0x10, 0x10101010 ),
]

three_diff_dest_rotated1 = [
  #           src  dest opaq  payload
  NetMsgType( 1,   1,   0x11, 0x11111111 ),
  NetMsgType( 2,   3,   0x12, 0x12121212 ),
  NetMsgType( 0,   2,   0x10, 0x10101010 ),
]

three_diff_dest_rotated2 = [
  #           src  dest opaq  payload
  NetMsgType( 1,   3,   0x11, 0x11111111 ),
  NetMsgType( 2,   2,   0x12, 0x12121212 ),
  NetMsgType( 0,   1,   0x10, 0x10101010 ),
]

# Tests with random dest and larger number of messages

large_rand_dest = []

curr_payload = 0x10101010
for i in [1, 2, 0]:
  for _ in range(50):
    rand_dest = random.randint(0, 3)
    rand_opaq = random.randint(0, 16)
    curr_payload += 1
    large_rand_dest.append(NetMsgType( i,   rand_dest,   rand_opaq, curr_payload ))

#-------------------------------------------------------------------------
# Test Case Table
#-------------------------------------------------------------------------

test_case_table = mk_test_case_table([
  (                               "msgs                     src_delay sink_delay delay_mode"),
  [ "one",                         one,                           0,  0,  'fixed'  ],
  [ "three",                       three,                         0,  0,  'fixed'  ],
  [ "three_diff_dest",             three_diff_dest,               0,  0,  'fixed'  ],
  [ "three_diff_dest_rotated0",    three_diff_dest_rotated0,      0,  0,  'fixed'  ],
  [ "three_diff_dest_rotated1",    three_diff_dest_rotated0,      0,  0,  'fixed'  ],
  [ "three_diff_dest_rotated2",    three_diff_dest_rotated0,      0,  0,  'fixed'  ],
  [ "large_rand_dest",             large_rand_dest,               0,  0,  'fixed'  ],

  # Directed and random src sink delays
  [ "delay_one",                         one,                           9,  0,  'fixed'  ],
  [ "delay_three",                       three,                         0,  3,  'fixed'  ],
  [ "delay_three_diff_dest",             three_diff_dest,               2,  0,  'fixed'  ],
  [ "delay_three_diff_dest_rotated0",    three_diff_dest_rotated0,      3,  6,  'fixed'  ],
  [ "delay_three_diff_dest_rotated1",    three_diff_dest_rotated0,      0,  1,  'random'  ],
  [ "delay_three_diff_dest_rotated2",    three_diff_dest_rotated0,      2,  0,  'fixed'  ],
  [ "delay_large_rand_dest",             large_rand_dest,               0,  2,  'fixed'  ],
  [ "delay_large_rand_dest",             large_rand_dest,               3,  3,  'fixed'  ],
  [ "delay_large_rand_dest",             large_rand_dest,               3,  5,  'fixed'  ],
  [ "delay_large_rand_dest",             large_rand_dest,               0,  0,  'random'  ],
  [ "delay_large_rand_dest",             large_rand_dest,               0,  0,  'random'  ],
  [ "delay_large_rand_dest",             large_rand_dest,               0,  0,  'random'  ],

])

#-------------------------------------------------------------------------
# test
#-------------------------------------------------------------------------

@pytest.mark.parametrize( **test_case_table )
def test( test_params, cmdline_opts ):

  th = TestHarness()

  th.set_param("top.srcs[0].construct",
    msgs                = [ m for m in test_params.msgs if m.src == 0 ],
    interval_delay_mode = test_params.delay_mode,
    initial_delay       = test_params.src_delay,
    interval_delay      = test_params.src_delay )

  th.set_param("top.srcs[1].construct",
    msgs                = [ m for m in test_params.msgs if m.src == 1 ],
    interval_delay_mode = test_params.delay_mode,
    initial_delay       = test_params.src_delay,
    interval_delay      = test_params.src_delay )

  th.set_param("top.srcs[2].construct",
    msgs                = [ m for m in test_params.msgs if m.src == 2 ],
    interval_delay_mode = test_params.delay_mode,
    initial_delay       = test_params.src_delay,
    interval_delay      = test_params.src_delay )

  th.set_param("top.sink.construct",
    msgs                = test_params.msgs,
    interval_delay_mode = test_params.delay_mode,
    initial_delay       = test_params.sink_delay,
    interval_delay      = test_params.sink_delay )

  th.elaborate()

  run_sim( th, cmdline_opts, duts=['sunit'] )
