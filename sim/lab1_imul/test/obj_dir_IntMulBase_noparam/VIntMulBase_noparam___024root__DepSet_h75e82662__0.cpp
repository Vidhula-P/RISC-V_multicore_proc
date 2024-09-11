// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See VIntMulBase_noparam.h for the primary calling header

#include "VIntMulBase_noparam__pch.h"
#include "VIntMulBase_noparam___024root.h"

void VIntMulBase_noparam___024root___ico_sequent__TOP__0(VIntMulBase_noparam___024root* vlSelf);

void VIntMulBase_noparam___024root___eval_ico(VIntMulBase_noparam___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VIntMulBase_noparam__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VIntMulBase_noparam___024root___eval_ico\n"); );
    // Body
    if ((1ULL & vlSelf->__VicoTriggered.word(0U))) {
        VIntMulBase_noparam___024root___ico_sequent__TOP__0(vlSelf);
    }
}

VL_INLINE_OPT void VIntMulBase_noparam___024root___ico_sequent__TOP__0(VIntMulBase_noparam___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VIntMulBase_noparam__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VIntMulBase_noparam___024root___ico_sequent__TOP__0\n"); );
    // Body
    vlSelf->IntMulBase_noparam__DOT__v__DOT__datapathUnitBase_I__DOT__b_mux_out 
        = ((IData)(vlSelf->IntMulBase_noparam__DOT__v__DOT__b_mux_sel)
            ? ((IData)(vlSelf->IntMulBase_noparam__DOT__v__DOT__b_mux_sel)
                ? VL_SHIFTR_III(32,32,32, vlSelf->IntMulBase_noparam__DOT__v__DOT__datapathUnitBase_I__DOT__b_reg_out, 1U)
                : 0U) : (IData)(vlSelf->istream_msg));
    vlSelf->IntMulBase_noparam__DOT__v__DOT__datapathUnitBase_I__DOT__a_mux_out 
        = ((IData)(vlSelf->IntMulBase_noparam__DOT__v__DOT__a_mux_sel)
            ? ((IData)(vlSelf->IntMulBase_noparam__DOT__v__DOT__a_mux_sel)
                ? VL_SHIFTL_III(32,32,32, vlSelf->IntMulBase_noparam__DOT__v__DOT__datapathUnitBase_I__DOT__a_reg_out, 1U)
                : 0U) : (IData)((vlSelf->istream_msg 
                                 >> 0x20U)));
    vlSelf->IntMulBase_noparam__DOT__v__DOT__controlUnitBase_I__DOT__next_state 
        = ((0U == (IData)(vlSelf->IntMulBase_noparam__DOT__v__DOT__controlUnitBase_I__DOT__curr_state))
            ? ((IData)(vlSelf->istream_val) ? 1U : 0U)
            : ((1U == (IData)(vlSelf->IntMulBase_noparam__DOT__v__DOT__controlUnitBase_I__DOT__curr_state))
                ? ((0x20U > (IData)(vlSelf->IntMulBase_noparam__DOT__v__DOT__controlUnitBase_I__DOT__counter))
                    ? 1U : 2U) : ((2U == (IData)(vlSelf->IntMulBase_noparam__DOT__v__DOT__controlUnitBase_I__DOT__curr_state))
                                   ? ((IData)(vlSelf->ostream_rdy)
                                       ? 0U : 2U) : 0U)));
}

void VIntMulBase_noparam___024root___eval_triggers__ico(VIntMulBase_noparam___024root* vlSelf);

bool VIntMulBase_noparam___024root___eval_phase__ico(VIntMulBase_noparam___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VIntMulBase_noparam__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VIntMulBase_noparam___024root___eval_phase__ico\n"); );
    // Init
    CData/*0:0*/ __VicoExecute;
    // Body
    VIntMulBase_noparam___024root___eval_triggers__ico(vlSelf);
    __VicoExecute = vlSelf->__VicoTriggered.any();
    if (__VicoExecute) {
        VIntMulBase_noparam___024root___eval_ico(vlSelf);
    }
    return (__VicoExecute);
}

void VIntMulBase_noparam___024root___eval_act(VIntMulBase_noparam___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VIntMulBase_noparam__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VIntMulBase_noparam___024root___eval_act\n"); );
}

void VIntMulBase_noparam___024root___nba_sequent__TOP__0(VIntMulBase_noparam___024root* vlSelf);

void VIntMulBase_noparam___024root___eval_nba(VIntMulBase_noparam___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VIntMulBase_noparam__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VIntMulBase_noparam___024root___eval_nba\n"); );
    // Body
    if ((2ULL & vlSelf->__VnbaTriggered.word(0U))) {
        VIntMulBase_noparam___024root___nba_sequent__TOP__0(vlSelf);
    }
}

extern const VlUnpacked<CData/*0:0*/, 8> VIntMulBase_noparam__ConstPool__TABLE_h04283ef2_0;
extern const VlUnpacked<CData/*0:0*/, 8> VIntMulBase_noparam__ConstPool__TABLE_h93919e28_0;
extern const VlUnpacked<CData/*0:0*/, 8> VIntMulBase_noparam__ConstPool__TABLE_hc2e726e8_0;
extern const VlUnpacked<CData/*0:0*/, 8> VIntMulBase_noparam__ConstPool__TABLE_h895c8fc4_0;
extern const VlUnpacked<CData/*0:0*/, 8> VIntMulBase_noparam__ConstPool__TABLE_h80cae639_0;

VL_INLINE_OPT void VIntMulBase_noparam___024root___nba_sequent__TOP__0(VIntMulBase_noparam___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VIntMulBase_noparam__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VIntMulBase_noparam___024root___nba_sequent__TOP__0\n"); );
    // Init
    CData/*0:0*/ IntMulBase_noparam__DOT__v__DOT__result_mux_sel;
    IntMulBase_noparam__DOT__v__DOT__result_mux_sel = 0;
    CData/*0:0*/ IntMulBase_noparam__DOT__v__DOT__add_mux_sel;
    IntMulBase_noparam__DOT__v__DOT__add_mux_sel = 0;
    CData/*2:0*/ __Vtableidx1;
    __Vtableidx1 = 0;
    // Body
    if (vlSelf->reset) {
        vlSelf->IntMulBase_noparam__DOT__v__DOT__controlUnitBase_I__DOT__counter = 0U;
        vlSelf->IntMulBase_noparam__DOT__v__DOT__controlUnitBase_I__DOT__curr_state = 0U;
    } else {
        vlSelf->IntMulBase_noparam__DOT__v__DOT__controlUnitBase_I__DOT__counter 
            = ((1U == (IData)(vlSelf->IntMulBase_noparam__DOT__v__DOT__controlUnitBase_I__DOT__curr_state))
                ? (0x3fU & ((IData)(1U) + (IData)(vlSelf->IntMulBase_noparam__DOT__v__DOT__controlUnitBase_I__DOT__counter)))
                : 0U);
        vlSelf->IntMulBase_noparam__DOT__v__DOT__controlUnitBase_I__DOT__curr_state 
            = vlSelf->IntMulBase_noparam__DOT__v__DOT__controlUnitBase_I__DOT__next_state;
    }
    vlSelf->IntMulBase_noparam__DOT__v__DOT__datapathUnitBase_I__DOT__a_reg_out 
        = vlSelf->IntMulBase_noparam__DOT__v__DOT__datapathUnitBase_I__DOT__a_mux_out;
    if (vlSelf->IntMulBase_noparam__DOT__v__DOT__result_en) {
        vlSelf->IntMulBase_noparam__DOT__v__DOT__datapathUnitBase_I__DOT__result_reg_out 
            = vlSelf->IntMulBase_noparam__DOT__v__DOT__datapathUnitBase_I__DOT__result_mux_out;
    }
    vlSelf->IntMulBase_noparam__DOT__v__DOT__datapathUnitBase_I__DOT__b_reg_out 
        = vlSelf->IntMulBase_noparam__DOT__v__DOT__datapathUnitBase_I__DOT__b_mux_out;
    vlSelf->ostream_msg = vlSelf->IntMulBase_noparam__DOT__v__DOT__datapathUnitBase_I__DOT__result_reg_out;
    vlSelf->IntMulBase_noparam__DOT__v__DOT__controlUnitBase_I__DOT__next_state 
        = ((0U == (IData)(vlSelf->IntMulBase_noparam__DOT__v__DOT__controlUnitBase_I__DOT__curr_state))
            ? ((IData)(vlSelf->istream_val) ? 1U : 0U)
            : ((1U == (IData)(vlSelf->IntMulBase_noparam__DOT__v__DOT__controlUnitBase_I__DOT__curr_state))
                ? ((0x20U > (IData)(vlSelf->IntMulBase_noparam__DOT__v__DOT__controlUnitBase_I__DOT__counter))
                    ? 1U : 2U) : ((2U == (IData)(vlSelf->IntMulBase_noparam__DOT__v__DOT__controlUnitBase_I__DOT__curr_state))
                                   ? ((IData)(vlSelf->ostream_rdy)
                                       ? 0U : 2U) : 0U)));
    __Vtableidx1 = ((4U & (vlSelf->IntMulBase_noparam__DOT__v__DOT__datapathUnitBase_I__DOT__b_reg_out 
                           << 2U)) | (IData)(vlSelf->IntMulBase_noparam__DOT__v__DOT__controlUnitBase_I__DOT__curr_state));
    vlSelf->IntMulBase_noparam__DOT__v__DOT__b_mux_sel 
        = VIntMulBase_noparam__ConstPool__TABLE_h04283ef2_0
        [__Vtableidx1];
    IntMulBase_noparam__DOT__v__DOT__result_mux_sel 
        = VIntMulBase_noparam__ConstPool__TABLE_h04283ef2_0
        [__Vtableidx1];
    vlSelf->IntMulBase_noparam__DOT__v__DOT__a_mux_sel 
        = VIntMulBase_noparam__ConstPool__TABLE_h04283ef2_0
        [__Vtableidx1];
    vlSelf->IntMulBase_noparam__DOT__v__DOT__result_en 
        = VIntMulBase_noparam__ConstPool__TABLE_h93919e28_0
        [__Vtableidx1];
    IntMulBase_noparam__DOT__v__DOT__add_mux_sel = 
        VIntMulBase_noparam__ConstPool__TABLE_hc2e726e8_0
        [__Vtableidx1];
    vlSelf->istream_rdy = VIntMulBase_noparam__ConstPool__TABLE_h895c8fc4_0
        [__Vtableidx1];
    vlSelf->ostream_val = VIntMulBase_noparam__ConstPool__TABLE_h80cae639_0
        [__Vtableidx1];
    vlSelf->IntMulBase_noparam__DOT__v__DOT__datapathUnitBase_I__DOT__b_mux_out 
        = ((IData)(vlSelf->IntMulBase_noparam__DOT__v__DOT__b_mux_sel)
            ? ((IData)(vlSelf->IntMulBase_noparam__DOT__v__DOT__b_mux_sel)
                ? VL_SHIFTR_III(32,32,32, vlSelf->IntMulBase_noparam__DOT__v__DOT__datapathUnitBase_I__DOT__b_reg_out, 1U)
                : 0U) : (IData)(vlSelf->istream_msg));
    vlSelf->IntMulBase_noparam__DOT__v__DOT__datapathUnitBase_I__DOT__a_mux_out 
        = ((IData)(vlSelf->IntMulBase_noparam__DOT__v__DOT__a_mux_sel)
            ? ((IData)(vlSelf->IntMulBase_noparam__DOT__v__DOT__a_mux_sel)
                ? VL_SHIFTL_III(32,32,32, vlSelf->IntMulBase_noparam__DOT__v__DOT__datapathUnitBase_I__DOT__a_reg_out, 1U)
                : 0U) : (IData)((vlSelf->istream_msg 
                                 >> 0x20U)));
    vlSelf->IntMulBase_noparam__DOT__v__DOT__datapathUnitBase_I__DOT__result_mux_out 
        = ((IData)(IntMulBase_noparam__DOT__v__DOT__result_mux_sel)
            ? ((IData)(IntMulBase_noparam__DOT__v__DOT__result_mux_sel)
                ? ((IData)(IntMulBase_noparam__DOT__v__DOT__add_mux_sel)
                    ? ((IData)(IntMulBase_noparam__DOT__v__DOT__add_mux_sel)
                        ? (vlSelf->IntMulBase_noparam__DOT__v__DOT__datapathUnitBase_I__DOT__result_reg_out 
                           + vlSelf->IntMulBase_noparam__DOT__v__DOT__datapathUnitBase_I__DOT__a_reg_out)
                        : 0U) : vlSelf->IntMulBase_noparam__DOT__v__DOT__datapathUnitBase_I__DOT__result_reg_out)
                : 0U) : 0U);
}

void VIntMulBase_noparam___024root___eval_triggers__act(VIntMulBase_noparam___024root* vlSelf);

bool VIntMulBase_noparam___024root___eval_phase__act(VIntMulBase_noparam___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VIntMulBase_noparam__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VIntMulBase_noparam___024root___eval_phase__act\n"); );
    // Init
    VlTriggerVec<2> __VpreTriggered;
    CData/*0:0*/ __VactExecute;
    // Body
    VIntMulBase_noparam___024root___eval_triggers__act(vlSelf);
    __VactExecute = vlSelf->__VactTriggered.any();
    if (__VactExecute) {
        __VpreTriggered.andNot(vlSelf->__VactTriggered, vlSelf->__VnbaTriggered);
        vlSelf->__VnbaTriggered.thisOr(vlSelf->__VactTriggered);
        VIntMulBase_noparam___024root___eval_act(vlSelf);
    }
    return (__VactExecute);
}

bool VIntMulBase_noparam___024root___eval_phase__nba(VIntMulBase_noparam___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VIntMulBase_noparam__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VIntMulBase_noparam___024root___eval_phase__nba\n"); );
    // Init
    CData/*0:0*/ __VnbaExecute;
    // Body
    __VnbaExecute = vlSelf->__VnbaTriggered.any();
    if (__VnbaExecute) {
        VIntMulBase_noparam___024root___eval_nba(vlSelf);
        vlSelf->__VnbaTriggered.clear();
    }
    return (__VnbaExecute);
}

#ifdef VL_DEBUG
VL_ATTR_COLD void VIntMulBase_noparam___024root___dump_triggers__ico(VIntMulBase_noparam___024root* vlSelf);
#endif  // VL_DEBUG
#ifdef VL_DEBUG
VL_ATTR_COLD void VIntMulBase_noparam___024root___dump_triggers__nba(VIntMulBase_noparam___024root* vlSelf);
#endif  // VL_DEBUG
#ifdef VL_DEBUG
VL_ATTR_COLD void VIntMulBase_noparam___024root___dump_triggers__act(VIntMulBase_noparam___024root* vlSelf);
#endif  // VL_DEBUG

void VIntMulBase_noparam___024root___eval(VIntMulBase_noparam___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VIntMulBase_noparam__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VIntMulBase_noparam___024root___eval\n"); );
    // Init
    IData/*31:0*/ __VicoIterCount;
    CData/*0:0*/ __VicoContinue;
    IData/*31:0*/ __VnbaIterCount;
    CData/*0:0*/ __VnbaContinue;
    // Body
    __VicoIterCount = 0U;
    vlSelf->__VicoFirstIteration = 1U;
    __VicoContinue = 1U;
    while (__VicoContinue) {
        if (VL_UNLIKELY((0x64U < __VicoIterCount))) {
#ifdef VL_DEBUG
            VIntMulBase_noparam___024root___dump_triggers__ico(vlSelf);
#endif
            VL_FATAL_MT("lab1_imul/IntMulBase.v", 367, "", "Input combinational region did not converge.");
        }
        __VicoIterCount = ((IData)(1U) + __VicoIterCount);
        __VicoContinue = 0U;
        if (VIntMulBase_noparam___024root___eval_phase__ico(vlSelf)) {
            __VicoContinue = 1U;
        }
        vlSelf->__VicoFirstIteration = 0U;
    }
    __VnbaIterCount = 0U;
    __VnbaContinue = 1U;
    while (__VnbaContinue) {
        if (VL_UNLIKELY((0x64U < __VnbaIterCount))) {
#ifdef VL_DEBUG
            VIntMulBase_noparam___024root___dump_triggers__nba(vlSelf);
#endif
            VL_FATAL_MT("lab1_imul/IntMulBase.v", 367, "", "NBA region did not converge.");
        }
        __VnbaIterCount = ((IData)(1U) + __VnbaIterCount);
        __VnbaContinue = 0U;
        vlSelf->__VactIterCount = 0U;
        vlSelf->__VactContinue = 1U;
        while (vlSelf->__VactContinue) {
            if (VL_UNLIKELY((0x64U < vlSelf->__VactIterCount))) {
#ifdef VL_DEBUG
                VIntMulBase_noparam___024root___dump_triggers__act(vlSelf);
#endif
                VL_FATAL_MT("lab1_imul/IntMulBase.v", 367, "", "Active region did not converge.");
            }
            vlSelf->__VactIterCount = ((IData)(1U) 
                                       + vlSelf->__VactIterCount);
            vlSelf->__VactContinue = 0U;
            if (VIntMulBase_noparam___024root___eval_phase__act(vlSelf)) {
                vlSelf->__VactContinue = 1U;
            }
        }
        if (VIntMulBase_noparam___024root___eval_phase__nba(vlSelf)) {
            __VnbaContinue = 1U;
        }
    }
}

#ifdef VL_DEBUG
void VIntMulBase_noparam___024root___eval_debug_assertions(VIntMulBase_noparam___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VIntMulBase_noparam__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VIntMulBase_noparam___024root___eval_debug_assertions\n"); );
    // Body
    if (VL_UNLIKELY((vlSelf->clk & 0xfeU))) {
        Verilated::overWidthError("clk");}
    if (VL_UNLIKELY((vlSelf->reset & 0xfeU))) {
        Verilated::overWidthError("reset");}
    if (VL_UNLIKELY((vlSelf->istream_val & 0xfeU))) {
        Verilated::overWidthError("istream_val");}
    if (VL_UNLIKELY((vlSelf->ostream_rdy & 0xfeU))) {
        Verilated::overWidthError("ostream_rdy");}
}
#endif  // VL_DEBUG
