#=========================================================================
# ProcFL_jump_test.py
#=========================================================================
# We group all our test cases into a class so that we can easily reuse
# these test cases in our RTL tests. We can simply inherit from this test
# class, overload the setup_class method, and set the ProcType
# appropriately.

import pytest

from pymtl3 import *
from lab2_proc.test.harness import asm_test, run_test
from lab2_proc.ProcFL import ProcFL

from lab2_proc.test import inst_jal
from lab2_proc.test import inst_jalr

#-------------------------------------------------------------------------
# Tests
#-------------------------------------------------------------------------

@pytest.mark.usefixtures("cmdline_opts")
class Tests:

  @classmethod
  def setup_class( cls ):
    cls.ProcType = ProcFL

  #-----------------------------------------------------------------------
  # jal
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_jal.gen_basic_test                     ) ,
    asm_test( inst_jal.gen_jal_nested_test                ) ,
    asm_test( inst_jal.gen_jal_imm_test                   ) ,
    asm_test( inst_jal.gen_jal_no_return_test             ) ,
    asm_test( inst_jal.gen_jal_with_branch_taken_test     ) ,
    asm_test( inst_jal.gen_jal_with_branch_not_taken_test ) ,
    asm_test( inst_jal.gen_jal_function_call_test         ) ,
    asm_test( inst_jal.gen_jal_dep_tests                  ) ,
    asm_test( inst_jal.gen_jal_large_offset_tests         ) ,
    asm_test( inst_jal.gen_jal_random_tests               ) ,
  ])

  def test_jal( s, name, test ):
    run_test( s.ProcType, test, cmdline_opts=s.__class__.cmdline_opts )

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # random stall and delay
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

  #-----------------------------------------------------------------------
  # jalr
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_jalr.gen_basic_test    ),
    asm_test( inst_jalr.gen_jalr_imm_test ),
    asm_test( inst_jalr.gen_jalr_nested_test ),
    asm_test( inst_jalr.gen_jalr_no_return_test ),
    asm_test( inst_jalr.gen_jalr_with_branch_not_taken_test ),
    asm_test( inst_jalr.gen_jalr_with_branch_taken_test ),
    asm_test( inst_jalr.gen_jalr_function_call_test ),
  ])

  def test_jalr( s, name, test ):
    run_test( s.ProcType, test, cmdline_opts=s.__class__.cmdline_opts )

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # random stall and delay
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

