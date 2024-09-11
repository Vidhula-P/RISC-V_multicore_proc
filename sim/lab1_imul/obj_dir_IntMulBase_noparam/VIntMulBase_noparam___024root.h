// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See VIntMulBase_noparam.h for the primary calling header

#ifndef VERILATED_VINTMULBASE_NOPARAM___024ROOT_H_
#define VERILATED_VINTMULBASE_NOPARAM___024ROOT_H_  // guard

#include "verilated.h"


class VIntMulBase_noparam__Syms;

class alignas(VL_CACHE_LINE_BYTES) VIntMulBase_noparam___024root final : public VerilatedModule {
  public:

    // DESIGN SPECIFIC STATE
    VL_IN8(clk,0,0);
    VL_IN8(reset,0,0);
    VL_OUT8(istream_rdy,0,0);
    VL_IN8(istream_val,0,0);
    VL_IN8(ostream_rdy,0,0);
    VL_OUT8(ostream_val,0,0);
    CData/*0:0*/ IntMulBase_noparam__DOT__v__DOT__b_mux_sel;
    CData/*0:0*/ IntMulBase_noparam__DOT__v__DOT__a_mux_sel;
    CData/*0:0*/ IntMulBase_noparam__DOT__v__DOT__result_en;
    CData/*1:0*/ IntMulBase_noparam__DOT__v__DOT__controlUnitBase_I__DOT__curr_state;
    CData/*1:0*/ IntMulBase_noparam__DOT__v__DOT__controlUnitBase_I__DOT__next_state;
    CData/*5:0*/ IntMulBase_noparam__DOT__v__DOT__controlUnitBase_I__DOT__counter;
    CData/*0:0*/ __Vdpi_export_trigger;
    CData/*0:0*/ __VstlFirstIteration;
    CData/*0:0*/ __VicoFirstIteration;
    CData/*0:0*/ __Vtrigprevexpr___TOP__clk__0;
    CData/*0:0*/ __VactContinue;
    VL_OUT(ostream_msg,31,0);
    VlWide<128>/*4095:0*/ IntMulBase_noparam__DOT__v__DOT__str;
    IData/*31:0*/ IntMulBase_noparam__DOT__v__DOT__datapathUnitBase_I__DOT__b_mux_out;
    IData/*31:0*/ IntMulBase_noparam__DOT__v__DOT__datapathUnitBase_I__DOT__b_reg_out;
    IData/*31:0*/ IntMulBase_noparam__DOT__v__DOT__datapathUnitBase_I__DOT__a_mux_out;
    IData/*31:0*/ IntMulBase_noparam__DOT__v__DOT__datapathUnitBase_I__DOT__a_reg_out;
    IData/*31:0*/ IntMulBase_noparam__DOT__v__DOT__datapathUnitBase_I__DOT__result_mux_out;
    IData/*31:0*/ IntMulBase_noparam__DOT__v__DOT__datapathUnitBase_I__DOT__result_reg_out;
    IData/*31:0*/ IntMulBase_noparam__DOT__v__DOT__vc_trace__DOT__len0;
    IData/*31:0*/ IntMulBase_noparam__DOT__v__DOT__vc_trace__DOT__idx0;
    IData/*31:0*/ IntMulBase_noparam__DOT__v__DOT__vc_trace__DOT__idx1;
    IData/*31:0*/ __VactIterCount;
    VL_IN64(istream_msg,63,0);
    VlTriggerVec<1> __VstlTriggered;
    VlTriggerVec<2> __VicoTriggered;
    VlTriggerVec<2> __VactTriggered;
    VlTriggerVec<2> __VnbaTriggered;

    // INTERNAL VARIABLES
    VIntMulBase_noparam__Syms* const vlSymsp;

    // CONSTRUCTORS
    VIntMulBase_noparam___024root(VIntMulBase_noparam__Syms* symsp, const char* v__name);
    ~VIntMulBase_noparam___024root();
    VL_UNCOPYABLE(VIntMulBase_noparam___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
