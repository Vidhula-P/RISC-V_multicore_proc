//========================================================================
// Network Router
//========================================================================

`ifndef LAB4_SYS_NET_ROUTER_V
`define LAB4_SYS_NET_ROUTER_V

`include "vc/net-msgs.v"
`include "vc/trace.v"
`include "vc/queues.v"

`include "lab4_sys/NetRouterRouteUnit.v"
`include "lab4_sys/NetRouterSwitchUnit.v"



module lab4_sys_NetRouter
#(
  parameter p_msg_nbits = 44
)
(
  input  logic                   clk,
  input  logic                   reset,

  // Router id (which router is this in the network?)

  input  logic     [1:0]         router_id,

  // Input streams

  input  logic [p_msg_nbits-1:0] istream_msg [3],
  input  logic                   istream_val [3],
  output logic                   istream_rdy [3],

  // Output streams

  output logic [p_msg_nbits-1:0] ostream_msg [3],
  output logic                   ostream_val [3],
  input  logic                   ostream_rdy [3]
);

  //''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // Implement router with input queues, route units, and switch units
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

  //----------------------------------------------------------------------
  // Input Queues
  //----------------------------------------------------------------------

  logic inq0_num_free_entries;
  logic inq1_num_free_entries;
  logic inq2_num_free_entries;

  logic [p_msg_nbits-1:0] inq_msg [3];   // Messages dequeued from the queues
  logic                   inq_val [3];   // Validity signal from queues
  logic                   inq_rdy [3];   // Readiness signals to queues

  logic [p_msg_nbits-1:0] route_msg [3];   // Routed messages
  logic                   route_val [3];   // Validity signals from route unit
  logic                   route_rdy [3];   // Readiness signals to route unit

  // Queue 0: Handles istream_msg[0]
  vc_Queue#( 
    .p_type(`VC_QUEUE_NORMAL), 
    .p_msg_nbits(44), 
    .p_num_msgs(2) 
  ) queue0 (
    .clk                (clk),
    .reset              (reset),
    .enq_val            (istream_val[0]),
    .enq_rdy            (istream_rdy[0]),
    .enq_msg            (istream_msg[0]),
    .deq_val            (inq_val[0]),
    .deq_rdy            (inq_rdy[0]),
    .deq_msg            (inq_msg[0]),
    .num_free_entries   (inq0_num_free_entries)
  );

  // Queue 1: Handles istream_msg[1]
  vc_Queue#( 
    .p_type(`VC_QUEUE_NORMAL), 
    .p_msg_nbits(44), 
    .p_num_msgs(2) 
  ) queue1 (
    .clk                (clk),
    .reset              (reset),
    .enq_val            (istream_val[1]),
    .enq_rdy            (istream_rdy[1]),
    .enq_msg            (istream_msg[1]),
    .deq_val            (inq_val[1]),
    .deq_rdy            (inq_rdy[1]),
    .deq_msg            (inq_msg[1]),
    .num_free_entries   (inq1_num_free_entries)
  );

  // Queue 2: Handles istream_msg[2]
  vc_Queue#( 
    .p_type(`VC_QUEUE_NORMAL), 
    .p_msg_nbits(44), 
    .p_num_msgs(2) 
  ) queue2 (
    .clk                (clk),
    .reset              (reset),
    .enq_val            (istream_val[2]),
    .enq_rdy            (istream_rdy[2]),
    .enq_msg            (istream_msg[2]),
    .deq_val            (inq_val[2]),
    .deq_rdy            (inq_rdy[2]),
    .deq_msg            (inq_msg[2]),
    .num_free_entries   (inq2_num_free_entries)
  );

 // Instantiating the router
 lab4_sys_NetRouterRouteUnit#(44) route_unit (
  .clk            (clk),
  .reset          (reset),
  .router_id      (router_id),
  .istream_msg    (inq_msg),  // Messages from queues
  .istream_val    (inq_val),  // Vailidity readiness
  .istream_rdy    (inq_rdy),  // Input readiness
  .ostream_msg    (route_msg), // Routed messages
  .ostream_val    (route_val), // Validity for next stage
  .ostream_rdy    (route_rdy)  // Readiness from next stage
 );
 
 // Output Connections
  assign ostream_msg[0] = route_unit.ostream_msg[0];
  assign ostream_val[0] = route_unit.ostream_val[0];
  assign ostream_rdy[0] = route_unit.ostream_rdy[0];

  assign ostream_msg[1] = route_unit.ostream_msg[1];
  assign ostream_val[1] = route_unit.ostream_val[1];
  assign ostream_rdy[1] = route_unit.ostream_rdy[1];

  assign ostream_msg[2] = route_unit.ostream_msg[2];
  assign ostream_val[2] = route_unit.ostream_val[2];
  assign ostream_rdy[2] = route_unit.ostream_rdy[2];

  assign ostream_msg[3] = route_unit.ostream_msg[3];
  assign ostream_val[3] = route_unit.ostream_val[3];
  assign ostream_rdy[3] = route_unit.ostream_rdy[3];

  //----------------------------------------------------------------------
  // Line Tracing
  //----------------------------------------------------------------------

  `ifndef SYNTHESIS

  vc_NetMsgTrace#(p_msg_nbits) ostream0_trace
  (
    .clk   (clk),
    .reset (reset),
    .msg   (ostream_msg[0]),
    .val   (ostream_val[0]),
    .rdy   (ostream_rdy[0])
  );

  vc_NetMsgTrace#(p_msg_nbits) ostream1_trace
  (
    .clk   (clk),
    .reset (reset),
    .msg   (ostream_msg[1]),
    .val   (ostream_val[1]),
    .rdy   (ostream_rdy[1])
  );

  vc_NetMsgTrace#(p_msg_nbits) ostream2_trace
  (
    .clk   (clk),
    .reset (reset),
    .msg   (ostream_msg[2]),
    .val   (ostream_val[2]),
    .rdy   (ostream_rdy[2])
  );

  logic [`VC_TRACE_NBITS-1:0] str;
  `VC_TRACE_BEGIN /*
  begin

    // Line tracing for input queues

    case ( inq0_num_free_entries )
      4: vc_trace.append_str( trace_str, " " );
      3: vc_trace.append_str( trace_str, "." );
      2: vc_trace.append_str( trace_str, ":" );
      1: vc_trace.append_str( trace_str, "*" );
      0: vc_trace.append_str( trace_str, "#" );
    endcase

    case ( inq1_num_free_entries )
      4: vc_trace.append_str( trace_str, " " );
      3: vc_trace.append_str( trace_str, "." );
      2: vc_trace.append_str( trace_str, ":" );
      1: vc_trace.append_str( trace_str, "*" );
      0: vc_trace.append_str( trace_str, "#" );
    endcase

    case ( inq2_num_free_entries )
      4: vc_trace.append_str( trace_str, " " );
      3: vc_trace.append_str( trace_str, "." );
      2: vc_trace.append_str( trace_str, ":" );
      1: vc_trace.append_str( trace_str, "*" );
      0: vc_trace.append_str( trace_str, "#" );
    endcase

    vc_trace.append_str( trace_str, "|" );

    // Line tracing for switch units

    sunit0.line_trace( trace_str );
    sunit1.line_trace( trace_str );
    sunit2.line_trace( trace_str );

  end */
  `VC_TRACE_END

  `endif /* SYNTHESIS */

endmodule

`endif /* NET_ROUTER_V */
