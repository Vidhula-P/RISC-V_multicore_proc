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

  //----------------------------------------------------------------------
  // Input Queues
  //----------------------------------------------------------------------

  logic [2:0] inq0_num_free_entries;
  logic [2:0] inq1_num_free_entries;
  logic [2:0] inq2_num_free_entries;

  logic [p_msg_nbits-1:0] inq_msg [3];   // Messages dequeued from the queues
  logic                   inq_val [3];   // Validity signal from queues
  logic                   inq_rdy [3];   // Readiness signals to queues

  // Queue 0: Handles istream_msg[0]
  vc_Queue#(
    .p_type(`VC_QUEUE_NORMAL),
    .p_msg_nbits(p_msg_nbits),
    .p_num_msgs(4)
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
    .p_msg_nbits(p_msg_nbits),
    .p_num_msgs(4)
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
    .p_msg_nbits(p_msg_nbits),
    .p_num_msgs(4)
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

  // Outputs from each route unit

  logic [p_msg_nbits-1:0] runit0_msg [3];
  logic                   runit0_val [3];
  logic                   runit0_rdy [3];

  logic [p_msg_nbits-1:0] runit1_msg [3];
  logic                   runit1_val [3];
  logic                   runit1_rdy [3];

  logic [p_msg_nbits-1:0] runit2_msg [3];
  logic                   runit2_val [3];
  logic                   runit2_rdy [3];

  logic [p_msg_nbits-1:0] sunit0_istream_msg [3];
  logic                   sunit0_istream_val [3];
  logic                   sunit0_istream_rdy [3];

  logic [p_msg_nbits-1:0] sunit1_istream_msg [3];
  logic                   sunit1_istream_val [3];
  logic                   sunit1_istream_rdy [3];

  logic [p_msg_nbits-1:0] sunit2_istream_msg [3];
  logic                   sunit2_istream_val [3];
  logic                   sunit2_istream_rdy [3];

  always @(*) begin
    // Concatenate messages for each switch unit (sunit0, sunit1, sunit2)
    sunit0_istream_msg = {runit0_msg[0], runit1_msg[0], runit2_msg[0]};
    sunit1_istream_msg = {runit0_msg[1], runit1_msg[1], runit2_msg[1]};
    sunit2_istream_msg = {runit0_msg[2], runit1_msg[2], runit2_msg[2]};

    // Concatenate valid signals for each switch unit
    sunit0_istream_val = {runit0_val[0], runit1_val[0], runit2_val[0]};
    sunit1_istream_val = {runit0_val[1], runit1_val[1], runit2_val[1]};
    sunit2_istream_val = {runit0_val[2], runit1_val[2], runit2_val[2]};

    // Assign ready signals for route units
    runit0_rdy = {sunit0_istream_rdy[0], sunit1_istream_rdy[0], sunit2_istream_rdy[0]};
    runit1_rdy = {sunit0_istream_rdy[1], sunit1_istream_rdy[1], sunit2_istream_rdy[1]};
    runit2_rdy = {sunit0_istream_rdy[2], sunit1_istream_rdy[2], sunit2_istream_rdy[2]};
  end

  // Instantiating three route units
  lab4_sys_NetRouterRouteUnit #(p_msg_nbits) runit0 (
    .clk            (clk),
    .reset          (reset),
    .router_id      (router_id),
    .istream_msg    (inq_msg[0]),  // Messages from queues
    .istream_val    (inq_val[0]),  // Vailidity readiness
    .istream_rdy    (inq_rdy[0]),  // Input readiness
    .ostream_msg    ({runit0_msg[0], runit0_msg[1], runit0_msg[2]}), // Routed messages
    .ostream_val    (runit0_val), // Validity for next stage
    .ostream_rdy    (runit0_rdy)  // Readiness from next stage
  );

  lab4_sys_NetRouterRouteUnit #(p_msg_nbits) runit1 (
    .clk            (clk),
    .reset          (reset),
    .router_id      (router_id),
    .istream_msg    (inq_msg[1]),  // Messages from queues
    .istream_val    (inq_val[1]),  // Vailidity readiness
    .istream_rdy    (inq_rdy[1]),  // Input readiness
    .ostream_msg    ({runit1_msg[0], runit1_msg[1], runit1_msg[2]}), // Routed messages
    .ostream_val    (runit1_val), // Validity for next stage
    .ostream_rdy    (runit1_rdy)  // Readiness from next stage
  );

  lab4_sys_NetRouterRouteUnit #(p_msg_nbits) runit2 (
    .clk            (clk),
    .reset          (reset),
    .router_id      (router_id),
    .istream_msg    (inq_msg[2]),  // Messages from queues
    .istream_val    (inq_val[2]),  // Vailidity readiness
    .istream_rdy    (inq_rdy[2]),  // Input readiness
    .ostream_msg    ({runit2_msg[0], runit2_msg[1], runit2_msg[2]}), // Routed messages
    .ostream_val    (runit2_val), // Validity for next stage
    .ostream_rdy    (runit2_rdy)  // Readiness from next stage
  );

  // Instantiating three switch units
  lab4_sys_NetRouterSwitchUnit #(p_msg_nbits) sunit0 (
    .clk            (clk),
    .reset          (reset),
    .istream_msg    ({sunit0_istream_msg[0], sunit0_istream_msg[1], sunit0_istream_msg[2]}),
    .istream_val    (sunit0_istream_val),
    .istream_rdy    (sunit0_istream_rdy),
    .ostream_msg    (ostream_msg[0]),
    .ostream_val    (ostream_val[0]),
    .ostream_rdy    (ostream_rdy[0])
  );

  lab4_sys_NetRouterSwitchUnit #(p_msg_nbits) sunit1 (
    .clk            (clk),
    .reset          (reset),
    .istream_msg    ({sunit1_istream_msg[0], sunit1_istream_msg[1], sunit1_istream_msg[2]}),
    .istream_val    (sunit1_istream_val),
    .istream_rdy    (sunit1_istream_rdy),
    .ostream_msg    (ostream_msg[1]),
    .ostream_val    (ostream_val[1]),
    .ostream_rdy    (ostream_rdy[1])
  );

  lab4_sys_NetRouterSwitchUnit #(p_msg_nbits) sunit2 (
    .clk            (clk),
    .reset          (reset),
    .istream_msg    ({sunit2_istream_msg[0], sunit2_istream_msg[1], sunit2_istream_msg[2]}),
    .istream_val    (sunit2_istream_val),
    .istream_rdy    (sunit2_istream_rdy),
    .ostream_msg    (ostream_msg[2]),
    .ostream_val    (ostream_val[2]),
    .ostream_rdy    (ostream_rdy[2])
  );

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
  `VC_TRACE_BEGIN
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

    runit0.line_trace( trace_str );
    runit1.line_trace( trace_str );
    runit2.line_trace( trace_str );

    vc_trace.append_str( trace_str, "|" );

    // Line tracing for switch units

    sunit0.line_trace( trace_str );
    sunit1.line_trace( trace_str );
    sunit2.line_trace( trace_str );

  end
  `VC_TRACE_END

  `endif /* SYNTHESIS */

endmodule

`endif /* NET_ROUTER_V */
