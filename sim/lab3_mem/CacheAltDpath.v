//=========================================================================
// Alt Blocking Cache Datapath
//=========================================================================

`ifndef LAB3_MEM_CACHE_ALT_DPATH_V
`define LAB3_MEM_CACHE_ALT_DPATH_V

`include "vc/mem-msgs.v"
`include "vc/srams.v"
`include "vc/regs.v"
`include "vc/muxes.v"
`include "vc/arithmetic.v"

`include "lab3_mem/WbenDecoder.v"
`include "lab3_mem/ReplUnit.v"

module lab3_mem_CacheAltDpath
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
  input logic           wben_mux_sel,
  input logic           read_data_zero_mux_sel,
  input logic           memreq_addr_mux_sel,
  input logic           read_data_reg_en,
  input logic           evict_addr_reg_en,
  input logic [3:0]     cacheresp_type,
  input logic           hit,
  input logic [3:0]     memreq_type,

  input logic           lru_bit,

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
  logic  [1:0] cachereq_addr_bank;
  logic  [2:0] cachereq_addr_index;
  logic [24:0] cachereq_addr_tag;

  always @(*) begin
    if ( p_num_banks == 1 ) begin
      cachereq_addr_byte_offset = cachereq_addr[1:0];
      cachereq_addr_word_offset = cachereq_addr[3:2];
      cachereq_addr_bank        = 2'b0;
      cachereq_addr_index       = cachereq_addr[6:4];
      cachereq_addr_tag         = cachereq_addr[31:7];
    end
    else if ( p_num_banks == 4 ) begin
      // handle address mapping for four banks
      cachereq_addr_byte_offset = cachereq_addr[1:0];
      cachereq_addr_word_offset = cachereq_addr[3:2];
      cachereq_addr_bank        = cachereq_addr[5:4];
      cachereq_addr_index       = cachereq_addr[8:6];
      cachereq_addr_tag         = {2'b0, cachereq_addr[31:9]}; // can either pad tag with zeroes or just include bank?
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
    .in0(cachereq_data_replicated),
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
    .in0(wben_decoder_out),
    .in1(16'hFFFF),
    .sel(wben_mux_sel),
    .out(wben_mux_out)
  );

  // Way 0 Tag array ( tags, 25 bits/tag)

  logic [24:0] tag_array_read_out_way0;

  vc_CombinationalBitSRAM_1rw
  #(
    .p_data_nbits  (25),
    .p_num_entries (8)
  )
  way0_tag_array
  (
    .clk           (clk),
    .reset         (reset),
    .read_addr     (cachereq_addr_index),
    .read_data     (tag_array_read_out_way0),
    .write_en      (tag_array_wen),
    .read_en       (tag_array_ren),
    .write_addr    (cachereq_addr_index),
    .write_data    (cachereq_addr_tag)
  );

  // Way 1 Tag array ( tags, 25 bits/tag)

  logic [24:0] tag_array_read_out_way1;

  vc_CombinationalBitSRAM_1rw
  #(
    .p_data_nbits  (25),
    .p_num_entries (8)
  )
  way1_tag_array
  (
    .clk           (clk),
    .reset         (reset),
    .read_addr     (cachereq_addr_index),
    .read_data     (tag_array_read_out_way1),
    .write_en      (tag_array_wen),
    .read_en       (tag_array_ren),
    .write_addr    (cachereq_addr_index),
    .write_data    (cachereq_addr_tag)
  );

  logic way0_tag_match;

  //check if tags match in way 0 to determine if hit or miss
  vc_EqComparator
  #(
    .p_nbits(25)
  ) way0_cmp (
    .in0(cachereq_addr_tag),
    .in1(tag_array_read_out_way0),
    .out(way0_tag_match)
  );

  logic way1_tag_match;

  //check if tags match in way 1 to determine if hit or miss
  vc_EqComparator
  #(
    .p_nbits(25)
  ) way1_cmp (
    .in0(cachereq_addr_tag),
    .in1(tag_array_read_out_way1),
    .out(way1_tag_match)
  );

  assign tag_match = {way0_tag_match , way1_tag_match};

  //evicting a cache line back to main memory
  logic [31:0] evict_addr;
  logic [31:0] evict_addr_way0;
  logic [31:0] evict_addr_way1;

  lab3_mem_mkaddr
  #(
      .p_nbits(25),
      .c_nbits(3)
  ) addr_dataread_index_way0 (
      .in_0(tag_array_read_out_way0),
      .in_1(cachereq_addr_index),
      .out_(evict_addr_way0)
  );

  lab3_mem_mkaddr
  #(
      .p_nbits(25),
      .c_nbits(3)
  ) addr_dataread_index_way1 (
      .in_0(tag_array_read_out_way1),
      .in_1(cachereq_addr_index),
      .out_(evict_addr_way1)
  );

  always @(*) begin
    evict_addr = 32'b0;  // Default assignment to avoid latch inference

    if (lru_bit == 0) begin // if LRU was way 0, evict way 0
        if (p_num_banks == 1) begin
            evict_addr = evict_addr_way0;
        end
        else begin
            evict_addr = {tag_array_read_out_way0[22:0], cachereq_addr_index, cachereq_addr_bank, 4'b0};
        end
    end 
    else if (lru_bit == 1) begin // if LRU was way 1, evict way 1
        if (p_num_banks == 1) begin
            evict_addr = evict_addr_way1;
        end
        else begin
            evict_addr = {tag_array_read_out_way1[22:0], cachereq_addr_index, cachereq_addr_bank, 4'b0};
        end
    end
end

  logic [31:0] evict_addr_reg_out;

  vc_EnResetReg #(32,0) evict_addr_reg
  (
    .clk    (clk),
    .reset  (reset),
    .en     (evict_addr_reg_en),
    .d      (evict_addr),
    .q      (evict_addr_reg_out)
  );

  //refill the data from memory into the correct cache line after miss event
  logic [31:0] refill;

  if (p_num_banks == 1) begin
    lab3_mem_mkaddr //{tag, index, 3'b000}
    #(
      .p_nbits(25),
      .c_nbits(3)
    ) addr_tag_index(
      .in_0(cachereq_addr_tag),
      .in_1(cachereq_addr_index),
      .out_(refill)
    );
  end
  else begin
    assign refill = {cachereq_addr[31:3], 3'b0};
  end

  logic [31:0] memreq_addr_mux_out;

  vc_Mux2
  #(
    .p_nbits(32)
  ) memreq_addr_mux
  (
    .in0(evict_addr_reg_out),
    .in1(refill),
    .sel(memreq_addr_mux_sel),
    .out(memreq_addr_mux_out)
  );

  // Way 0 Data array (16 cacheslines, 128 bits/cacheline)

  logic [127:0] data_array_read_out;

  vc_CombinationalSRAM_1rw #(128,16) data_array_way0
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
    .in0(data_array_read_out),
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

  always @(*) begin
    if (cacheresp_type == `VC_MEM_RESP_MSG_TYPE_WRITE_INIT)  cacheresp_msg.data = 0;
    else if (cacheresp_type == `VC_MEM_RESP_MSG_TYPE_WRITE)  cacheresp_msg.data = 0;
    else                                                      cacheresp_msg.data = cacheresp_msg_data;
  end

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
  input logic  [p_nbits-1:0]              in_0,
  input logic  [c_nbits-1:0]              in_1,
  output logic [p_nbits + c_nbits +4-1:0] out_
);
  //addr of data to evict from cache - tag + index + 0000
  assign out_ = { in_0, in_1, 4'b0};
endmodule

`endif

