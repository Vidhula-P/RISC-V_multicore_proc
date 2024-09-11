
#=========================================================================
# VIntMulAlt_noparam_v.py
#=========================================================================
"""Provide a template of PyMTL wrapper to import verilated models.

This wrapper makes a Verilator-generated C++ model appear as if it were a
normal PyMTL model. This template is based on PyMTL v2.
"""

import copy
import os
import gc
import weakref

from cffi import FFI

from pymtl3.datatypes import *
from pymtl3.dsl import Component, connect, InPort, OutPort, Wire, update, update_ff

#-------------------------------------------------------------------------
# IntMulAlt_noparam
#-------------------------------------------------------------------------

class IntMulAlt_noparam( Component ):
  id_ = 0

  def __init__( s, *args, **kwargs ):
    s._finalization_count = 0

    # initialize FFI, define the exposed interface
    s.ffi = FFI()
    s.ffi.cdef("""
      typedef struct {

        // Exposed port interface
        uint8_t * clk;        
        uint8_t * reset;        
        uint64_t * istream_msg;        
        uint8_t * istream_rdy;        
        uint8_t * istream_val;        
        uint32_t * ostream_msg;        
        uint8_t * ostream_rdy;        
        uint8_t * ostream_val;

        // Verilator model
        void * _cffi_model;

        // Verilator simulation context
        void * _cffi_context_ptr;

        // VCD state
        int _cffi_vcd_en;

        // VCD tracing helpers
        void *       _cffi_tfp;
        unsigned int _cffi_trace_time;

        // Verilog line trace buffer
        char _cffi_line_trace_str[512];

      } VIntMulAlt_noparam_t;

      VIntMulAlt_noparam_t * VIntMulAlt_noparam_create_model( const char * );
      void VIntMulAlt_noparam_destroy_model( VIntMulAlt_noparam_t *);
      void VIntMulAlt_noparam_comb_eval( VIntMulAlt_noparam_t * );
      void VIntMulAlt_noparam_seq_eval( VIntMulAlt_noparam_t * );
      void VIntMulAlt_noparam_assert_on( VIntMulAlt_noparam_t *, bool );
      bool VIntMulAlt_noparam_has_assert_fired( VIntMulAlt_noparam_t * );
      void VIntMulAlt_noparam_line_trace( VIntMulAlt_noparam_t *, char * );

    """)

    # Print the modification time stamp of the shared lib
    # print('Modification time of {}: {}'.format(
    #       'libIntMulAlt_noparam_v.so', os.path.getmtime( './libIntMulAlt_noparam_v.so' ) ))

    # Import the shared library containing the model. We defer
    # construction to the elaborate_logic function to allow the user to
    # set the vcd_file.
    # NOTE: the RTLD_NODELETE flag is necessary in this dlopen() to make sure
    # all loaded shared libraries stick to the current processes (i.e., cannot
    # be unloaded) until the exit of the main process. This behavior is necessary
    # to avoid segfaults at exits due to destruction of thread-local variables,
    # which are heavily used in Verilator's runtime library.
    s._ffi_inst = s.ffi.dlopen('./libIntMulAlt_noparam_v.so', s.ffi.RTLD_NODELETE | s.ffi.RTLD_NOW)

    # increment instance count
    IntMulAlt_noparam.id_ += 1

  def finalize( s ):
    """Finalize the imported component.

    This method closes the shared library opened through CFFI. If an imported
    component is not finalized explicitly (i.e. if you rely on GC to collect a
    no longer used imported component), importing a component with the same
    name before all previous imported components are GCed might lead to
    confusing behaviors. This is because once opened, the shared lib
    is cached by the OS until the OS reference counter for this lib reaches
    0 (you can decrement the reference counter by calling `dl_close()` syscall).

    Fortunately real designs tend to always have the same shared lib corresponding
    to the components with the same name. If you are doing translation testing and
    use the same component class name even if they refer to different designs,
    you might need to call `imported_object.finalize()` at the end of each test
    to ensure correct behaviors.
    """
    # print(f"In finalize() method of an instance of {str(s.__class__)}")
    assert s._finalization_count == 0,      'Imported component can only be finalized once!'
    s._finalization_count += 1

    # Clean up python side FFI references
    s._convert_string = None

    s._ffi_inst.VIntMulAlt_noparam_destroy_model( s._ffi_m )
    # print("End of finalize()")

  def __del__( s ):
    # print(f"In __del__() method of an instance of {str(s.__class__)}")
    if s._finalization_count == 0:
      s._finalization_count += 1

      # Clean up python side FFI references
      s._convert_string = None

      s._ffi_inst.VIntMulAlt_noparam_destroy_model( s._ffi_m )
    # print("End of __del__")

  def construct( s, *args, **kwargs ):
    # Set up the VCD file name
    verilator_vcd_file = ""
    if 0:
      if False:
        verilator_vcd_file = ".verilator1.vcd"
      else:
        verilator_vcd_file = "IntMulAlt_noparam.verilator1.vcd"

    # Convert string to `bytes` which is required by CFFI on python 3
    verilator_vcd_file = verilator_vcd_file.encode('ascii')

    # Construct the model
    # PP: we need to keep the new'ed object alive by assigning it to
    # a variable. See more about this:
    # https://cffi.readthedocs.io/en/stable/ref.html#ffi-new
    ffi_vl_vcd_file = s.ffi.new("char[]", verilator_vcd_file)
    s._ffi_m = s._ffi_inst.VIntMulAlt_noparam_create_model( ffi_vl_vcd_file )

    # Buffer for line tracing
    s._convert_string = s.ffi.string

    # Use non-attribute varialbe to reduce CPython bytecode count
    _ffi_m = s._ffi_m
    _ffi_inst_comb_eval = s._ffi_inst.VIntMulAlt_noparam_comb_eval
    _ffi_inst_seq_eval  = s._ffi_inst.VIntMulAlt_noparam_seq_eval

    # declare the port interface
    s.istream = IStreamIfc( Bits64 )
    s.ostream = OStreamIfc( Bits32 )

    # update blocks that converts ffi interface to/from pymtl ports
    
    s.s_DOT_reset = Wire( Bits1 )
    @update
    def isignal_s_DOT_reset():
      s.s_DOT_reset @= s.reset
    
    s.s_DOT_istream_DOT_msg = Wire( Bits64 )
    @update
    def isignal_s_DOT_istream_DOT_msg():
      s.s_DOT_istream_DOT_msg @= s.istream.msg
    
    s.s_DOT_istream_DOT_val = Wire( Bits1 )
    @update
    def isignal_s_DOT_istream_DOT_val():
      s.s_DOT_istream_DOT_val @= s.istream.val
    
    s.s_DOT_ostream_DOT_rdy = Wire( Bits1 )
    @update
    def isignal_s_DOT_ostream_DOT_rdy():
      s.s_DOT_ostream_DOT_rdy @= s.ostream.rdy
    
    s.s_DOT_istream_DOT_rdy = Wire( Bits1 )
    @update
    def osignal_s_DOT_istream_DOT_rdy():
      s.istream.rdy @= s.s_DOT_istream_DOT_rdy
    
    s.s_DOT_ostream_DOT_msg = Wire( Bits32 )
    @update
    def osignal_s_DOT_ostream_DOT_msg():
      s.ostream.msg @= s.s_DOT_ostream_DOT_msg
    
    s.s_DOT_ostream_DOT_val = Wire( Bits1 )
    @update
    def osignal_s_DOT_ostream_DOT_val():
      s.ostream.val @= s.s_DOT_ostream_DOT_val

    @update
    def comb_upblk():

      # Set inputs
      
      _ffi_m.reset[0] = int(s.s_DOT_reset)
      
      _ffi_m.istream_msg[0] = int(s.s_DOT_istream_DOT_msg)
      
      _ffi_m.istream_val[0] = int(s.s_DOT_istream_DOT_val)
      
      _ffi_m.ostream_rdy[0] = int(s.s_DOT_ostream_DOT_rdy)

      _ffi_inst_comb_eval( _ffi_m )

      # Write all outputs
      
      s.s_DOT_istream_DOT_rdy @= _ffi_m.istream_rdy[0]
      
      s.s_DOT_ostream_DOT_msg @= _ffi_m.ostream_msg[0]
      
      s.s_DOT_ostream_DOT_val @= _ffi_m.ostream_val[0]

    @update_ff
    def seq_upblk():
      # seq_eval will automatically tick clock in C land
      _ffi_inst_seq_eval( _ffi_m )

      if s._ffi_inst.VIntMulAlt_noparam_has_assert_fired( _ffi_m ):
        raise AssertionError("A Verilog assertion fired in the Verilator simulation!")

  def assert_on( s, enable ):
    assert isinstance( enable, bool )
    s._ffi_inst.VIntMulAlt_noparam_assert_on( s._ffi_m, enable )

  def line_trace( s ):
    if 1:
      s._ffi_inst.VIntMulAlt_noparam_line_trace( s._ffi_m, s._ffi_m._cffi_line_trace_str )
      return s._convert_string( s._ffi_m._cffi_line_trace_str ).decode('ascii')
    else:
      return f' clk={s.clk}, reset={s.reset}, istream.msg={s.istream.msg}, istream.rdy={s.istream.rdy}, istream.val={s.istream.val}, ostream.msg={s.ostream.msg}, ostream.rdy={s.ostream.rdy}, ostream.val={s.ostream.val},'

  def internal_line_trace( s ):
    return ''
