#=========================================================================
# extra multicore memory tests
#=========================================================================

import random

# Fix the random seed so results are reproducible
random.seed(0xdeadbeef)

from pymtl3 import *

#-------------------------------------------------------------------------
# Basic test
#-------------------------------------------------------------------------

def gen_basic_test():
  return """
    csrr x1, mngr2proc < {0x00002000,0x00002004,0x00002008,0x0000200c}
    csrr x2, mngr2proc < {0x0a0b0c0d,0x1a1b1c1d,0x2a2b2c2d,0x3a3b3c3d}
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    sw   x2, 0(x1)
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    lw   x3, 0(x1)
    csrw proc2mngr, x3 > {0x0a0b0c0d,0x1a1b1c1d,0x2a2b2c2d,0x3a3b3c3d}

    .data
    .word 0x01020304
    .word 0x11121314
    .word 0x21222324
    .word 0x31323334
  """

#-------------------------------------------------------------------------
# Elements of array added over different cores
#-------------------------------------------------------------------------

def add_diff_cores():
  return """
  csrr x2, mngr2proc < {1,2,3,4} # Core-specific initialization
  csrr x3, mngr2proc < {2,3,4,5} 
  add x4, x2, x3
  csrw proc2mngr, x4 > {3,5,7,9} # Verifying core-specific 
  
  """
#-------------------------------------------------------------------------
# Test where each core loads from one address and stores to a separate address,
#    ensuring no overlapping regions to avoid race conditions
#-------------------------------------------------------------------------

def lw_sw_multicore():
    return """
    csrr x1, mngr2proc < {0x00003000, 0x00003010, 0x00003020, 0x00003030} # Load addresses
    csrr x2, mngr2proc < {0x00004000, 0x00004010, 0x00004020, 0x00004030} # Store addresses
    csrr x3, mngr2proc < {0xdeadbeef, 0xabadcafe, 0x12345678, 0xabcdef12} # Data to store

    lw   x4, 0(x1)                                                      # Load unused value
    sw   x3, 0(x2)                                                      # Store new value
    lw   x5, 0(x2)                                                      # Reload stored value
    csrw proc2mngr, x5 > {0xdeadbeef, 0xabadcafe, 0x12345678, 0xabcdef12} # Verify stored data

    .data
    .word 0x01010101
    .word 0x02020202
    .word 0x03030303
    .word 0x04040404
    """

#-------------------------------------------------------------------------
# Accessing different words in the same cache line
#-------------------------------------------------------------------------

def same_cache_line():
    return """
    csrr x1, mngr2proc < {0x00005000, 0x00005004, 0x00005008, 0x0000500c} # Addresses in same cache line
    csrr x2, mngr2proc < {0x11111111, 0x22222222, 0x33333333, 0x44444444} # Data to write

    sw   x2, 0(x1)                                                      # Store data
    lw   x3, 0(x1)                                                      # Load data
    csrw proc2mngr, x3 > {0x11111111, 0x22222222, 0x33333333, 0x44444444} # Verify data

    .data
    .word 0x00000000
    .word 0x00000000
    .word 0x00000000
    .word 0x00000000
    """

#-------------------------------------------------------------------------
# Cores write to adjacent cache lines to stress cache line boundary handling
#-------------------------------------------------------------------------

def adjacent_addr():
    return """
    csrr x1, mngr2proc < {0x00007000, 0x00007010, 0x00007020, 0x00007030} # Cache line boundaries
    csrr x2, mngr2proc < {0x12312312, 0x45645645, 0x78978978, 0xabcabcab} # Data to write

    sw   x2, 0(x1)                                                      # Store data
    lw   x3, 0(x1)                                                      # Reload data
    csrw proc2mngr, x3 > {0x12312312, 0x45645645, 0x78978978, 0xabcabcab} # Verify data

    .data
    .word 0x00000000
    .word 0x00000000
    .word 0x00000000
    .word 0x00000000
    """

#-------------------------------------------------------------------------
# Cores write and read alternately
#-------------------------------------------------------------------------

def alt_read_write():
    """
    Test with interleaved access patterns where cores write and read alternately.
    """
    return """
    csrr x1, mngr2proc < {0x00008000, 0x00008010, 0x00008020, 0x00008030} # Memory regions
    csrr x2, mngr2proc < {0xdeadbeef, 0xabadcafe, 0x12345678, 0xabcdef12} # Data to write

    sw   x2, 0(x1)                                                      # Core writes
    lw   x3, 0(x1)                                                      # Core reads
    csrw proc2mngr, x3 > {0xdeadbeef, 0xabadcafe, 0x12345678, 0xabcdef12} # Verify data
    sw   x3, 0(x1)                                                      # Core writes back
    lw   x4, 0(x1)                                                      # Core re-reads
    csrw proc2mngr, x4 > {0xdeadbeef, 0xabadcafe, 0x12345678, 0xabcdef12} # Verify re-read

    .data
    .word 0x00000000
    .word 0x00000000
    .word 0x00000000
    .word 0x00000000
    """

#-------------------------------------------------------------------------
# Cores read and write alternately
#-------------------------------------------------------------------------

def alt_write_read():
  """
  Test with interleaved access patterns where cores write and read alternately.
  """
  return """
  csrr x1, mngr2proc < {0x0000A000, 0x0000A010, 0x0000A020, 0x0000A030} # Memory regions (cold cache)
  csrr x2, mngr2proc < {0xdeadbeef, 0xabadcafe, 0x12345678, 0xabcdef12} # Data to write

  lw   x3, 0(x1)                                                      # Core reads
  sw   x2, 0(x1)                                                      # Core writes
  csrw proc2mngr, x3 > {0x00000000, 0x00000000, 0x00000000, 0x00000000} # Verify data- default value of x1 stored in x3
  lw   x4, 0(x1)                                                      # Core re-reads
  sw   x3, 0(x1)                                                      # Core writes back
  csrw proc2mngr, x4 > {0xdeadbeef, 0xabadcafe, 0x12345678, 0xabcdef12} # Verify re-read- values changed but still out-of-sync

  .data
  .word 0x00000000
  .word 0x00000000
  .word 0x00000000
  .word 0x00000000
  """

#-------------------------------------------------------------------------
# Cores write to non-aligned addresses
#-------------------------------------------------------------------------
def non_aligned():
    return """
    csrr x1, mngr2proc < {0x0000a001, 0x0000a005, 0x0000a009, 0x0000a00d} # Unaligned addresses
    csrr x2, mngr2proc < {0x11111111, 0x22222222, 0x33333333, 0x44444444} # Data to write

    sw   x2, 0(x1)                                                      # Store data
    lw   x3, 0(x1)                                                      # Reload data
    csrw proc2mngr, x3 > {0x11111111, 0x22222222, 0x33333333, 0x44444444} # Verify data

    .data
    .word 0x00000000
    .word 0x00000000
    .word 0x00000000
    .word 0x00000000
    """