//========================================================================
// VIntMulAlt_noparam_v.cpp
//========================================================================
// This file provides a template for the C wrapper used in the import
// pass. The wrapper exposes a C interface to CFFI so that a
// Verilator-generated C++ model can be driven from Python.
// This templated is based on PyMTL v2.

#include "obj_dir_IntMulAlt_noparam/VIntMulAlt_noparam.h"
#include "stdio.h"
#include "stdint.h"
#include "verilated.h"
#include "verilated_vcd_c.h"

// set to true if the model has clk signal
#define HAS_CLK 1

// set to true when VCD tracing is enabled in Verilator
#define DUMP_VCD 0

// set to true to enable on-demand VCD dumping
#define ON_DEMAND_DUMP_VCD 0

// top level port to be used in on-demand VCD dumping; only dump vars when
// that port has a non-zero value.
#define ON_DEMAND_VCD_ENABLE 0

// set to true when Verilog module has line tracing
#define VLINETRACE 1

#if VLINETRACE
#include "obj_dir_IntMulAlt_noparam/VIntMulAlt_noparam__Syms.h"
#include "svdpi.h"
#endif

//------------------------------------------------------------------------
// CFFI Interface
//------------------------------------------------------------------------
// simulation methods and model interface ports exposed to CFFI

extern "C" {
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

    // The following variables have a _cffi_ prefix to avoid name conflicts
    // with the port names.

    // Verilator model
    void * _cffi_model;

    // Verilator simulation context
    void * _cffi_context_ptr;

    // VCD state
    int _cffi_vcd_en;

    // VCD tracing helpers. Note that these fields are not used if DUMP_VCD
    // is 0.
    void *        _cffi_tfp;
    unsigned int  _cffi_trace_time;

    // Verilog line trace buffer. Refer to the comments to the trace function
    // below for more details.
    char _cffi_line_trace_str[512];

  } VIntMulAlt_noparam_t;

  // Exposed methods
  VIntMulAlt_noparam_t * VIntMulAlt_noparam_create_model( const char * );
  void VIntMulAlt_noparam_destroy_model( VIntMulAlt_noparam_t *);
  void VIntMulAlt_noparam_comb_eval( VIntMulAlt_noparam_t * );
  void VIntMulAlt_noparam_seq_eval( VIntMulAlt_noparam_t * );
  void VIntMulAlt_noparam_assert_on( VIntMulAlt_noparam_t *, bool );
  bool VIntMulAlt_noparam_has_assert_fired( VIntMulAlt_noparam_t * );

  #if VLINETRACE
  void VIntMulAlt_noparam_line_trace( VIntMulAlt_noparam_t *, char * );
  #endif

}

//------------------------------------------------------------------------
// create_model()
//------------------------------------------------------------------------
// Construct a new verilator simulation, initialize interface signals
// exposed via CFFI, and setup VCD tracing if enabled.

VIntMulAlt_noparam_t * VIntMulAlt_noparam_create_model( const char *vcd_filename ) {

  VIntMulAlt_noparam_t  * m;
  VIntMulAlt_noparam * model;
  VerilatedContext     * context_ptr;

  context_ptr = new VerilatedContext;

  context_ptr->debug(0);
  context_ptr->randReset( 0 );
  context_ptr->randSeed( 0 );

  // We enable assertions by default. We also prevent Verilator from calling
  // the fatal std::abort() on error by default.
  context_ptr->assertOn(true);
  context_ptr->fatalOnError(false);

  m     = new VIntMulAlt_noparam_t;
  model = new VIntMulAlt_noparam(context_ptr);

  m->_cffi_model       = (void *) model;
  m->_cffi_context_ptr = (void *) context_ptr;

  // Enable tracing. We have added a feature where if the vcd_filename is
  // "" then we don't do any VCD dumping even if DUMP_VCD is true.

  m->_cffi_vcd_en = 0;
  #if DUMP_VCD
  if ( strlen( vcd_filename ) != 0 ) {
    m->_cffi_vcd_en = 1;
    context_ptr->traceEverOn( true );
    VerilatedVcdC * tfp = new VerilatedVcdC();

    model->trace( tfp, 99 );
    tfp->spTrace()->set_time_resolution( "10ps" );
    tfp->open( vcd_filename );

    m->_cffi_tfp        = (void *) tfp;
    m->_cffi_trace_time = 0;
  }
  #else
  m->_cffi_tfp = NULL;
  m->_cffi_trace_time = 0;
  #endif

  // initialize exposed model interface pointers
  m->clk = &model->clk;
  m->reset = &model->reset;
  m->istream_msg = &model->istream_msg;
  m->istream_rdy = &model->istream_rdy;
  m->istream_val = &model->istream_val;
  m->ostream_msg = &model->ostream_msg;
  m->ostream_rdy = &model->ostream_rdy;
  m->ostream_val = &model->ostream_val;

  return m;

}

//------------------------------------------------------------------------
// destroy_model()
//------------------------------------------------------------------------
// Finalize the Verilator simulation, close files, call destructors.

void VIntMulAlt_noparam_destroy_model( VIntMulAlt_noparam_t * m ) {

  #if VM_COVERAGE
    VerilatedCov::write( "coverage.dat" );
  #endif

  VIntMulAlt_noparam * model = (VIntMulAlt_noparam *) m->_cffi_model;
  VerilatedContext * context_ptr = (VerilatedContext *) m->_cffi_context_ptr;

  // finalize verilator simulation
  model->final();

  #if DUMP_VCD
  if ( m->_cffi_vcd_en ) {
    // printf("DESTROYING %d\n", m->_cffi_trace_time);
    VerilatedVcdC * tfp = (VerilatedVcdC *) m->_cffi_tfp;
    tfp->close();
    delete tfp;
  }
  #endif

  delete model;
  delete context_ptr;
  delete m;

}

//------------------------------------------------------------------------
// comb_eval()
//------------------------------------------------------------------------
// Simulate one time-step in the Verilated model.

void VIntMulAlt_noparam_comb_eval( VIntMulAlt_noparam_t * m ) {

  VIntMulAlt_noparam * model = (VIntMulAlt_noparam *) m->_cffi_model;

  // evaluate one time step
  model->eval();

  // Shunning: calling dump multiple times leads to unsuppressable warning
  //           under verilator 4.036
  // #if DUMP_VCD
  // if ( m->_cffi_vcd_en ) {
  //   // dump current signal values
  //   VerilatedVcdC * tfp = (VerilatedVcdC *) m->_cffi_tfp;
  //   tfp->dump( m->_cffi_trace_time );
  //   tfp->flush();
  // }
  // #endif

}

//------------------------------------------------------------------------
// seq_eval()
//------------------------------------------------------------------------
// Simulate the positive clock edge in the Verilated model.

void VIntMulAlt_noparam_seq_eval( VIntMulAlt_noparam_t * m ) {

  VIntMulAlt_noparam * model = (VIntMulAlt_noparam *) m->_cffi_model;
  VerilatedContext * context_ptr = (VerilatedContext *) m->_cffi_context_ptr;

  // evaluate one time cycle

  #if HAS_CLK
  model->clk = 0;
  #endif

  model->eval();

  #if DUMP_VCD
  if ( m->_cffi_vcd_en && (ON_DEMAND_VCD_ENABLE || !ON_DEMAND_DUMP_VCD) ) {

    // PP: this is hacky -- we want the waveform to look like all signals
    // except the CLK has toggled. We temporarily set the CLK signal
    // back to 1 (as if it has not toggled) and dump VCD.
    #if HAS_CLK
    model->clk = 1;
    #endif

    // dump current signal values
    VerilatedVcdC * tfp = (VerilatedVcdC *) m->_cffi_tfp;
    tfp->dump( m->_cffi_trace_time );
    tfp->flush();

    // PP: now that we have generated the VCD we need to set CLK back to 0.
    // We need to dump VCD again to register this clock toggle.
    m->_cffi_trace_time += 50;

    #if HAS_CLK
    model->clk = 0;
    #endif

    // This eval() here is necessary to propagate the CLK signal. All other
    // signals will not toggle.
    model->eval();

    tfp->dump( m->_cffi_trace_time );
    tfp->flush();

  }
  #endif

  #if HAS_CLK
  model->clk = 1;
  #endif

  model->eval();
  context_ptr->timeInc(1);

  #if DUMP_VCD
  if ( m->_cffi_vcd_en && (ON_DEMAND_VCD_ENABLE || !ON_DEMAND_DUMP_VCD) ) {

    // update simulation time only on clock toggle
    m->_cffi_trace_time += 50;

  }
  #endif
}

//------------------------------------------------------------------------
// assert_on()
//------------------------------------------------------------------------
// Enable or disable assertions controlled by --assert. Assertions are
// enabled by default.

void VIntMulAlt_noparam_assert_on( VIntMulAlt_noparam_t * m, bool enable ) {

  VerilatedContext * context_ptr = (VerilatedContext *) m->_cffi_context_ptr;

  context_ptr->assertOn(enable);

  // We prevent the fatal std::abort() call on assertion failure. Instead,
  // we query the error and finish status in the context pointer to determine
  // if an assertion has fired.
  context_ptr->fatalOnError(!enable);

}

//------------------------------------------------------------------------
// has_assert_fired()
//------------------------------------------------------------------------
// Return true if an assertion has fired in the current context.

bool VIntMulAlt_noparam_has_assert_fired( VIntMulAlt_noparam_t * m ) {

  VerilatedContext * context_ptr = (VerilatedContext *) m->_cffi_context_ptr;

  return context_ptr->gotError() && context_ptr->gotFinish();

}

//------------------------------------------------------------------------
// trace()
//------------------------------------------------------------------------
// Note that we assume a trace string buffer of 512 characters. This is
// assumed in a couple of places, including the Python wrapper template
// and the Verilog vc/trace.v code. So if we change it, we need to change
// it everywhere.

#if VLINETRACE
void VIntMulAlt_noparam_line_trace( VIntMulAlt_noparam_t * m, char* str ) {

  VIntMulAlt_noparam * model = (VIntMulAlt_noparam *) m->_cffi_model;

  const int nchars = 512;
  const int nwords = nchars/4;

  uint32_t words[nwords];
  words[0] = nchars-1;

  // Setup scope for accessing the line tracing function throug DPI.
  // Note, I tried using just this:
  //
  //  svSetScope( svGetScopeFromName("TOP.v.verilog_module") );
  //
  // but it did not seem to work. We would see correct line tracing for
  // the first test case but not any of the remaining tests cases. After
  // digging around a bit, it seemed like the line_trace task was still
  // associated with the very first model as opposed to the newly
  // instantiated models. Directly setting the scope seemed to fix
  // this issue.
  //
  // Note that this issue implies that the mysterious extra .v is no
  // longer present:
  //
  //  https://www.veripool.org/issues/1050-Verilator-Extra-v-in-full-signal-pathnames
  //
  // So now we need to explicitly use the model name instead of
  // Vscope_v__verilog_module.

  // PP: also note that since we add a wrapper around the external Verilog
  // module, the scope we are trying to set is actually the _wrapped_ module
  // which is called `v`.
  // svSetScope( &model->__VlSymsp->__Vscope_IntMulAlt_noparam__v );

  // PP update: the above (commented) way of setting scope is not
  // compatible with newer versions of Verilator because it relies on
  // Verilator's internal implementation. It is recommended to get scope through
  // a dotted hierarchical name as shown below.

  const svScope dut_scope = svGetScopeFromName("TOP.IntMulAlt_noparam.v");
  assert( dut_scope );
  svSetScope( dut_scope );

  VIntMulAlt_noparam::line_trace( words );

  // Note that the way the line tracing works, the line tracing function
  // will store how the last character used in the line trace in the
  // first element of the word array. The line tracing functions store
  // the line trace starting from the most-signicant character due to the
  // way that Verilog handles strings.

  int nchar_last  = words[0];
  int nchars_used = ( nchars - 1 - nchar_last );

  // We subtract since one of the words (i.e., 4 characters) is for
  // storing the nchars_used.

  assert ( nchars_used < (nchars - 4) );

  // Now we need to iterate from the most-significant character to the
  // last character written by the line tracing functions and copy these
  // characters into the given character array. So we are kind of
  // flipping the order of the characters due to the different between
  // how Verilog and C handle strings.

  int j = 0;
  for ( int i = nchars-1; i > nchar_last; i-- ) {
    char c = static_cast<char>( words[i/4] >> (8*(i%4)) );
    str[j] = c;
    j++;
  }
  str[j] = '\0';

}
#endif

//------------------------------------------------------------------------
// sc_time_stamp
//------------------------------------------------------------------------
// This is now a lgeacy function required only so linking works on Cygwin
// and MSVC++:
// https://github.com/verilator/verilator/blob/master/examples/make_tracing_c/sim_main.cpp

double sc_time_stamp()
{

  return 0;

}
