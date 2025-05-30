#=========================================================================
# CacheAlt_test.py
#=========================================================================

import pytest

from pymtl3 import *

from lab3_mem.test.harness      import run_test
from lab3_mem.test.CacheFL_test import \
  ( test_case_table_generic, test_case_table_random,
    test_case_table_sassoc, test_case_table_bank, cmp_wo_test_field )

from lab3_mem.CacheAlt         import CacheAlt

#-------------------------------------------------------------------------
# Generic tests for both baseline and alternative design
#-------------------------------------------------------------------------

@pytest.mark.parametrize( **test_case_table_generic )
def test_generic( test_params, cmdline_opts ):
  run_test( CacheAlt(), test_params, cmdline_opts )

#-------------------------------------------------------------------------
# Random tests for both baseline and alternative design
#-------------------------------------------------------------------------

@pytest.mark.parametrize( **test_case_table_random )
def test_random( test_params, cmdline_opts ):
  run_test( CacheAlt(), test_params, cmdline_opts, cmp_wo_test_field )

#-------------------------------------------------------------------------
# Tests for just alternative design
#-------------------------------------------------------------------------

@pytest.mark.parametrize( **test_case_table_sassoc )
def test_sassoc( test_params, cmdline_opts ):
  run_test( CacheAlt(), test_params, cmdline_opts )

#-------------------------------------------------------------------------
# Tests for banking
#-------------------------------------------------------------------------

@pytest.mark.parametrize( **test_case_table_bank )
def test_bank( test_params, cmdline_opts ):
  run_test( CacheAlt(p_num_banks=4), test_params, cmdline_opts )

