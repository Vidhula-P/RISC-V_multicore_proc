//========================================================================
// Integer Multiplier Fixed-Latency Implementation
//========================================================================

`ifndef LAB1_IMUL_INT_MUL_BASE_V
`define LAB1_IMUL_INT_MUL_BASE_V

`include "vc/trace.v"

// ''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
// Define datapath and control unit here.
// '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

module lab1_imul_DatapathUnitBase
(
  input  logic        clk,
  input  logic        reset,

  input  logic        result_mux_sel,
  input  logic        a_mux_sel,
  input  logic        b_mux_sel,
  input  logic        add_mux_sel,

  input  logic        result_en,

  input  logic [63:0] istream_msg,
  output logic [31:0] ostream_msg,

  output logic        b_lsb
);

  logic [31:0] result_adder_cout_null;

  // Circuit for b
  logic [31:0] b_mux_out;
  logic [31:0] b_reg_out;

  assign b_lsb = b_reg_out[0];

  vc_Mux2
  #(
    .p_nbits(32)
  ) b_mux (
    .in0(b_reg_out >> 1),
    .in1(istream_msg[31:0]),
    .sel(b_mux_sel),
    .out(b_mux_out)
  );

  vc_Reg
  #(
    .p_nbits(32)
  ) b_reg (
    .clk(clk),
    .q  (b_reg_out),
    .d  (b_mux_out)
  );

  // Circuit for a
  logic [31:0] a_mux_out;
  logic [31:0] a_reg_out;

  vc_Mux2
  #(
    .p_nbits(32)
  ) a_mux (
    .in0(a_reg_out << 1),
    .in1(istream_msg[63:32]),
    .sel(a_mux_sel),
    .out(a_mux_out)
  );

  vc_Reg
  #(
    .p_nbits(32)
  ) a_reg (
    .clk(clk),
    .q  (a_reg_out),
    .d  (a_mux_out)
  );

  // Circuit for result
  logic [31:0] result_mux_out;
  logic [31:0] result_reg_out;
  logic [31:0] result_adder_out;
  logic [31:0] result_adder_mux_out;

  assign ostream_msg = result_reg_out;

  vc_Mux2
  #(
    .p_nbits(32)
  ) result_mux (
    .in0(result_adder_mux_out),
    .in1(32'b0),
    .sel(result_mux_sel),
    .out(result_mux_out)
  );

  vc_EnReg
  #(
    .p_nbits(32)
  ) result_reg (
    .clk  (clk),
    .reset(reset),
    .q    (result_reg_out),
    .d    (result_mux_out),
    .en   (result_en)
  );

  vc_Adder
  #(
    .p_nbits(32)
  ) result_adder (
    .in0  (a_reg_out),
    .in1  (result_reg_out),
    .cin  (32'b0),
    .out  (result_adder_out),
    .cout (result_adder_cout_null)
  );

  vc_Mux2
  #(
    .p_nbits(32)
  ) result_adder_mux (
    .in0(result_adder_out),
    .in1(result_reg_out),
    .sel(add_mux_sel),
    .out(result_adder_mux_out)
  );

endmodule

//========================================================================
// Integer Multiplier Fixed-Latency Implementation
//========================================================================

module lab1_imul_IntMulBase
(
  input  logic        clk,
  input  logic        reset,

  input  logic        istream_val,
  output logic        istream_rdy,
  input  logic [63:0] istream_msg,

  output logic        ostream_val,
  input  logic        ostream_rdy,
  output logic [31:0] ostream_msg
);

  // ''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // Instantiate datapath and control models here and then connect them
  // together.
  // '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

  //----------------------------------------------------------------------
  // Line Tracing
  //----------------------------------------------------------------------

  `ifndef SYNTHESIS

  logic [`VC_TRACE_NBITS-1:0] str;
  `VC_TRACE_BEGIN
  begin

    $sformat( str, "%x", istream_msg );
    vc_trace.append_val_rdy_str( trace_str, istream_val, istream_rdy, str );

    vc_trace.append_str( trace_str, "(" );

    // ''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''
    // Add additional line tracing using the helper tasks for
    // internal state including the current FSM state.
    // '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    vc_trace.append_str( trace_str, ")" );

    $sformat( str, "%x", ostream_msg );
    vc_trace.append_val_rdy_str( trace_str, ostream_val, ostream_rdy, str );

  end
  `VC_TRACE_END

  `endif /* SYNTHESIS */

endmodule

`endif /* LAB1_IMUL_INT_MUL_BASE_V */

