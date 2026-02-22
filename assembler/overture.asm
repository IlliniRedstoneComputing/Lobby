; Register definitions
#subruledef register
{
    r0 => 0b000
    r1 => 0b001
    r2 => 0b010
    r3 => 0b011
    r4 => 0b100
    r5 => 0b101
    r6 => 0b110
}

; Include 'in' for source registers 
#subruledef source
{
    {r: register} => r
    in => 0b111
}

; Include 'out' for destination registers
#subruledef destination
{
    {r: register} => r
    out => 0b111
}

; Branch definitions
#subruledef conditional
{
    {} => 0b000
    p => 0b001
    z => 0b010
    zp => 0b011
    n => 0b100
    np => 0b101
    nz => 0b110
    nzp => 0b111
}

; Main assembly definitions
#ruledef
{
    load {value: i6} => 0b00 @ value
    copy {src: source}, {dst: destination} => 0b10 @ src @ dst

    ; Calculate instructions
    or => 0b01 @ 0b000 @ 0b000
    nand => 0b01 @ 0b000 @ 0b001
    nor => 0b01 @ 0b000 @ 0b010
    and => 0b01 @ 0b000 @ 0b011
    add => 0b01 @ 0b000 @ 0b100
    sub => 0b01 @ 0b000 @ 0b101

    ; Conditional instructions
    BR{cond: conditional} => 0b11 @ 0b000 @ cond


    ; Extra instructions
    halt => 0b01 @ 0b000 @ 0b111
    nop => 0b11 @ 0b000 @ 0b000
}