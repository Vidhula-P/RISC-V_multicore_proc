#=========================================================================
# MultiCoreSysFL_mem_test.py
#=========================================================================
# This is where you should include directed tests meant to specifically
# stress the multicore memory system. So focus on tests with different
# load/store access patterns, but keep in mind that different cores
# should not load/store the same word! If two cores load, modify, store
# different values to the same address there is no guarantee what the
# final correct result should be. This is a "race condition". You
# _should_ include tests where multiple cores are accessing different
# words on the same cache line. Random testing is also great to help
# stress the multicore memory system.

import pytest

from pymtl3 import *

from lab4_sys.test.harness import asm_test
from lab4_sys.test.harness import run_mcore_test as run_test

from lab4_sys.MultiCoreSysFL import MultiCoreSysFL

from lab4_sys.test  import inst_mem_mcore

#-------------------------------------------------------------------------
# Tests
#-------------------------------------------------------------------------

@pytest.mark.usefixtures("cmdline_opts")
class Tests:

  @classmethod
  def setup_class( cls ):
    cls.SysType = MultiCoreSysFL

  #-----------------------------------------------------------------------
  # mem_mcore
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_mem_mcore.gen_basic_test     ),
    asm_test( inst_mem_mcore.add_diff_cores ),
    asm_test( inst_mem_mcore.lw_sw_multicore ),
    asm_test( inst_mem_mcore.same_cache_line ),
    asm_test( inst_mem_mcore.adjacent_addr ),
    asm_test( inst_mem_mcore.alt_read_write ),
    asm_test( inst_mem_mcore.alt_write_read ),
    asm_test( inst_mem_mcore.non_aligned ),
  ])
  def test_mem_mcore( s, name, test ):
    run_test( s.SysType, test, cmdline_opts=s.__class__.cmdline_opts )
    
  # Random stall and delay

  def test_mem_mcore_delays( s ):
    run_test( s.SysType, inst_mem_mcore.gen_basic_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )
