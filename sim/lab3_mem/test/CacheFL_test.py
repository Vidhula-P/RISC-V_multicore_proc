#=========================================================================
# CacheFL_test.py
#=========================================================================

import pytest

from random import seed, randint, random, choice

from pymtl3 import *
from pymtl3.stdlib.mem        import MemMsgType
from pymtl3.stdlib.test_utils import mk_test_case_table

from lab3_mem.test.harness import req, resp, run_test
from lab3_mem.CacheFL      import CacheFL

seed(0xa4e28cc2)

#-------------------------------------------------------------------------
# cmp_wo_test_field
#-------------------------------------------------------------------------
# The test field in the cache response is used to indicate if the
# corresponding memory access resulted in a hit or a miss. However, the
# FL model always sets the test field to zero since it does not track
# hits/misses. So we need to do something special to ignore the test
# field when using the FL model. To do this, we can pass in a specialized
# comparison function to the StreamSinkFL.

def cmp_wo_test_field( msg, ref ):

  if msg.type_ != ref.type_:
    return False

  if msg.len != ref.len:
    return False

  if msg.opaque != msg.opaque:
    return False

  if ref.data != msg.data:
    return False

  # do not check the test field

  return True

#-------------------------------------------------------------------------
# Data
#-------------------------------------------------------------------------
# These functions are used to specify the address/data to preload into
# the main memory before running a test.

# 64B of sequential data

def data_64B():
  return [
    # addr      data
    0x00001000, 0x000c0ffe,
    0x00001004, 0x10101010,
    0x00001008, 0x20202020,
    0x0000100c, 0x30303030,
    0x00001010, 0x40404040,
    0x00001014, 0x50505050,
    0x00001018, 0x60606060,
    0x0000101c, 0x70707070,
    0x00001020, 0x80808080,
    0x00001024, 0x90909090,
    0x00001028, 0xa0a0a0a0,
    0x0000102c, 0xb0b0b0b0,
    0x00001030, 0xc0c0c0c0,
    0x00001034, 0xd0d0d0d0,
    0x00001038, 0xe0e0e0e0,
    0x0000103c, 0xf0f0f0f0,
  ]

# 512B of sequential data

def data_512B():
  data = []
  for i in range(128):
    data.extend([0x00001000+i*4,0xabcd1000+i*4])
  return data

# 1024B of sequential data

def data_8192B():
  data = []
  for i in range(2048):
    data.extend([0x00001000+i*4,0xabcd1000+i*4])
  return data

# 1024B of random data

def data_random():
  seed(0xdeadbeef)
  data = []
  for i in range(256):
    data.extend([0x00001000+i*4,randint(0,0xffffffff)])
  return data

#----------------------------------------------------------------------
# Test Cases for Write Init
#----------------------------------------------------------------------

# Just make sure a single write init goes through the memory system.

def write_init_word():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x1000, 0, 0xdeadbeef ), resp( 'in', 0x0, 0,   0,  0    ),
  ]

# Write init a word multiple times, also tests opaque bits

def write_init_multi_word():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x1000, 0, 0xdeadbeef ), resp( 'in', 0x0, 0,   0,  0    ),
    req( 'in', 0x1, 0x1000, 0, 0xdeadbeef ), resp( 'in', 0x1, 0,   0,  0    ),
    req( 'in', 0x2, 0x1000, 0, 0xdeadbeef ), resp( 'in', 0x2, 0,   0,  0    ),
    req( 'in', 0x3, 0x1000, 0, 0xdeadbeef ), resp( 'in', 0x3, 0,   0,  0    ),
  ]

# Use write inits for each word in a cache line

def write_init_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x1000, 0, 0x01010101 ), resp( 'in', 0x0, 0,   0,  0    ),
    req( 'in', 0x1, 0x1004, 0, 0x02020202 ), resp( 'in', 0x1, 0,   0,  0    ),
    req( 'in', 0x2, 0x1008, 0, 0x03030303 ), resp( 'in', 0x2, 0,   0,  0    ),
    req( 'in', 0x3, 0x100c, 0, 0x04040404 ), resp( 'in', 0x3, 0,   0,  0    ),
  ]

# Write init one word in each cacheline in half the cache. For the direct
# mapped cache, this will write the first half of all the sets. For the
# set associative cache, this will write all of the sets in the first
# way.

def write_init_multi_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x0000, 0, 0x00000000 ), resp( 'in', 0x0, 0,   0,  0    ),
    req( 'in', 0x1, 0x1010, 0, 0x01010101 ), resp( 'in', 0x1, 0,   0,  0    ),
    req( 'in', 0x2, 0x2020, 0, 0x02020202 ), resp( 'in', 0x2, 0,   0,  0    ),
    req( 'in', 0x3, 0x3030, 0, 0x03030303 ), resp( 'in', 0x3, 0,   0,  0    ),
    req( 'in', 0x4, 0x4040, 0, 0x04040404 ), resp( 'in', 0x4, 0,   0,  0    ),
    req( 'in', 0x5, 0x5050, 0, 0x05050505 ), resp( 'in', 0x5, 0,   0,  0    ),
    req( 'in', 0x6, 0x6060, 0, 0x06060606 ), resp( 'in', 0x6, 0,   0,  0    ),
    req( 'in', 0x7, 0x7070, 0, 0x07070707 ), resp( 'in', 0x7, 0,   0,  0    ),
  ]

def write_init_all_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x0000, 0, 0x00000000 ), resp( 'in', 0x0, 0,   0,  0    ),
    req( 'in', 0x1, 0x1010, 0, 0x01010101 ), resp( 'in', 0x1, 0,   0,  0    ),
    req( 'in', 0x2, 0x2020, 0, 0x02020202 ), resp( 'in', 0x2, 0,   0,  0    ),
    req( 'in', 0x3, 0x3030, 0, 0x03030303 ), resp( 'in', 0x3, 0,   0,  0    ),
    req( 'in', 0x4, 0x4040, 0, 0x04040404 ), resp( 'in', 0x4, 0,   0,  0    ),
    req( 'in', 0x5, 0x5050, 0, 0x05050505 ), resp( 'in', 0x5, 0,   0,  0    ),
    req( 'in', 0x6, 0x6060, 0, 0x06060606 ), resp( 'in', 0x6, 0,   0,  0    ),
    req( 'in', 0x7, 0x7070, 0, 0x07070707 ), resp( 'in', 0x7, 0,   0,  0    ),
    req( 'in', 0x8, 0x8080, 0, 0x08080808 ), resp( 'in', 0x8, 0,   0,  0    ),
    req( 'in', 0x9, 0x9090, 0, 0x09090909 ), resp( 'in', 0x9, 0,   0,  0    ),
    req( 'in', 0xa, 0xa0a0, 0, 0x0a0a0a0a ), resp( 'in', 0xa, 0,   0,  0    ),
    req( 'in', 0xb, 0xb0b0, 0, 0x0b0b0b0b ), resp( 'in', 0xb, 0,   0,  0    ),
    req( 'in', 0xc, 0xc0c0, 0, 0x0c0c0c0c ), resp( 'in', 0xc, 0,   0,  0    ),
    req( 'in', 0xd, 0xd0d0, 0, 0x0d0d0d0d ), resp( 'in', 0xd, 0,   0,  0    ),
    req( 'in', 0xe, 0xe0e0, 0, 0x0e0e0e0e ), resp( 'in', 0xe, 0,   0,  0    ),
    req( 'in', 0xf, 0xf0f0, 0, 0x0f0f0f0f ), resp( 'in', 0xf, 0,   0,  0    ),
  ]

#----------------------------------------------------------------------
# Test Cases for Read Hits
#----------------------------------------------------------------------

# Single read hit

def read_hit_word():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x1000, 0, 0xdeadbeef ), resp( 'in', 0x0, 0,   0,  0          ),
    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0xdeadbeef ),
  ]

# Read same word multiple times, also tests opaque bits

def read_hit_multi_word():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x1000, 0, 0xdeadbeef ), resp( 'in', 0x0, 0,   0,  0    ),

    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0xdeadbeef ),
    req( 'rd', 0x1, 0x1000, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0xdeadbeef ),
    req( 'rd', 0x2, 0x1000, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0xdeadbeef ),
    req( 'rd', 0x3, 0x1000, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0xdeadbeef ),
  ]

# Read every word in cache line

def read_hit_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x1000, 0, 0x01010101 ), resp( 'in', 0x0, 0,   0,  0    ),
    req( 'in', 0x1, 0x1004, 0, 0x02020202 ), resp( 'in', 0x1, 0,   0,  0    ),
    req( 'in', 0x2, 0x1008, 0, 0x03030303 ), resp( 'in', 0x2, 0,   0,  0    ),
    req( 'in', 0x3, 0x100c, 0, 0x04040404 ), resp( 'in', 0x3, 0,   0,  0    ),

    req( 'rd', 0x4, 0x1000, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0x01010101 ),
    req( 'rd', 0x5, 0x1004, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0x02020202 ),
    req( 'rd', 0x6, 0x1008, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0x03030303 ),
    req( 'rd', 0x7, 0x100c, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0x04040404 ),
  ]

# Read one word from each cacheline

def read_hit_multi_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x0000, 0, 0x00000000 ), resp( 'in', 0x0, 0,   0,  0          ),
    req( 'in', 0x1, 0x1010, 0, 0x01010101 ), resp( 'in', 0x1, 0,   0,  0          ),
    req( 'in', 0x2, 0x2020, 0, 0x02020202 ), resp( 'in', 0x2, 0,   0,  0          ),
    req( 'in', 0x3, 0x3030, 0, 0x03030303 ), resp( 'in', 0x3, 0,   0,  0          ),
    req( 'in', 0x4, 0x4040, 0, 0x04040404 ), resp( 'in', 0x4, 0,   0,  0          ),
    req( 'in', 0x5, 0x5050, 0, 0x05050505 ), resp( 'in', 0x5, 0,   0,  0          ),
    req( 'in', 0x6, 0x6060, 0, 0x06060606 ), resp( 'in', 0x6, 0,   0,  0          ),
    req( 'in', 0x7, 0x7070, 0, 0x07070707 ), resp( 'in', 0x7, 0,   0,  0          ),

    req( 'rd', 0x0, 0x0000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0x00000000 ),
    req( 'rd', 0x1, 0x1010, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0x01010101 ),
    req( 'rd', 0x2, 0x2020, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x02020202 ),
    req( 'rd', 0x3, 0x3030, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0x03030303 ),
    req( 'rd', 0x4, 0x4040, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0x04040404 ),
    req( 'rd', 0x5, 0x5050, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0x05050505 ),
    req( 'rd', 0x6, 0x6060, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0x06060606 ),
    req( 'rd', 0x7, 0x7070, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0x07070707 ),
  ]

def read_hit_all_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x0000, 0, 0x00000000 ), resp( 'in', 0x0, 0,   0,  0          ),
    req( 'in', 0x1, 0x1010, 0, 0x01010101 ), resp( 'in', 0x1, 0,   0,  0          ),
    req( 'in', 0x2, 0x2020, 0, 0x02020202 ), resp( 'in', 0x2, 0,   0,  0          ),
    req( 'in', 0x3, 0x3030, 0, 0x03030303 ), resp( 'in', 0x3, 0,   0,  0          ),
    req( 'in', 0x4, 0x4040, 0, 0x04040404 ), resp( 'in', 0x4, 0,   0,  0          ),
    req( 'in', 0x5, 0x5050, 0, 0x05050505 ), resp( 'in', 0x5, 0,   0,  0          ),
    req( 'in', 0x6, 0x6060, 0, 0x06060606 ), resp( 'in', 0x6, 0,   0,  0          ),
    req( 'in', 0x7, 0x7070, 0, 0x07070707 ), resp( 'in', 0x7, 0,   0,  0          ),
    req( 'in', 0x8, 0x8080, 0, 0x08080808 ), resp( 'in', 0x8, 0,   0,  0          ),
    req( 'in', 0x9, 0x9090, 0, 0x09090909 ), resp( 'in', 0x9, 0,   0,  0          ),
    req( 'in', 0xa, 0xa0a0, 0, 0x0a0a0a0a ), resp( 'in', 0xa, 0,   0,  0          ),
    req( 'in', 0xb, 0xb0b0, 0, 0x0b0b0b0b ), resp( 'in', 0xb, 0,   0,  0          ),
    req( 'in', 0xc, 0xc0c0, 0, 0x0c0c0c0c ), resp( 'in', 0xc, 0,   0,  0          ),
    req( 'in', 0xd, 0xd0d0, 0, 0x0d0d0d0d ), resp( 'in', 0xd, 0,   0,  0          ),
    req( 'in', 0xe, 0xe0e0, 0, 0x0e0e0e0e ), resp( 'in', 0xe, 0,   0,  0          ),
    req( 'in', 0xf, 0xf0f0, 0, 0x0f0f0f0f ), resp( 'in', 0xf, 0,   0,  0          ),

    req( 'rd', 0x0, 0x0000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0x00000000 ),
    req( 'rd', 0x1, 0x1010, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0x01010101 ),
    req( 'rd', 0x2, 0x2020, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x02020202 ),
    req( 'rd', 0x3, 0x3030, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0x03030303 ),
    req( 'rd', 0x4, 0x4040, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0x04040404 ),
    req( 'rd', 0x5, 0x5050, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0x05050505 ),
    req( 'rd', 0x6, 0x6060, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0x06060606 ),
    req( 'rd', 0x7, 0x7070, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0x07070707 ),
    req( 'rd', 0x8, 0x8080, 0, 0          ), resp( 'rd', 0x8, 1,   0,  0x08080808 ),
    req( 'rd', 0x9, 0x9090, 0, 0          ), resp( 'rd', 0x9, 1,   0,  0x09090909 ),
    req( 'rd', 0xa, 0xa0a0, 0, 0          ), resp( 'rd', 0xa, 1,   0,  0x0a0a0a0a ),
    req( 'rd', 0xb, 0xb0b0, 0, 0          ), resp( 'rd', 0xb, 1,   0,  0x0b0b0b0b ),
    req( 'rd', 0xc, 0xc0c0, 0, 0          ), resp( 'rd', 0xc, 1,   0,  0x0c0c0c0c ),
    req( 'rd', 0xd, 0xd0d0, 0, 0          ), resp( 'rd', 0xd, 1,   0,  0x0d0d0d0d ),
    req( 'rd', 0xe, 0xe0e0, 0, 0          ), resp( 'rd', 0xe, 1,   0,  0x0e0e0e0e ),
    req( 'rd', 0xf, 0xf0f0, 0, 0          ), resp( 'rd', 0xf, 1,   0,  0x0f0f0f0f ),
  ]

#----------------------------------------------------------------------
# Test Cases for Write Hits
#----------------------------------------------------------------------

# Single write hit to one word

def write_hit_word():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x1000, 0, 0xdeadbeef ), resp( 'in', 0x0, 0,   0,  0          ),
    req( 'wr', 0x0, 0x1000, 0, 0xcafecafe ), resp( 'wr', 0x0, 1,   0,  0          ),
    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0xcafecafe ),
  ]

# Write/read word multiple times, also tests opaque bits

def write_hit_multi_word():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x1000, 0, 0xdeadbeef ), resp( 'in', 0x0, 0,   0,  0          ),

    req( 'wr', 0x1, 0x1000, 0, 0x01010101 ), resp( 'wr', 0x1, 1,   0,  0          ),
    req( 'rd', 0x2, 0x1000, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x01010101 ),
    req( 'wr', 0x3, 0x1000, 0, 0x02020202 ), resp( 'wr', 0x3, 1,   0,  0          ),
    req( 'rd', 0x4, 0x1000, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0x02020202 ),
    req( 'wr', 0x5, 0x1000, 0, 0x03030303 ), resp( 'wr', 0x5, 1,   0,  0          ),
    req( 'rd', 0x6, 0x1000, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0x03030303 ),
    req( 'wr', 0x7, 0x1000, 0, 0x04040404 ), resp( 'wr', 0x7, 1,   0,  0          ),
    req( 'rd', 0x8, 0x1000, 0, 0          ), resp( 'rd', 0x8, 1,   0,  0x04040404 ),
  ]

# Write/read every word in cache line

def write_hit_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x1000, 0, 0x01010101 ), resp( 'in', 0x0, 0,   0,  0          ),
    req( 'in', 0x0, 0x1004, 0, 0x02020202 ), resp( 'in', 0x0, 0,   0,  0          ),
    req( 'in', 0x0, 0x1008, 0, 0x03030303 ), resp( 'in', 0x0, 0,   0,  0          ),
    req( 'in', 0x0, 0x100c, 0, 0x04040404 ), resp( 'in', 0x0, 0,   0,  0          ),

    req( 'wr', 0x1, 0x1000, 0, 0x01010101 ), resp( 'wr', 0x1, 1,   0,  0          ),
    req( 'wr', 0x3, 0x1004, 0, 0x02020202 ), resp( 'wr', 0x3, 1,   0,  0          ),
    req( 'wr', 0x5, 0x1008, 0, 0x03030303 ), resp( 'wr', 0x5, 1,   0,  0          ),
    req( 'wr', 0x7, 0x100c, 0, 0x04040404 ), resp( 'wr', 0x7, 1,   0,  0          ),

    req( 'rd', 0x2, 0x1000, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x01010101 ),
    req( 'rd', 0x4, 0x1004, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0x02020202 ),
    req( 'rd', 0x6, 0x1008, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0x03030303 ),
    req( 'rd', 0x8, 0x100c, 0, 0          ), resp( 'rd', 0x8, 1,   0,  0x04040404 ),
  ]

# Write/read one word from each cacheline

def write_hit_multi_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x0000, 0, 0x00000000 ), resp( 'in', 0x0, 0,   0,  0          ),
    req( 'in', 0x1, 0x1010, 0, 0x01010101 ), resp( 'in', 0x1, 0,   0,  0          ),
    req( 'in', 0x2, 0x2020, 0, 0x02020202 ), resp( 'in', 0x2, 0,   0,  0          ),
    req( 'in', 0x3, 0x3030, 0, 0x03030303 ), resp( 'in', 0x3, 0,   0,  0          ),
    req( 'in', 0x4, 0x4040, 0, 0x04040404 ), resp( 'in', 0x4, 0,   0,  0          ),
    req( 'in', 0x5, 0x5050, 0, 0x05050505 ), resp( 'in', 0x5, 0,   0,  0          ),
    req( 'in', 0x6, 0x6060, 0, 0x06060606 ), resp( 'in', 0x6, 0,   0,  0          ),
    req( 'in', 0x7, 0x7070, 0, 0x07070707 ), resp( 'in', 0x7, 0,   0,  0          ),

    req( 'wr', 0x0, 0x0000, 0, 0x10101010 ), resp( 'wr', 0x0, 1,   0,  0          ),
    req( 'wr', 0x1, 0x1010, 0, 0x11111111 ), resp( 'wr', 0x1, 1,   0,  0          ),
    req( 'wr', 0x2, 0x2020, 0, 0x12121212 ), resp( 'wr', 0x2, 1,   0,  0          ),
    req( 'wr', 0x3, 0x3030, 0, 0x13131313 ), resp( 'wr', 0x3, 1,   0,  0          ),
    req( 'wr', 0x4, 0x4040, 0, 0x14141414 ), resp( 'wr', 0x4, 1,   0,  0          ),
    req( 'wr', 0x5, 0x5050, 0, 0x15151515 ), resp( 'wr', 0x5, 1,   0,  0          ),
    req( 'wr', 0x6, 0x6060, 0, 0x16161616 ), resp( 'wr', 0x6, 1,   0,  0          ),
    req( 'wr', 0x7, 0x7070, 0, 0x17171717 ), resp( 'wr', 0x7, 1,   0,  0          ),

    req( 'rd', 0x0, 0x0000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0x10101010 ),
    req( 'rd', 0x1, 0x1010, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0x11111111 ),
    req( 'rd', 0x2, 0x2020, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x12121212 ),
    req( 'rd', 0x3, 0x3030, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0x13131313 ),
    req( 'rd', 0x4, 0x4040, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0x14141414 ),
    req( 'rd', 0x5, 0x5050, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0x15151515 ),
    req( 'rd', 0x6, 0x6060, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0x16161616 ),
    req( 'rd', 0x7, 0x7070, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0x17171717 ),
  ]

def write_hit_all_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x0000, 0, 0x00000000 ), resp( 'in', 0x0, 0,   0,  0          ),
    req( 'in', 0x1, 0x1010, 0, 0x01010101 ), resp( 'in', 0x1, 0,   0,  0          ),
    req( 'in', 0x2, 0x2020, 0, 0x02020202 ), resp( 'in', 0x2, 0,   0,  0          ),
    req( 'in', 0x3, 0x3030, 0, 0x03030303 ), resp( 'in', 0x3, 0,   0,  0          ),
    req( 'in', 0x4, 0x4040, 0, 0x04040404 ), resp( 'in', 0x4, 0,   0,  0          ),
    req( 'in', 0x5, 0x5050, 0, 0x05050505 ), resp( 'in', 0x5, 0,   0,  0          ),
    req( 'in', 0x6, 0x6060, 0, 0x06060606 ), resp( 'in', 0x6, 0,   0,  0          ),
    req( 'in', 0x7, 0x7070, 0, 0x07070707 ), resp( 'in', 0x7, 0,   0,  0          ),
    req( 'in', 0x8, 0x8080, 0, 0x08080808 ), resp( 'in', 0x8, 0,   0,  0          ),
    req( 'in', 0x9, 0x9090, 0, 0x09090909 ), resp( 'in', 0x9, 0,   0,  0          ),
    req( 'in', 0xa, 0xa0a0, 0, 0x0a0a0a0a ), resp( 'in', 0xa, 0,   0,  0          ),
    req( 'in', 0xb, 0xb0b0, 0, 0x0b0b0b0b ), resp( 'in', 0xb, 0,   0,  0          ),
    req( 'in', 0xc, 0xc0c0, 0, 0x0c0c0c0c ), resp( 'in', 0xc, 0,   0,  0          ),
    req( 'in', 0xd, 0xd0d0, 0, 0x0d0d0d0d ), resp( 'in', 0xd, 0,   0,  0          ),
    req( 'in', 0xe, 0xe0e0, 0, 0x0e0e0e0e ), resp( 'in', 0xe, 0,   0,  0          ),
    req( 'in', 0xf, 0xf0f0, 0, 0x0f0f0f0f ), resp( 'in', 0xf, 0,   0,  0          ),

    req( 'wr', 0x0, 0x0000, 0, 0x10101010 ), resp( 'wr', 0x0, 1,   0,  0          ),
    req( 'wr', 0x1, 0x1010, 0, 0x11111111 ), resp( 'wr', 0x1, 1,   0,  0          ),
    req( 'wr', 0x2, 0x2020, 0, 0x12121212 ), resp( 'wr', 0x2, 1,   0,  0          ),
    req( 'wr', 0x3, 0x3030, 0, 0x13131313 ), resp( 'wr', 0x3, 1,   0,  0          ),
    req( 'wr', 0x4, 0x4040, 0, 0x14141414 ), resp( 'wr', 0x4, 1,   0,  0          ),
    req( 'wr', 0x5, 0x5050, 0, 0x15151515 ), resp( 'wr', 0x5, 1,   0,  0          ),
    req( 'wr', 0x6, 0x6060, 0, 0x16161616 ), resp( 'wr', 0x6, 1,   0,  0          ),
    req( 'wr', 0x7, 0x7070, 0, 0x17171717 ), resp( 'wr', 0x7, 1,   0,  0          ),
    req( 'wr', 0x8, 0x8080, 0, 0x18181818 ), resp( 'wr', 0x8, 1,   0,  0          ),
    req( 'wr', 0x9, 0x9090, 0, 0x19191919 ), resp( 'wr', 0x9, 1,   0,  0          ),
    req( 'wr', 0xa, 0xa0a0, 0, 0x1a1a1a1a ), resp( 'wr', 0xa, 1,   0,  0          ),
    req( 'wr', 0xb, 0xb0b0, 0, 0x1b1b1b1b ), resp( 'wr', 0xb, 1,   0,  0          ),
    req( 'wr', 0xc, 0xc0c0, 0, 0x1c1c1c1c ), resp( 'wr', 0xc, 1,   0,  0          ),
    req( 'wr', 0xd, 0xd0d0, 0, 0x1d1d1d1d ), resp( 'wr', 0xd, 1,   0,  0          ),
    req( 'wr', 0xe, 0xe0e0, 0, 0x1e1e1e1e ), resp( 'wr', 0xe, 1,   0,  0          ),
    req( 'wr', 0xf, 0xf0f0, 0, 0x1f1f1f1f ), resp( 'wr', 0xf, 1,   0,  0          ),


    req( 'rd', 0x0, 0x0000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0x10101010 ),
    req( 'rd', 0x1, 0x1010, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0x11111111 ),
    req( 'rd', 0x2, 0x2020, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x12121212 ),
    req( 'rd', 0x3, 0x3030, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0x13131313 ),
    req( 'rd', 0x4, 0x4040, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0x14141414 ),
    req( 'rd', 0x5, 0x5050, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0x15151515 ),
    req( 'rd', 0x6, 0x6060, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0x16161616 ),
    req( 'rd', 0x7, 0x7070, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0x17171717 ),
    req( 'rd', 0x8, 0x8080, 0, 0          ), resp( 'rd', 0x8, 1,   0,  0x18181818 ),
    req( 'rd', 0x9, 0x9090, 0, 0          ), resp( 'rd', 0x9, 1,   0,  0x19191919 ),
    req( 'rd', 0xa, 0xa0a0, 0, 0          ), resp( 'rd', 0xa, 1,   0,  0x1a1a1a1a ),
    req( 'rd', 0xb, 0xb0b0, 0, 0          ), resp( 'rd', 0xb, 1,   0,  0x1b1b1b1b ),
    req( 'rd', 0xc, 0xc0c0, 0, 0          ), resp( 'rd', 0xc, 1,   0,  0x1c1c1c1c ),
    req( 'rd', 0xd, 0xd0d0, 0, 0          ), resp( 'rd', 0xd, 1,   0,  0x1d1d1d1d ),
    req( 'rd', 0xe, 0xe0e0, 0, 0          ), resp( 'rd', 0xe, 1,   0,  0x1e1e1e1e ),
    req( 'rd', 0xf, 0xf0f0, 0, 0          ), resp( 'rd', 0xf, 1,   0,  0x1f1f1f1f ),
  ]

#----------------------------------------------------------------------
# Test Cases for Write Hits on Dirty Lines
#----------------------------------------------------------------------

# Single write hit to one word

def write_hit_word_dirty():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x1000, 0, 0xdeadbeef ), resp( 'in', 0x0, 0,   0,  0          ),
    req( 'wr', 0x0, 0x1000, 0, 0xcafecafe ), resp( 'wr', 0x0, 1,   0,  0          ),
    req( 'wr', 0x0, 0x1000, 0, 0xfecafeca ), resp( 'wr', 0x0, 1,   0,  0          ),
    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0xfecafeca ),
  ]

# Write/read word multiple times, also tests opaque bits

def write_hit_multi_word_dirty():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x1000, 0, 0xdeadbeef ), resp( 'in', 0x0, 0,   0,  0          ),

    req( 'wr', 0x1, 0x1000, 0, 0x01010101 ), resp( 'wr', 0x1, 1,   0,  0          ),
    req( 'wr', 0x1, 0x1000, 0, 0x10101010 ), resp( 'wr', 0x1, 1,   0,  0          ),
    req( 'rd', 0x2, 0x1000, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x10101010 ),
    req( 'wr', 0x3, 0x1000, 0, 0x02020202 ), resp( 'wr', 0x3, 1,   0,  0          ),
    req( 'wr', 0x3, 0x1000, 0, 0x20202020 ), resp( 'wr', 0x3, 1,   0,  0          ),
    req( 'rd', 0x4, 0x1000, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0x20202020 ),
    req( 'wr', 0x5, 0x1000, 0, 0x03030303 ), resp( 'wr', 0x5, 1,   0,  0          ),
    req( 'wr', 0x5, 0x1000, 0, 0x30303030 ), resp( 'wr', 0x5, 1,   0,  0          ),
    req( 'rd', 0x6, 0x1000, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0x30303030 ),
    req( 'wr', 0x7, 0x1000, 0, 0x04040404 ), resp( 'wr', 0x7, 1,   0,  0          ),
    req( 'wr', 0x7, 0x1000, 0, 0x40404040 ), resp( 'wr', 0x7, 1,   0,  0          ),
    req( 'rd', 0x8, 0x1000, 0, 0          ), resp( 'rd', 0x8, 1,   0,  0x40404040 ),
  ]

# Write/read every word in cache line

def write_hit_cacheline_dirty():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x1000, 0, 0x01010101 ), resp( 'in', 0x0, 0,   0,  0          ),
    req( 'in', 0x0, 0x1004, 0, 0x02020202 ), resp( 'in', 0x0, 0,   0,  0          ),
    req( 'in', 0x0, 0x1008, 0, 0x03030303 ), resp( 'in', 0x0, 0,   0,  0          ),
    req( 'in', 0x0, 0x100c, 0, 0x04040404 ), resp( 'in', 0x0, 0,   0,  0          ),

    req( 'wr', 0x1, 0x1000, 0, 0x01010101 ), resp( 'wr', 0x1, 1,   0,  0          ),
    req( 'wr', 0x3, 0x1004, 0, 0x02020202 ), resp( 'wr', 0x3, 1,   0,  0          ),
    req( 'wr', 0x5, 0x1008, 0, 0x03030303 ), resp( 'wr', 0x5, 1,   0,  0          ),
    req( 'wr', 0x7, 0x100c, 0, 0x04040404 ), resp( 'wr', 0x7, 1,   0,  0          ),

    req( 'wr', 0x1, 0x1000, 0, 0x10101010 ), resp( 'wr', 0x1, 1,   0,  0          ),
    req( 'wr', 0x3, 0x1004, 0, 0x20202020 ), resp( 'wr', 0x3, 1,   0,  0          ),
    req( 'wr', 0x5, 0x1008, 0, 0x30303030 ), resp( 'wr', 0x5, 1,   0,  0          ),
    req( 'wr', 0x7, 0x100c, 0, 0x40404040 ), resp( 'wr', 0x7, 1,   0,  0          ),

    req( 'rd', 0x2, 0x1000, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x10101010 ),
    req( 'rd', 0x4, 0x1004, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0x20202020 ),
    req( 'rd', 0x6, 0x1008, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0x30303030 ),
    req( 'rd', 0x8, 0x100c, 0, 0          ), resp( 'rd', 0x8, 1,   0,  0x40404040 ),
  ]

# Write/read one word from each cacheline

def write_hit_multi_cacheline_dirty():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x0000, 0, 0x00000000 ), resp( 'in', 0x0, 0,   0,  0          ),
    req( 'in', 0x1, 0x1010, 0, 0x01010101 ), resp( 'in', 0x1, 0,   0,  0          ),
    req( 'in', 0x2, 0x2020, 0, 0x02020202 ), resp( 'in', 0x2, 0,   0,  0          ),
    req( 'in', 0x3, 0x3030, 0, 0x03030303 ), resp( 'in', 0x3, 0,   0,  0          ),
    req( 'in', 0x4, 0x4040, 0, 0x04040404 ), resp( 'in', 0x4, 0,   0,  0          ),
    req( 'in', 0x5, 0x5050, 0, 0x05050505 ), resp( 'in', 0x5, 0,   0,  0          ),
    req( 'in', 0x6, 0x6060, 0, 0x06060606 ), resp( 'in', 0x6, 0,   0,  0          ),
    req( 'in', 0x7, 0x7070, 0, 0x07070707 ), resp( 'in', 0x7, 0,   0,  0          ),

    req( 'wr', 0x0, 0x0000, 0, 0x10101010 ), resp( 'wr', 0x0, 1,   0,  0          ),
    req( 'wr', 0x1, 0x1010, 0, 0x11111111 ), resp( 'wr', 0x1, 1,   0,  0          ),
    req( 'wr', 0x2, 0x2020, 0, 0x12121212 ), resp( 'wr', 0x2, 1,   0,  0          ),
    req( 'wr', 0x3, 0x3030, 0, 0x13131313 ), resp( 'wr', 0x3, 1,   0,  0          ),
    req( 'wr', 0x4, 0x4040, 0, 0x14141414 ), resp( 'wr', 0x4, 1,   0,  0          ),
    req( 'wr', 0x5, 0x5050, 0, 0x15151515 ), resp( 'wr', 0x5, 1,   0,  0          ),
    req( 'wr', 0x6, 0x6060, 0, 0x16161616 ), resp( 'wr', 0x6, 1,   0,  0          ),
    req( 'wr', 0x7, 0x7070, 0, 0x17171717 ), resp( 'wr', 0x7, 1,   0,  0          ),

    req( 'wr', 0x0, 0x0000, 0, 0x01010101 ), resp( 'wr', 0x0, 1,   0,  0          ),
    req( 'wr', 0x1, 0x1010, 0, 0x11111111 ), resp( 'wr', 0x1, 1,   0,  0          ),
    req( 'wr', 0x2, 0x2020, 0, 0x21212121 ), resp( 'wr', 0x2, 1,   0,  0          ),
    req( 'wr', 0x3, 0x3030, 0, 0x31313131 ), resp( 'wr', 0x3, 1,   0,  0          ),
    req( 'wr', 0x4, 0x4040, 0, 0x41414141 ), resp( 'wr', 0x4, 1,   0,  0          ),
    req( 'wr', 0x5, 0x5050, 0, 0x51515151 ), resp( 'wr', 0x5, 1,   0,  0          ),
    req( 'wr', 0x6, 0x6060, 0, 0x61616161 ), resp( 'wr', 0x6, 1,   0,  0          ),
    req( 'wr', 0x7, 0x7070, 0, 0x71717171 ), resp( 'wr', 0x7, 1,   0,  0          ),

    req( 'rd', 0x0, 0x0000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0x01010101 ),
    req( 'rd', 0x1, 0x1010, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0x11111111 ),
    req( 'rd', 0x2, 0x2020, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x21212121 ),
    req( 'rd', 0x3, 0x3030, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0x31313131 ),
    req( 'rd', 0x4, 0x4040, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0x41414141 ),
    req( 'rd', 0x5, 0x5050, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0x51515151 ),
    req( 'rd', 0x6, 0x6060, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0x61616161 ),
    req( 'rd', 0x7, 0x7070, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0x71717171 ),
  ]

def write_hit_all_cacheline_dirty():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x0000, 0, 0x00000000 ), resp( 'in', 0x0, 0,   0,  0          ),
    req( 'in', 0x1, 0x1010, 0, 0x01010101 ), resp( 'in', 0x1, 0,   0,  0          ),
    req( 'in', 0x2, 0x2020, 0, 0x02020202 ), resp( 'in', 0x2, 0,   0,  0          ),
    req( 'in', 0x3, 0x3030, 0, 0x03030303 ), resp( 'in', 0x3, 0,   0,  0          ),
    req( 'in', 0x4, 0x4040, 0, 0x04040404 ), resp( 'in', 0x4, 0,   0,  0          ),
    req( 'in', 0x5, 0x5050, 0, 0x05050505 ), resp( 'in', 0x5, 0,   0,  0          ),
    req( 'in', 0x6, 0x6060, 0, 0x06060606 ), resp( 'in', 0x6, 0,   0,  0          ),
    req( 'in', 0x7, 0x7070, 0, 0x07070707 ), resp( 'in', 0x7, 0,   0,  0          ),
    req( 'in', 0x8, 0x8080, 0, 0x08080808 ), resp( 'in', 0x8, 0,   0,  0          ),
    req( 'in', 0x9, 0x9090, 0, 0x09090909 ), resp( 'in', 0x9, 0,   0,  0          ),
    req( 'in', 0xa, 0xa0a0, 0, 0x0a0a0a0a ), resp( 'in', 0xa, 0,   0,  0          ),
    req( 'in', 0xb, 0xb0b0, 0, 0x0b0b0b0b ), resp( 'in', 0xb, 0,   0,  0          ),
    req( 'in', 0xc, 0xc0c0, 0, 0x0c0c0c0c ), resp( 'in', 0xc, 0,   0,  0          ),
    req( 'in', 0xd, 0xd0d0, 0, 0x0d0d0d0d ), resp( 'in', 0xd, 0,   0,  0          ),
    req( 'in', 0xe, 0xe0e0, 0, 0x0e0e0e0e ), resp( 'in', 0xe, 0,   0,  0          ),
    req( 'in', 0xf, 0xf0f0, 0, 0x0f0f0f0f ), resp( 'in', 0xf, 0,   0,  0          ),

    req( 'wr', 0x0, 0x0000, 0, 0x10101010 ), resp( 'wr', 0x0, 1,   0,  0          ),
    req( 'wr', 0x1, 0x1010, 0, 0x11111111 ), resp( 'wr', 0x1, 1,   0,  0          ),
    req( 'wr', 0x2, 0x2020, 0, 0x12121212 ), resp( 'wr', 0x2, 1,   0,  0          ),
    req( 'wr', 0x3, 0x3030, 0, 0x13131313 ), resp( 'wr', 0x3, 1,   0,  0          ),
    req( 'wr', 0x4, 0x4040, 0, 0x14141414 ), resp( 'wr', 0x4, 1,   0,  0          ),
    req( 'wr', 0x5, 0x5050, 0, 0x15151515 ), resp( 'wr', 0x5, 1,   0,  0          ),
    req( 'wr', 0x6, 0x6060, 0, 0x16161616 ), resp( 'wr', 0x6, 1,   0,  0          ),
    req( 'wr', 0x7, 0x7070, 0, 0x17171717 ), resp( 'wr', 0x7, 1,   0,  0          ),
    req( 'wr', 0x8, 0x8080, 0, 0x18181818 ), resp( 'wr', 0x8, 1,   0,  0          ),
    req( 'wr', 0x9, 0x9090, 0, 0x19191919 ), resp( 'wr', 0x9, 1,   0,  0          ),
    req( 'wr', 0xa, 0xa0a0, 0, 0x1a1a1a1a ), resp( 'wr', 0xa, 1,   0,  0          ),
    req( 'wr', 0xb, 0xb0b0, 0, 0x1b1b1b1b ), resp( 'wr', 0xb, 1,   0,  0          ),
    req( 'wr', 0xc, 0xc0c0, 0, 0x1c1c1c1c ), resp( 'wr', 0xc, 1,   0,  0          ),
    req( 'wr', 0xd, 0xd0d0, 0, 0x1d1d1d1d ), resp( 'wr', 0xd, 1,   0,  0          ),
    req( 'wr', 0xe, 0xe0e0, 0, 0x1e1e1e1e ), resp( 'wr', 0xe, 1,   0,  0          ),
    req( 'wr', 0xf, 0xf0f0, 0, 0x1f1f1f1f ), resp( 'wr', 0xf, 1,   0,  0          ),

    req( 'wr', 0x0, 0x0000, 0, 0x01010101 ), resp( 'wr', 0x0, 1,   0,  0          ),
    req( 'wr', 0x1, 0x1010, 0, 0x11111111 ), resp( 'wr', 0x1, 1,   0,  0          ),
    req( 'wr', 0x2, 0x2020, 0, 0x21212121 ), resp( 'wr', 0x2, 1,   0,  0          ),
    req( 'wr', 0x3, 0x3030, 0, 0x31313131 ), resp( 'wr', 0x3, 1,   0,  0          ),
    req( 'wr', 0x4, 0x4040, 0, 0x41414141 ), resp( 'wr', 0x4, 1,   0,  0          ),
    req( 'wr', 0x5, 0x5050, 0, 0x51515151 ), resp( 'wr', 0x5, 1,   0,  0          ),
    req( 'wr', 0x6, 0x6060, 0, 0x61616161 ), resp( 'wr', 0x6, 1,   0,  0          ),
    req( 'wr', 0x7, 0x7070, 0, 0x71717171 ), resp( 'wr', 0x7, 1,   0,  0          ),
    req( 'wr', 0x8, 0x8080, 0, 0x81818181 ), resp( 'wr', 0x8, 1,   0,  0          ),
    req( 'wr', 0x9, 0x9090, 0, 0x91919191 ), resp( 'wr', 0x9, 1,   0,  0          ),
    req( 'wr', 0xa, 0xa0a0, 0, 0xa1a1a1a1 ), resp( 'wr', 0xa, 1,   0,  0          ),
    req( 'wr', 0xb, 0xb0b0, 0, 0xb1b1b1b1 ), resp( 'wr', 0xb, 1,   0,  0          ),
    req( 'wr', 0xc, 0xc0c0, 0, 0xc1c1c1c1 ), resp( 'wr', 0xc, 1,   0,  0          ),
    req( 'wr', 0xd, 0xd0d0, 0, 0xd1d1d1d1 ), resp( 'wr', 0xd, 1,   0,  0          ),
    req( 'wr', 0xe, 0xe0e0, 0, 0xe1e1e1e1 ), resp( 'wr', 0xe, 1,   0,  0          ),
    req( 'wr', 0xf, 0xf0f0, 0, 0xf1f1f1f1 ), resp( 'wr', 0xf, 1,   0,  0          ),

    req( 'rd', 0x0, 0x0000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0x01010101 ),
    req( 'rd', 0x1, 0x1010, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0x11111111 ),
    req( 'rd', 0x2, 0x2020, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x21212121 ),
    req( 'rd', 0x3, 0x3030, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0x31313131 ),
    req( 'rd', 0x4, 0x4040, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0x41414141 ),
    req( 'rd', 0x5, 0x5050, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0x51515151 ),
    req( 'rd', 0x6, 0x6060, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0x61616161 ),
    req( 'rd', 0x7, 0x7070, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0x71717171 ),
    req( 'rd', 0x8, 0x8080, 0, 0          ), resp( 'rd', 0x8, 1,   0,  0x81818181 ),
    req( 'rd', 0x9, 0x9090, 0, 0          ), resp( 'rd', 0x9, 1,   0,  0x91919191 ),
    req( 'rd', 0xa, 0xa0a0, 0, 0          ), resp( 'rd', 0xa, 1,   0,  0xa1a1a1a1 ),
    req( 'rd', 0xb, 0xb0b0, 0, 0          ), resp( 'rd', 0xb, 1,   0,  0xb1b1b1b1 ),
    req( 'rd', 0xc, 0xc0c0, 0, 0          ), resp( 'rd', 0xc, 1,   0,  0xc1c1c1c1 ),
    req( 'rd', 0xd, 0xd0d0, 0, 0          ), resp( 'rd', 0xd, 1,   0,  0xd1d1d1d1 ),
    req( 'rd', 0xe, 0xe0e0, 0, 0          ), resp( 'rd', 0xe, 1,   0,  0xe1e1e1e1 ),
    req( 'rd', 0xf, 0xf0f0, 0, 0          ), resp( 'rd', 0xf, 1,   0,  0xf1f1f1f1 ),
  ]

#----------------------------------------------------------------------
# Test Cases for Refill on Read Miss (No eviction)
#----------------------------------------------------------------------

# Single read miss (uses data_64B)

def read_miss_word():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 0,   0,  0x000c0ffe ),
  ]

# Read same word multiple times, also tests opaque bits (uses data_64B)

def read_miss_multi_word():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 0,   0,  0x000c0ffe ),
    req( 'rd', 0x1, 0x1000, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0x000c0ffe ),
    req( 'rd', 0x2, 0x1000, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x000c0ffe ),
    req( 'rd', 0x3, 0x1000, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0x000c0ffe ),
  ]

# Read every word in cache line (uses data_64B)

def read_miss_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'rd', 0x1, 0x1000, 0, 0          ), resp( 'rd', 0x1, 0,   0,  0x000c0ffe ),
    req( 'rd', 0x2, 0x1004, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x10101010 ),
    req( 'rd', 0x3, 0x1008, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0x20202020 ),
    req( 'rd', 0x4, 0x100c, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0x30303030 ),
  ]

# Read miss for each cacheline, then read hit for each cacheline (uses data_512B)

def read_miss_multi_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 0,   0,  0xabcd1000 ),
    req( 'rd', 0x1, 0x1010, 0, 0          ), resp( 'rd', 0x1, 0,   0,  0xabcd1010 ),
    req( 'rd', 0x2, 0x1020, 0, 0          ), resp( 'rd', 0x2, 0,   0,  0xabcd1020 ),
    req( 'rd', 0x3, 0x1030, 0, 0          ), resp( 'rd', 0x3, 0,   0,  0xabcd1030 ),
    req( 'rd', 0x4, 0x1040, 0, 0          ), resp( 'rd', 0x4, 0,   0,  0xabcd1040 ),
    req( 'rd', 0x5, 0x1050, 0, 0          ), resp( 'rd', 0x5, 0,   0,  0xabcd1050 ),
    req( 'rd', 0x6, 0x1060, 0, 0          ), resp( 'rd', 0x6, 0,   0,  0xabcd1060 ),
    req( 'rd', 0x7, 0x1070, 0, 0          ), resp( 'rd', 0x7, 0,   0,  0xabcd1070 ),
    req( 'rd', 0x8, 0x1080, 0, 0          ), resp( 'rd', 0x8, 0,   0,  0xabcd1080 ),
    req( 'rd', 0x9, 0x1090, 0, 0          ), resp( 'rd', 0x9, 0,   0,  0xabcd1090 ),
    req( 'rd', 0xa, 0x10a0, 0, 0          ), resp( 'rd', 0xa, 0,   0,  0xabcd10a0 ),
    req( 'rd', 0xb, 0x10b0, 0, 0          ), resp( 'rd', 0xb, 0,   0,  0xabcd10b0 ),
    req( 'rd', 0xc, 0x10c0, 0, 0          ), resp( 'rd', 0xc, 0,   0,  0xabcd10c0 ),
    req( 'rd', 0xd, 0x10d0, 0, 0          ), resp( 'rd', 0xd, 0,   0,  0xabcd10d0 ),
    req( 'rd', 0xe, 0x10e0, 0, 0          ), resp( 'rd', 0xe, 0,   0,  0xabcd10e0 ),
    req( 'rd', 0xf, 0x10f0, 0, 0          ), resp( 'rd', 0xf, 0,   0,  0xabcd10f0 ),

    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0xabcd1000 ),
    req( 'rd', 0x1, 0x1010, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0xabcd1010 ),
    req( 'rd', 0x2, 0x1020, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0xabcd1020 ),
    req( 'rd', 0x3, 0x1030, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0xabcd1030 ),
    req( 'rd', 0x4, 0x1040, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0xabcd1040 ),
    req( 'rd', 0x5, 0x1050, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0xabcd1050 ),
    req( 'rd', 0x6, 0x1060, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0xabcd1060 ),
    req( 'rd', 0x7, 0x1070, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0xabcd1070 ),
    req( 'rd', 0x8, 0x1080, 0, 0          ), resp( 'rd', 0x8, 1,   0,  0xabcd1080 ),
    req( 'rd', 0x9, 0x1090, 0, 0          ), resp( 'rd', 0x9, 1,   0,  0xabcd1090 ),
    req( 'rd', 0xa, 0x10a0, 0, 0          ), resp( 'rd', 0xa, 1,   0,  0xabcd10a0 ),
    req( 'rd', 0xb, 0x10b0, 0, 0          ), resp( 'rd', 0xb, 1,   0,  0xabcd10b0 ),
    req( 'rd', 0xc, 0x10c0, 0, 0          ), resp( 'rd', 0xc, 1,   0,  0xabcd10c0 ),
    req( 'rd', 0xd, 0x10d0, 0, 0          ), resp( 'rd', 0xd, 1,   0,  0xabcd10d0 ),
    req( 'rd', 0xe, 0x10e0, 0, 0          ), resp( 'rd', 0xe, 1,   0,  0xabcd10e0 ),
    req( 'rd', 0xf, 0x10f0, 0, 0          ), resp( 'rd', 0xf, 1,   0,  0xabcd10f0 ),

    req( 'rd', 0x0, 0x1004, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0xabcd1004 ),
    req( 'rd', 0x1, 0x1014, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0xabcd1014 ),
    req( 'rd', 0x2, 0x1024, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0xabcd1024 ),
    req( 'rd', 0x3, 0x1034, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0xabcd1034 ),
    req( 'rd', 0x4, 0x1044, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0xabcd1044 ),
    req( 'rd', 0x5, 0x1054, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0xabcd1054 ),
    req( 'rd', 0x6, 0x1064, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0xabcd1064 ),
    req( 'rd', 0x7, 0x1074, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0xabcd1074 ),
    req( 'rd', 0x8, 0x1084, 0, 0          ), resp( 'rd', 0x8, 1,   0,  0xabcd1084 ),
    req( 'rd', 0x9, 0x1094, 0, 0          ), resp( 'rd', 0x9, 1,   0,  0xabcd1094 ),
    req( 'rd', 0xa, 0x10a4, 0, 0          ), resp( 'rd', 0xa, 1,   0,  0xabcd10a4 ),
    req( 'rd', 0xb, 0x10b4, 0, 0          ), resp( 'rd', 0xb, 1,   0,  0xabcd10b4 ),
    req( 'rd', 0xc, 0x10c4, 0, 0          ), resp( 'rd', 0xc, 1,   0,  0xabcd10c4 ),
    req( 'rd', 0xd, 0x10d4, 0, 0          ), resp( 'rd', 0xd, 1,   0,  0xabcd10d4 ),
    req( 'rd', 0xe, 0x10e4, 0, 0          ), resp( 'rd', 0xe, 1,   0,  0xabcd10e4 ),
    req( 'rd', 0xf, 0x10f4, 0, 0          ), resp( 'rd', 0xf, 1,   0,  0xabcd10f4 ),
  ]

#----------------------------------------------------------------------
# Test Cases for Refill on Write Miss
#----------------------------------------------------------------------

# Single write miss to one word (uses data_64B)

def write_miss_word():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'wr', 0x0, 0x1000, 0, 0xcafecafe ), resp( 'wr', 0x0, 0,   0,  0          ),
    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0xcafecafe ),
  ]

# Write/read word multiple times, also tests opaque bits (uses data_64B)

def write_miss_multi_word():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'wr', 0x1, 0x1000, 0, 0x01010101 ), resp( 'wr', 0x1, 0,   0,  0          ),
    req( 'rd', 0x2, 0x1000, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x01010101 ),
    req( 'wr', 0x3, 0x1000, 0, 0x02020202 ), resp( 'wr', 0x3, 1,   0,  0          ),
    req( 'rd', 0x4, 0x1000, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0x02020202 ),
    req( 'wr', 0x5, 0x1000, 0, 0x03030303 ), resp( 'wr', 0x5, 1,   0,  0          ),
    req( 'rd', 0x6, 0x1000, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0x03030303 ),
    req( 'wr', 0x7, 0x1000, 0, 0x04040404 ), resp( 'wr', 0x7, 1,   0,  0          ),
    req( 'rd', 0x8, 0x1000, 0, 0          ), resp( 'rd', 0x8, 1,   0,  0x04040404 ),
  ]

# Write/read every word in cache line (uses data_64B)

def write_miss_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'wr', 0x1, 0x1000, 0, 0x01010101 ), resp( 'wr', 0x1, 0,   0,  0          ),
    req( 'wr', 0x2, 0x1004, 0, 0x02020202 ), resp( 'wr', 0x2, 1,   0,  0          ),
    req( 'wr', 0x3, 0x1008, 0, 0x03030303 ), resp( 'wr', 0x3, 1,   0,  0          ),
    req( 'wr', 0x4, 0x100c, 0, 0x04040404 ), resp( 'wr', 0x4, 1,   0,  0          ),

    req( 'rd', 0x5, 0x1000, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0x01010101 ),
    req( 'rd', 0x6, 0x1004, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0x02020202 ),
    req( 'rd', 0x7, 0x1008, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0x03030303 ),
    req( 'rd', 0x8, 0x100c, 0, 0          ), resp( 'rd', 0x8, 1,   0,  0x04040404 ),
  ]

# Write/read one word from each cacheline (uses data_512B)

def write_miss_multi_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'wr', 0x0, 0x1000, 0, 0x10101010 ), resp( 'wr', 0x0, 0,   0,  0          ),
    req( 'wr', 0x1, 0x1010, 0, 0x11111111 ), resp( 'wr', 0x1, 0,   0,  0          ),
    req( 'wr', 0x2, 0x1020, 0, 0x12121212 ), resp( 'wr', 0x2, 0,   0,  0          ),
    req( 'wr', 0x3, 0x1030, 0, 0x13131313 ), resp( 'wr', 0x3, 0,   0,  0          ),
    req( 'wr', 0x4, 0x1040, 0, 0x14141414 ), resp( 'wr', 0x4, 0,   0,  0          ),
    req( 'wr', 0x5, 0x1050, 0, 0x15151515 ), resp( 'wr', 0x5, 0,   0,  0          ),
    req( 'wr', 0x6, 0x1060, 0, 0x16161616 ), resp( 'wr', 0x6, 0,   0,  0          ),
    req( 'wr', 0x7, 0x1070, 0, 0x17171717 ), resp( 'wr', 0x7, 0,   0,  0          ),
    req( 'wr', 0x8, 0x1080, 0, 0x18181818 ), resp( 'wr', 0x8, 0,   0,  0          ),
    req( 'wr', 0x9, 0x1090, 0, 0x19191919 ), resp( 'wr', 0x9, 0,   0,  0          ),
    req( 'wr', 0xa, 0x10a0, 0, 0x1a1a1a1a ), resp( 'wr', 0xa, 0,   0,  0          ),
    req( 'wr', 0xb, 0x10b0, 0, 0x1b1b1b1b ), resp( 'wr', 0xb, 0,   0,  0          ),
    req( 'wr', 0xc, 0x10c0, 0, 0x1c1c1c1c ), resp( 'wr', 0xc, 0,   0,  0          ),
    req( 'wr', 0xd, 0x10d0, 0, 0x1d1d1d1d ), resp( 'wr', 0xd, 0,   0,  0          ),
    req( 'wr', 0xe, 0x10e0, 0, 0x1e1e1e1e ), resp( 'wr', 0xe, 0,   0,  0          ),
    req( 'wr', 0xf, 0x10f0, 0, 0x1f1f1f1f ), resp( 'wr', 0xf, 0,   0,  0          ),

    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0x10101010 ),
    req( 'rd', 0x1, 0x1010, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0x11111111 ),
    req( 'rd', 0x2, 0x1020, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x12121212 ),
    req( 'rd', 0x3, 0x1030, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0x13131313 ),
    req( 'rd', 0x4, 0x1040, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0x14141414 ),
    req( 'rd', 0x5, 0x1050, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0x15151515 ),
    req( 'rd', 0x6, 0x1060, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0x16161616 ),
    req( 'rd', 0x7, 0x1070, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0x17171717 ),
    req( 'rd', 0x8, 0x1080, 0, 0          ), resp( 'rd', 0x8, 1,   0,  0x18181818 ),
    req( 'rd', 0x9, 0x1090, 0, 0          ), resp( 'rd', 0x9, 1,   0,  0x19191919 ),
    req( 'rd', 0xa, 0x10a0, 0, 0          ), resp( 'rd', 0xa, 1,   0,  0x1a1a1a1a ),
    req( 'rd', 0xb, 0x10b0, 0, 0          ), resp( 'rd', 0xb, 1,   0,  0x1b1b1b1b ),
    req( 'rd', 0xc, 0x10c0, 0, 0          ), resp( 'rd', 0xc, 1,   0,  0x1c1c1c1c ),
    req( 'rd', 0xd, 0x10d0, 0, 0          ), resp( 'rd', 0xd, 1,   0,  0x1d1d1d1d ),
    req( 'rd', 0xe, 0x10e0, 0, 0          ), resp( 'rd', 0xe, 1,   0,  0x1e1e1e1e ),
    req( 'rd', 0xf, 0x10f0, 0, 0          ), resp( 'rd', 0xf, 1,   0,  0x1f1f1f1f ),
  ]

#----------------------------------------------------------------------
# Test Cases for Evict (Read miss causing refill and eviction)
#----------------------------------------------------------------------

# Write miss to two cachelines, and then a read to a third cacheline.
# This read to the third cacheline is guaranteed to cause an eviction on
# both the direct mapped and set associative caches. (uses data_512B)

def evict_word():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'wr', 0x0, 0x1000, 0, 0xcafecafe ), resp( 'wr', 0x0, 0,   0,  0          ),
    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0xcafecafe ),
    req( 'wr', 0x0, 0x1080, 0, 0x000c0ffe ), resp( 'wr', 0x0, 0,   0,  0          ),
    req( 'rd', 0x0, 0x1080, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0x000c0ffe ),
    req( 'rd', 0x0, 0x1100, 0, 0          ), resp( 'rd', 0x0, 0,   0,  0xabcd1100 ), # conflicts
    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 0,   0,  0xcafecafe ),
  ]

# Write word and evict multiple times. Test is carefully crafted to
# ensure it applies to both direct mapped and set associative caches.
# (uses data_512B)

def evict_multi_word():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'wr', 0x0, 0x1000, 0, 0x01010101 ), resp( 'wr', 0x0, 0,   0,  0          ),
    req( 'rd', 0x1, 0x1000, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0x01010101 ),
    req( 'wr', 0x2, 0x1080, 0, 0x11111111 ), resp( 'wr', 0x2, 0,   0,  0          ),
    req( 'rd', 0x3, 0x1080, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0x11111111 ),
    req( 'rd', 0x4, 0x1100, 0, 0          ), resp( 'rd', 0x4, 0,   0,  0xabcd1100 ), # conflicts
    req( 'rd', 0x5, 0x1080, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0x11111111 ), # make sure way1 is still LRU

    req( 'wr', 0x6, 0x1000, 0, 0x02020202 ), resp( 'wr', 0x6, 0,   0,  0          ),
    req( 'rd', 0x7, 0x1000, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0x02020202 ),
    req( 'wr', 0x8, 0x1080, 0, 0x12121212 ), resp( 'wr', 0x8, 1,   0,  0          ),
    req( 'rd', 0x9, 0x1080, 0, 0          ), resp( 'rd', 0x9, 1,   0,  0x12121212 ),
    req( 'rd', 0xa, 0x1100, 0, 0          ), resp( 'rd', 0xa, 0,   0,  0xabcd1100 ), # conflicts
    req( 'rd', 0xb, 0x1080, 0, 0          ), resp( 'rd', 0xb, 1,   0,  0x12121212 ), # make sure way1 is still LRU

    req( 'wr', 0xc, 0x1000, 0, 0x03030303 ), resp( 'wr', 0xc, 0,   0,  0          ),
    req( 'rd', 0xd, 0x1000, 0, 0          ), resp( 'rd', 0xd, 1,   0,  0x03030303 ),
    req( 'wr', 0xe, 0x1080, 0, 0x13131313 ), resp( 'wr', 0xe, 1,   0,  0          ),
    req( 'rd', 0xf, 0x1080, 0, 0          ), resp( 'rd', 0xf, 1,   0,  0x13131313 ),
    req( 'rd', 0x0, 0x1100, 0, 0          ), resp( 'rd', 0x0, 0,   0,  0xabcd1100 ), # conflicts
    req( 'rd', 0x1, 0x1080, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0x13131313 ), # make sure way1 is still LRU

    req( 'wr', 0x2, 0x1000, 0, 0x04040404 ), resp( 'wr', 0x2, 0,   0,  0          ),
    req( 'rd', 0x3, 0x1000, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0x04040404 ),
    req( 'wr', 0x4, 0x1080, 0, 0x14141414 ), resp( 'wr', 0x4, 1,   0,  0          ),
    req( 'rd', 0x5, 0x1080, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0x14141414 ),
    req( 'rd', 0x6, 0x1100, 0, 0          ), resp( 'rd', 0x6, 0,   0,  0xabcd1100 ), # conflicts
    req( 'rd', 0x7, 0x1080, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0x14141414 ), # make sure way1 is still LRU

    req( 'rd', 0x8, 0x1000, 0, 0          ), resp( 'rd', 0x8, 0,   0,  0x04040404 ),
  ]

# Write every word on two cachelines, and then a read to a third
# cacheline. This read to the third cacheline is guaranteed to cause an
# eviction on both the direct mapped and set associative caches. (uses
# data_512B)

def evict_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'wr', 0x0, 0x1000, 0, 0x01010101 ), resp( 'wr', 0x0, 0,   0,  0          ),
    req( 'wr', 0x1, 0x1004, 0, 0x02020202 ), resp( 'wr', 0x1, 1,   0,  0          ),
    req( 'wr', 0x2, 0x1008, 0, 0x03030303 ), resp( 'wr', 0x2, 1,   0,  0          ),
    req( 'wr', 0x3, 0x100c, 0, 0x04040404 ), resp( 'wr', 0x3, 1,   0,  0          ),

    req( 'wr', 0x4, 0x1080, 0, 0x11111111 ), resp( 'wr', 0x4, 0,   0,  0          ),
    req( 'wr', 0x5, 0x1084, 0, 0x12121212 ), resp( 'wr', 0x5, 1,   0,  0          ),
    req( 'wr', 0x6, 0x1088, 0, 0x13131313 ), resp( 'wr', 0x6, 1,   0,  0          ),
    req( 'wr', 0x7, 0x108c, 0, 0x14141414 ), resp( 'wr', 0x7, 1,   0,  0          ),

    req( 'rd', 0x8, 0x1100, 0, 0          ), resp( 'rd', 0x8, 0,   0,  0xabcd1100 ), # conflicts

    req( 'rd', 0x9, 0x1000, 0, 0          ), resp( 'rd', 0x9, 0,   0,  0x01010101 ),
    req( 'rd', 0xa, 0x1004, 0, 0          ), resp( 'rd', 0xa, 1,   0,  0x02020202 ),
    req( 'rd', 0xb, 0x1008, 0, 0          ), resp( 'rd', 0xb, 1,   0,  0x03030303 ),
    req( 'rd', 0xc, 0x100c, 0, 0          ), resp( 'rd', 0xc, 1,   0,  0x04040404 ),
  ]

# Write one word from each cacheline, then evict (uses data_512B)

def evict_multi_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'wr', 0x0, 0x1000, 0, 0x10101010 ), resp( 'wr', 0x0, 0,   0,  0          ),
    req( 'wr', 0x1, 0x1010, 0, 0x11111111 ), resp( 'wr', 0x1, 0,   0,  0          ),
    req( 'wr', 0x2, 0x1020, 0, 0x12121212 ), resp( 'wr', 0x2, 0,   0,  0          ),
    req( 'wr', 0x3, 0x1030, 0, 0x13131313 ), resp( 'wr', 0x3, 0,   0,  0          ),
    req( 'wr', 0x4, 0x1040, 0, 0x14141414 ), resp( 'wr', 0x4, 0,   0,  0          ),
    req( 'wr', 0x5, 0x1050, 0, 0x15151515 ), resp( 'wr', 0x5, 0,   0,  0          ),
    req( 'wr', 0x6, 0x1060, 0, 0x16161616 ), resp( 'wr', 0x6, 0,   0,  0          ),
    req( 'wr', 0x7, 0x1070, 0, 0x17171717 ), resp( 'wr', 0x7, 0,   0,  0          ),
    req( 'wr', 0x8, 0x1080, 0, 0x18181818 ), resp( 'wr', 0x8, 0,   0,  0          ),
    req( 'wr', 0x9, 0x1090, 0, 0x19191919 ), resp( 'wr', 0x9, 0,   0,  0          ),
    req( 'wr', 0xa, 0x10a0, 0, 0x1a1a1a1a ), resp( 'wr', 0xa, 0,   0,  0          ),
    req( 'wr', 0xb, 0x10b0, 0, 0x1b1b1b1b ), resp( 'wr', 0xb, 0,   0,  0          ),
    req( 'wr', 0xc, 0x10c0, 0, 0x1c1c1c1c ), resp( 'wr', 0xc, 0,   0,  0          ),
    req( 'wr', 0xd, 0x10d0, 0, 0x1d1d1d1d ), resp( 'wr', 0xd, 0,   0,  0          ),
    req( 'wr', 0xe, 0x10e0, 0, 0x1e1e1e1e ), resp( 'wr', 0xe, 0,   0,  0          ),
    req( 'wr', 0xf, 0x10f0, 0, 0x1f1f1f1f ), resp( 'wr', 0xf, 0,   0,  0          ),

    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0x10101010 ),
    req( 'rd', 0x1, 0x1010, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0x11111111 ),
    req( 'rd', 0x2, 0x1020, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x12121212 ),
    req( 'rd', 0x3, 0x1030, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0x13131313 ),
    req( 'rd', 0x4, 0x1040, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0x14141414 ),
    req( 'rd', 0x5, 0x1050, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0x15151515 ),
    req( 'rd', 0x6, 0x1060, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0x16161616 ),
    req( 'rd', 0x7, 0x1070, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0x17171717 ),
    req( 'rd', 0x8, 0x1080, 0, 0          ), resp( 'rd', 0x8, 1,   0,  0x18181818 ),
    req( 'rd', 0x9, 0x1090, 0, 0          ), resp( 'rd', 0x9, 1,   0,  0x19191919 ),
    req( 'rd', 0xa, 0x10a0, 0, 0          ), resp( 'rd', 0xa, 1,   0,  0x1a1a1a1a ),
    req( 'rd', 0xb, 0x10b0, 0, 0          ), resp( 'rd', 0xb, 1,   0,  0x1b1b1b1b ),
    req( 'rd', 0xc, 0x10c0, 0, 0          ), resp( 'rd', 0xc, 1,   0,  0x1c1c1c1c ),
    req( 'rd', 0xd, 0x10d0, 0, 0          ), resp( 'rd', 0xd, 1,   0,  0x1d1d1d1d ),
    req( 'rd', 0xe, 0x10e0, 0, 0          ), resp( 'rd', 0xe, 1,   0,  0x1e1e1e1e ),
    req( 'rd', 0xf, 0x10f0, 0, 0          ), resp( 'rd', 0xf, 1,   0,  0x1f1f1f1f ),

    req( 'rd', 0x0, 0x1100, 0, 0          ), resp( 'rd', 0x0, 0,   0,  0xabcd1100 ), # conflicts
    req( 'rd', 0x1, 0x1110, 0, 0          ), resp( 'rd', 0x1, 0,   0,  0xabcd1110 ), # conflicts
    req( 'rd', 0x2, 0x1120, 0, 0          ), resp( 'rd', 0x2, 0,   0,  0xabcd1120 ), # conflicts
    req( 'rd', 0x3, 0x1130, 0, 0          ), resp( 'rd', 0x3, 0,   0,  0xabcd1130 ), # conflicts
    req( 'rd', 0x4, 0x1140, 0, 0          ), resp( 'rd', 0x4, 0,   0,  0xabcd1140 ), # conflicts
    req( 'rd', 0x5, 0x1150, 0, 0          ), resp( 'rd', 0x5, 0,   0,  0xabcd1150 ), # conflicts
    req( 'rd', 0x6, 0x1160, 0, 0          ), resp( 'rd', 0x6, 0,   0,  0xabcd1160 ), # conflicts
    req( 'rd', 0x7, 0x1170, 0, 0          ), resp( 'rd', 0x7, 0,   0,  0xabcd1170 ), # conflicts
    req( 'rd', 0x8, 0x1180, 0, 0          ), resp( 'rd', 0x8, 0,   0,  0xabcd1180 ), # conflicts
    req( 'rd', 0x9, 0x1190, 0, 0          ), resp( 'rd', 0x9, 0,   0,  0xabcd1190 ), # conflicts
    req( 'rd', 0xa, 0x11a0, 0, 0          ), resp( 'rd', 0xa, 0,   0,  0xabcd11a0 ), # conflicts
    req( 'rd', 0xb, 0x11b0, 0, 0          ), resp( 'rd', 0xb, 0,   0,  0xabcd11b0 ), # conflicts
    req( 'rd', 0xc, 0x11c0, 0, 0          ), resp( 'rd', 0xc, 0,   0,  0xabcd11c0 ), # conflicts
    req( 'rd', 0xd, 0x11d0, 0, 0          ), resp( 'rd', 0xd, 0,   0,  0xabcd11d0 ), # conflicts
    req( 'rd', 0xe, 0x11e0, 0, 0          ), resp( 'rd', 0xe, 0,   0,  0xabcd11e0 ), # conflicts
    req( 'rd', 0xf, 0x11f0, 0, 0          ), resp( 'rd', 0xf, 0,   0,  0xabcd11f0 ), # conflicts

    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 0,   0,  0x10101010 ),
    req( 'rd', 0x1, 0x1010, 0, 0          ), resp( 'rd', 0x1, 0,   0,  0x11111111 ),
    req( 'rd', 0x2, 0x1020, 0, 0          ), resp( 'rd', 0x2, 0,   0,  0x12121212 ),
    req( 'rd', 0x3, 0x1030, 0, 0          ), resp( 'rd', 0x3, 0,   0,  0x13131313 ),
    req( 'rd', 0x4, 0x1040, 0, 0          ), resp( 'rd', 0x4, 0,   0,  0x14141414 ),
    req( 'rd', 0x5, 0x1050, 0, 0          ), resp( 'rd', 0x5, 0,   0,  0x15151515 ),
    req( 'rd', 0x6, 0x1060, 0, 0          ), resp( 'rd', 0x6, 0,   0,  0x16161616 ),
    req( 'rd', 0x7, 0x1070, 0, 0          ), resp( 'rd', 0x7, 0,   0,  0x17171717 ),
    req( 'rd', 0x8, 0x1080, 0, 0          ), resp( 'rd', 0x8, 0,   0,  0x18181818 ),
    req( 'rd', 0x9, 0x1090, 0, 0          ), resp( 'rd', 0x9, 0,   0,  0x19191919 ),
    req( 'rd', 0xa, 0x10a0, 0, 0          ), resp( 'rd', 0xa, 0,   0,  0x1a1a1a1a ),
    req( 'rd', 0xb, 0x10b0, 0, 0          ), resp( 'rd', 0xb, 0,   0,  0x1b1b1b1b ),
    req( 'rd', 0xc, 0x10c0, 0, 0          ), resp( 'rd', 0xc, 0,   0,  0x1c1c1c1c ),
    req( 'rd', 0xd, 0x10d0, 0, 0          ), resp( 'rd', 0xd, 0,   0,  0x1d1d1d1d ),
    req( 'rd', 0xe, 0x10e0, 0, 0          ), resp( 'rd', 0xe, 0,   0,  0x1e1e1e1e ),
    req( 'rd', 0xf, 0x10f0, 0, 0          ), resp( 'rd', 0xf, 0,   0,  0x1f1f1f1f ),
  ]

#----------------------------------------------------------------------
# Test Cases for Evict (Write miss causing refill and eviction)
#----------------------------------------------------------------------

# Write miss to two cachelines, and then a write to a third cacheline.
# This write to the third cacheline is guaranteed to cause an eviction on
# both the direct mapped and set associative caches. (uses data_512B)

def evict_word_write():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'wr', 0x0, 0x1000, 0, 0xcafecafe ), resp( 'wr', 0x0, 0,   0,  0          ),
    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0xcafecafe ),
    req( 'wr', 0x0, 0x1080, 0, 0x000c0ffe ), resp( 'wr', 0x0, 0,   0,  0          ),
    req( 'rd', 0x0, 0x1080, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0x000c0ffe ),
    req( 'wr', 0x0, 0x1100, 0, 0xfecafeca ), resp( 'wr', 0x0, 0,   0,  0          ), # conflicts
    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 0,   0,  0xcafecafe ),
  ]

# Write word and evict multiple times. Test is carefully crafted to
# ensure it applies to both direct mapped and set associative caches.
# (uses data_512B)

def evict_multi_word_write():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'wr', 0x0, 0x1000, 0, 0x01010101 ), resp( 'wr', 0x0, 0,   0,  0          ),
    req( 'rd', 0x1, 0x1000, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0x01010101 ),
    req( 'wr', 0x2, 0x1080, 0, 0x11111111 ), resp( 'wr', 0x2, 0,   0,  0          ),
    req( 'rd', 0x3, 0x1080, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0x11111111 ),
    req( 'wr', 0x4, 0x1100, 0, 0x22222222 ), resp( 'wr', 0x4, 0,   0,  0          ), # conflicts
    req( 'rd', 0x5, 0x1080, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0x11111111 ), # make sure way1 is still LRU

    req( 'wr', 0x6, 0x1000, 0, 0x02020202 ), resp( 'wr', 0x6, 0,   0,  0          ),
    req( 'rd', 0x7, 0x1000, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0x02020202 ),
    req( 'wr', 0x8, 0x1080, 0, 0x12121212 ), resp( 'wr', 0x8, 1,   0,  0          ),
    req( 'rd', 0x9, 0x1080, 0, 0          ), resp( 'rd', 0x9, 1,   0,  0x12121212 ),
    req( 'wr', 0x4, 0x1100, 0, 0x22222222 ), resp( 'wr', 0x4, 0,   0,  0          ), # conflicts
    req( 'rd', 0xb, 0x1080, 0, 0          ), resp( 'rd', 0xb, 1,   0,  0x12121212 ), # make sure way1 is still LRU

    req( 'wr', 0xc, 0x1000, 0, 0x03030303 ), resp( 'wr', 0xc, 0,   0,  0          ),
    req( 'rd', 0xd, 0x1000, 0, 0          ), resp( 'rd', 0xd, 1,   0,  0x03030303 ),
    req( 'wr', 0xe, 0x1080, 0, 0x13131313 ), resp( 'wr', 0xe, 1,   0,  0          ),
    req( 'rd', 0xf, 0x1080, 0, 0          ), resp( 'rd', 0xf, 1,   0,  0x13131313 ),
    req( 'wr', 0x4, 0x1100, 0, 0x22222222 ), resp( 'wr', 0x4, 0,   0,  0          ), # conflicts
    req( 'rd', 0x1, 0x1080, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0x13131313 ), # make sure way1 is still LRU

    req( 'wr', 0x2, 0x1000, 0, 0x04040404 ), resp( 'wr', 0x2, 0,   0,  0          ),
    req( 'rd', 0x3, 0x1000, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0x04040404 ),
    req( 'wr', 0x4, 0x1080, 0, 0x14141414 ), resp( 'wr', 0x4, 1,   0,  0          ),
    req( 'rd', 0x5, 0x1080, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0x14141414 ),
    req( 'wr', 0x4, 0x1100, 0, 0x22222222 ), resp( 'wr', 0x4, 0,   0,  0          ), # conflicts
    req( 'rd', 0x7, 0x1080, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0x14141414 ), # make sure way1 is still LRU

    req( 'rd', 0x8, 0x1000, 0, 0          ), resp( 'rd', 0x8, 0,   0,  0x04040404 ),
  ]

# Write every word on two cachelines, and then a read to a third
# cacheline. This read to the third cacheline is guaranteed to cause an
# eviction on both the direct mapped and set associative caches. (uses
# data_512B)

def evict_cacheline_write():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'wr', 0x0, 0x1000, 0, 0x01010101 ), resp( 'wr', 0x0, 0,   0,  0          ),
    req( 'wr', 0x1, 0x1004, 0, 0x02020202 ), resp( 'wr', 0x1, 1,   0,  0          ),
    req( 'wr', 0x2, 0x1008, 0, 0x03030303 ), resp( 'wr', 0x2, 1,   0,  0          ),
    req( 'wr', 0x3, 0x100c, 0, 0x04040404 ), resp( 'wr', 0x3, 1,   0,  0          ),

    req( 'wr', 0x4, 0x1080, 0, 0x11111111 ), resp( 'wr', 0x4, 0,   0,  0          ),
    req( 'wr', 0x5, 0x1084, 0, 0x12121212 ), resp( 'wr', 0x5, 1,   0,  0          ),
    req( 'wr', 0x6, 0x1088, 0, 0x13131313 ), resp( 'wr', 0x6, 1,   0,  0          ),
    req( 'wr', 0x7, 0x108c, 0, 0x14141414 ), resp( 'wr', 0x7, 1,   0,  0          ),

    req( 'wr', 0x8, 0x1100, 0, 0x21212121 ), resp( 'wr', 0x8, 0,   0,  0          ), # conflicts

    req( 'rd', 0x9, 0x1000, 0, 0          ), resp( 'rd', 0x9, 0,   0,  0x01010101 ),
    req( 'rd', 0xa, 0x1004, 0, 0          ), resp( 'rd', 0xa, 1,   0,  0x02020202 ),
    req( 'rd', 0xb, 0x1008, 0, 0          ), resp( 'rd', 0xb, 1,   0,  0x03030303 ),
    req( 'rd', 0xc, 0x100c, 0, 0          ), resp( 'rd', 0xc, 1,   0,  0x04040404 ),
  ]

# Write one word from each cacheline, then evict (uses data_512B)

def evict_multi_cacheline_write():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'wr', 0x0, 0x1000, 0, 0x10101010 ), resp( 'wr', 0x0, 0,   0,  0          ),
    req( 'wr', 0x1, 0x1010, 0, 0x11111111 ), resp( 'wr', 0x1, 0,   0,  0          ),
    req( 'wr', 0x2, 0x1020, 0, 0x12121212 ), resp( 'wr', 0x2, 0,   0,  0          ),
    req( 'wr', 0x3, 0x1030, 0, 0x13131313 ), resp( 'wr', 0x3, 0,   0,  0          ),
    req( 'wr', 0x4, 0x1040, 0, 0x14141414 ), resp( 'wr', 0x4, 0,   0,  0          ),
    req( 'wr', 0x5, 0x1050, 0, 0x15151515 ), resp( 'wr', 0x5, 0,   0,  0          ),
    req( 'wr', 0x6, 0x1060, 0, 0x16161616 ), resp( 'wr', 0x6, 0,   0,  0          ),
    req( 'wr', 0x7, 0x1070, 0, 0x17171717 ), resp( 'wr', 0x7, 0,   0,  0          ),
    req( 'wr', 0x8, 0x1080, 0, 0x18181818 ), resp( 'wr', 0x8, 0,   0,  0          ),
    req( 'wr', 0x9, 0x1090, 0, 0x19191919 ), resp( 'wr', 0x9, 0,   0,  0          ),
    req( 'wr', 0xa, 0x10a0, 0, 0x1a1a1a1a ), resp( 'wr', 0xa, 0,   0,  0          ),
    req( 'wr', 0xb, 0x10b0, 0, 0x1b1b1b1b ), resp( 'wr', 0xb, 0,   0,  0          ),
    req( 'wr', 0xc, 0x10c0, 0, 0x1c1c1c1c ), resp( 'wr', 0xc, 0,   0,  0          ),
    req( 'wr', 0xd, 0x10d0, 0, 0x1d1d1d1d ), resp( 'wr', 0xd, 0,   0,  0          ),
    req( 'wr', 0xe, 0x10e0, 0, 0x1e1e1e1e ), resp( 'wr', 0xe, 0,   0,  0          ),
    req( 'wr', 0xf, 0x10f0, 0, 0x1f1f1f1f ), resp( 'wr', 0xf, 0,   0,  0          ),

    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0x10101010 ),
    req( 'rd', 0x1, 0x1010, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0x11111111 ),
    req( 'rd', 0x2, 0x1020, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x12121212 ),
    req( 'rd', 0x3, 0x1030, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0x13131313 ),
    req( 'rd', 0x4, 0x1040, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0x14141414 ),
    req( 'rd', 0x5, 0x1050, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0x15151515 ),
    req( 'rd', 0x6, 0x1060, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0x16161616 ),
    req( 'rd', 0x7, 0x1070, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0x17171717 ),
    req( 'rd', 0x8, 0x1080, 0, 0          ), resp( 'rd', 0x8, 1,   0,  0x18181818 ),
    req( 'rd', 0x9, 0x1090, 0, 0          ), resp( 'rd', 0x9, 1,   0,  0x19191919 ),
    req( 'rd', 0xa, 0x10a0, 0, 0          ), resp( 'rd', 0xa, 1,   0,  0x1a1a1a1a ),
    req( 'rd', 0xb, 0x10b0, 0, 0          ), resp( 'rd', 0xb, 1,   0,  0x1b1b1b1b ),
    req( 'rd', 0xc, 0x10c0, 0, 0          ), resp( 'rd', 0xc, 1,   0,  0x1c1c1c1c ),
    req( 'rd', 0xd, 0x10d0, 0, 0          ), resp( 'rd', 0xd, 1,   0,  0x1d1d1d1d ),
    req( 'rd', 0xe, 0x10e0, 0, 0          ), resp( 'rd', 0xe, 1,   0,  0x1e1e1e1e ),
    req( 'rd', 0xf, 0x10f0, 0, 0          ), resp( 'rd', 0xf, 1,   0,  0x1f1f1f1f ),

    req( 'wr', 0x0, 0x1100, 0, 0x20202020 ), resp( 'wr', 0x0, 0,   0,  0          ), # conflicts
    req( 'wr', 0x1, 0x1110, 0, 0x21212121 ), resp( 'wr', 0x1, 0,   0,  0          ), # conflicts
    req( 'wr', 0x2, 0x1120, 0, 0x22222222 ), resp( 'wr', 0x2, 0,   0,  0          ), # conflicts
    req( 'wr', 0x3, 0x1130, 0, 0x23232323 ), resp( 'wr', 0x3, 0,   0,  0          ), # conflicts
    req( 'wr', 0x4, 0x1140, 0, 0x24242424 ), resp( 'wr', 0x4, 0,   0,  0          ), # conflicts
    req( 'wr', 0x5, 0x1150, 0, 0x25252525 ), resp( 'wr', 0x5, 0,   0,  0          ), # conflicts
    req( 'wr', 0x6, 0x1160, 0, 0x26262626 ), resp( 'wr', 0x6, 0,   0,  0          ), # conflicts
    req( 'wr', 0x7, 0x1170, 0, 0x27272727 ), resp( 'wr', 0x7, 0,   0,  0          ), # conflicts
    req( 'wr', 0x8, 0x1180, 0, 0x28282828 ), resp( 'wr', 0x8, 0,   0,  0          ), # conflicts
    req( 'wr', 0x9, 0x1190, 0, 0x29292929 ), resp( 'wr', 0x9, 0,   0,  0          ), # conflicts
    req( 'wr', 0xa, 0x11a0, 0, 0x2a2a2a2a ), resp( 'wr', 0xa, 0,   0,  0          ), # conflicts
    req( 'wr', 0xb, 0x11b0, 0, 0x2b2b2b2b ), resp( 'wr', 0xb, 0,   0,  0          ), # conflicts
    req( 'wr', 0xc, 0x11c0, 0, 0x2c2c2c2c ), resp( 'wr', 0xc, 0,   0,  0          ), # conflicts
    req( 'wr', 0xd, 0x11d0, 0, 0x2d2d2d2d ), resp( 'wr', 0xd, 0,   0,  0          ), # conflicts
    req( 'wr', 0xe, 0x11e0, 0, 0x2e2e2e2e ), resp( 'wr', 0xe, 0,   0,  0          ), # conflicts
    req( 'wr', 0xf, 0x11f0, 0, 0x2f2f2f2f ), resp( 'wr', 0xf, 0,   0,  0          ), # conflicts

    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 0,   0,  0x10101010 ),
    req( 'rd', 0x1, 0x1010, 0, 0          ), resp( 'rd', 0x1, 0,   0,  0x11111111 ),
    req( 'rd', 0x2, 0x1020, 0, 0          ), resp( 'rd', 0x2, 0,   0,  0x12121212 ),
    req( 'rd', 0x3, 0x1030, 0, 0          ), resp( 'rd', 0x3, 0,   0,  0x13131313 ),
    req( 'rd', 0x4, 0x1040, 0, 0          ), resp( 'rd', 0x4, 0,   0,  0x14141414 ),
    req( 'rd', 0x5, 0x1050, 0, 0          ), resp( 'rd', 0x5, 0,   0,  0x15151515 ),
    req( 'rd', 0x6, 0x1060, 0, 0          ), resp( 'rd', 0x6, 0,   0,  0x16161616 ),
    req( 'rd', 0x7, 0x1070, 0, 0          ), resp( 'rd', 0x7, 0,   0,  0x17171717 ),
    req( 'rd', 0x8, 0x1080, 0, 0          ), resp( 'rd', 0x8, 0,   0,  0x18181818 ),
    req( 'rd', 0x9, 0x1090, 0, 0          ), resp( 'rd', 0x9, 0,   0,  0x19191919 ),
    req( 'rd', 0xa, 0x10a0, 0, 0          ), resp( 'rd', 0xa, 0,   0,  0x1a1a1a1a ),
    req( 'rd', 0xb, 0x10b0, 0, 0          ), resp( 'rd', 0xb, 0,   0,  0x1b1b1b1b ),
    req( 'rd', 0xc, 0x10c0, 0, 0          ), resp( 'rd', 0xc, 0,   0,  0x1c1c1c1c ),
    req( 'rd', 0xd, 0x10d0, 0, 0          ), resp( 'rd', 0xd, 0,   0,  0x1d1d1d1d ),
    req( 'rd', 0xe, 0x10e0, 0, 0          ), resp( 'rd', 0xe, 0,   0,  0x1e1e1e1e ),
    req( 'rd', 0xf, 0x10f0, 0, 0          ), resp( 'rd', 0xf, 0,   0,  0x1f1f1f1f ),
  ]

#-------------------------------------------------------------------------
# Test case for capacity miss
# Test for capacity miss by reading the same index with different tags more than 16 times
#-------------------------------------------------------------------------

def capacity_miss():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 0,   0,  0xabcd1000 ), # Compulsory miss
    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0xabcd1000 ),
    req( 'rd', 0x1, 0x1100, 0, 0          ), resp( 'rd', 0x1, 0,   0,  0xabcd1100 ), # Conflict miss
    req( 'rd', 0x1, 0x1100, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0xabcd1100 ),
    req( 'rd', 0x2, 0x1200, 0, 0          ), resp( 'rd', 0x2, 0,   0,  0xabcd1200 ), # Conflict miss
    req( 'rd', 0x2, 0x1200, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0xabcd1200 ),
    req( 'rd', 0x3, 0x1300, 0, 0          ), resp( 'rd', 0x3, 0,   0,  0xabcd1300 ), # Conflict miss
    req( 'rd', 0x3, 0x1300, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0xabcd1300 ),
    req( 'rd', 0x4, 0x1400, 0, 0          ), resp( 'rd', 0x4, 0,   0,  0xabcd1400 ), # Conflict miss
    req( 'rd', 0x4, 0x1400, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0xabcd1400 ),
    req( 'rd', 0x5, 0x1500, 0, 0          ), resp( 'rd', 0x5, 0,   0,  0xabcd1500 ), # Conflict miss
    req( 'rd', 0x5, 0x1500, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0xabcd1500 ),
    req( 'rd', 0x6, 0x1600, 0, 0          ), resp( 'rd', 0x6, 0,   0,  0xabcd1600 ), # Conflict miss
    req( 'rd', 0x6, 0x1600, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0xabcd1600 ),
    req( 'rd', 0x7, 0x1700, 0, 0          ), resp( 'rd', 0x7, 0,   0,  0xabcd1700 ), # Conflict miss
    req( 'rd', 0x7, 0x1700, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0xabcd1700 ),
    req( 'rd', 0x8, 0x1800, 0, 0          ), resp( 'rd', 0x8, 0,   0,  0xabcd1800 ), # Conflict miss
    req( 'rd', 0x8, 0x1800, 0, 0          ), resp( 'rd', 0x8, 1,   0,  0xabcd1800 ),
    req( 'rd', 0x9, 0x1900, 0, 0          ), resp( 'rd', 0x9, 0,   0,  0xabcd1900 ), # Conflict miss
    req( 'rd', 0x9, 0x1900, 0, 0          ), resp( 'rd', 0x9, 1,   0,  0xabcd1900 ),
    req( 'rd', 0xa, 0x1a00, 0, 0          ), resp( 'rd', 0xa, 0,   0,  0xabcd1a00 ), # Conflict miss
    req( 'rd', 0xa, 0x1a00, 0, 0          ), resp( 'rd', 0xa, 1,   0,  0xabcd1a00 ),
    req( 'rd', 0xb, 0x1b00, 0, 0          ), resp( 'rd', 0xb, 0,   0,  0xabcd1b00 ), # Conflict miss
    req( 'rd', 0xb, 0x1b00, 0, 0          ), resp( 'rd', 0xb, 1,   0,  0xabcd1b00 ),
    req( 'rd', 0xc, 0x1c00, 0, 0          ), resp( 'rd', 0xc, 0,   0,  0xabcd1c00 ), # Conflict miss
    req( 'rd', 0xc, 0x1c00, 0, 0          ), resp( 'rd', 0xc, 1,   0,  0xabcd1c00 ),
    req( 'rd', 0xd, 0x1d00, 0, 0          ), resp( 'rd', 0xd, 0,   0,  0xabcd1d00 ), # Conflict miss
    req( 'rd', 0xd, 0x1d00, 0, 0          ), resp( 'rd', 0xd, 1,   0,  0xabcd1d00 ),
    req( 'rd', 0xe, 0x1e00, 0, 0          ), resp( 'rd', 0xe, 0,   0,  0xabcd1e00 ), # Conflict miss
    req( 'rd', 0xe, 0x1e00, 0, 0          ), resp( 'rd', 0xe, 1,   0,  0xabcd1e00 ),
    req( 'rd', 0xf, 0x1f00, 0, 0          ), resp( 'rd', 0xf, 0,   0,  0xabcd1f00 ), # Conflict miss
    req( 'rd', 0xf, 0x1f00, 0, 0          ), resp( 'rd', 0xf, 1,   0,  0xabcd1f00 ),

    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 0,   0,  0xabcd1000 ), # Capacity miss
    req( 'rd', 0x1, 0x1100, 0, 0          ), resp( 'rd', 0x1, 0,   0,  0xabcd1100 ), # Capacity miss
    req( 'rd', 0x2, 0x1200, 0, 0          ), resp( 'rd', 0x2, 0,   0,  0xabcd1200 ), # Capacity miss
    req( 'rd', 0x3, 0x1300, 0, 0          ), resp( 'rd', 0x3, 0,   0,  0xabcd1300 ), # Capacity miss
    req( 'rd', 0x4, 0x1400, 0, 0          ), resp( 'rd', 0x4, 0,   0,  0xabcd1400 ), # Capacity miss
    req( 'rd', 0x5, 0x1500, 0, 0          ), resp( 'rd', 0x5, 0,   0,  0xabcd1500 ), # Capacity miss
    req( 'rd', 0x6, 0x1600, 0, 0          ), resp( 'rd', 0x6, 0,   0,  0xabcd1600 ), # Capacity miss
    req( 'rd', 0x7, 0x1700, 0, 0          ), resp( 'rd', 0x7, 0,   0,  0xabcd1700 ), # Capacity miss
    req( 'rd', 0x8, 0x1800, 0, 0          ), resp( 'rd', 0x8, 0,   0,  0xabcd1800 ), # Capacity miss
    req( 'rd', 0x9, 0x1900, 0, 0          ), resp( 'rd', 0x9, 0,   0,  0xabcd1900 ), # Capacity miss
    req( 'rd', 0xa, 0x1a00, 0, 0          ), resp( 'rd', 0xa, 0,   0,  0xabcd1a00 ), # Capacity miss
    req( 'rd', 0xb, 0x1b00, 0, 0          ), resp( 'rd', 0xb, 0,   0,  0xabcd1b00 ), # Capacity miss
    req( 'rd', 0xc, 0x1c00, 0, 0          ), resp( 'rd', 0xc, 0,   0,  0xabcd1c00 ), # Capacity miss
    req( 'rd', 0xd, 0x1d00, 0, 0          ), resp( 'rd', 0xd, 0,   0,  0xabcd1d00 ), # Capacity miss
    req( 'rd', 0xe, 0x1e00, 0, 0          ), resp( 'rd', 0xe, 0,   0,  0xabcd1e00 ), # Capacity miss
    req( 'rd', 0xf, 0x1f00, 0, 0          ), resp( 'rd', 0xf, 0,   0,  0xabcd1f00 ), # Capacity miss
  ]

#-------------------------------------------------------------------------
# Generic tests
#-------------------------------------------------------------------------

test_case_table_generic = mk_test_case_table([
  (                                              "msg_func                          mem_data_func stall lat src sink"),

  [ "write_init_word",                            write_init_word,                  None,         0.0,  0,  0,  0    ],
  [ "write_init_multi_word",                      write_init_multi_word,            None,         0.0,  0,  0,  0    ],
  [ "write_init_cacheline",                       write_init_cacheline,             None,         0.0,  0,  0,  0    ],
  [ "write_init_multi_cacheline",                 write_init_multi_cacheline,       None,         0.0,  0,  0,  0    ],
  [ "write_init_multi_word_sink_delay",           write_init_multi_word,            None,         0.0,  0,  0,  10   ],
  [ "write_init_multi_word_src_delay",            write_init_multi_word,            None,         0.0,  0,  10, 0    ],
  [ "write_init_multi_word_sink_delay_random",    write_init_multi_word,            None,         random(),  0,  0,  randint(0,100)   ],
  [ "write_init_multi_word_src_delay_random",     write_init_multi_word,            None,         random(),  0,  randint(0,100), 0    ],
  [ "write_init_multi_word_delay_random",         write_init_multi_word,            None,         random(),  randint(0,100),  randint(0,100), randint(0,100)    ],

  # Read hit path for clean lines
  [ "read_hit_word",                              read_hit_word,                    None,         0.0,  0,  0,  0    ],
  [ "read_hit_multi_word",                        read_hit_multi_word,              None,         0.0,  0,  0,  0    ],
  [ "read_hit_cacheline",                         read_hit_cacheline,               None,         0.0,  0,  0,  0    ],
  [ "read_hit_multi_cacheline",                   read_hit_multi_cacheline,         None,         0.0,  0,  0,  0    ],
  [ "read_hit_multi_word_sink_delay",             read_hit_multi_word,              None,         0.0,  0,  0,  10   ],
  [ "read_hit_multi_word_src_delay",              read_hit_multi_word,              None,         0.0,  0,  10, 0    ],
  [ "read_hit_multi_word_sink_delay_random",      read_hit_multi_word,              None,         random(),  0,  0,  randint(0,100)   ],
  [ "read_hit_multi_word_src_delay_random",       read_hit_multi_word,              None,         random(),  0,  randint(0,100), 0    ],
  [ "read_hit_multi_word_delay_random",           read_hit_multi_word,              None,         random(),  randint(0,100),  randint(0,100), randint(0,100)    ],

  # Write hit path for clean lines + Read hit path for dirty lines
  [ "write_hit_word",                             write_hit_word,                   None,         0.0,  0,  0,  0    ],
  [ "write_hit_multi_word",                       write_hit_multi_word,             None,         0.0,  0,  0,  0    ],
  [ "write_hit_cacheline",                        write_hit_cacheline,              None,         0.0,  0,  0,  0    ],
  [ "write_hit_multi_cacheline",                  write_hit_multi_cacheline,        None,         0.0,  0,  0,  0    ],
  [ "write_hit_multi_word_sink_delay",            write_hit_multi_word,             None,         0.0,  0,  0,  10   ],
  [ "write_hit_multi_word_src_delay",             write_hit_multi_word,             None,         0.0,  0,  10, 0    ],
  [ "write_hit_multi_word_sink_delay_random",     write_hit_multi_word,             None,         random(),  0,  0,  randint(0,100)   ],
  [ "write_hit_multi_word_src_delay_random",      write_hit_multi_word,             None,         random(),  0,  randint(0,100), 0    ],
  [ "write_hit_multi_word_delay_random",          write_hit_multi_word,             None,         random(),  randint(0,100),  randint(0,100), randint(0,100)    ],

  # Write hit path for dirty lines
  [ "write_hit_word_dirty",                       write_hit_word_dirty,             None,         0.0,  0,  0,  0    ],
  [ "write_hit_multi_word_dirty",                 write_hit_multi_word_dirty,       None,         0.0,  0,  0,  0    ],
  [ "write_hit_cacheline_dirty",                  write_hit_cacheline_dirty,        None,         0.0,  0,  0,  0    ],
  [ "write_hit_multi_cacheline_dirty",            write_hit_multi_cacheline_dirty,  None,         0.0,  0,  0,  0    ],
  [ "write_hit_multi_word_sink_delay_dirty",      write_hit_multi_word_dirty,       None,         0.0,  0,  0,  10   ],
  [ "write_hit_multi_word_src_delay_dirty",       write_hit_multi_word_dirty,       None,         0.0,  0,  10, 0    ],

  # Read miss with refill and no eviction
  [ "read_miss_word",                             read_miss_word,                   data_64B,     0.0,  0,  0,  0    ],
  [ "read_miss_multi_word",                       read_miss_multi_word,             data_64B,     0.0,  0,  0,  0    ],
  [ "read_miss_cacheline",                        read_miss_cacheline,              data_64B,     0.0,  0,  0,  0    ],
  [ "read_miss_multi_cacheline",                  read_miss_multi_cacheline,        data_512B,    0.0,  0,  0,  0    ], # Test that stresses entire cache
  [ "read_miss_multi_word_sink_delay",            read_miss_multi_word,             data_64B,     0.9,  3,  0,  10   ],
  [ "read_miss_multi_word_src_delay",             read_miss_multi_word,             data_64B,     0.9,  3,  10, 0    ],

  # Write miss with refill and no eviction
  [ "write_miss_word",                            write_miss_word,                  data_64B,     0.0,  0,  0,  0    ],
  [ "write_miss_multi_word",                      write_miss_multi_word,            data_64B,     0.0,  0,  0,  0    ],
  [ "write_miss_cacheline",                       write_miss_cacheline,             data_64B,     0.0,  0,  0,  0    ],
  [ "write_miss_multi_cacheline",                 write_miss_multi_cacheline,       data_512B,    0.0,  0,  0,  0    ], # Test that stresses entire cache
  [ "write_miss_multi_word_sink_delay",           write_miss_multi_word,            data_64B,     0.9,  3,  0,  10   ],
  [ "write_miss_multi_word_src_delay",            write_miss_multi_word,            data_64B,     0.5,  3,  10, 0    ],

  # Read miss with refill and eviction + Conflict misses
  [ "evict_word",                                 evict_word,                       data_512B,    0.0,  0,  0,  0    ],
  [ "evict_multi_word",                           evict_multi_word,                 data_512B,    0.0,  0,  0,  0    ],
  [ "evict_cacheline",                            evict_cacheline,                  data_512B,    0.0,  0,  0,  0    ],
  [ "evict_multi_cacheline",                      evict_multi_cacheline,            data_512B,    0.0,  0,  0,  0    ], # Test that stresses entire cache
  [ "evict_multi_word_sink_delay",                evict_multi_word,                 data_512B,    0.5,  3,  0,  10   ],
  [ "evict_multi_word_src_delay",                 evict_multi_word,                 data_512B,    0.9,  3,  10, 0    ],

  # Write miss with refill and eviction + Conflict misses
  [ "evict_word_write",                           evict_word_write,                 data_512B,    0.0,  0,  0,  0    ],
  [ "evict_multi_word_write",                     evict_multi_word_write,           data_512B,    0.0,  0,  0,  0    ],
  [ "evict_cacheline_write",                      evict_cacheline_write,            data_512B,    0.0,  0,  0,  0    ],
  [ "evict_multi_cacheline_write",                evict_multi_cacheline_write,      data_512B,    0.0,  0,  0,  0    ], # Test that stresses entire cache
  [ "evict_multi_word_sink_delay_write",          evict_multi_word_write,           data_512B,    0.9,  3,  0,  10   ],
  [ "evict_multi_word_src_delay_write",           evict_multi_word_write,           data_512B,    0.9,  3,  10, 0    ],
  [ "evict_multi_word_sink_delay_write_random",   evict_multi_word_write,           data_512B,    random(),  0,  0,  randint(0,100)   ],
  [ "evict_multi_word_src_delay_write_random",    evict_multi_word_write,           data_512B,    random(),  0,  randint(0,100), 0    ],
  [ "evict_multi_word_delay_write_random",        evict_multi_word_write,           data_512B,    random(),  randint(0,100),  randint(0,100), randint(0,100)    ],

  # Tests which stress entire cache, not just a few cache lines
  [ "write_init_all_cacheline",                   write_init_all_cacheline,         None,         0.0,  0,  0,  0    ],
  [ "read_hit_all_cacheline",                     read_hit_all_cacheline,           None,         0.0,  0,  0,  0    ],
  [ "write_hit_all_cacheline",                    write_hit_all_cacheline,          None,         0.0,  0,  0,  0    ],
  [ "write_hit_all_cacheline_dirty",              write_hit_all_cacheline_dirty,    None,         0.0,  0,  0,  0    ],
  [ "write_hit_all_cacheline_sink_delay",         write_hit_all_cacheline,          None,         0.0,  0,  0,  10   ],
  [ "write_hit_all_cacheline_dirty_src_delay",    write_hit_all_cacheline_dirty,    None,         0.0,  0,  10,  0   ],
  # Some of the tests above these also test the entire cache. They have been labelled with comments.

  # Conflict and Capacity Misses
  [ "capacity_miss",                              capacity_miss,                    data_8192B,   0.0,  0,  0,  0    ],
])

@pytest.mark.parametrize( **test_case_table_generic )
def test_generic( test_params, cmdline_opts ):
  run_test( CacheFL(), test_params, cmdline_opts, cmp_wo_test_field )

#-------------------------------------------------------------------------
# Test Case with Random Addresses and Data
#-------------------------------------------------------------------------

def write_init_random():
  return [
    #    type  opq  addr                  len data                           type  opq  test len data
    req( 'in', 0x0, randint(0x1000,0xffff), 0, randint(0,0xffffffff) ), resp( 'in', 0x0, 0,   0,  0    ),
    req( 'in', 0x1, randint(0x1000,0xffff), 0, randint(0,0xffffffff) ), resp( 'in', 0x1, 0,   0,  0    ),
    req( 'in', 0x2, randint(0x1000,0xffff), 0, randint(0,0xffffffff) ), resp( 'in', 0x2, 0,   0,  0    ),
    req( 'in', 0x3, randint(0x1000,0xffff), 0, randint(0,0xffffffff) ), resp( 'in', 0x3, 0,   0,  0    ),
    req( 'in', 0x4, randint(0x1000,0xffff), 0, randint(0,0xffffffff) ), resp( 'in', 0x4, 0,   0,  0    ),
    req( 'in', 0x5, randint(0x1000,0xffff), 0, randint(0,0xffffffff) ), resp( 'in', 0x5, 0,   0,  0    ),
    req( 'in', 0x6, randint(0x1000,0xffff), 0, randint(0,0xffffffff) ), resp( 'in', 0x6, 0,   0,  0    ),
    req( 'in', 0x7, randint(0x1000,0xffff), 0, randint(0,0xffffffff) ), resp( 'in', 0x7, 0,   0,  0    ),
    req( 'in', 0x8, randint(0x1000,0xffff), 0, randint(0,0xffffffff) ), resp( 'in', 0x8, 0,   0,  0    ),
    req( 'in', 0x9, randint(0x1000,0xffff), 0, randint(0,0xffffffff) ), resp( 'in', 0x9, 0,   0,  0    ),
    req( 'in', 0xa, randint(0x1000,0xffff), 0, randint(0,0xffffffff) ), resp( 'in', 0xa, 0,   0,  0    ),
    req( 'in', 0xb, randint(0x1000,0xffff), 0, randint(0,0xffffffff) ), resp( 'in', 0xb, 0,   0,  0    ),
    req( 'in', 0xc, randint(0x1000,0xffff), 0, randint(0,0xffffffff) ), resp( 'in', 0xc, 0,   0,  0    ),
    req( 'in', 0xd, randint(0x1000,0xffff), 0, randint(0,0xffffffff) ), resp( 'in', 0xd, 0,   0,  0    ),
    req( 'in', 0xe, randint(0x1000,0xffff), 0, randint(0,0xffffffff) ), resp( 'in', 0xe, 0,   0,  0    ),
    req( 'in', 0xf, randint(0x1000,0xffff), 0, randint(0,0xffffffff) ), resp( 'in', 0xf, 0,   0,  0    ),
  ]

def read_hit_all_cacheline_random_data():
  calls = []
  random_datas = []
  addrs = [0x0000, 0x1010, 0x2020, 0x3030, 0x4040, 0x5050, 0x6060, 0x7070, 0x8080, 0x9090,
                  0xa0a0, 0xb0b0, 0xc0c0, 0xd0d0, 0xe0e0, 0xf0f0]
  for i in range(16):
    random_data = randint(0,0xffffffff)
    random_datas.append(random_data)

    calls.extend(
      #    type  opq  addr        len data                type  opq  test len data
      [req( 'in', i, addrs[i], 0, random_data ), resp( 'in', i, 0,   0,  0          )],
    )

  for i in range(16):
    calls.extend(
      #    type  opq  addr        len data                type  opq  test len data
      [req( 'rd', i, addrs[i], 0, 0 ), resp( 'rd', i, 1,   0,  random_datas[i] )],
    )

  return calls


def write_miss_multi_word_random():
    calls = [
      #    type  opq  addr   len data                type  opq  test len data
      req( 'wr', 0x1, 0x1000, 0, 0x01010101 ), resp( 'wr', 0x1, 0,   0,  0          ),
      req( 'rd', 0x2, 0x1000, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x01010101 ),
    ]
    for i in range(3, 8, 2):

      random_data = randint(0,0xffffffff)

      calls.extend([
        #    type  opq  addr   len data                type  opq  test len data
        req( 'wr', i, 0x1000, 0, random_data ), resp( 'wr', 0x1, 1,   0,  0          ),
      ])

      calls.extend([
        #    type  opq  addr   len data                type  opq  test len data
        req( 'rd', i+1, 0x1000, 0, 0          ), resp( 'rd', 0x2, 1,   0,  random_data ),
      ])

    return calls

def evict_word_write_random():
  calls = []

  for i in range(5):

    random_addr = randint(0x1000,0xffff)
    random_data = randint(0,0xffffffff)

    calls.extend([
      req( 'wr', 0x0, random_addr, 0, random_data ), resp( 'wr', 0x0, 0,   0,  0          ),
    ])

    calls.extend([
      req( 'rd', 0x0, random_addr, 0, 0           ), resp( 'rd', 0x0, 1,   0,  random_data ),
    ])

  return calls

def write_hit_all_cacheline_random():
  random_datas = []

  for _ in range(32):
    random_datas.append(randint(0,0xffffffff))

  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x0000, 0, random_datas[0] ), resp( 'in', 0x0, 0,   0,  0          ),
    req( 'in', 0x1, 0x1010, 0, random_datas[1] ), resp( 'in', 0x1, 0,   0,  0          ),
    req( 'in', 0x2, 0x2020, 0, random_datas[2] ), resp( 'in', 0x2, 0,   0,  0          ),
    req( 'in', 0x3, 0x3030, 0, random_datas[3] ), resp( 'in', 0x3, 0,   0,  0          ),
    req( 'in', 0x4, 0x4040, 0, random_datas[4] ), resp( 'in', 0x4, 0,   0,  0          ),
    req( 'in', 0x5, 0x5050, 0, random_datas[5] ), resp( 'in', 0x5, 0,   0,  0          ),
    req( 'in', 0x6, 0x6060, 0, random_datas[6] ), resp( 'in', 0x6, 0,   0,  0          ),
    req( 'in', 0x7, 0x7070, 0, random_datas[7] ), resp( 'in', 0x7, 0,   0,  0          ),
    req( 'in', 0x8, 0x8080, 0, random_datas[8] ), resp( 'in', 0x8, 0,   0,  0          ),
    req( 'in', 0x9, 0x9090, 0, random_datas[9] ), resp( 'in', 0x9, 0,   0,  0          ),
    req( 'in', 0xa, 0xa0a0, 0, random_datas[10] ), resp( 'in', 0xa, 0,   0,  0          ),
    req( 'in', 0xb, 0xb0b0, 0, random_datas[11] ), resp( 'in', 0xb, 0,   0,  0          ),
    req( 'in', 0xc, 0xc0c0, 0, random_datas[12] ), resp( 'in', 0xc, 0,   0,  0          ),
    req( 'in', 0xd, 0xd0d0, 0, random_datas[13] ), resp( 'in', 0xd, 0,   0,  0          ),
    req( 'in', 0xe, 0xe0e0, 0, random_datas[14] ), resp( 'in', 0xe, 0,   0,  0          ),
    req( 'in', 0xf, 0xf0f0, 0, random_datas[15] ), resp( 'in', 0xf, 0,   0,  0          ),

    req( 'wr', 0x0, 0x0000, 0, random_datas[16] ), resp( 'wr', 0x0, 1,   0,  0          ),
    req( 'wr', 0x1, 0x1010, 0, random_datas[17] ), resp( 'wr', 0x1, 1,   0,  0          ),
    req( 'wr', 0x2, 0x2020, 0, random_datas[18] ), resp( 'wr', 0x2, 1,   0,  0          ),
    req( 'wr', 0x3, 0x3030, 0, random_datas[19] ), resp( 'wr', 0x3, 1,   0,  0          ),
    req( 'wr', 0x4, 0x4040, 0, random_datas[20] ), resp( 'wr', 0x4, 1,   0,  0          ),
    req( 'wr', 0x5, 0x5050, 0, random_datas[21] ), resp( 'wr', 0x5, 1,   0,  0          ),
    req( 'wr', 0x6, 0x6060, 0, random_datas[22] ), resp( 'wr', 0x6, 1,   0,  0          ),
    req( 'wr', 0x7, 0x7070, 0, random_datas[23] ), resp( 'wr', 0x7, 1,   0,  0          ),
    req( 'wr', 0x8, 0x8080, 0, random_datas[24] ), resp( 'wr', 0x8, 1,   0,  0          ),
    req( 'wr', 0x9, 0x9090, 0, random_datas[25] ), resp( 'wr', 0x9, 1,   0,  0          ),
    req( 'wr', 0xa, 0xa0a0, 0, random_datas[26] ), resp( 'wr', 0xa, 1,   0,  0          ),
    req( 'wr', 0xb, 0xb0b0, 0, random_datas[27] ), resp( 'wr', 0xb, 1,   0,  0          ),
    req( 'wr', 0xc, 0xc0c0, 0, random_datas[28] ), resp( 'wr', 0xc, 1,   0,  0          ),
    req( 'wr', 0xd, 0xd0d0, 0, random_datas[29] ), resp( 'wr', 0xd, 1,   0,  0          ),
    req( 'wr', 0xe, 0xe0e0, 0, random_datas[30] ), resp( 'wr', 0xe, 1,   0,  0          ),
    req( 'wr', 0xf, 0xf0f0, 0, random_datas[31] ), resp( 'wr', 0xf, 1,   0,  0          ),


    req( 'rd', 0x0, 0x0000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  random_datas[16] ),
    req( 'rd', 0x1, 0x1010, 0, 0          ), resp( 'rd', 0x1, 1,   0,  random_datas[17] ),
    req( 'rd', 0x2, 0x2020, 0, 0          ), resp( 'rd', 0x2, 1,   0,  random_datas[18] ),
    req( 'rd', 0x3, 0x3030, 0, 0          ), resp( 'rd', 0x3, 1,   0,  random_datas[19] ),
    req( 'rd', 0x4, 0x4040, 0, 0          ), resp( 'rd', 0x4, 1,   0,  random_datas[20] ),
    req( 'rd', 0x5, 0x5050, 0, 0          ), resp( 'rd', 0x5, 1,   0,  random_datas[21] ),
    req( 'rd', 0x6, 0x6060, 0, 0          ), resp( 'rd', 0x6, 1,   0,  random_datas[22] ),
    req( 'rd', 0x7, 0x7070, 0, 0          ), resp( 'rd', 0x7, 1,   0,  random_datas[23] ),
    req( 'rd', 0x8, 0x8080, 0, 0          ), resp( 'rd', 0x8, 1,   0,  random_datas[24] ),
    req( 'rd', 0x9, 0x9090, 0, 0          ), resp( 'rd', 0x9, 1,   0,  random_datas[25] ),
    req( 'rd', 0xa, 0xa0a0, 0, 0          ), resp( 'rd', 0xa, 1,   0,  random_datas[26] ),
    req( 'rd', 0xb, 0xb0b0, 0, 0          ), resp( 'rd', 0xb, 1,   0,  random_datas[27] ),
    req( 'rd', 0xc, 0xc0c0, 0, 0          ), resp( 'rd', 0xc, 1,   0,  random_datas[28] ),
    req( 'rd', 0xd, 0xd0d0, 0, 0          ), resp( 'rd', 0xd, 1,   0,  random_datas[29] ),
    req( 'rd', 0xe, 0xe0e0, 0, 0          ), resp( 'rd', 0xe, 1,   0,  random_datas[30] ),
    req( 'rd', 0xf, 0xf0f0, 0, 0          ), resp( 'rd', 0xf, 1,   0,  random_datas[31] ),
  ]

def read_miss_cacheline_random():
  random_data = data_random()
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'rd', 0x1, 0x1000, 0, 0          ), resp( 'rd', 0x1, 0,   0,  random_data[0*2+1] ),
    req( 'rd', 0x2, 0x1004, 0, 0          ), resp( 'rd', 0x2, 1,   0,  random_data[1*2+1] ),
    req( 'rd', 0x3, 0x1008, 0, 0          ), resp( 'rd', 0x3, 1,   0,  random_data[2*2+1] ),
    req( 'rd', 0x4, 0x100c, 0, 0          ), resp( 'rd', 0x4, 1,   0,  random_data[3*2+1] ),
  ]

def random_address_request_data():
  calls = []
  type_list = ['rd', 'wr']
  reference_memory = data_random()
  write_addr_list = []

  for _ in range(500):
    random_addr = (randint(0x1000,0x13FC)//4*4)
    random_data = randint(0, 0xffffffff)
    random_type = choice(type_list)

    if random_type == 'wr':
      write_addr_list.append(random_addr)
      addr_index = reference_memory.index(random_addr)
      # Replace the element after the address (the data) with random_data
      reference_memory[addr_index + 1] = random_data
      calls.extend([
        req( 'wr', 0x0, random_addr, 0, random_data ), resp( 'wr', 0x0, 0,   0,  0          ),
      ])
    else:
      addr_index = reference_memory.index(random_addr)
      # Replace the element after the address (the data) with random_data
      data_reference = reference_memory[addr_index + 1]
      calls.extend([
        req( 'rd', 0x0, random_addr, 0, 0          ), resp( 'rd', 0x0, 0,   0,  data_reference),
      ])

  # check that all the writes overwrite memory
  for write_addr in write_addr_list:
    addr_index = reference_memory.index(write_addr)
    # Replace the element after the address (the data) with random_data
    data_reference = reference_memory[addr_index + 1]
    calls.extend([
      req( 'rd', 0x0, write_addr, 0, 0          ), resp( 'rd', 0x0, 0,   0,  data_reference),
    ])

  return calls

test_case_table_random = mk_test_case_table([
  (                                       "msg_func                                 mem_data_func stall lat src sink"),

  # Simple address patterns, simple request type, with random data
  [ "write_miss_multi_word_random",       write_miss_multi_word_random,             None,         0.0,  0,  0,  0    ],

  # Random address patterns, simple request type, with random data
  [ "write_init_random",                  write_init_random,                        None,         0.0,  0,  0,  0    ],
  [ "evict_word_write_random",            evict_word_write_random,                  None,         0.0,  0,  0,  0    ],

  # Stride with random data
  [ "read_hit_all_cacheline_random_data", read_hit_all_cacheline_random_data,       None,         0.0,  0,  0,  0    ],
  [ "write_hit_all_cacheline_random",     write_hit_all_cacheline_random,           None,         0.0,  0,  0,  0    ],
  [ "read_miss_cacheline_random",         read_miss_cacheline_random,               data_random,   0.0,  0,  0,  0   ],

  # Random address patterns, request types, and data
  [ "random_address_request_data",         random_address_request_data,             data_random,   0.0,  0,  0,  0   ],

])

@pytest.mark.parametrize( **test_case_table_random )
def test_random( test_params, cmdline_opts ):
  run_test( CacheFL(), test_params, cmdline_opts, cmp_wo_test_field )

#-------------------------------------------------------------------------
# Test Cases for Direct Mapped
#-------------------------------------------------------------------------

def write_hit_dirty_read_miss_dirty_all_cacheline_dmap():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'wr', 0x0, 0x0000, 0, 0x00000000 ), resp( 'wr', 0x0, 0,   0,  0          ),
    req( 'wr', 0x1, 0x1010, 0, 0x01010101 ), resp( 'wr', 0x1, 0,   0,  0          ),
    req( 'wr', 0x2, 0x2020, 0, 0x02020202 ), resp( 'wr', 0x2, 0,   0,  0          ),
    req( 'wr', 0x3, 0x3030, 0, 0x03030303 ), resp( 'wr', 0x3, 0,   0,  0          ),
    req( 'wr', 0x4, 0x4040, 0, 0x04040404 ), resp( 'wr', 0x4, 0,   0,  0          ),
    req( 'wr', 0x5, 0x5050, 0, 0x05050505 ), resp( 'wr', 0x5, 0,   0,  0          ),
    req( 'wr', 0x6, 0x6060, 0, 0x06060606 ), resp( 'wr', 0x6, 0,   0,  0          ),
    req( 'wr', 0x7, 0x7070, 0, 0x07070707 ), resp( 'wr', 0x7, 0,   0,  0          ),
    req( 'wr', 0x8, 0x8080, 0, 0x08080808 ), resp( 'wr', 0x8, 0,   0,  0          ),
    req( 'wr', 0x9, 0x9090, 0, 0x09090909 ), resp( 'wr', 0x9, 0,   0,  0          ),
    req( 'wr', 0xa, 0xa0a0, 0, 0x0a0a0a0a ), resp( 'wr', 0xa, 0,   0,  0          ),
    req( 'wr', 0xb, 0xb0b0, 0, 0x0b0b0b0b ), resp( 'wr', 0xb, 0,   0,  0          ),
    req( 'wr', 0xc, 0xc0c0, 0, 0x0c0c0c0c ), resp( 'wr', 0xc, 0,   0,  0          ),
    req( 'wr', 0xd, 0xd0d0, 0, 0x0d0d0d0d ), resp( 'wr', 0xd, 0,   0,  0          ),
    req( 'wr', 0xe, 0xe0e0, 0, 0x0e0e0e0e ), resp( 'wr', 0xe, 0,   0,  0          ),
    req( 'wr', 0xf, 0xf0f0, 0, 0x0f0f0f0f ), resp( 'wr', 0xf, 0,   0,  0          ),

    req( 'wr', 0x0, 0x0100, 0, 0x00000000 ), resp( 'wr', 0x0, 0,   0,  0          ), # This set repeats indices for above
    req( 'wr', 0x1, 0x1110, 0, 0x10101010 ), resp( 'wr', 0x1, 0,   0,  0          ),
    req( 'wr', 0x2, 0x2120, 0, 0x20202020 ), resp( 'wr', 0x2, 0,   0,  0          ),
    req( 'wr', 0x3, 0x3130, 0, 0x30303030 ), resp( 'wr', 0x3, 0,   0,  0          ),
    req( 'wr', 0x4, 0x4140, 0, 0x40404040 ), resp( 'wr', 0x4, 0,   0,  0          ),
    req( 'wr', 0x5, 0x5150, 0, 0x50505050 ), resp( 'wr', 0x5, 0,   0,  0          ),
    req( 'wr', 0x6, 0x6160, 0, 0x60606060 ), resp( 'wr', 0x6, 0,   0,  0          ),
    req( 'wr', 0x7, 0x7170, 0, 0x70707070 ), resp( 'wr', 0x7, 0,   0,  0          ),
    req( 'wr', 0x8, 0x8180, 0, 0x80808080 ), resp( 'wr', 0x8, 0,   0,  0          ),
    req( 'wr', 0x9, 0x9190, 0, 0x90909090 ), resp( 'wr', 0x9, 0,   0,  0          ),
    req( 'wr', 0xa, 0xa1a0, 0, 0xa0a0a0a0 ), resp( 'wr', 0xa, 0,   0,  0          ),
    req( 'wr', 0xb, 0xb1b0, 0, 0xb0b0b0b0 ), resp( 'wr', 0xb, 0,   0,  0          ),
    req( 'wr', 0xc, 0xc1c0, 0, 0xc0c0c0c0 ), resp( 'wr', 0xc, 0,   0,  0          ),
    req( 'wr', 0xd, 0xd1d0, 0, 0xd0d0d0d0 ), resp( 'wr', 0xd, 0,   0,  0          ),
    req( 'wr', 0xe, 0xe1e0, 0, 0xe0e0e0e0 ), resp( 'wr', 0xe, 0,   0,  0          ),
    req( 'wr', 0xf, 0xf1f0, 0, 0xf0f0f0f0 ), resp( 'wr', 0xf, 0,   0,  0          ),

    req( 'rd', 0x0, 0x0000, 0, 0          ), resp( 'rd', 0x0, 0,   0,  0x00000000 ), # Should all miss for direct mapped design
    req( 'rd', 0x1, 0x1010, 0, 0          ), resp( 'rd', 0x1, 0,   0,  0x01010101 ),
    req( 'rd', 0x2, 0x2020, 0, 0          ), resp( 'rd', 0x2, 0,   0,  0x02020202 ),
    req( 'rd', 0x3, 0x3030, 0, 0          ), resp( 'rd', 0x3, 0,   0,  0x03030303 ),
    req( 'rd', 0x4, 0x4040, 0, 0          ), resp( 'rd', 0x4, 0,   0,  0x04040404 ),
    req( 'rd', 0x5, 0x5050, 0, 0          ), resp( 'rd', 0x5, 0,   0,  0x05050505 ),
    req( 'rd', 0x6, 0x6060, 0, 0          ), resp( 'rd', 0x6, 0,   0,  0x06060606 ),
    req( 'rd', 0x7, 0x7070, 0, 0          ), resp( 'rd', 0x7, 0,   0,  0x07070707 ),
    req( 'rd', 0x8, 0x8080, 0, 0          ), resp( 'rd', 0x8, 0,   0,  0x08080808 ),
    req( 'rd', 0x9, 0x9090, 0, 0          ), resp( 'rd', 0x9, 0,   0,  0x09090909 ),
    req( 'rd', 0xa, 0xa0a0, 0, 0          ), resp( 'rd', 0xa, 0,   0,  0x0a0a0a0a ),
    req( 'rd', 0xb, 0xb0b0, 0, 0          ), resp( 'rd', 0xb, 0,   0,  0x0b0b0b0b ),
    req( 'rd', 0xc, 0xc0c0, 0, 0          ), resp( 'rd', 0xc, 0,   0,  0x0c0c0c0c ),
    req( 'rd', 0xd, 0xd0d0, 0, 0          ), resp( 'rd', 0xd, 0,   0,  0x0d0d0d0d ),
    req( 'rd', 0xe, 0xe0e0, 0, 0          ), resp( 'rd', 0xe, 0,   0,  0x0e0e0e0e ),
    req( 'rd', 0xf, 0xf0f0, 0, 0          ), resp( 'rd', 0xf, 0,   0,  0x0f0f0f0f ),
  ]

test_case_table_dmap = mk_test_case_table([
  (                                                         "msg_func                                                 mem_data_func stall lat src sink"),
  # Write hit path for dirty line + Read miss path for dirty line + Stress entire cache
  [ "write_hit_dirty_read_miss_dirty_all_cacheline_dmap",   write_hit_dirty_read_miss_dirty_all_cacheline_dmap,       None,         0.0,  0,  0,  0    ],

])

@pytest.mark.parametrize( **test_case_table_dmap )
def test_dmap( test_params, cmdline_opts ):
  run_test( CacheFL(), test_params, cmdline_opts, cmp_wo_test_field )

#-------------------------------------------------------------------------
# Test Cases for Set Associative
#-------------------------------------------------------------------------

def write_miss_read_hit_dirty_all_cacheline_sassoc():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    # Way 0
    req( 'wr', 0x0, 0x0000, 0, 0x00000000 ), resp( 'wr', 0x0, 0,   0,  0          ),
    req( 'wr', 0x1, 0x1010, 0, 0x01010101 ), resp( 'wr', 0x1, 0,   0,  0          ),
    req( 'wr', 0x2, 0x2020, 0, 0x02020202 ), resp( 'wr', 0x2, 0,   0,  0          ),
    req( 'wr', 0x3, 0x3030, 0, 0x03030303 ), resp( 'wr', 0x3, 0,   0,  0          ),
    req( 'wr', 0x4, 0x4040, 0, 0x04040404 ), resp( 'wr', 0x4, 0,   0,  0          ),
    req( 'wr', 0x5, 0x5050, 0, 0x05050505 ), resp( 'wr', 0x5, 0,   0,  0          ),
    req( 'wr', 0x6, 0x6060, 0, 0x06060606 ), resp( 'wr', 0x6, 0,   0,  0          ),
    req( 'wr', 0x7, 0x7070, 0, 0x07070707 ), resp( 'wr', 0x7, 0,   0,  0          ),

    # Way 1
    req( 'wr', 0x0, 0x0100, 0, 0x00000000 ), resp( 'wr', 0x0, 0,   0,  0          ),
    req( 'wr', 0x1, 0x1110, 0, 0x10101010 ), resp( 'wr', 0x1, 0,   0,  0          ),
    req( 'wr', 0x2, 0x2120, 0, 0x20202020 ), resp( 'wr', 0x2, 0,   0,  0          ),
    req( 'wr', 0x3, 0x3130, 0, 0x30303030 ), resp( 'wr', 0x3, 0,   0,  0          ),
    req( 'wr', 0x4, 0x4140, 0, 0x40404040 ), resp( 'wr', 0x4, 0,   0,  0          ),
    req( 'wr', 0x5, 0x5150, 0, 0x50505050 ), resp( 'wr', 0x5, 0,   0,  0          ),
    req( 'wr', 0x6, 0x6160, 0, 0x60606060 ), resp( 'wr', 0x6, 0,   0,  0          ),
    req( 'wr', 0x7, 0x7170, 0, 0x70707070 ), resp( 'wr', 0x7, 0,   0,  0          ),

    req( 'rd', 0x0, 0x0000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0x00000000 ), # Should all still hit for 2 way set-assoc design
    req( 'rd', 0x1, 0x1010, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0x01010101 ),
    req( 'rd', 0x2, 0x2020, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x02020202 ),
    req( 'rd', 0x3, 0x3030, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0x03030303 ),
    req( 'rd', 0x4, 0x4040, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0x04040404 ),
    req( 'rd', 0x5, 0x5050, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0x05050505 ),
    req( 'rd', 0x6, 0x6060, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0x06060606 ),
    req( 'rd', 0x7, 0x7070, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0x07070707 ),
  ]

def write_miss_clean_read_hit_dirty_all_cacheline_sassoc():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x0000, 0, 0x00000000 ), resp( 'in', 0x0, 0,   0,  0          ),
    req( 'in', 0x1, 0x1010, 0, 0x01010101 ), resp( 'in', 0x1, 0,   0,  0          ),
    req( 'in', 0x2, 0x1020, 0, 0x02020202 ), resp( 'in', 0x2, 0,   0,  0          ),
    req( 'in', 0x3, 0x1030, 0, 0x03030303 ), resp( 'in', 0x3, 0,   0,  0          ),
    req( 'in', 0x4, 0x1040, 0, 0x04040404 ), resp( 'in', 0x4, 0,   0,  0          ),
    req( 'in', 0x5, 0x1050, 0, 0x05050505 ), resp( 'in', 0x5, 0,   0,  0          ),
    req( 'in', 0x6, 0x1060, 0, 0x06060606 ), resp( 'in', 0x6, 0,   0,  0          ),
    req( 'in', 0x7, 0x1070, 0, 0x07070707 ), resp( 'in', 0x7, 0,   0,  0          ),

    req( 'wr', 0x0, 0x1100, 0, 0x00000000 ), resp( 'wr', 0x0, 0,   0,  0          ), # This set repeats indices for above
    req( 'wr', 0x1, 0x1110, 0, 0x10101010 ), resp( 'wr', 0x1, 0,   0,  0          ),
    req( 'wr', 0x2, 0x1120, 0, 0x20202020 ), resp( 'wr', 0x2, 0,   0,  0          ),
    req( 'wr', 0x3, 0x1130, 0, 0x30303030 ), resp( 'wr', 0x3, 0,   0,  0          ),
    req( 'wr', 0x4, 0x1140, 0, 0x40404040 ), resp( 'wr', 0x4, 0,   0,  0          ),
    req( 'wr', 0x5, 0x1150, 0, 0x50505050 ), resp( 'wr', 0x5, 0,   0,  0          ),
    req( 'wr', 0x6, 0x1160, 0, 0x60606060 ), resp( 'wr', 0x6, 0,   0,  0          ),
    req( 'wr', 0x7, 0x1170, 0, 0x70707070 ), resp( 'wr', 0x7, 0,   0,  0          ),

    req( 'rd', 0x0, 0x0000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0x00000000 ), # Should all hit for 2 way set assoc design
    req( 'rd', 0x1, 0x1010, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0x01010101 ), # and data should be different
    req( 'rd', 0x2, 0x1020, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x02020202 ),
    req( 'rd', 0x3, 0x1030, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0x03030303 ),
    req( 'rd', 0x4, 0x1040, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0x04040404 ),
    req( 'rd', 0x5, 0x1050, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0x05050505 ),
    req( 'rd', 0x6, 0x1060, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0x06060606 ),
    req( 'rd', 0x7, 0x1070, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0x07070707 ),
  ]

def lru_bit_single_cacheline_sassoc():
  return [
    req( 'wr', 0x0, 0x0100, 0, 0x00000000 ), resp( 'wr', 0x0, 0,   0,  0          ), # Set 0 Way 0. Set 0 LRU is now 1
    req( 'wr', 0x0, 0x1100, 0, 0x00001111 ), resp( 'wr', 0x0, 0,   0,  0          ), # Set 0 Way 1. Set 0 LRU is now 0

    # This should evict Set 0 Way 0.
    req( 'wr', 0x3, 0x2100, 0, 0x20202020 ), resp( 'wr', 0x3, 0,   0,  0          ),
    # Read for what should be in Set 0 Way 1. It should be a hit to show that it is not evicted in the last instruction.
    req( 'rd', 0x3, 0x1100, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0x00001111 ),
  ]

def lru_bit_multi_cacheline_sassoc():
  return [
    req( 'wr', 0x0, 0x0100, 0, 0x00000000 ), resp( 'wr', 0x0, 0,   0,  0          ), # Set 0 Way 0. Set 0 LRU is now 1
    req( 'wr', 0x0, 0x1100, 0, 0x00001111 ), resp( 'wr', 0x0, 0,   0,  0          ), # Set 0 Way 1. Set 0 LRU is now 0

    req( 'wr', 0x1, 0x0110, 0, 0x10101010 ), resp( 'wr', 0x1, 0,   0,  0          ), # Set 1 Way 0. Set 1 LRU is now 1
    req( 'wr', 0x1, 0x1110, 0, 0x11110000 ), resp( 'wr', 0x1, 0,   0,  0          ), # Set 1 Way 0. Set 1 LRU is now 0

    req( 'rd', 0x2, 0x0110, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x10101010 ), # Set 1 Way 0. Set 1 LRU is now 1

    # This should evict Set 0 Way 0. If it uses Way 1, it means that the LRU bit is not stored correctly and independently between cache lines
    req( 'wr', 0x3, 0x2100, 0, 0x20202020 ), resp( 'wr', 0x3, 0,   0,  0          ),
    # Read for what should be in Set 0 Way 1. It should be a hit to show that it is not evicted in the last instruction.
    req( 'rd', 0x3, 0x1100, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0x00001111 ),
  ]

test_case_table_sassoc = mk_test_case_table([
  (                                                           "msg_func                                                 mem_data_func    stall lat src sink"),

  # Write miss with refill, no eviction + read hit for dirty line + Stress test entire cache
  [ "write_miss_read_hit_dirty_all_cacheline_sassoc",         write_miss_read_hit_dirty_all_cacheline_sassoc,           None,         0.0,  0,  0,  0    ],
  [ "write_miss_clean_read_hit_dirty_all_cacheline_sassoc",   write_miss_clean_read_hit_dirty_all_cacheline_sassoc,     data_8192B,   0.0,  0,  0,  0    ],

  # LRU bit basic testing
  [ "lru_bit_single_cacheline_sassoc",                        lru_bit_single_cacheline_sassoc,                          None,         0.0,  0,  0,  0    ],

  # Test to make sure that the LRU is correctly maintained independently for each cache line, when multiple cache lines are used
  [ "lru_bit_multi_cacheline_sassoc",                         lru_bit_multi_cacheline_sassoc,                           None,         0.0,  0,  0,  0    ],
])

@pytest.mark.parametrize( **test_case_table_sassoc )
def test_sassoc( test_params, cmdline_opts ):
  run_test( CacheFL(), test_params, cmdline_opts, cmp_wo_test_field )

#-------------------------------------------------------------------------
# Banked cache test
#-------------------------------------------------------------------------
# This test case is to test if the bank offset is implemented correctly.
# The idea behind this test case is to differentiate between a cache with
# no bank bits and a design has one/two bank bits by looking at cache
# request hit/miss status.

# We first design a test case for 2-way set-associative cache. The last
# request should hit only if students implement the correct index bit to
# be [6:9]. If they implement the index bit to be [4:7] or [5:8], the
# last request is a miss, which is wrong. See below for explanation. This
# test case also works for the baseline direct-mapped cache.

# Direct-mapped
#
#   no bank(should fail):
#      idx
#   00 0000 0000
#   01 0000 0000
#   10 0000 0000
#   00 0000 0000
#   idx: 0, 0, 0 so the third one with tag 10 will evict the first one
#   with tag 00, and thus the fourth read will miss instead of hit.
#
#   4-bank(correct):
#    idx  bk
#   00 00 00 0000
#   01 00 00 0000
#   10 00 00 0000
#   00 00 00 0000
#   idx: 0, 4, 8 so the third one with tag 10 won't evict anything, and
#   thus the fourth read will hit.

# 2-way set-associative
#
#   no bank(should fail):
#        idx
#   00 0 000 0000
#   01 0 000 0000
#   10 0 000 0000
#   00 0 000 0000
#   idx: 0, 0, 0 so the third one with tag 10 will evict the first one
#   with tag 00, and thus the fourth read will miss instead of hit.
#
#   4-bank(correct):
#     idx  bk
#   0 0 00 00 0000
#   0 1 00 00 0000
#   1 0 00 00 0000
#   idx: 0, 4, 0 so the third one with tag 10 won't evict anything, and
#   thus the fourth read will hit.

def bank_test():
  return [
    #    type  opq  addr       len data                type  opq  test len data
    req( 'rd', 0x0, 0x00000000, 0, 0 ), resp( 'rd', 0x0, 0,   0,  0xdeadbeef ),
    req( 'rd', 0x1, 0x00000100, 0, 0 ), resp( 'rd', 0x1, 0,   0,  0x00c0ffee ),
    req( 'rd', 0x2, 0x00000200, 0, 0 ), resp( 'rd', 0x2, 0,   0,  0xffffffff ),
    req( 'rd', 0x3, 0x00000000, 0, 0 ), resp( 'rd', 0x3, 1,   0,  0xdeadbeef ),
  ]

def bank_test_data():
  return [
    # addr      data (in int)
    0x00000000, 0xdeadbeef,
    0x00000100, 0x00c0ffee,
    0x00000200, 0xffffffff,
  ]

test_case_table_bank = mk_test_case_table([
  (             "msg_func   mem_data_func   stall lat src sink"),
  [ "bank_test", bank_test, bank_test_data, 0.0,  0,  0,  0    ],

])

@pytest.mark.parametrize( **test_case_table_bank )
def test_bank( test_params, cmdline_opts ):
  run_test( CacheFL(), test_params, cmdline_opts, cmp_wo_test_field )
