// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table implementation internals

#include "VIntMulBase_noparam__pch.h"
#include "VIntMulBase_noparam.h"
#include "VIntMulBase_noparam___024root.h"

void VIntMulBase_noparam___024root____Vdpiexp_IntMulBase_noparam__DOT__v__DOT__line_trace_TOP(VIntMulBase_noparam__Syms* __restrict vlSymsp, VlWide<128>/*4095:0*/ &trace_str);

// FUNCTIONS
VIntMulBase_noparam__Syms::~VIntMulBase_noparam__Syms()
{
}

VIntMulBase_noparam__Syms::VIntMulBase_noparam__Syms(VerilatedContext* contextp, const char* namep, VIntMulBase_noparam* modelp)
    : VerilatedSyms{contextp}
    // Setup internal state of the Syms class
    , __Vm_modelp{modelp}
    // Setup module instances
    , TOP{this, namep}
{
        // Check resources
        Verilated::stackCheck(18005);
    // Configure time unit / time precision
    _vm_contextp__->timeunit(-12);
    _vm_contextp__->timeprecision(-12);
    // Setup each module's pointers to their submodules
    // Setup each module's pointer back to symbol table (for public functions)
    TOP.__Vconfigure(true);
    // Setup scopes
    __Vscope_IntMulBase_noparam__v.configure(this, name(), "IntMulBase_noparam.v", "v", -12, VerilatedScope::SCOPE_OTHER);
    // Setup export functions
    for (int __Vfinal = 0; __Vfinal < 2; ++__Vfinal) {
        __Vscope_IntMulBase_noparam__v.exportInsert(__Vfinal, "line_trace", (void*)(&VIntMulBase_noparam___024root____Vdpiexp_IntMulBase_noparam__DOT__v__DOT__line_trace_TOP));
    }
}
