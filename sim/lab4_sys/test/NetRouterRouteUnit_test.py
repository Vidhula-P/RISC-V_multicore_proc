#=========================================================================
# NetRouterRouteUnit_test
#=========================================================================

import pytest

from pymtl3 import *
from pymtl3.stdlib.test_utils import mk_test_case_table, run_sim
from pymtl3.stdlib.stream import StreamSourceFL, StreamSinkFL

from lab4_sys.NetMsg import mk_net_msg
from lab4_sys.NetRouterRouteUnit import NetRouterRouteUnit

import random

#-------------------------------------------------------------------------
# Message Types
#-------------------------------------------------------------------------

NetMsgType = mk_net_msg( 32 )

#-------------------------------------------------------------------------
# TestHarness
#-------------------------------------------------------------------------

class TestHarness( Component ):

  def construct( s, router_id=0 ):

    # Instantiate models

    s.src   = StreamSourceFL( NetMsgType )
    s.runit = NetRouterRouteUnit( p_msg_nbits=44 )
    s.sinks = [ StreamSinkFL( NetMsgType ) for _ in range(3) ]

    # Connect

    s.runit.router_id  //= router_id
    s.src.ostream      //= s.runit.istream
    s.runit.ostream[0] //= s.sinks[0].istream
    s.runit.ostream[1] //= s.sinks[1].istream
    s.runit.ostream[2] //= s.sinks[2].istream

  def done( s ):
    return s.src.done() and s.sinks[0].done() and s.sinks[1].done() and s.sinks[2].done()

  def line_trace( s ):
    return s.src.line_trace()   + " > (" + \
           s.runit.line_trace() + ") > " + \
           s.sinks[0].line_trace() + "|" + \
           s.sinks[1].line_trace() + "|" + \
           s.sinks[2].line_trace()

#-------------------------------------------------------------------------
# test_basic
#-------------------------------------------------------------------------
# This is an example of a basic test. This test may not be valid
# depending on your routing algorithm. You are free to change this test.
# We will not test your route unit since its functionality depends on the
# chosen routing algorithm.

def test_basic( cmdline_opts ):

  th = TestHarness( router_id=0 )

  msgs = [
    #           src  dest opaq  payload
    NetMsgType( 0,   0,   0x10, 0x10101010 ),
    NetMsgType( 0,   1,   0x11, 0x11111111 ),
    NetMsgType( 0,   2,   0x12, 0x12121212 ),
    NetMsgType( 0,   3,   0x13, 0x13131313 ),
  ]

  th.set_param("top.src.construct",   msgs=msgs  )
  th.set_param("top.sinks[0].construct", msgs=[ m for m in msgs if m.dest == 0 ] )
  th.set_param("top.sinks[1].construct", msgs=[ m for m in msgs if m.dest != 0 ] )
  th.set_param("top.sinks[2].construct", msgs=[] )

  th.elaborate()

  run_sim( th, cmdline_opts, duts=['runit'] )

#-------------------------------------------------------------------------
# Test Cases: Very Simple
#-------------------------------------------------------------------------
# These are examples of a simple tests using a test case table. These
# tests may not be valid depending on your routing algorithm. You are
# free to change these tests. We will not test your route unit since its
# functionality depends on the chosen routing algorithm.

one = [
  #           src  dest opaq  payload
  NetMsgType( 0,   0,   0x10, 0x10101010 ),
]

# Tests with different input sources

four = [
  #           src  dest opaq  payload
  NetMsgType( 0,   0,   0x10, 0x10101010 ),
  NetMsgType( 0,   1,   0x11, 0x11111111 ),
  NetMsgType( 0,   2,   0x12, 0x12121212 ),
  NetMsgType( 0,   3,   0x13, 0x13131313 ),
]

four_src_1 = [
  #           src  dest opaq  payload
  NetMsgType( 1,   0,   0x10, 0x10101010 ),
  NetMsgType( 1,   1,   0x11, 0x11111111 ),
  NetMsgType( 1,   2,   0x12, 0x12121212 ),
  NetMsgType( 1,   3,   0x13, 0x13131313 ),
]

four_src_2 = [
  #           src  dest opaq  payload
  NetMsgType( 2,   0,   0x10, 0x10101010 ),
  NetMsgType( 2,   1,   0x11, 0x11111111 ),
  NetMsgType( 2,   2,   0x12, 0x12121212 ),
  NetMsgType( 2,   3,   0x13, 0x13131313 ),
]

four_src_3 = [
  #           src  dest opaq  payload
  NetMsgType( 3,   0,   0x10, 0x10101010 ),
  NetMsgType( 3,   1,   0x11, 0x11111111 ),
  NetMsgType( 3,   2,   0x12, 0x12121212 ),
  NetMsgType( 3,   3,   0x13, 0x13131313 ),
]

# Tests with rotated order of destination

four_src_2_rotate0 = [
  #           src  dest opaq  payload
  NetMsgType( 2,   1,   0x10, 0x10101010 ),
  NetMsgType( 2,   2,   0x11, 0x11111111 ),
  NetMsgType( 2,   3,   0x12, 0x12121212 ),
  NetMsgType( 2,   0,   0x13, 0x13131313 ),
]

four_src_2_rotate1 = [
  #           src  dest opaq  payload
  NetMsgType( 2,   2,   0x10, 0x10101010 ),
  NetMsgType( 2,   3,   0x11, 0x11111111 ),
  NetMsgType( 2,   0,   0x12, 0x12121212 ),
  NetMsgType( 2,   1,   0x13, 0x13131313 ),
]

four_src_2_rotate2 = [
  #           src  dest opaq  payload
  NetMsgType( 2,   3,   0x10, 0x10101010 ),
  NetMsgType( 2,   0,   0x11, 0x11111111 ),
  NetMsgType( 2,   1,   0x12, 0x12121212 ),
  NetMsgType( 2,   2,   0x13, 0x13131313 ),
]

four_src_2_neworder = [
  #           src  dest opaq  payload
  NetMsgType( 2,   3,   0x10, 0x10101010 ),
  NetMsgType( 2,   1,   0x11, 0x11111111 ),
  NetMsgType( 2,   0,   0x12, 0x12121212 ),
  NetMsgType( 2,   2,   0x13, 0x13131313 ),
]

# Tests with different srcs rotated

four_diff_src = [
  #           src  dest opaq  payload
  NetMsgType( 3,   0,   0x10, 0x10101010 ),
  NetMsgType( 2,   1,   0x11, 0x11111111 ),
  NetMsgType( 1,   2,   0x12, 0x12121212 ),
  NetMsgType( 0,   3,   0x13, 0x13131313 ),
]

four_diff_src_rotate0 = [
  #           src  dest opaq  payload
  NetMsgType( 2,   0,   0x10, 0x10101010 ),
  NetMsgType( 1,   1,   0x11, 0x11111111 ),
  NetMsgType( 0,   2,   0x12, 0x12121212 ),
  NetMsgType( 3,   3,   0x13, 0x13131313 ),
]

four_diff_src_rotate1 = [
  #           src  dest opaq  payload
  NetMsgType( 1,   0,   0x10, 0x10101010 ),
  NetMsgType( 0,   1,   0x11, 0x11111111 ),
  NetMsgType( 3,   2,   0x12, 0x12121212 ),
  NetMsgType( 2,   3,   0x13, 0x13131313 ),
]
four_diff_src_rotate2 = [
  #           src  dest opaq  payload
  NetMsgType( 0,   0,   0x10, 0x10101010 ),
  NetMsgType( 3,   1,   0x11, 0x11111111 ),
  NetMsgType( 2,   2,   0x12, 0x12121212 ),
  NetMsgType( 1,   3,   0x13, 0x13131313 ),
]

four_diff_src_neworder = [
  #           src  dest opaq  payload
  NetMsgType( 0,   0,   0x10, 0x10101010 ),
  NetMsgType( 3,   1,   0x11, 0x11111111 ),
  NetMsgType( 2,   2,   0x12, 0x12121212 ),
  NetMsgType( 1,   3,   0x13, 0x13131313 ),
]

# Test with random src dest with larger number of messages

large_rand_src_dest = []

curr_payload = 0x10101010
for _ in range(50):
  rand_src = random.randint(0, 3)
  rand_dest = random.randint(0, 3)
  curr_payload += 1
  rand_opaq = random.randint(0, 16)
  large_rand_src_dest.append(NetMsgType( rand_src,   rand_dest,   rand_opaq, curr_payload ))

#-------------------------------------------------------------------------
# Test Case Table
#-------------------------------------------------------------------------

test_case_table = mk_test_case_table([
  (                              "msgs                src_delay sink_delay delay_mode"),
  [ "one",                        one,                    0,  0,  'fixed'  ],
  [ "four",                       four,                   0,  0,  'fixed'  ],
  [ "four_src_1",                 four_src_1,             0,  0,  'fixed'  ],
  [ "four_src_2",                 four_src_2,             0,  0,  'fixed'  ],
  [ "four_src_3",                 four_src_3,             0,  0,  'fixed'  ],
  [ "four_src_2_rotate0",         four_src_2_rotate0,     0,  0,  'fixed'  ],
  [ "four_src_2_rotate1",         four_src_2_rotate1,     0,  0,  'fixed'  ],
  [ "four_src_2_rotate2",         four_src_2_rotate2,     0,  0,  'fixed'  ],
  [ "four_src_2_neworder",        four_src_2_neworder,    0,  0,  'fixed'  ],
  [ "four",                       four,                   0,  0,  'fixed'  ],
  [ "four_diff_src",              four_diff_src,          0,  0,  'fixed'  ],
  [ "four_diff_src_rotate0",      four_diff_src_rotate0,  0,  0,  'fixed'  ],
  [ "four_diff_src_rotate1",      four_diff_src_rotate0,  0,  0,  'fixed'  ],
  [ "four_diff_src_rotate2",      four_diff_src_rotate0,  0,  0,  'fixed'  ],
  [ "four_diff_src_neworder",     four_diff_src_neworder, 0,  0,  'fixed'  ],
  [ "large_rand_src_dest",        large_rand_src_dest,    0,  0,  'fixed'  ],

  # Directed src sink delays, and random delay modes
  [ "delay_one",                        one,                    1,  0,  'fixed'  ],
  [ "delay_four",                       four,                   0,  3,  'fixed'  ],
  [ "delay_four_src_1",                 four_src_1,             4,  7,  'random'  ],
  [ "delay_four_src_2",                 four_src_2,             5,  0,  'fixed'  ],
  [ "delay_four_src_3",                 four_src_3,             0,  1,  'fixed'  ],
  [ "delay_four_src_2_rotate0",         four_src_2_rotate0,     0,  4,  'fixed'  ],
  [ "delay_four_src_2_rotate1",         four_src_2_rotate1,     7,  2,  'fixed'  ],
  [ "delay_four_src_2_rotate2",         four_src_2_rotate2,     0,  1,  'fixed'  ],
  [ "delay_four_src_2_neworder",        four_src_2_neworder,    1,  0,  'fixed'  ],
  [ "delay_four",                       four,                   0,  3,  'random'  ],
  [ "delay_four_diff_src",              four_diff_src,          30,  0,  'fixed'  ],
  [ "delay_four_diff_src_rotate0",      four_diff_src_rotate0,  0,  24,  'fixed'  ],
  [ "delay_four_diff_src_rotate1",      four_diff_src_rotate0,  25,  0,  'fixed'  ],
  [ "delay_four_diff_src_rotate2",      four_diff_src_rotate0,  0,  10,  'fixed'  ],
  [ "delay_four_diff_src_neworder",     four_diff_src_neworder, 3,  0,  'fixed'  ],
  [ "delay_large_rand_src_dest",        large_rand_src_dest,    10,  0, 'fixed'  ],
  [ "delay_large_rand_src_dest",        large_rand_src_dest,    0,  5,  'fixed'  ],
  [ "delay_large_rand_src_dest",        large_rand_src_dest,    2,  6,  'fixed'  ],
  [ "delay_large_rand_src_dest",        large_rand_src_dest,    0,  0,  'random'  ],


])

#-------------------------------------------------------------------------
# test w/ router id 0, 1, 2, 3
#-------------------------------------------------------------------------

@pytest.mark.parametrize( **test_case_table )
def test_router_id_0( test_params, cmdline_opts ):

  th = TestHarness( router_id=0 )

  th.set_param("top.src.construct",
    msgs                = test_params.msgs,
    interval_delay_mode = test_params.delay_mode,
    initial_delay       = test_params.src_delay,
    interval_delay      = test_params.src_delay )

  th.set_param("top.sinks[0].construct",
    msgs                = [ m for m in test_params.msgs if m.dest == 0 ],
    interval_delay_mode = test_params.delay_mode,
    initial_delay       = test_params.sink_delay,
    interval_delay      = test_params.sink_delay )

  th.set_param("top.sinks[1].construct",
    msgs                = [ m for m in test_params.msgs if m.dest != 0 ],
    interval_delay_mode = test_params.delay_mode,
    initial_delay       = test_params.sink_delay,
    interval_delay      = test_params.sink_delay )

  th.set_param("top.sinks[2].construct",
    msgs                = [],
    interval_delay_mode = test_params.delay_mode,
    initial_delay       = test_params.sink_delay,
    interval_delay      = test_params.sink_delay )

  th.elaborate()

  run_sim( th, cmdline_opts, duts=['runit'] )

@pytest.mark.parametrize( **test_case_table )
def test_router_id_1( test_params, cmdline_opts ):

  th = TestHarness( router_id=1 )

  th.set_param("top.src.construct",
    msgs                = test_params.msgs,
    interval_delay_mode = test_params.delay_mode,
    initial_delay       = test_params.src_delay,
    interval_delay      = test_params.src_delay )

  th.set_param("top.sinks[0].construct",
    msgs                = [ m for m in test_params.msgs if m.dest == 1 ],
    interval_delay_mode = test_params.delay_mode,
    initial_delay       = test_params.sink_delay,
    interval_delay      = test_params.sink_delay )

  th.set_param("top.sinks[1].construct",
    msgs                = [ m for m in test_params.msgs if m.dest != 1 ],
    interval_delay_mode = test_params.delay_mode,
    initial_delay       = test_params.sink_delay,
    interval_delay      = test_params.sink_delay )

  th.set_param("top.sinks[2].construct",
    msgs                = [],
    interval_delay_mode = test_params.delay_mode,
    initial_delay       = test_params.sink_delay,
    interval_delay      = test_params.sink_delay )

  th.elaborate()

  run_sim( th, cmdline_opts, duts=['runit'] )

@pytest.mark.parametrize( **test_case_table )
def test_router_id_2( test_params, cmdline_opts ):

  th = TestHarness( router_id=2 )

  th.set_param("top.src.construct",
    msgs                = test_params.msgs,
    interval_delay_mode = test_params.delay_mode,
    initial_delay       = test_params.src_delay,
    interval_delay      = test_params.src_delay )

  th.set_param("top.sinks[0].construct",
    msgs                = [ m for m in test_params.msgs if m.dest == 2 ],
    interval_delay_mode = test_params.delay_mode,
    initial_delay       = test_params.sink_delay,
    interval_delay      = test_params.sink_delay )

  th.set_param("top.sinks[1].construct",
    msgs                = [ m for m in test_params.msgs if m.dest != 2 ],
    interval_delay_mode = test_params.delay_mode,
    initial_delay       = test_params.sink_delay,
    interval_delay      = test_params.sink_delay )

  th.set_param("top.sinks[2].construct",
    msgs                = [],
    interval_delay_mode = test_params.delay_mode,
    initial_delay       = test_params.sink_delay,
    interval_delay      = test_params.sink_delay )

  th.elaborate()

  run_sim( th, cmdline_opts, duts=['runit'] )

@pytest.mark.parametrize( **test_case_table )
def test_router_id_3( test_params, cmdline_opts ):

  th = TestHarness( router_id=3 )

  th.set_param("top.src.construct",
    msgs                = test_params.msgs,
    interval_delay_mode = test_params.delay_mode,
    initial_delay       = test_params.src_delay,
    interval_delay      = test_params.src_delay )

  th.set_param("top.sinks[0].construct",
    msgs                = [ m for m in test_params.msgs if m.dest == 3 ],
    interval_delay_mode = test_params.delay_mode,
    initial_delay       = test_params.sink_delay,
    interval_delay      = test_params.sink_delay )

  th.set_param("top.sinks[1].construct",
    msgs                = [ m for m in test_params.msgs if m.dest != 3 ],
    interval_delay_mode = test_params.delay_mode,
    initial_delay       = test_params.sink_delay,
    interval_delay      = test_params.sink_delay )

  th.set_param("top.sinks[2].construct",
    msgs                = [],
    interval_delay_mode = test_params.delay_mode,
    initial_delay       = test_params.sink_delay,
    interval_delay      = test_params.sink_delay )

  th.elaborate()

  run_sim( th, cmdline_opts, duts=['runit'] )

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

