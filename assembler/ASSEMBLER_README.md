# Overture ISA Assembler

This tool will assemble our definition of the Overture ISA into binary files.

## Overview

We will use [customasm](https://hlorenzi.github.io/customasm/) for implementing and assembling the ISA.

`init.asm` is the starting block for user programs. It includes `overture.asm`, which contains the ISA definitions and rules used by the assembler.

**Write your program by editing** `init.asm` **or by creating a new assembly file with** `#include overture.asm` **and your program body.**

## Prerequisites

You may either:
1. Download a pre-built `customasm` executable from the project's Releases page: https://github.com/hlorenzi/customasm/releases

If you choose this method, make sure to place the executable on your PATH.

OR

2. Install via cargo--You will first need to install a recent version of Rust using rustup: https://rustup.rs

Installing via cargo gives you the `customasm` CLI in your PATH:

```sh
# Install using cargo (requires Rust/cargo installed)
cargo install customasm
```

## Basic usage

To assemble your program, simply run `customasm` on your assembly file. Example (from repository root):

```sh
# Assemble the default/binary output for init.asm
customasm assembler/init.asm -f binary -o build/init.bin

# If outputting to binary without changing the file name, this is equivalent:
customasm assembler/init.asm
```

Notes:
- `assembler/init.asm` includes `overture.asm` so assembling `init.asm` will assemble the ISA definitions in addition to your program; no need for assembling multiple files.
- The `-f` / `--format` option selects an output format (e.g. `binary`, `hexdump`, `annotated`, `symbols`, ...).
- The `-o` / `--output` option sets the output filename. Use `-p` / `--print` to print to stdout instead of writing a file.

### Examples:

```sh
# Produce a binary file
customasm assembler/init.asm -f binary -o build/init.bin

# Produce a human-readable annotated listing
customasm assembler/init.asm -f annotated -o build/init_annotated.txt

# Emit the symbol table
customasm assembler/init.asm -f symbols -o build/symbols.txt

# Print the default output to screen
customasm assembler/init.asm -p
```

## Assembly Language

This section documents the assembly language tokens and primary instructions implemented in `overture.asm`.

### Registers & tokens

- Available registers: `r0`, `r1`, `r2`, `r3`, `r4`, `r5`, `r6` (3-bit encodings).
- I/O registers: `in` (source), `out` (destination)

Register encoding are defined in `overture.asm`'s `#subruledef` blocks.

### Instruction reference

All encodings below are written as defined in `overture.asm` (bit fields shown conceptually).

- Load

	- Syntax: `load {value: i6}`
	- Description: Load a 6-bit immediate into `r0`.
	- Notes: immediate is a 6-bit value (`i6`) — use signed values when appropriate (roughly -32..31 for signed immediates).
	- Encoding: `0b11 @ value`
	- Example:

		```asm
		load 5          ; r0 <- 5
		```

- Copy

	- Syntax: `copy {src}, {dst}`
	- Description: Copy the value from `src` to `dst`. `src` may be a register or `in`. `dst` may be a register or `out`.
	- Encoding: `0b10 @ src @ dst` (3-bit `src`, 3-bit `dst`)
	- Example:

		```asm
		copy r0, r1     ; r1 <- r0
		copy r3, out    ; send value of r3 to output
		```

- Calculate (ALU family)

	- Syntax: `or`, `nand`, `nor`, `and`, `add`, `sub` (no explicit operands)
	- Description: Perform the named operation using fixed register operands: operate on `r1` and `r2`, store result in `r3`.
	- Encoding: `0b01 @ 0b000 @ <op-code>` where `<op-code>` selects the operation (see `overture.asm` for mapping).
	- Example:

		```asm
		add     ; compute r3 <- r1 + r2
		```

- Conditional branch

	- Syntax: `BR`, `BRp`, `BRz`, `BRzp`, `BRn`, `BRnp`, `BRnz`, `BRnzp` (condition appended after `BR`)
	- Description: Branch to the address contained in `r0` if the condition holds for `r3` (condition tests negative/zero/positive).
	- Encoding: `0b00 @ 0b000 @ <cond>` where `<cond>` is a 3-bit mask (see `overture.asm`'s `conditional` subrule).
	- Example:

		```asm
		BRz     ; if r3 == 0, jump to address in r0
		```

- Halt / NOP

	- `halt` — stops program execution. (Encoding in `overture.asm`.)
	- `nop` — does nothing.

### Labels and addressing

Labels are named anchors that mark a specific address in your program. They allow you to:

- **Define a label**: end a line with a colon (`:`). The label's value becomes the current byte address.

  ```asm
  my_label:
      load 1
      copy r0, out
  ```

- **Reference a label**: use the label name in expressions. The assembler evaluates the label to its address.

  ```asm
  load my_label   ; r0 <- address of my_label
  BRz               ; if r3 == 0, jump to address in r0 (my_label)
  ```

Labels are useful for:
- Creating jump targets for conditional and unconditional branches
- Organizing code into named sections
- Avoiding hard-coded addresses

The assembler resolves label references to byte addresses during assembly, so you can focus on program logic rather than manual address calculations.

See the example program in the next section for a complete usage pattern.

#### Problems
The load instruction can only accept unsigned integers from 0 to 63, so extra logic will have to be done in order to jump to addresses outside this range. Here's a rough example:
```asm
load big_label  ; This will fail
...
big_label:
    ... ; Address 0x73
```

### Bank and output region

`overture.asm` defines a `#bankdef overture` that sets default assembly parameters:

- `bits = 8` (byte width)
- `addr = 0x00` start address
- `addr_end = 0x100` end address (fill to this address when `fill = true`)
- `outp = 0x00` default output group

This means assembling `init.asm` will produce a byte-addressed output region starting at `0x00` and filling unused addresses with zero bytes when `fill` is enabled.

### Small example

```asm
#include "overture.asm"
; Add two inputs, if the result is positive output 1, else 0

copy in, r1     ; Store input into r1
copy in, r2     ; Store input into r2
add             ; r3 <- r1 + r2

load 'my_label' ; Load address of 'my_label' into r0
BRp             ; Branch to r0 (my_label) if r3 is positive
load 0          ; Otherwise, output 0
copy r0, out    ;  ...
halt            ;  ...

my_label:
    load 1          ; Output 1
    copy r0, out    ;  ...
    halt            ;  ...
```

For exact encodings and additional output formats you can request from `customasm`, see `overture.asm` and the `customasm` CLI docs: https://hlorenzi.github.io/customasm/src/usage_help.html