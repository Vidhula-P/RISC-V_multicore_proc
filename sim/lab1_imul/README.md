Hey Vidhula, Hubert here, just using this temporarily as a place to track where we are individually with our work, so that we can collaborate better.
Also a good place to leave notes for one another to make the work / the eventual report easier.

### Hubert's Task List:
- [x] IntMulBase: Defined datapath unit for lab1_imul_IntMulBase
- [x] IntMulBase: Defined control unit for lab1_imul_IntMulBase
- [x] IntMulBase: Passed original provided test cases

### TODO:
- [ ] Check module definition, instantiation, and variable naming conventions
- [ ] Look at trace / waveform to see that test cases truly passing

### Hubert's Notes:

1. Using Verilator linting

    Verilator can be used to lint your code. You can run linting with the following command. You can find out about the arguments online, or test omitting each argument to see why I included the following arguments for our specific purpose:
    ```
    $ verilator --lint-only -Wall -Wno-DECLFILENAME --top lab1_imul_IntMulBase lab1_imul/IntMulBase.v
    ```

2. Nulling unused pins for the Verilator linter

    This is just a convention that was adopted at my workplace, but we can decide on how we both want to do it for our codebase. Leaving a pin unassigned as per below causes the Verilator linter to raise a PINCONNECTEMPTY warning.

    ```verilog
    vc_Adder
    #(
        .p_nbits(32)
    ) result_adder (
        .in0  (result_reg_out),
        .in1  (a_reg_out),
        .cin  (1'b0),
        .out  (result_adder_out),
        .cout ()
    );
    ```
    There are several options to manage this:
    1. Ignore the warning
    2. Wrap a pragma around the offending line to disable it as below, or disable the warning globally from the command line call
        ```verilog
        vc_Adder
        #(
            .p_nbits(32)
        ) result_adder (
            .in0  (a_reg_out),
            .in1  (result_reg_out),
            .cin  (1'b0),
            .out  (result_adder_out),
            /* verilator lint_off PINCONNECTEMPTY */
            .cout ()
            /* verilator lint_on PINCONNECTEMPTY */
        );
        ```
    3. Null the pin by connecting it a a dummy wire. This is what was adopted at my workplace.
        ```verilog
        /* verilator lint_off unused */
        logic result_adder_cout_null;
        /* verilator lint_on unused */

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
        ```