//========================================================================
// Integer Multiplier Fixed-Latency Implementation
//========================================================================

`ifndef LAB1_IMUL_INT_MUL_BASE_V
`define LAB1_IMUL_INT_MUL_BASE_V

`include "vc/trace.v"
`include "vc/muxes.v"
`include "vc/regs.v"
`include "vc/arithmetic.v"

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

  /* verilator lint_off unused */
  logic result_adder_cout_null;
  /* verilator lint_on unused */

  // Circuit for b
  logic [31:0] b_mux_out;
  logic [31:0] b_reg_out;
  logic [31:0] b_shifted_out;

  assign b_lsb = b_reg_out[0];

  vc_RightLogicalShifter
  #(
    .p_nbits      (32),
    .p_shamt_nbits(1)
  ) right_shift (
    .in   (b_reg_out),
    .shamt(1'b1),
    .out  (b_shifted_out)
  );

  vc_Mux2 //2-1 multiplexer
  #(
    .p_nbits(32) //input and output are 32 b long
  ) b_mux (
    .in0(istream_msg[31:0]), //first 32 b of the 64 b input message is b
    .in1(b_shifted_out), //output of b circuit after being shifted by 'shift_amount' to the right
    .sel(b_mux_sel), //selection line for b mux
    .out(b_mux_out) //output of b mux = input to b_reg
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
  logic [31:0] a_shifted_out;

  vc_LeftLogicalShifter
  #(
    .p_nbits      (32),
    .p_shamt_nbits(1)
  ) left_shift (
    .in   (a_reg_out),
    .shamt(1'b1),
    .out  (a_shifted_out)
  );

  vc_Mux2 //2-1 multiplexer
  #(
    .p_nbits(32) //input and output are 32 b long
  ) a_mux (
    .in0(istream_msg[63:32]), //last 32 b of the 64 b input message is s
    .in1(a_shifted_out),//output of a circuit after being shifted by shift_amount to the left
    .sel(a_mux_sel), //selection line for a mux
    .out(a_mux_out) //output of a mux = input to a_reg
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
    .in0(32'b0),
    .in1(result_adder_mux_out),
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
    .in0  (result_reg_out),
    .in1  (a_reg_out),
    .cin  (1'b0),
    .out  (result_adder_out),
    .cout (result_adder_cout_null)
  );

  vc_Mux2
  #(
    .p_nbits(32)
  ) result_adder_mux (
    .in0(result_reg_out),
    .in1(result_adder_out),
    .sel(add_mux_sel),
    .out(result_adder_mux_out)
  );

endmodule

module lab1_imul_ControlUnitBase
(
  input  logic clk,
  input  logic reset,

  output logic istream_rdy,
  input  logic istream_val,
  input  logic ostream_rdy,
  output logic ostream_val,

  input  logic b_lsb,
  output logic b_mux_sel,
  output logic a_mux_sel,
  output logic result_mux_sel,
  output logic add_mux_sel,
  output logic result_en
);

  typedef enum logic [1:0] {
    IDLE,
    CALC,
    DONE
  } state_t;

  state_t curr_state;
  state_t next_state;

  logic [5:0] counter;

  // Change state on clock edge
  always_ff @(posedge clk)
  begin
    if (reset)  curr_state <= IDLE;
    else        curr_state <= next_state;
  end

  always_ff @(posedge clk)
  begin
    if (reset)                    counter <= 0;
    else if (curr_state == CALC)  counter <= counter + 1;
    else                          counter <= 0;
  end

  // Handle state transitions
  always_comb
  begin
    case (curr_state)
      IDLE:
      begin
        if (!istream_val) next_state = IDLE;
        else              next_state = CALC;
      end
      CALC:
      begin
        if (counter < 6'd32)  next_state  = CALC;
        else                  next_state  = DONE;
      end
      DONE:
      begin
        if (!ostream_rdy) next_state = DONE;
        else              next_state = IDLE;
      end
      default:
      begin
        next_state    = IDLE;
      end
    endcase
  end

  // Handle state output
  always_comb
  begin
    case (curr_state)
      IDLE:
      begin
        b_mux_sel       = 0;
        result_mux_sel  = 0;
        a_mux_sel       = 0;
        result_en       = 1;
        add_mux_sel     = 0;
        istream_rdy     = 1;
        ostream_val     = 0;
      end
      CALC:
      begin
        b_mux_sel       = 1;
        result_mux_sel  = 1;
        a_mux_sel       = 1;
        result_en       = 1;
        if (b_lsb == 0) add_mux_sel = 0;
        else            add_mux_sel = 1;
        istream_rdy     = 0;
        ostream_val     = 0;
      end
      DONE:
      begin
        b_mux_sel       = 0;
        result_mux_sel  = 0;
        a_mux_sel       = 0;
        result_en       = 0;
        add_mux_sel     = 0;
        istream_rdy     = 0;
        ostream_val     = 1;
      end
      default:
      begin
        b_mux_sel       = 0;
        result_mux_sel  = 0;
        a_mux_sel       = 0;
        result_en       = 1;
        add_mux_sel     = 0;
        istream_rdy     = 0;
        ostream_val     = 0;
      end
    endcase
  end

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

  logic b_lsb;
  logic b_mux_sel;
  logic a_mux_sel;
  logic result_mux_sel;
  logic add_mux_sel;
  logic result_en;

  lab1_imul_ControlUnitBase controlUnitBase_I
  (
    .clk            (clk),
    .reset          (reset),

    .istream_rdy    (istream_rdy),
    .istream_val    (istream_val),
    .ostream_rdy    (ostream_rdy),
    .ostream_val    (ostream_val),

    .b_lsb          (b_lsb),
    .b_mux_sel      (b_mux_sel),
    .a_mux_sel      (a_mux_sel),
    .result_mux_sel (result_mux_sel),
    .add_mux_sel    (add_mux_sel),
    .result_en      (result_en)
  );

  lab1_imul_DatapathUnitBase datapathUnitBase_I
  (
    .clk            (clk),
    .reset          (reset),

    .result_mux_sel (result_mux_sel),
    .a_mux_sel      (a_mux_sel),
    .b_mux_sel      (b_mux_sel),
    .add_mux_sel    (add_mux_sel),

    .result_en      (result_en),

    .istream_msg    (istream_msg),
    .ostream_msg    (ostream_msg),

    .b_lsb          (b_lsb)
  );

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

