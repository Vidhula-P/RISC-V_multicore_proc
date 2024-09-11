// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See VIntMulAlt_noparam.h for the primary calling header

#ifndef VERILATED_VINTMULALT_NOPARAM___024ROOT_H_
#define VERILATED_VINTMULALT_NOPARAM___024ROOT_H_  // guard

#include "verilated.h"


class VIntMulAlt_noparam__Syms;

class alignas(VL_CACHE_LINE_BYTES) VIntMulAlt_noparam___024root final : public VerilatedModule {
  public:

    // DESIGN SPECIFIC STATE
    VL_IN8(clk,0,0);
    VL_IN8(reset,0,0);
    VL_OUT8(istream_rdy,0,0);
    VL_IN8(istream_val,0,0);
    VL_IN8(ostream_rdy,0,0);
    VL_OUT8(ostream_val,0,0);
    CData/*0:0*/ __Vdpi_export_trigger;
    CData/*0:0*/ __VactContinue;
    VL_OUT(ostream_msg,31,0);
    VlWide<128>/*4095:0*/ IntMulAlt_noparam__DOT__v__DOT__str;
    IData/*31:0*/ IntMulAlt_noparam__DOT__v__DOT__vc_trace__DOT__len0;
    IData/*31:0*/ IntMulAlt_noparam__DOT__v__DOT__vc_trace__DOT__idx0;
    IData/*31:0*/ IntMulAlt_noparam__DOT__v__DOT__vc_trace__DOT__idx1;
    IData/*31:0*/ __VactIterCount;
    VL_IN64(istream_msg,63,0);
    VlTriggerVec<1> __VactTriggered;
    VlTriggerVec<1> __VnbaTriggered;

    // INTERNAL VARIABLES
    VIntMulAlt_noparam__Syms* const vlSymsp;

    // CONSTRUCTORS
    VIntMulAlt_noparam___024root(VIntMulAlt_noparam__Syms* symsp, const char* v__name);
    ~VIntMulAlt_noparam___024root();
    VL_UNCOPYABLE(VIntMulAlt_noparam___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
