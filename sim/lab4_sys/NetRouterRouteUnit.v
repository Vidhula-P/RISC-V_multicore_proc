//========================================================================
// Network Router Route Unit
//========================================================================

`ifndef LAB4_SYS_NET_ROUTER_ROUTE_UNIT_V
`define LAB4_SYS_NET_ROUTER_ROUTE_UNIT_V

`include "vc/net-msgs.v"
`include "vc/trace.v"

//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

module lab4_sys_NetRouterRouteUnit
#(
  parameter p_msg_nbits = 44
)
(
  input  logic                   clk,
  input  logic                   reset,

  // Router id (which router is this in the network?)

  input  logic [1:0]             router_id,

  // Input stream

  input  logic [p_msg_nbits-1:0] istream_msg,
  input  logic                   istream_val,
  output logic                   istream_rdy,

  // Output streams

  output logic [p_msg_nbits-1:0] ostream_msg [3],
  output logic                   ostream_val [3],
  input  logic                   ostream_rdy [3]
);

  net_msg_hdr_t istream_msg_hdr;
  assign istream_msg_hdr = istream_msg[`VC_NET_MSGS_HDR(p_msg_nbits)];

  //''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // Implement route unit logic
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

  // Local Parameters
  localparam NUM_PORTS = 4;  // We have 4 processor, hence 4 ports

  // Determine clockwise port
  logic [1:0] next_port;
  assign next_port = (router_id + 1) % NUM_PORTS;

  // Connect input stream to the appropriate output port
  always_comb begin
    // Default values
    foreach (ostream_msg[i]) begin
      ostream_msg[i] = 1'b0;
    end
    foreach (ostream_val[i]) begin
      ostream_val[i] = 1'b0;
    end
    istream_rdy = 1'b0;

    // Route to clockwise port if ready
    if (istream_val && ostream_rdy[next_port]) begin
      ostream_msg[next_port] = istream_msg;
      ostream_val[next_port] = 1'b1;
      istream_rdy = 1'b1; // Downstream is ready
    end
  end


  //----------------------------------------------------------------------
  // Line Tracing
  //----------------------------------------------------------------------

  `ifndef SYNTHESIS

  logic [`VC_TRACE_NBITS-1:0] str;
  `VC_TRACE_BEGIN
  begin

    if ( istream_val && istream_rdy ) begin
      $sformat( str, "%d", istream_msg_hdr.dest );
      vc_trace.append_str( trace_str, str );
    end
    else
      vc_trace.append_str( trace_str, " " );

  end
  `VC_TRACE_END

  `endif /* SYNTHESIS */

endmodule

`endif /* NET_ROUTER_ROUTE_UNIT_V */
