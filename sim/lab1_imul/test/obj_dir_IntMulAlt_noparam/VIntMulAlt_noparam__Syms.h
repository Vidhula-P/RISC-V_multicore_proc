// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table internal header
//
// Internal details; most calling programs do not need this header,
// unless using verilator public meta comments.

#ifndef VERILATED_VINTMULALT_NOPARAM__SYMS_H_
#define VERILATED_VINTMULALT_NOPARAM__SYMS_H_  // guard

#include "verilated.h"

// INCLUDE MODEL CLASS

#include "VIntMulAlt_noparam.h"

// INCLUDE MODULE CLASSES
#include "VIntMulAlt_noparam___024root.h"

// DPI TYPES for DPI Export callbacks (Internal use)
using VIntMulAlt_noparam__Vcb_line_trace_t = void (*) (VIntMulAlt_noparam__Syms* __restrict vlSymsp, VlWide<128>/*4095:0*/ &trace_str);

// SYMS CLASS (contains all model state)
class alignas(VL_CACHE_LINE_BYTES)VIntMulAlt_noparam__Syms final : public VerilatedSyms {
  public:
    // INTERNAL STATE
    VIntMulAlt_noparam* const __Vm_modelp;
    VlDeleter __Vm_deleter;
    bool __Vm_didInit = false;

    // MODULE INSTANCE STATE
    VIntMulAlt_noparam___024root   TOP;

    // SCOPE NAMES
    VerilatedScope __Vscope_IntMulAlt_noparam__v;

    // CONSTRUCTORS
    VIntMulAlt_noparam__Syms(VerilatedContext* contextp, const char* namep, VIntMulAlt_noparam* modelp);
    ~VIntMulAlt_noparam__Syms();

    // METHODS
    const char* name() { return TOP.name(); }
};

#endif  // guard
