## Definition
> **Arithmetic Operations** are assembly instructions that perform mathematical calculations on data. These include basic operations like addition, subtraction, multiplication, and division, as well as increment/decrement operations. Results often affect CPU flags which are used for conditional operations.

---
## Tags 
#Material #Assembly #BinaryExploitation

---
## Quick Reference Table

| Instruction     | Operation              | Result Location |
| --------------- | ---------------------- | --------------- |
| `add dest, src` | dest + src             | dest            |
| `sub dest, src` | dest - src             | dest            |
| `inc dest`      | dest + 1               | dest            |
| `dec dest`      | dest - 1               | dest            |
| `neg dest`      | 0 - dest               | dest            |
| `mul src`       | RAX × src              | RDX:RAX         |
| `imul src`      | RAX × src (signed)     | RDX:RAX         |
| `div src`       | RDX:RAX ÷ src          | RAX(Q), RDX(R)  |
| `idiv src`      | RDX:RAX ÷ src (signed) | RAX(Q), RDX(R)  |
| `adc dest, src` | dest + src + CF        | dest            |
| `sbb dest, src` | dest - src - CF        | dest            |

**Q** = Quotient, **R** = Remainder

---
## ADD - Addition

Adds source to destination and stores result in destination.

### Syntax
```asm
add destination, source
```

### Usage Examples
```asm
; Register to register
add rax, rbx            ; RAX = RAX + RBX

; Immediate to register
add rax, 10             ; RAX = RAX + 10
add rcx, 0x20           ; RCX = RCX + 32

; Memory to register
add rax, [rbx]          ; RAX = RAX + value at [RBX]

; Register to memory
add [rax], rbx          ; [RAX] = [RAX] + RBX

; Immediate to memory
add qword [rax], 5      ; [RAX] = [RAX] + 5
```

### Flags Affected
- **ZF** (Zero Flag): Set if result is zero
- **SF** (Sign Flag): Set if result is negative
- **CF** (Carry Flag): Set if unsigned overflow
- **OF** (Overflow Flag): Set if signed overflow

### Example with Flags
```asm
mov rax, 0xFFFFFFFFFFFFFFFF    ; RAX = -1 (or max unsigned)
add rax, 1                      ; RAX = 0, sets ZF=1, CF=1
```

---
## SUB - Subtraction

Subtracts source from destination and stores result in destination.

### Syntax
```asm
sub destination, source
```

### Usage Examples
```asm
; Register to register
sub rax, rbx            ; RAX = RAX - RBX

; Immediate to register
sub rax, 10             ; RAX = RAX - 10
sub rcx, 0x20           ; RCX = RCX - 32

; Memory to register
sub rax, [rbx]          ; RAX = RAX - value at [RBX]

; Register to memory
sub [rax], rbx          ; [RAX] = [RAX] - RBX
```

### Flags Affected
Same as ADD (ZF, SF, CF, OF)

### Common Pattern - Checking if Equal
```asm
sub rax, rbx            ; RAX = RAX - RBX
jz equal                ; Jump if result is zero (RAX == RBX)
```

---
## INC - Increment

Adds 1 to operand. Faster and shorter than `add operand, 1`.

### Syntax
```asm
inc operand
```

### Usage Examples
```asm
inc rax                 ; RAX = RAX + 1
inc rcx                 ; RCX = RCX + 1
inc qword [rbx]         ; [RBX] = [RBX] + 1
inc byte [buffer]       ; Increment byte at buffer
```

### Flags Affected
- **ZF, SF, OF, PF** - affected
- **CF** - **NOT affected** (this is different from ADD!)

### Common Use - Loop Counter
```asm
mov rcx, 0
loop_start:
    ; ... do something ...
    inc rcx             ; Counter++
    cmp rcx, 10
    jl loop_start       ; Loop while RCX < 10
```

---
## DEC - Decrement

Subtracts 1 from operand. Faster and shorter than `sub operand, 1`.

### Syntax
```asm
dec operand
```

### Usage Examples
```asm
dec rax                 ; RAX = RAX - 1
dec rcx                 ; RCX = RCX - 1
dec qword [rbx]         ; [RBX] = [RBX] - 1
```

### Flags Affected
Same as INC (ZF, SF, OF, PF - but **NOT CF**)

### Common Use - Countdown Loop
```asm
mov rcx, 10
loop_start:
    ; ... do something ...
    dec rcx             ; Counter--
    jnz loop_start      ; Loop while RCX != 0
```

---
## NEG - Negate (Two's Complement)

Negates the operand by computing two's complement (changes sign).

### Syntax
```asm
neg operand
```

### Usage Examples
```asm
mov rax, 5
neg rax                 ; RAX = -5 (0xFFFFFFFFFFFFFFFB)

mov rbx, -10
neg rbx                 ; RBX = 10

neg qword [rcx]         ; [RCX] = -[RCX]
```

### How It Works
```
NEG performs: 0 - operand
Equivalent to: NOT operand + 1
```

### Example
```asm
; RAX = 5 (binary: 0000...0101)
neg rax
; RAX = -5 (binary: 1111...1011)
```

---
## MUL - Unsigned Multiplication

Multiplies unsigned values. Result can be twice the size of operands.

### Syntax
```asm
mul source
```

### How It Works
- **8-bit**: `AL × source → AX` (16-bit result)
- **16-bit**: `AX × source → DX:AX` (32-bit result, high in DX, low in AX)
- **32-bit**: `EAX × source → EDX:EAX` (64-bit result)
- **64-bit**: `RAX × source → RDX:RAX` (128-bit result)

### Usage Examples
```asm
; 64-bit multiplication
mov rax, 10
mov rbx, 20
mul rbx                 ; RAX = 200, RDX = 0 (result fits in RAX)

; 64-bit with large numbers
mov rax, 0x8000000000000000
mov rbx, 2
mul rbx                 ; RAX = 0 (low 64 bits), RDX = 1 (high 64 bits)

; Memory operand
mul qword [rbx]         ; RAX × [RBX] → RDX:RAX
```

### Flags Affected
- **CF, OF**: Set if result doesn't fit in lower half (overflow)
- **SF, ZF, AF, PF**: Undefined

---
## IMUL - Signed Multiplication

Multiplies signed values. Has multiple forms.

### Syntax Forms

**Form 1: One operand (like MUL)**
```asm
imul source             ; RAX × source → RDX:RAX
```

**Form 2: Two operands**
```asm
imul destination, source    ; dest = dest × source
```

**Form 3: Three operands**
```asm
imul destination, source, immediate    ; dest = source × immediate
```

### Usage Examples
```asm
; Form 1 - Result in RDX:RAX
mov rax, -10
mov rbx, 20
imul rbx                ; RAX = -200, RDX = -1 (sign extended)

; Form 2 - Result in first operand
mov rax, 10
imul rax, rbx           ; RAX = RAX × RBX

; Form 3 - Most flexible
imul rax, rbx, 5        ; RAX = RBX × 5
imul rcx, [rbx], 10     ; RCX = [RBX] × 10
```

### Common Use - Array Indexing
```asm
; Calculate offset: index × element_size
mov rdi, 5              ; Index = 5
imul rdi, rdi, 8        ; RDI = 5 × 8 = 40 (offset for 8-byte elements)
```

---
## DIV - Unsigned Division

Divides unsigned values. Dividend is twice the size of divisor.

### Syntax
```asm
div divisor
```

### How It Works
- **8-bit**: `AX ÷ divisor → AL (quotient), AH (remainder)`
- **16-bit**: `DX:AX ÷ divisor → AX (quotient), DX (remainder)`
- **32-bit**: `EDX:EAX ÷ divisor → EAX (quotient), EDX (remainder)`
- **64-bit**: `RDX:RAX ÷ divisor → RAX (quotient), RDX (remainder)`

### Usage Examples
```asm
; 64-bit division: 100 ÷ 3
mov rax, 100
xor rdx, rdx            ; IMPORTANT: Clear RDX before DIV!
mov rbx, 3
div rbx                 ; RAX = 33 (quotient), RDX = 1 (remainder)

; Another example
mov rax, 50
xor rdx, rdx            ; Must clear RDX!
mov rcx, 7
div rcx                 ; RAX = 7, RDX = 1 (50 = 7×7 + 1)
```

### Critical Note - Clear RDX/EDX!
```asm
; WRONG - Will cause incorrect result or crash
mov rax, 100
div rbx                 ; ❌ RDX not cleared! Treats RDX:RAX as 128-bit

; CORRECT
mov rax, 100
xor rdx, rdx            ; ✓ Clear upper 64 bits
div rbx
```

### Divide by Zero
- Causes **CPU exception** (program crashes)
- Always check divisor before DIV!
```asm
test rbx, rbx           ; Check if RBX is zero
jz error_handler        ; Jump if zero
div rbx                 ; Safe to divide
```

---
## IDIV - Signed Division

Divides signed values. Same behavior as DIV but handles negative numbers.

### Syntax
```asm
idiv divisor
```

### How It Works
Same as DIV, but for signed integers:
- **64-bit**: `RDX:RAX ÷ divisor → RAX (quotient), RDX (remainder)`

### Usage Examples
```asm
; Signed division: -100 ÷ 3
mov rax, -100
cqo                     ; Sign-extend RAX into RDX (for signed division)
mov rbx, 3
idiv rbx                ; RAX = -33, RDX = -1

; Positive division
mov rax, 100
cqo                     ; Sign-extend RAX into RDX
mov rbx, 3
idiv rbx                ; RAX = 33, RDX = 1
```

### Critical Note - Use CQO/CDQ!

For **signed** division, use sign extension instead of clearing:
```asm
; WRONG for signed numbers
mov rax, -100
xor rdx, rdx            ; ❌ Wrong for negative numbers!
idiv rbx

; CORRECT for signed numbers
mov rax, -100
cqo                     ; ✓ Sign-extend RAX → RDX:RAX
idiv rbx
```

### Sign Extension Instructions

| Instruction | Purpose |
|-------------|---------|
| `cbw` | Sign-extend AL → AX |
| `cwd` | Sign-extend AX → DX:AX |
| `cdq` | Sign-extend EAX → EDX:EAX |
| `cqo` | Sign-extend RAX → RDX:RAX |

---
## ADC - Add with Carry

Adds source and destination, plus the carry flag (CF).

### Syntax
```asm
adc destination, source
```

### Usage - Multi-precision Arithmetic

Used for adding numbers larger than 64 bits:
```asm
; Add two 128-bit numbers
; Number 1: RDX:RAX, Number 2: RCX:RBX

add rax, rbx            ; Add lower 64 bits
adc rdx, rcx            ; Add upper 64 bits + carry from lower addition
```

### Example - Adding 128-bit Numbers
```asm
; Add: 0x0000000000000001_FFFFFFFFFFFFFFFF + 0x0000000000000000_0000000000000002
mov rax, 0xFFFFFFFFFFFFFFFF    ; Lower 64 bits of number 1
mov rdx, 0x0000000000000001    ; Upper 64 bits of number 1
mov rbx, 0x0000000000000002    ; Lower 64 bits of number 2
mov rcx, 0x0000000000000000    ; Upper 64 bits of number 2

add rax, rbx            ; RAX = 0x0000000000000001, CF = 1
adc rdx, rcx            ; RDX = 0x0000000000000002 (includes carry)
; Result: RDX:RAX = 0x0000000000000002_0000000000000001
```

---
## SBB - Subtract with Borrow

Subtracts source and carry flag from destination.

### Syntax
```asm
sbb destination, source
```

### Usage - Multi-precision Subtraction
```asm
; Subtract two 128-bit numbers
sub rax, rbx            ; Subtract lower 64 bits
sbb rdx, rcx            ; Subtract upper 64 bits - borrow
```

---
## Common Arithmetic Patterns

### Pattern 1: Multiply by Power of 2 (Use Shift Instead)
```asm
; Slow
mov rax, 10
imul rax, 8             ; RAX × 8

; Fast - bit shift left
mov rax, 10
shl rax, 3              ; RAX × 2³ = RAX × 8 (covered in Logic & Bitwise)
```

### Pattern 2: Check if Even/Odd
```asm
test rax, 1             ; Check lowest bit
jz even                 ; Jump if zero (even number)
jnz odd                 ; Jump if not zero (odd number)
```

### Pattern 3: Absolute Value
```asm
; Get absolute value of RAX
cqo                     ; Sign-extend RAX to RDX:RAX
xor rax, rdx            ; Conditional NOT
sub rax, rdx            ; Conditional +1
```

### Pattern 4: Division by Constant (Compiler Optimization)
```asm
; Instead of: RAX ÷ 10
; Compilers often use multiplication by reciprocal (faster)
mov rdx, 0xCCCCCCCCCCCCCCCD
mul rdx
shr rdx, 3              ; Magic constants for division by 10
```

### Pattern 5: Modulo (Remainder)
```asm
; Get RAX % RBX
xor rdx, rdx            ; Clear RDX
div rbx                 ; Divide
; RDX now contains the remainder (RAX % RBX)
```

---
## Important Notes

### Division Gotchas
1. **Always clear/sign-extend before DIV/IDIV**
   - `xor rdx, rdx` for unsigned (DIV)
   - `cqo` for signed (IDIV)

2. **Check for divide by zero**
```asm
   test divisor, divisor
   jz error
```

3. **Division is SLOW** - avoid in loops if possible

### Multiplication Gotchas
1. **MUL/IMUL (one operand) changes RDX** - save it if needed
2. **IMUL (two/three operands) only uses destination** - easier to use
3. **Overflow checking** - Check CF/OF after multiplication

### Performance Tips
- Use `INC/DEC` instead of `ADD/SUB` with 1
- Use bit shifts instead of MUL/DIV by powers of 2
- Use `LEA` for simple arithmetic (covered in Data Movement)

---
## Others:
- For detailed flag behavior: Intel® 64 and IA-32 Architectures Software Developer's Manual Vol. 1
- For optimization tips: Agner Fog's optimization manuals

---
## Related Source:
- [[Assembly]] - Main assembly documentation
- [[Assembly - Registers]] - Registers used in arithmetic operations
- [[Assembly - Data Movement]] - MOV operations that precede arithmetic
- [[Assembly - Control Flow]] - Using arithmetic results for conditional jumps
- [[Assembly - Logic & Bitwise]] - Logical operations and bit manipulation
- [[GDB]] - Viewing arithmetic operations and flags in real-time