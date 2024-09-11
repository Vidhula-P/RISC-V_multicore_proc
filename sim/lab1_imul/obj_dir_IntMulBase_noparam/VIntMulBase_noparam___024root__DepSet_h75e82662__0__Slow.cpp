// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See VIntMulBase_noparam.h for the primary calling header

#include "VIntMulBase_noparam__pch.h"
#include "VIntMulBase_noparam___024root.h"

VL_ATTR_COLD void VIntMulBase_noparam___024root___eval_static(VIntMulBase_noparam___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VIntMulBase_noparam__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VIntMulBase_noparam___024root___eval_static\n"); );
}

VL_ATTR_COLD void VIntMulBase_noparam___024root___eval_initial(VIntMulBase_noparam___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VIntMulBase_noparam__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VIntMulBase_noparam___024root___eval_initial\n"); );
    // Body
    vlSelf->__Vtrigprevexpr___TOP__clk__0 = vlSelf->clk;
}

VL_ATTR_COLD void VIntMulBase_noparam___024root___eval_final(VIntMulBase_noparam___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VIntMulBase_noparam__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VIntMulBase_noparam___024root___eval_final\n"); );
}

#ifdef VL_DEBUG
VL_ATTR_COLD void VIntMulBase_noparam___024root___dump_triggers__stl(VIntMulBase_noparam___024root* vlSelf);
#endif  // VL_DEBUG
VL_ATTR_COLD bool VIntMulBase_noparam___024root___eval_phase__stl(VIntMulBase_noparam___024root* vlSelf);

VL_ATTR_COLD void VIntMulBase_noparam___024root___eval_settle(VIntMulBase_noparam___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VIntMulBase_noparam__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VIntMulBase_noparam___024root___eval_settle\n"); );
    // Init
    IData/*31:0*/ __VstlIterCount;
    CData/*0:0*/ __VstlContinue;
    // Body
    __VstlIterCount = 0U;
    vlSelf->__VstlFirstIteration = 1U;
    __VstlContinue = 1U;
    while (__VstlContinue) {
        if (VL_UNLIKELY((0x64U < __VstlIterCount))) {
#ifdef VL_DEBUG
            VIntMulBase_noparam___024root___dump_triggers__stl(vlSelf);
#endif
            VL_FATAL_MT("lab1_imul/IntMulBase.v", 367, "", "Settle region did not converge.");
        }
        __VstlIterCount = ((IData)(1U) + __VstlIterCount);
        __VstlContinue = 0U;
        if (VIntMulBase_noparam___024root___eval_phase__stl(vlSelf)) {
            __VstlContinue = 1U;
        }
        vlSelf->__VstlFirstIteration = 0U;
    }
}

#ifdef VL_DEBUG
VL_ATTR_COLD void VIntMulBase_noparam___024root___dump_triggers__stl(VIntMulBase_noparam___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VIntMulBase_noparam__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VIntMulBase_noparam___024root___dump_triggers__stl\n"); );
    // Body
    if ((1U & (~ vlSelf->__VstlTriggered.any()))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelf->__VstlTriggered.word(0U))) {
        VL_DBG_MSGF("         'stl' region trigger index 0 is active: Internal 'stl' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void VIntMulBase_noparam___024root___stl_sequent__TOP__0(VIntMulBase_noparam___024root* vlSelf);

VL_ATTR_COLD void VIntMulBase_noparam___024root___eval_stl(VIntMulBase_noparam___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VIntMulBase_noparam__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VIntMulBase_noparam___024root___eval_stl\n"); );
    // Body
    if ((1ULL & vlSelf->__VstlTriggered.word(0U))) {
        VIntMulBase_noparam___024root___stl_sequent__TOP__0(vlSelf);
    }
}

extern const VlUnpacked<CData/*0:0*/, 8> VIntMulBase_noparam__ConstPool__TABLE_h04283ef2_0;
extern const VlUnpacked<CData/*0:0*/, 8> VIntMulBase_noparam__ConstPool__TABLE_h93919e28_0;
extern const VlUnpacked<CData/*0:0*/, 8> VIntMulBase_noparam__ConstPool__TABLE_hc2e726e8_0;
extern const VlUnpacked<CData/*0:0*/, 8> VIntMulBase_noparam__ConstPool__TABLE_h895c8fc4_0;
extern const VlUnpacked<CData/*0:0*/, 8> VIntMulBase_noparam__ConstPool__TABLE_h80cae639_0;

VL_ATTR_COLD void VIntMulBase_noparam___024root___stl_sequent__TOP__0(VIntMulBase_noparam___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VIntMulBase_noparam__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VIntMulBase_noparam___024root___stl_sequent__TOP__0\n"); );
    // Init
    CData/*0:0*/ IntMulBase_noparam__DOT__v__DOT__result_mux_sel;
    IntMulBase_noparam__DOT__v__DOT__result_mux_sel = 0;
    CData/*0:0*/ IntMulBase_noparam__DOT__v__DOT__add_mux_sel;
    IntMulBase_noparam__DOT__v__DOT__add_mux_sel = 0;
    CData/*2:0*/ __Vtableidx1;
    __Vtableidx1 = 0;
    // Body
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

VL_ATTR_COLD void VIntMulBase_noparam___024root___eval_triggers__stl(VIntMulBase_noparam___024root* vlSelf);

VL_ATTR_COLD bool VIntMulBase_noparam___024root___eval_phase__stl(VIntMulBase_noparam___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VIntMulBase_noparam__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VIntMulBase_noparam___024root___eval_phase__stl\n"); );
    // Init
    CData/*0:0*/ __VstlExecute;
    // Body
    VIntMulBase_noparam___024root___eval_triggers__stl(vlSelf);
    __VstlExecute = vlSelf->__VstlTriggered.any();
    if (__VstlExecute) {
        VIntMulBase_noparam___024root___eval_stl(vlSelf);
    }
    return (__VstlExecute);
}

#ifdef VL_DEBUG
VL_ATTR_COLD void VIntMulBase_noparam___024root___dump_triggers__ico(VIntMulBase_noparam___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VIntMulBase_noparam__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VIntMulBase_noparam___024root___dump_triggers__ico\n"); );
    // Body
    if ((1U & (~ vlSelf->__VicoTriggered.any()))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelf->__VicoTriggered.word(0U))) {
        VL_DBG_MSGF("         'ico' region trigger index 0 is active: Internal 'ico' trigger - first iteration\n");
    }
    if ((2ULL & vlSelf->__VicoTriggered.word(0U))) {
        VL_DBG_MSGF("         'ico' region trigger index 1 is active: Internal 'ico' trigger - DPI export trigger\n");
    }
}
#endif  // VL_DEBUG

#ifdef VL_DEBUG
VL_ATTR_COLD void VIntMulBase_noparam___024root___dump_triggers__act(VIntMulBase_noparam___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VIntMulBase_noparam__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VIntMulBase_noparam___024root___dump_triggers__act\n"); );
    // Body
    if ((1U & (~ vlSelf->__VactTriggered.any()))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelf->__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 0 is active: Internal 'act' trigger - DPI export trigger\n");
    }
    if ((2ULL & vlSelf->__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 1 is active: @(posedge clk)\n");
    }
}
#endif  // VL_DEBUG

#ifdef VL_DEBUG
VL_ATTR_COLD void VIntMulBase_noparam___024root___dump_triggers__nba(VIntMulBase_noparam___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VIntMulBase_noparam__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VIntMulBase_noparam___024root___dump_triggers__nba\n"); );
    // Body
    if ((1U & (~ vlSelf->__VnbaTriggered.any()))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelf->__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 0 is active: Internal 'nba' trigger - DPI export trigger\n");
    }
    if ((2ULL & vlSelf->__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 1 is active: @(posedge clk)\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void VIntMulBase_noparam___024root___ctor_var_reset(VIntMulBase_noparam___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VIntMulBase_noparam__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VIntMulBase_noparam___024root___ctor_var_reset\n"); );
    // Body
    vlSelf->clk = VL_RAND_RESET_I(1);
    vlSelf->reset = VL_RAND_RESET_I(1);
    vlSelf->istream_msg = VL_RAND_RESET_Q(64);
    vlSelf->istream_rdy = VL_RAND_RESET_I(1);
    vlSelf->istream_val = VL_RAND_RESET_I(1);
    vlSelf->ostream_msg = VL_RAND_RESET_I(32);
    vlSelf->ostream_rdy = VL_RAND_RESET_I(1);
    vlSelf->ostream_val = VL_RAND_RESET_I(1);
    vlSelf->IntMulBase_noparam__DOT__v__DOT__b_mux_sel = VL_RAND_RESET_I(1);
    vlSelf->IntMulBase_noparam__DOT__v__DOT__a_mux_sel = VL_RAND_RESET_I(1);
    vlSelf->IntMulBase_noparam__DOT__v__DOT__result_en = VL_RAND_RESET_I(1);
    VL_RAND_RESET_W(4096, vlSelf->IntMulBase_noparam__DOT__v__DOT__str);
    vlSelf->IntMulBase_noparam__DOT__v__DOT__controlUnitBase_I__DOT__curr_state = VL_RAND_RESET_I(2);
    vlSelf->IntMulBase_noparam__DOT__v__DOT__controlUnitBase_I__DOT__next_state = VL_RAND_RESET_I(2);
    vlSelf->IntMulBase_noparam__DOT__v__DOT__controlUnitBase_I__DOT__counter = VL_RAND_RESET_I(6);
    vlSelf->IntMulBase_noparam__DOT__v__DOT__datapathUnitBase_I__DOT__b_mux_out = VL_RAND_RESET_I(32);
    vlSelf->IntMulBase_noparam__DOT__v__DOT__datapathUnitBase_I__DOT__b_reg_out = VL_RAND_RESET_I(32);
    vlSelf->IntMulBase_noparam__DOT__v__DOT__datapathUnitBase_I__DOT__a_mux_out = VL_RAND_RESET_I(32);
    vlSelf->IntMulBase_noparam__DOT__v__DOT__datapathUnitBase_I__DOT__a_reg_out = VL_RAND_RESET_I(32);
    vlSelf->IntMulBase_noparam__DOT__v__DOT__datapathUnitBase_I__DOT__result_mux_out = VL_RAND_RESET_I(32);
    vlSelf->IntMulBase_noparam__DOT__v__DOT__datapathUnitBase_I__DOT__result_reg_out = VL_RAND_RESET_I(32);
    vlSelf->IntMulBase_noparam__DOT__v__DOT__vc_trace__DOT__len0 = VL_RAND_RESET_I(32);
    vlSelf->IntMulBase_noparam__DOT__v__DOT__vc_trace__DOT__idx0 = VL_RAND_RESET_I(32);
    vlSelf->IntMulBase_noparam__DOT__v__DOT__vc_trace__DOT__idx1 = VL_RAND_RESET_I(32);
    vlSelf->__Vdpi_export_trigger = 0;
    vlSelf->__Vtrigprevexpr___TOP__clk__0 = VL_RAND_RESET_I(1);
}
