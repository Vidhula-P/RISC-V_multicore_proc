#=========================================================================
# ProcBase_rr_test.py
#=========================================================================
# It is as simple as inheriting from FL tests and change the ProcType.

from lab2_proc.ProcBase import ProcBase
from lab2_proc.test.ProcFL_rr_test import Tests as ProcFL_rr_TestsBaseClass

#-------------------------------------------------------------------------
# Tests
#-------------------------------------------------------------------------

class Tests( ProcFL_rr_TestsBaseClass ):

  @classmethod
  def setup_class( cls ):
    cls.ProcType = ProcBase

