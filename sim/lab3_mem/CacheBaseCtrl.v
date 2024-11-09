//=========================================================================
// Base Blocking Cache Control
//=========================================================================

`ifndef LAB3_MEM_CACHE_BASE_CTRL_V
`define LAB3_MEM_CACHE_BASE_CTRL_V

`include "vc/regfiles.v"
`include "vc/regs.v"
`include "vc/mem-msgs.v"

module lab3_mem_CacheBaseCtrl
#(
  parameter p_num_banks = 1
)
(
  input  logic        clk,
  input  logic        reset,

  // Processor <-> Cache Interface

  input  logic        cachereq_val,
  output logic        cachereq_rdy,

  output logic        cacheresp_val,
  input  logic        cacheresp_rdy,

  // Cache <-> Memory Interface

  output logic        memreq_val,
  input  logic        memreq_rdy,

  input  logic        memresp_val,
  output logic        memresp_rdy,

  // control signals (ctrl->dpath)

  output logic        cachereq_reg_en,
  output logic        tag_array_wen,
  output logic        tag_array_ren,
  output logic        data_array_wen,
  output logic        data_array_ren,

  output logic        memresp_en,
  output logic        write_data_mux_sel,
  output logic        wben_mux_sel,
  output logic        read_data_zero_mux_sel,
  output logic        memreq_addr_mux_sel,
  output logic        read_data_reg_en,
  output logic        evict_addr_reg_en,
  output logic [3:0]  cacheresp_type,
  output logic        hit,
  output logic [3:0]  memreq_type,

  // status signals (dpath->ctrl)

  input  logic  [3:0] cachereq_type,
  input  logic [31:0] cachereq_addr,
  input  logic        tag_match
);

  //----------------------------------------------------------------------
  // State Definitions
  //----------------------------------------------------------------------

  localparam STATE_IDLE              = 5'd0;
  localparam STATE_TAG_CHECK         = 5'd1;
  localparam STATE_INIT_DATA_ACCESS  = 5'd2;
  localparam STATE_READ_DATA_ACCESS  = 5'd3;
  localparam STATE_WRITE_DATA_ACCESS = 5'd4;
  localparam STATE_REFILL_REQUEST    = 5'd5;
  localparam STATE_REFILL_WAIT       = 5'd6;
  localparam STATE_REFILL_UPDATE     = 5'd7;
  localparam STATE_EVICT_PREPARE     = 5'd8;
  localparam STATE_EVICT_REQUEST     = 5'd9;
  localparam STATE_EVICT_WAIT        = 5'd10;
  localparam STATE_WAIT              = 5'd11;

  //----------------------------------------------------------------------
  // State
  //----------------------------------------------------------------------

  always @( posedge clk ) begin
    if ( reset ) begin
      state_reg <= STATE_IDLE;
    end
    else begin
      state_reg <= next_state;
    end
  end

  //----------------------------------------------------------------------
  // State Transitions
  //----------------------------------------------------------------------

  logic is_read;
  logic is_write;
  logic is_init;

  logic hit_TC;
  assign hit_TC = is_valid && tag_match;

  assign is_read  = (cachereq_type == `VC_MEM_REQ_MSG_TYPE_READ);
  assign is_write = (cachereq_type == `VC_MEM_REQ_MSG_TYPE_WRITE);
  assign is_init  = (cachereq_type == `VC_MEM_REQ_MSG_TYPE_WRITE_INIT);

  logic [4:0] state_reg;
  logic [4:0] next_state;

  logic is_dirty;
  logic is_valid;

  always @(*) begin

    case ( state_reg )

      STATE_IDLE: begin
        // Waits for a cache request and then transitions to STATE_TAG_CHECK if a request is valid.
        if ( cachereq_val ) next_state = STATE_TAG_CHECK;
        else                next_state = STATE_IDLE;
      end

      STATE_TAG_CHECK: begin
        if ( is_init )                   next_state = STATE_INIT_DATA_ACCESS;
        else if ( is_read && hit_TC )    next_state = STATE_READ_DATA_ACCESS;  //Read hit
        else if ( is_write && hit_TC )   next_state = STATE_WRITE_DATA_ACCESS; //Write hit
        else if ( !hit_TC && is_dirty )  next_state = STATE_EVICT_PREPARE;     //Write miss when cache line is dirty
        else if ( !hit_TC && !is_dirty ) next_state = STATE_REFILL_REQUEST;    //Read miss or Write miss when cache line is NOT dirty
        else                             next_state = STATE_IDLE;
      end

      STATE_INIT_DATA_ACCESS: begin
        next_state = STATE_WAIT;
      end

      STATE_READ_DATA_ACCESS: begin
        next_state = STATE_WAIT;
      end

      STATE_WRITE_DATA_ACCESS: begin
        next_state = STATE_WAIT;
      end

      STATE_REFILL_REQUEST: begin
        if (memreq_rdy) next_state = STATE_REFILL_WAIT;
        else            next_state = STATE_REFILL_REQUEST;
      end

      STATE_REFILL_WAIT: begin
        if (memresp_val)  next_state = STATE_REFILL_UPDATE;
        else              next_state = STATE_REFILL_WAIT;
      end

      STATE_REFILL_UPDATE: begin
        if (is_write)     next_state = STATE_WRITE_DATA_ACCESS;
        else if (is_read) next_state = STATE_READ_DATA_ACCESS;
        else              next_state = STATE_IDLE;
      end

      STATE_EVICT_PREPARE: begin
        next_state = STATE_EVICT_REQUEST;
      end

      STATE_EVICT_REQUEST: begin
        if (memreq_rdy) next_state = STATE_EVICT_WAIT;
        else            next_state = STATE_EVICT_REQUEST;
      end

      STATE_EVICT_WAIT: begin
        if (memresp_val)  next_state = STATE_REFILL_REQUEST;
        else              next_state = STATE_EVICT_WAIT;
      end

      STATE_WAIT: begin
        if (cacheresp_rdy)  next_state = STATE_IDLE;
        else                next_state = STATE_WAIT;
      end

      default: begin
        next_state = STATE_IDLE;
      end

    endcase

  end

  //----------------------------------------------------------------------
  // Valid/Dirty bits record
  // Store valid and dirty bits for each cache entry / set
  //----------------------------------------------------------------------

  logic [3:0] cachereq_addr_index;

  always @(*) begin
    if ( p_num_banks == 1 ) begin
      cachereq_addr_index = cachereq_addr[7:4];
    end
    else if ( p_num_banks == 4 ) begin
      cachereq_addr_index = cachereq_addr[9:6];
    end
  end

  logic valid_bits_write_en;
  logic dirty_bits_write_en;
  logic valid_bit_in;
  logic dirty_bit_in;

  vc_ResetRegfile_1r1w
  #(
    .p_data_nbits (1),
    .p_num_entries(16),
    .p_reset_value(0)     // On reset, all values are not valid.
  ) valid_bits
  (
    .clk        (clk),
    .reset      (reset),
    .read_addr  (cachereq_addr_index),
    .read_data  (is_valid),
    .write_en   (valid_bits_write_en),
    .write_addr (cachereq_addr_index),
    .write_data (valid_bit_in)
  );

    vc_ResetRegfile_1r1w
  #(
    .p_data_nbits (1),
    .p_num_entries(16),
    .p_reset_value(0)     // On reset, all values are not dirty.
  ) dirty_bits
  (
    .clk        (clk),
    .reset      (reset),
    .read_addr  (cachereq_addr_index),
    .read_data  (is_dirty),
    .write_en   (dirty_bits_write_en),
    .write_addr (cachereq_addr_index),
    .write_data (dirty_bit_in)
  );

  //----------------------------------------------------------------------
  // Store cache_resp_type and hit in a enable_register
  //----------------------------------------------------------------------
  logic       cacheresp_type_wen;
  logic       hit_wen;
  logic [3:0] cacheresp_type_in;

  vc_EnResetReg
  #(
    .p_nbits(1),
    .p_reset_value(0)
  ) hit_reg
  (
    .clk(clk),
    .reset(reset),
    .d(cachereq_type == `VC_MEM_REQ_MSG_TYPE_WRITE_INIT ? 1'b0 : hit_TC),
    .q(hit),
    .en(hit_wen)
  );

  vc_EnResetReg
  #(
    .p_nbits(4),
    .p_reset_value(`VC_MEM_RESP_MSG_TYPE_X)
  ) cacheresp_type_reg
  (
    .clk(clk),
    .reset(reset),
    .d(cacheresp_type_in),
    .q(cacheresp_type),
    .en(cacheresp_type_wen)
  );

  //----------------------------------------------------------------------
  // State Outputs
  //----------------------------------------------------------------------

  task cs
  (
    input logic         cs_cachereq_rdy,
    input logic         cs_cacheresp_val,
    input logic         cs_cachereq_reg_en,
    input logic         cs_tag_array_wen,
    input logic         cs_tag_array_ren,
    input logic         cs_data_array_wen,
    input logic         cs_data_array_ren,
    input logic         cs_valid_bit_in,
    input logic         cs_valid_bits_write_en,
    input logic         cs_dirty_bit_in,
    input logic         cs_dirty_bits_write_en,
    input logic         cs_memreq_val,
    input logic         cs_memresp_rdy,
    input logic         cs_memresp_en,
    input logic         cs_write_data_mux_sel,
    input logic         cs_wb_mux_sel,
    input logic         cs_read_data_zero_mux_sel,
    input logic         cs_memreq_addr_mux_sel,
    input logic         cs_read_data_reg_en,
    input logic         cs_evict_addr_reg_en,
    input logic         cs_hit_wen,
    input logic         cs_cacheresp_type_wen,     // update registered value of hit and cacheresp_type on HIGH
    input logic [3:0]   cs_cacheresp_type,
    input logic [3:0]   cs_memreq_type
  );
  begin
    cachereq_rdy            = cs_cachereq_rdy;
    cacheresp_val           = cs_cacheresp_val;
    cachereq_reg_en         = cs_cachereq_reg_en;
    tag_array_wen           = cs_tag_array_wen;
    tag_array_ren           = cs_tag_array_ren;
    data_array_wen          = cs_data_array_wen;
    data_array_ren          = cs_data_array_ren;
    valid_bit_in            = cs_valid_bit_in;
    valid_bits_write_en     = cs_valid_bits_write_en;
    dirty_bit_in            = cs_dirty_bit_in;
    dirty_bits_write_en     = cs_dirty_bits_write_en;
    memreq_val              = cs_memreq_val;
    memresp_rdy             = cs_memresp_rdy;
    memresp_en              = cs_memresp_en;
    write_data_mux_sel      = cs_write_data_mux_sel;
    wben_mux_sel            = cs_wb_mux_sel;
    read_data_zero_mux_sel  = cs_read_data_zero_mux_sel;
    memreq_addr_mux_sel     = cs_memreq_addr_mux_sel;
    read_data_reg_en        = cs_read_data_reg_en;
    evict_addr_reg_en       = cs_evict_addr_reg_en;
    hit_wen                 = cs_hit_wen;
    cacheresp_type_wen      = cs_cacheresp_type_wen;
    cacheresp_type_in       = cs_cacheresp_type;
    memreq_type             = cs_memreq_type;
  end
  endtask

  // Set outputs using a control signal "table"

  always @(*) begin
                                    cs( 0,    0,    0,    0,    0,    0,    0,    0,    0,     0,    0,     0,     0,     0,      0,      0,    0,     0,       0,      0,       0,     0,        `VC_MEM_RESP_MSG_TYPE_X,            `VC_MEM_REQ_MSG_TYPE_X );
      case ( state_reg )
              //                        cache cache cache tag   tag   data  data  valid valid  dirty dirty  mem    mem    mem     write   wben  read   memreq   read    evict    hit    cache     cache                               mem
              //                        req   resp  req   array array array array bit   write  bit   write  req    resp   resp    data    sel   zero   addr     data    addr     wen    resp      resp                                req
              //                        rdy   val   en    wen   ren   wen   ren   in    en     in    en     val    rdy    en      sel           sel    sel      en      en              type wen  type                                type
          STATE_IDLE:               cs( 1,    0,    1,    0,    0,    0,    0,    0,    0,     0,    0,     0,     0,     0,      0,      0,    0,     0,       0,      0,       0,     0,        `VC_MEM_RESP_MSG_TYPE_X,            `VC_MEM_REQ_MSG_TYPE_X);
          STATE_TAG_CHECK:          cs( 0,    0,    0,    0,    1,    0,    0,    0,    0,     0,    0,     0,     0,     0,      0,      0,    0,     0,       0,      0,       1,     0,        `VC_MEM_RESP_MSG_TYPE_X,            `VC_MEM_REQ_MSG_TYPE_X);
          STATE_INIT_DATA_ACCESS:   cs( 0,    0,    0,    1,    0,    1,    0,    1,    1,     0,    1,     0,     0,     0,      0,      0,    0,     0,       0,      0,       0,     1,        `VC_MEM_RESP_MSG_TYPE_WRITE_INIT,   `VC_MEM_REQ_MSG_TYPE_X);
          STATE_READ_DATA_ACCESS:   cs( 0,    0,    0,    0,    0,    0,    1,    0,    0,     0,    1,     0,     0,     0,      0,      0,    0,     0,       1,      0,       0,     1,        `VC_MEM_RESP_MSG_TYPE_READ,         `VC_MEM_REQ_MSG_TYPE_X); // read data access happens either on read hit or a refill from a miss, so always clean
          STATE_WRITE_DATA_ACCESS:  cs( 0,    0,    0,    0,    0,    1,    0,    1,    1,     1,    1,     0,     0,     0,      0,      0,    0,     0,       0,      0,       0,     1,        `VC_MEM_RESP_MSG_TYPE_WRITE,        `VC_MEM_REQ_MSG_TYPE_X); // write data access happens on write hit or refill + write, so always dirty
          STATE_REFILL_REQUEST:     cs( 0,    0,    0,    0,    0,    0,    0,    0,    0,     0,    0,     1,     0,     0,      0,      0,    0,     1,       0,      0,       0,     0,        `VC_MEM_RESP_MSG_TYPE_X,            `VC_MEM_REQ_MSG_TYPE_READ);
          STATE_REFILL_WAIT:        cs( 0,    0,    0,    0,    0,    0,    0,    0,    0,     0,    0,     0,     1,     1,      0,      0,    0,     0,       0,      0,       0,     0,        `VC_MEM_RESP_MSG_TYPE_X,            `VC_MEM_REQ_MSG_TYPE_X);
          STATE_REFILL_UPDATE:      cs( 0,    0,    0,    1,    0,    1,    0,    1,    1,     0,    0,     0,     0,     0,      1,      1,    0,     0,       0,      0,       0,     0,        `VC_MEM_RESP_MSG_TYPE_X,            `VC_MEM_REQ_MSG_TYPE_X);
          STATE_EVICT_PREPARE:      cs( 0,    0,    0,    0,    0,    0,    0,    0,    0,     0,    0,     0,     0,     0,      0,      0,    0,     0,       0,      0,       0,     0,        `VC_MEM_RESP_MSG_TYPE_X,            `VC_MEM_REQ_MSG_TYPE_X );
          // STATE_EVICT_REQUEST:
          // STATE_EVICT_WAIT:
          STATE_WAIT:               cs( 0,    1,    0,    0,    0,    0,    0,    0,    0,     0,    0,     0,     0,     0,      0,      0,    0,     0,       0,      0,       0,     0,        `VC_MEM_RESP_MSG_TYPE_X,            `VC_MEM_REQ_MSG_TYPE_X);
          default:                  cs( 1,    0,    1,    0,    0,    0,    0,    0,    0,     0,    0,     0,     0,     0,      0,      0,    0,     0,       0,      0,       0,     0,        `VC_MEM_RESP_MSG_TYPE_X,            `VC_MEM_REQ_MSG_TYPE_X);
      endcase
  end


endmodule

`endif


