// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Model implementation (design independent parts)

#include "VIntMulBase_noparam__pch.h"

//============================================================
// Constructors

VIntMulBase_noparam::VIntMulBase_noparam(VerilatedContext* _vcontextp__, const char* _vcname__)
    : VerilatedModel{*_vcontextp__}
    , vlSymsp{new VIntMulBase_noparam__Syms(contextp(), _vcname__, this)}
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

VIntMulBase_noparam::VIntMulBase_noparam(const char* _vcname__)
    : VIntMulBase_noparam(Verilated::threadContextp(), _vcname__)
{
}

//============================================================
// Destructor

VIntMulBase_noparam::~VIntMulBase_noparam() {
    delete vlSymsp;
}

//============================================================
// Evaluation function

#ifdef VL_DEBUG
void VIntMulBase_noparam___024root___eval_debug_assertions(VIntMulBase_noparam___024root* vlSelf);
#endif  // VL_DEBUG
void VIntMulBase_noparam___024root___eval_static(VIntMulBase_noparam___024root* vlSelf);
void VIntMulBase_noparam___024root___eval_initial(VIntMulBase_noparam___024root* vlSelf);
void VIntMulBase_noparam___024root___eval_settle(VIntMulBase_noparam___024root* vlSelf);
void VIntMulBase_noparam___024root___eval(VIntMulBase_noparam___024root* vlSelf);

void VIntMulBase_noparam::eval_step() {
    VL_DEBUG_IF(VL_DBG_MSGF("+++++TOP Evaluate VIntMulBase_noparam::eval_step\n"); );
#ifdef VL_DEBUG
    // Debug assertions
    VIntMulBase_noparam___024root___eval_debug_assertions(&(vlSymsp->TOP));
#endif  // VL_DEBUG
    vlSymsp->__Vm_deleter.deleteAll();
    if (VL_UNLIKELY(!vlSymsp->__Vm_didInit)) {
        vlSymsp->__Vm_didInit = true;
        VL_DEBUG_IF(VL_DBG_MSGF("+ Initial\n"););
        VIntMulBase_noparam___024root___eval_static(&(vlSymsp->TOP));
        VIntMulBase_noparam___024root___eval_initial(&(vlSymsp->TOP));
        VIntMulBase_noparam___024root___eval_settle(&(vlSymsp->TOP));
    }
    VL_DEBUG_IF(VL_DBG_MSGF("+ Eval\n"););
    VIntMulBase_noparam___024root___eval(&(vlSymsp->TOP));
    // Evaluate cleanup
    Verilated::endOfEval(vlSymsp->__Vm_evalMsgQp);
}

//============================================================
// Events and timing
bool VIntMulBase_noparam::eventsPending() { return false; }

uint64_t VIntMulBase_noparam::nextTimeSlot() {
    VL_FATAL_MT(__FILE__, __LINE__, "", "%Error: No delays in the design");
    return 0;
}

//============================================================
// Utilities

const char* VIntMulBase_noparam::name() const {
    return vlSymsp->name();
}

//============================================================
// Invoke final blocks

void VIntMulBase_noparam___024root___eval_final(VIntMulBase_noparam___024root* vlSelf);

VL_ATTR_COLD void VIntMulBase_noparam::final() {
    VIntMulBase_noparam___024root___eval_final(&(vlSymsp->TOP));
}

//============================================================
// Implementations of abstract methods from VerilatedModel

const char* VIntMulBase_noparam::hierName() const { return vlSymsp->name(); }
const char* VIntMulBase_noparam::modelName() const { return "VIntMulBase_noparam"; }
unsigned VIntMulBase_noparam::threads() const { return 1; }
void VIntMulBase_noparam::prepareClone() const { contextp()->prepareClone(); }
void VIntMulBase_noparam::atClone() const {
    contextp()->threadPoolpOnClone();
}
