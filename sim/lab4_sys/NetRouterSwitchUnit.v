//========================================================================
// Network Router Switch Unit
//========================================================================

`ifndef LAB4_SYS_NET_ROUTER_SWITCH_UNIT_V
`define LAB4_SYS_NET_ROUTER_SWITCH_UNIT_V

`include "vc/net-msgs.v"
`include "vc/trace.v"

module lab4_sys_NetRouterSwitchUnit
#(
  parameter p_msg_nbits = 44
)
(
  input  logic                   clk,
  input  logic                   reset,

  // Input streams

  input  logic [p_msg_nbits-1:0] istream_msg [3],
  input  logic                   istream_val [3],
  output logic                   istream_rdy [3],

  // Output stream

  output logic [p_msg_nbits-1:0] ostream_msg,
  output logic                   ostream_val,
  input  logic                   ostream_rdy
);

  logic [1:0] selected_input;    // Tracks the selected input stream
  logic [p_msg_nbits-1:0] selected_msg; // Selected message to forward

  logic [1:0] input_select; // input selector
  logic       input_val;

  assign input_val = (istream_val[0] || istream_val[1] || istream_val[2]);

  // Arbiter (Fixed Priority 1 > 2 > 0)
  always @(*) begin
    input_select = 0;

    if      (istream_val[1]) input_select = 2'd1;
    else if (istream_val[2]) input_select = 2'd2;
    else if (istream_val[0]) input_select = 2'd0;
  end

  // Forward message from input to output
  always @(*) begin
    foreach (istream_rdy[i]) begin
      istream_rdy[i] = 0;
    end
    ostream_msg = 'b0;
    ostream_val = 1'b0;

    if (input_val) begin
      istream_rdy[input_select] = ostream_rdy;
      ostream_msg = istream_msg[input_select];
      ostream_val = 1'b1;
    end
  end

  //----------------------------------------------------------------------
  // Line Tracing
  //----------------------------------------------------------------------

  `ifndef SYNTHESIS

  integer num_reqs = 0;

  logic [`VC_TRACE_NBITS-1:0] str;
  `VC_TRACE_BEGIN
  begin

    num_reqs = istream_val[0] + istream_val[1] + istream_val[2];

    case ( num_reqs )
      0: vc_trace.append_str( trace_str, " " );
      1: vc_trace.append_str( trace_str, "." );
      2: vc_trace.append_str( trace_str, ":" );
      3: vc_trace.append_str( trace_str, "#" );
    endcase

  end
  `VC_TRACE_END

  `endif /* SYNTHESIS */

endmodule

`endif /* NET_ROUTER_SWITCH_UNIT_V */
