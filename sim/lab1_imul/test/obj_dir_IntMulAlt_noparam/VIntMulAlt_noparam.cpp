// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Model implementation (design independent parts)

#include "VIntMulAlt_noparam__pch.h"

//============================================================
// Constructors

VIntMulAlt_noparam::VIntMulAlt_noparam(VerilatedContext* _vcontextp__, const char* _vcname__)
    : VerilatedModel{*_vcontextp__}
    , vlSymsp{new VIntMulAlt_noparam__Syms(contextp(), _vcname__, this)}
    , clk{vlSymsp->TOP.clk}
    , reset{vlSymsp->TOP.reset}
    , istream_rdy{vlSymsp->TOP.istream_rdy}
    , istream_val{vlSymsp->TOP.istream_val}
    , ostream_rdy{vlSymsp->TOP.ostream_rdy}
    , ostream_val{vlSymsp->TOP.ostream_val}
    , ostream_msg{vlSymsp->TOP.ostream_msg}
    , istream_msg{vlSymsp->TOP.istream_msg}
    , rootp{&(vlSymsp->TOP)}
{
    // Register model with the context
    contextp()->addModel(this);
}

VIntMulAlt_noparam::VIntMulAlt_noparam(const char* _vcname__)
    : VIntMulAlt_noparam(Verilated::threadContextp(), _vcname__)
{
}

//============================================================
// Destructor

VIntMulAlt_noparam::~VIntMulAlt_noparam() {
    delete vlSymsp;
}

//============================================================
// Evaluation function

#ifdef VL_DEBUG
void VIntMulAlt_noparam___024root___eval_debug_assertions(VIntMulAlt_noparam___024root* vlSelf);
#endif  // VL_DEBUG
void VIntMulAlt_noparam___024root___eval_static(VIntMulAlt_noparam___024root* vlSelf);
void VIntMulAlt_noparam___024root___eval_initial(VIntMulAlt_noparam___024root* vlSelf);
void VIntMulAlt_noparam___024root___eval_settle(VIntMulAlt_noparam___024root* vlSelf);
void VIntMulAlt_noparam___024root___eval(VIntMulAlt_noparam___024root* vlSelf);

void VIntMulAlt_noparam::eval_step() {
    VL_DEBUG_IF(VL_DBG_MSGF("+++++TOP Evaluate VIntMulAlt_noparam::eval_step\n"); );
#ifdef VL_DEBUG
    // Debug assertions
    VIntMulAlt_noparam___024root___eval_debug_assertions(&(vlSymsp->TOP));
#endif  // VL_DEBUG
    vlSymsp->__Vm_deleter.deleteAll();
    if (VL_UNLIKELY(!vlSymsp->__Vm_didInit)) {
        vlSymsp->__Vm_didInit = true;
        VL_DEBUG_IF(VL_DBG_MSGF("+ Initial\n"););
        VIntMulAlt_noparam___024root___eval_static(&(vlSymsp->TOP));
        VIntMulAlt_noparam___024root___eval_initial(&(vlSymsp->TOP));
        VIntMulAlt_noparam___024root___eval_settle(&(vlSymsp->TOP));
    }
    VL_DEBUG_IF(VL_DBG_MSGF("+ Eval\n"););
    VIntMulAlt_noparam___024root___eval(&(vlSymsp->TOP));
    // Evaluate cleanup
    Verilated::endOfEval(vlSymsp->__Vm_evalMsgQp);
}

//============================================================
// Events and timing
bool VIntMulAlt_noparam::eventsPending() { return false; }

uint64_t VIntMulAlt_noparam::nextTimeSlot() {
    VL_FATAL_MT(__FILE__, __LINE__, "", "%Error: No delays in the design");
    return 0;
}

//============================================================
// Utilities

const char* VIntMulAlt_noparam::name() const {
    return vlSymsp->name();
}

//============================================================
// Invoke final blocks

void VIntMulAlt_noparam___024root___eval_final(VIntMulAlt_noparam___024root* vlSelf);

VL_ATTR_COLD void VIntMulAlt_noparam::final() {
    VIntMulAlt_noparam___024root___eval_final(&(vlSymsp->TOP));
}

//============================================================
// Implementations of abstract methods from VerilatedModel

const char* VIntMulAlt_noparam::hierName() const { return vlSymsp->name(); }
const char* VIntMulAlt_noparam::modelName() const { return "VIntMulAlt_noparam"; }
unsigned VIntMulAlt_noparam::threads() const { return 1; }
void VIntMulAlt_noparam::prepareClone() const { contextp()->prepareClone(); }
void VIntMulAlt_noparam::atClone() const {
    contextp()->threadPoolpOnClone();
}
