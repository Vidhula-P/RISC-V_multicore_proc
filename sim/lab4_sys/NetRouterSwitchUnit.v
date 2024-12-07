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

  //''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // Implement switch unit logic
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

  logic [1:0] selected_input;    // Tracks the selected input stream
  logic [p_msg_nbits-1:0] selected_msg; // Selected message to forward

  // Arbitration logic- Fixed priority 0 > 1 > 2
  always_comb begin
    // Default values
    selected_input = 2'b00;
    selected_msg = '0;
    ostream_val = 0;
    foreach (istream_rdy[i]) begin
      istream_rdy[i] = 0;
    end    

    if (istream_val[0]) begin
      selected_input = 2'b00;
      selected_msg = istream_msg[0];
    end else if (istream_val[1]) begin
      selected_input = 2'b01;
      selected_msg = istream_msg[1];
    end else if (istream_val[2]) begin
      selected_input = 2'b10;
      selected_msg = istream_msg[2];
    end

    // Forward message if output stream is ready
    if (ostream_rdy && (istream_val[selected_input])) begin
      ostream_val = 1;
      ostream_msg = selected_msg;
      istream_rdy[selected_input] = 1;
    end else begin
      ostream_msg = '0;
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
