//=========================================================================
// Base Blocking Cache Datapath
//=========================================================================

`ifndef LAB3_MEM_CACHE_BASE_DPATH_V
`define LAB3_MEM_CACHE_BASE_DPATH_V

`include "vc/mem-msgs.v"
`include "vc/srams.v"
`include "vc/regs.v"

`include "lab3_mem/WbenDecoder.v"
`include "lab3_mem/ReplUnit.v"

module lab3_mem_CacheBaseDpath
#(
  parameter p_num_banks = 1
)
(
  input  logic          clk,
  input  logic          reset,

  // Processor <-> Cache Interface

  input  mem_req_4B_t   cachereq_msg,
  output mem_resp_4B_t  cacheresp_msg,

  // Cache <-> Memory Interface

  output mem_req_16B_t  memreq_msg,
  input  mem_resp_16B_t memresp_msg,

  // control signals (ctrl->dpath)

  input  logic          cachereq_reg_en,
  input  logic          tag_array_wen,
  input  logic          tag_array_ren,
  input  logic          data_array_wen,
  input  logic          data_array_ren,

  input logic           memresp_en,
  input logic           write_data_mux_sel,
  input logic           read_data_zero_mux_sel,
  input logic           read_data_reg_en,
  input logic           evict_addr_reg_en,
  input logic [3:0]     cacheresp_type,
  input logic           hit,
  input logic [3:0]     memreq_type,

  // status signals (dpath->ctrl)

  output logic  [3:0]   cachereq_type,
  output logic [31:0]   cachereq_addr,

  output logic          tag_match
);

  // Register the unpacked cachereq_msg

  logic [31:0] cachereq_addr_reg_out;
  logic [31:0] cachereq_data_reg_out;
  logic  [3:0] cachereq_type_reg_out;
  logic  [7:0] cachereq_opaque_reg_out;

  vc_EnResetReg #(4,0) cachereq_type_reg
  (
    .clk    (clk),
    .reset  (reset),
    .en     (cachereq_reg_en),
    .d      (cachereq_msg.type_),
    .q      (cachereq_type_reg_out)
  );

  vc_EnResetReg #(32,0) cachereq_addr_reg
  (
    .clk    (clk),
    .reset  (reset),
    .en     (cachereq_reg_en),
    .d      (cachereq_msg.addr),
    .q      (cachereq_addr_reg_out)
  );

  vc_EnResetReg #(8,0) cachereq_opaque_reg
  (
    .clk    (clk),
    .reset  (reset),
    .en     (cachereq_reg_en),
    .d      (cachereq_msg.opaque),
    .q      (cachereq_opaque_reg_out)
  );

  vc_EnResetReg #(32,0) cachereq_data_reg
  (
    .clk    (clk),
    .reset  (reset),
    .en     (cachereq_reg_en),
    .d      (cachereq_msg.data),
    .q      (cachereq_data_reg_out)
  );

  assign cachereq_type = cachereq_type_reg_out;
  assign cachereq_addr = cachereq_addr_reg_out;

  // Address Mapping

  logic  [1:0] cachereq_addr_byte_offset;
  logic  [1:0] cachereq_addr_word_offset;
  logic  [3:0] cachereq_addr_index;
  logic [23:0] cachereq_addr_tag;

  always @(*) begin
    if ( p_num_banks == 1 ) begin
      cachereq_addr_byte_offset = cachereq_addr[1:0];
      cachereq_addr_word_offset = cachereq_addr[3:2];
      cachereq_addr_index       = cachereq_addr[7:4];
      cachereq_addr_tag         = cachereq_addr[31:8];
    end
    else if ( p_num_banks == 4 ) begin
      // handle address mapping for four banks
      cachereq_addr_byte_offset = cachereq_addr[1:0];
      cachereq_addr_word_offset = cachereq_addr[3:2];
      cachereq_addr_index       = cachereq_addr[9:6];
      cachereq_addr_tag         = {cachereq_addr[31:10], 2'b0}; // can either pad tag with zeroes or just include bank?
    end
  end

  // Replicate 32-bit cachereq_data to make 128-bit data word

  logic [127:0] cachereq_data_replicated;

  lab3_mem_ReplUnit repl_unit
  (
    .in_ (cachereq_data_reg_out),
    .out (cachereq_data_replicated)
  );

  // Register memresp_msg

  logic [127:0] memresp_data_reg_out;
  logic [127:0] write_data_mux_out;

  vc_EnResetReg
  #(
    .p_nbits(128),
    .p_reset_value(0)
  ) memresp_data_reg
  (
    .clk(clk),
    .reset(reset),
    .d(memresp_msg.data),
    .q(memresp_data_reg_out),
    .en(memresp_en)
  );

  vc_Mux2
  #(
    .p_nbits(128)
  ) write_data_mux
  (
    .in0(cachereq_data_replicated)
    .in1(memresp_data_reg_out),
    .sel(write_data_mux_sel),
    .out(write_data_mux_out)
  );

  // Write byte enable decoder

  logic [15:0] wben_decoder_out;

  lab3_mem_WbenDecoder wben_decoder
  (
    .in_ (cachereq_addr_word_offset),
    .out (wben_decoder_out)
  );

  logic [15:0] wben_mux_out;

  vc_Mux2
  #(
    .p_nbits(16)
  ) write_byte_en_mux
  (
    .in0(wben_decoder_out)
    .in1(16'hFFFF),
    .sel(wben_mux_sel),
    .out(wben_mux_out)
  );

  // Tag array (16 tags, 24 bits/tag)

  logic [23:0] tag_array_read_out;

  vc_CombinationalBitSRAM_1rw
  #(
    .p_data_nbits  (24),
    .p_num_entries (16)
  )
  tag_array
  (
    .clk           (clk),
    .reset         (reset),
    .read_addr     (cachereq_addr_index),
    .read_data     (tag_array_read_out),
    .write_en      (tag_array_wen),
    .read_en       (tag_array_ren),
    .write_addr    (cachereq_addr_index),
    .write_data    (cachereq_addr_tag)
  );

  //check if tags match to determine if hit or miss
  vc_EqComparator
  #(
    .p_nbits(24)
  ) cmp (
    .in0(cachereq_addr_tag),
    .in1(tag_array_read_out),
    .out(tag_match)
  );

  //evicting a cache line back to main memory
  logic [31:0] evict_addr;

  lab3_mem_mkaddr //{read_data, index, 4'b0000}
  #(
    .p_nbits(24),
    .c_nbits(4)
  ) addr_dataread_index(
    .in_0(tag_array_read_out),
    .in_1(cachereq_addr_index),
    .out_(evict_addr),
  );

  logic [31:0] evict_addr_reg_out;

  vc_EnResetReg #(3,0) evict_addr_reg
  (
    .clk    (clk),
    .reset  (reset),
    .en     (evict_addr_reg_en),
    .d      (evict_addr)
    .q      (evict_addr_reg_out),
  );

  //refill the data from memory into the correct cache line after miss event
  logic [31:0] refill;

  lab3_mem_mkaddr //{tag, index, 4'b0000}
  #(
    .p_nbits(24),
    .c_nbits(4)
  ) addr_tag_index(
    .in_0(cachereq_addr_tag),
    .in_1(cachereq_addr_index),
    .out_(refill),
  );

  vc_Mux2
  #(
    .p_nbits(32)
  ) memreq_addr_mux
  (
    .in0(evict_addr_reg_out)
    .in1(refill),
    .sel(memreq_addr_mux_sel),
    .out(memreq_addr_mux_out)
  );

  // Data array (16 cacheslines, 128 bits/cacheline)

  logic [127:0] data_array_read_out;

  vc_CombinationalSRAM_1rw #(128,16) data_array
  (
    .clk           (clk),
    .reset         (reset),
    .read_addr     (cachereq_addr_index),
    .read_data     (data_array_read_out),
    .write_en      (data_array_wen),
    .read_en       (data_array_ren),
    .write_byte_en (wben_mux_out),
    .write_addr    (cachereq_addr_index),
    .write_data    (write_data_mux_out)
  );

  logic [127:0] read_data_zero_mux_out;

  vc_Mux2
  #(
    .p_nbits(128)
  ) read_data_zero_mux
  (
    .in0(data_array_read_out)
    .in1(128'b0),
    .sel(read_data_zero_mux_sel),
    .out(read_data_zero_mux_out)
  );

  logic [127:0] read_data_reg_out;

  vc_EnResetReg #(128,0) read_data_reg
  (
    .clk    (clk),
    .reset  (reset),
    .en     (read_data_reg_en),
    .d      (read_data_zero_mux_out),
    .q      (read_data_reg_out)
  );

  logic [31:0] cacheresp_msg_data;

  vc_Mux4
  #(
    .p_nbits(32)
  ) read_data_mux4 (
    .in0(read_data_reg_out[31:0]),
    .in1(read_data_reg_out[63:32]),
    .in2(read_data_reg_out[95:64]),
    .in3(read_data_reg_out[127:96]),
    .sel(cachereq_addr_word_offset),
    .out(cacheresp_msg_data)
  );

  assign cacheresp_msg.type_  = cacheresp_type;
  assign cacheresp_msg.opaque = cachereq_opaque_reg_out;
  assign cacheresp_msg.test   = {1'b0, hit};
  assign cacheresp_msg.len    = 2'b0;
  assign cacheresp_msg.data   = cacheresp_msg_data;

  assign memreq_msg.type_  = memreq_type;
  assign memreq_msg.opaque = 8'b0;
  assign memreq_msg.addr   = memreq_addr_mux_out;
  assign memreq_msg.len    = 4'b0;
  assign memreq_msg.data   = read_data_reg_out;

endmodule

module lab3_mem_mkaddr
#(
  parameter p_nbits = 1,
  parameter c_nbits = 1
)(
  input logic  [p_nbits-1:0] in_0,
  input logic  [c_nbits-1:0] in_1,
  output logic               out_
);
  //addr of data to evict from cache - tag + index + 0000
  assign out_ = { in_0, in_1, 4'b0};
endmodule

`endif


