## Definition
> **Control Flow Instructions** are assembly instructions that alter the sequential execution of a program. They include unconditional jumps, conditional jumps, comparisons, and loop instructions that determine which instruction executes next based on conditions or explicit transfers.

---
## Tags 
#Material #Assembly #BinaryExploitation

---
## Overview

Control flow instructions change the value of **RIP (Instruction Pointer)** to execute code at different locations. They are essential for:
- **Branching** - If/else statements
- **Loops** - While, for loops
- **Function calls** - Calling and returning from functions
- **Error handling** - Jump to error handlers

**Key Concept:**
- Most conditional jumps check **flags** set by previous instructions (CMP, TEST, arithmetic)
- **RIP cannot be directly modified** - must use control flow instructions

---
## Quick Reference Table

### Equality Jumps
| Jump | Condition | Meaning |
|------|-----------|---------|
| `je` | ZF = 1 | Equal |
| `jne` | ZF = 0 | Not Equal |

### Signed Jumps
| Jump | Condition | Meaning |
|------|-----------|---------|
| `jg` | ZF=0 AND SF=OF | Greater (signed) |
| `jge` | SF=OF | Greater or Equal (signed) |
| `jl` | SF≠OF | Less (signed) |
| `jle` | ZF=1 OR SF≠OF | Less or Equal (signed) |

### Unsigned Jumps
| Jump | Condition | Meaning |
|------|-----------|---------|
| `ja` | CF=0 AND ZF=0 | Above (unsigned) |
| `jae` | CF=0 | Above or Equal (unsigned) |
| `jb` | CF=1 | Below (unsigned) |
| `jbe` | CF=1 OR ZF=1 | Below or Equal (unsigned) |

### Flag Jumps
| Jump | Flag | Meaning |
|------|------|---------|
| `jz` | ZF = 1 | Zero |
| `jnz` | ZF = 0 | Not Zero |
| `js` | SF = 1 | Sign (negative) |
| `jns` | SF = 0 | No Sign (positive) |
| `jc` | CF = 1 | Carry |
| `jnc` | CF = 0 | No Carry |
| `jo` | OF = 1 | Overflow |
| `jno` | OF = 0 | No Overflow |

---
## JMP - Unconditional Jump

Transfers control to a different location unconditionally (always jumps).

### Syntax
```asm
jmp target
```

### Usage Examples
```asm
; Jump to label
jmp loop_start

; Jump to address
jmp 0x08048000

; Jump via register (indirect)
jmp rax                 ; Jump to address in RAX

; Jump via memory
jmp [rax]               ; Jump to address stored at memory location [RAX]
```

### Common Use Cases

**1. Infinite loop**
```asm
loop_forever:
    ; ... do something ...
    jmp loop_forever
```

**2. Skip code section**
```asm
    jmp skip_section
    ; This code is never executed
    mov rax, 42
skip_section:
    ; Continue here
```

**3. Jump table (switch statement)**
```asm
    mov rax, [jump_table + rcx*8]
    jmp rax
```

---
## CMP - Compare

Compares two values by performing subtraction (destination - source) but **doesn't store result** - only sets flags.

### Syntax
```asm
cmp operand1, operand2
```

### How It Works
```asm
cmp rax, rbx            ; Performs: RAX - RBX (sets flags, doesn't store)
```

**Flags set based on result:**
- **ZF = 1**: If operands are equal (result is 0)
- **SF = 1**: If result is negative
- **CF = 1**: If unsigned borrow (operand1 < operand2 unsigned)
- **OF = 1**: If signed overflow occurred

### Usage Examples
```asm
; Compare with immediate
cmp rax, 10
je equal                ; Jump if RAX == 10

; Compare registers
cmp rax, rbx
jg greater              ; Jump if RAX > RBX (signed)

; Compare with memory
cmp rax, [rbx]
jne not_equal           ; Jump if RAX != [RBX]

; Compare memory with immediate
cmp qword [rax], 0
jz is_zero              ; Jump if [RAX] == 0
```

### Common Patterns

**1. Check if equal**
```asm
cmp rax, rbx
je equal                ; Jump if RAX == RBX
```

**2. Check if greater**
```asm
cmp rax, 100
jg greater_than_100     ; Jump if RAX > 100 (signed)
```

**3. Check if less**
```asm
cmp rcx, 0
jl negative             ; Jump if RCX < 0 (signed)
```

**4. Range check**
```asm
cmp rax, 10
jl too_small            ; RAX < 10
cmp rax, 100
jg too_large            ; RAX > 100
; RAX is between 10 and 100
```

---
## Conditional Jumps

Jump to target **only if** specific condition is met (based on flags).

### Syntax
```asm
jcc target              ; cc = condition code
```

---
## Conditional Jumps - Equality

| Instruction | Condition | Flags Checked | Description |
|-------------|-----------|---------------|-------------|
| `je` / `jz` | Equal / Zero | ZF = 1 | Jump if equal (ZF set) |
| `jne` / `jnz` | Not Equal / Not Zero | ZF = 0 | Jump if not equal (ZF clear) |

### Usage Examples
```asm
; Check if equal
cmp rax, 10
je is_ten               ; Jump if RAX == 10

; Check if not equal
cmp rbx, 0
jne not_zero            ; Jump if RBX != 0

; After TEST
test rax, rax
jz is_zero              ; Jump if RAX == 0
jnz not_zero            ; Jump if RAX != 0
```

---
## Conditional Jumps - Signed Comparisons

For **signed** integers (can be negative).

| Instruction | Condition | Flags Checked | Description |
|-------------|-----------|---------------|-------------|
| `jg` / `jnle` | Greater | ZF=0 AND SF=OF | Jump if greater (signed) |
| `jge` / `jnl` | Greater or Equal | SF=OF | Jump if greater or equal (signed) |
| `jl` / `jnge` | Less | SF≠OF | Jump if less (signed) |
| `jle` / `jng` | Less or Equal | ZF=1 OR SF≠OF | Jump if less or equal (signed) |

### Usage Examples
```asm
; Check if greater (signed)
cmp rax, 10
jg greater              ; Jump if RAX > 10 (signed)

; Check if less (signed)
cmp rbx, 0
jl negative             ; Jump if RBX < 0

; Check if greater or equal
cmp rcx, -5
jge non_negative        ; Jump if RCX >= -5

; Check if less or equal
cmp rdx, 100
jle at_most_100         ; Jump if RDX <= 100
```

**Mnemonic help:**
- `jg` = "Jump if Greater"
- `jge` = "Jump if Greater or Equal"
- `jl` = "Jump if Less"
- `jle` = "Jump if Less or Equal"

---
## Conditional Jumps - Unsigned Comparisons

For **unsigned** integers (always positive).

| Instruction | Condition | Flags Checked | Description |
|-------------|-----------|---------------|-------------|
| `ja` / `jnbe` | Above | CF=0 AND ZF=0 | Jump if above (unsigned) |
| `jae` / `jnb` | Above or Equal | CF=0 | Jump if above or equal (unsigned) |
| `jb` / `jnae` | Below | CF=1 | Jump if below (unsigned) |
| `jbe` / `jna` | Below or Equal | CF=1 OR ZF=1 | Jump if below or equal (unsigned) |

### Usage Examples
```asm
; Check if above (unsigned)
cmp rax, 100
ja above_100            ; Jump if RAX > 100 (unsigned)

; Check if below (unsigned)
cmp rbx, 50
jb below_50             ; Jump if RBX < 50 (unsigned)

; Check array bounds
cmp rdi, array_size
jae out_of_bounds       ; Jump if index >= size (unsigned)

; Carry flag check
add rax, rbx
jc overflow             ; Jump if carry (unsigned overflow)
```

**Mnemonic help:**
- `ja` = "Jump if Above"
- `jae` = "Jump if Above or Equal"
- `jb` = "Jump if Below"
- `jbe` = "Jump if Below or Equal"

### Why Two Sets? (Signed vs Unsigned)
```asm
; Example: -1 vs 1
mov rax, -1             ; RAX = 0xFFFFFFFFFFFFFFFF
mov rbx, 1              ; RBX = 0x0000000000000001

cmp rax, rbx

; Signed comparison
jg signed_greater       ; Does NOT jump (-1 < 1 in signed)

; Unsigned comparison  
ja unsigned_above       ; JUMPS! (0xFFFF... > 0x0001 in unsigned)
```

---
## Conditional Jumps - Flag-Based

Jump based on individual flag values.

| Instruction | Condition | Flag Checked | Description |
|-------------|-----------|--------------|-------------|
| `jc` | Carry | CF = 1 | Jump if carry flag set |
| `jnc` | No Carry | CF = 0 | Jump if carry flag clear |
| `jo` | Overflow | OF = 1 | Jump if overflow flag set |
| `jno` | No Overflow | OF = 0 | Jump if overflow flag clear |
| `js` | Sign | SF = 1 | Jump if sign flag set (negative) |
| `jns` | No Sign | SF = 0 | Jump if sign flag clear (positive) |
| `jp` / `jpe` | Parity | PF = 1 | Jump if parity flag set (even) |
| `jnp` / `jpo` | No Parity | PF = 0 | Jump if parity flag clear (odd) |

### Usage Examples
```asm
; Check for unsigned overflow
add rax, rbx
jc overflow_handler     ; Jump if carry (addition overflow)

; Check for signed overflow
add rax, rbx
jo overflow_handler     ; Jump if signed overflow

; Check if negative
test rax, rax
js is_negative          ; Jump if sign flag set

; Check if positive or zero
test rax, rax
jns is_positive         ; Jump if sign flag clear
```

---
## LOOP - Loop with Counter

Decrements RCX and jumps if RCX ≠ 0. Useful for counted loops.

### Syntax
```asm
loop target
```

### How It Works
```asm
; LOOP does:
dec rcx
jnz target              ; Jump if RCX != 0
```

### Usage Examples
```asm
; Simple loop 10 times
mov rcx, 10
loop_start:
    ; ... loop body ...
    loop loop_start     ; Decrement RCX, jump if not zero

; Fill buffer with 'A'
mov rcx, 100            ; Loop 100 times
lea rdi, [buffer]
loop_fill:
    mov byte [rdi], 'A'
    inc rdi
    loop loop_fill
```

### Variants

| Instruction | Condition | Description |
|-------------|-----------|-------------|
| `loop` | RCX ≠ 0 | Decrement RCX, jump if not zero |
| `loope` / `loopz` | RCX ≠ 0 AND ZF = 1 | Loop while equal/zero |
| `loopne` / `loopnz` | RCX ≠ 0 AND ZF = 0 | Loop while not equal/zero |

**Note:** `LOOP` is often **slower** than manual `dec rcx; jnz` on modern CPUs. Manual decrement is preferred.

---
## Common Control Flow Patterns

### Pattern 1: If Statement
```asm
; if (rax == 10) { ... }
cmp rax, 10
jne skip_if             ; Jump if NOT equal
    ; Code inside if
    mov rbx, 1
skip_if:
    ; Continue
```

### Pattern 2: If-Else Statement
```asm
; if (rax > 10) { ... } else { ... }
cmp rax, 10
jle else_block          ; Jump to else if RAX <= 10
    ; If block
    mov rbx, 1
    jmp end_if
else_block:
    ; Else block
    mov rbx, 0
end_if:
    ; Continue
```

### Pattern 3: While Loop
```asm
; while (rax > 0) { ... }
loop_start:
    cmp rax, 0
    jle loop_end        ; Exit if RAX <= 0
    ; Loop body
    dec rax
    jmp loop_start
loop_end:
    ; Continue
```

### Pattern 4: For Loop
```asm
; for (i = 0; i < 10; i++) { ... }
xor rcx, rcx            ; i = 0
for_loop:
    cmp rcx, 10
    jge for_end         ; Exit if i >= 10
    ; Loop body
    inc rcx             ; i++
    jmp for_loop
for_end:
    ; Continue
```

### Pattern 5: Do-While Loop
```asm
; do { ... } while (rax > 0);
do_loop:
    ; Loop body
    dec rax
    cmp rax, 0
    jg do_loop          ; Continue if RAX > 0
    ; Continue
```

### Pattern 6: Switch Statement (Jump Table)
```asm
; switch (rax) { case 0:... case 1:... case 2:... }
cmp rax, 2
ja default_case         ; If RAX > 2, go to default

; Jump table
lea rbx, [jump_table]
jmp [rbx + rax*8]       ; Jump to case handler

jump_table:
    dq case_0
    dq case_1
    dq case_2

case_0:
    ; Handle case 0
    jmp end_switch
case_1:
    ; Handle case 1
    jmp end_switch
case_2:
    ; Handle case 2
    jmp end_switch
default_case:
    ; Handle default
end_switch:
    ; Continue
```

### Pattern 7: Break from Loop
```asm
mov rcx, 100
loop_start:
    ; Check break condition
    cmp rax, 0
    je loop_end         ; Break if RAX == 0
    
    ; Loop body
    dec rcx
    jnz loop_start
loop_end:
    ; Continue
```

### Pattern 8: Continue in Loop
```asm
mov rcx, 100
loop_start:
    ; Check continue condition
    test rax, 1
    jz loop_continue    ; Skip if even
    
    ; Loop body (only for odd numbers)
    ; ...
    
loop_continue:
    dec rcx
    jnz loop_start
    ; Continue
```

---
## Jump Optimization Tips

### Short Jumps vs Near Jumps
```asm
; Short jump (1-byte offset, -128 to +127 bytes)
jmp short nearby        ; 2 bytes total

; Near jump (4-byte offset, anywhere in same segment)
jmp nearby              ; 5 bytes total
```

**Rule:** Assembler chooses automatically, but you can force `short` for size optimization.

### Conditional Jump Limitations
- Conditional jumps can only be **short jumps** on some architectures
- If target is too far, use opposite condition + unconditional jump:
```asm
; If target is far
cmp rax, 10
je far_target           ; May not reach!

; Solution: Invert condition
cmp rax, 10
jne skip
jmp far_target          ; Unconditional can jump far
skip:
```

---
## Common Mistakes

### Mistake 1: Wrong Comparison Type
```asm
; Comparing -1 and 1
mov rax, -1
mov rbx, 1
cmp rax, rbx

jg wrong                ; Wrong! -1 < 1 (signed)
ja wrong_too            ; Wrong! 0xFFFF... > 1 (unsigned)

; Use correct comparison for your data type!
```

### Mistake 2: Forgetting to Set Flags
```asm
mov rax, 10
je target               ; Wrong! No CMP before jump

; Correct:
mov rax, 10
cmp rax, 10
je target
```

### Mistake 3: Flag Clobbering
```asm
cmp rax, 10
mov rbx, 5              ; MOV doesn't affect flags (safe)
je equal                ; Still works

cmp rax, 10
add rbx, 5              ; ADD affects flags! (clobbers comparison)
je equal                ; Wrong! Checks ADD result, not CMP
```

---
## Others:
- For detailed instruction behavior: Intel® 64 and IA-32 Architectures Software Developer's Manual Vol. 2
- Jump optimization guide: Agner Fog's microarchitecture manual

---
## Related Source:
- [[Assembly]] - Main assembly documentation
- [[Assembly - Registers]] - RIP register and flags
- [[Assembly - Logic & Bitwise]] - TEST instruction for flag setting
- [[Assembly - Arithmetic Operations]] - CMP vs SUB
- [[Assembly - Stack Operations]] - CALL/RET use control flow
- [[GDB]] - Stepping through jumps and viewing flags