## Definition
> **Data Movement Instructions** are assembly instructions used to transfer data between registers, memory locations, and immediate values. These are the most fundamental operations in assembly - moving data around is the basis for all computation.

---
## Tags 
#Material #Assembly #BinaryExploitation

---
## Overview

Data movement instructions **do not perform arithmetic** - they simply copy or exchange values. The most common data movement instruction is `MOV`, but there are specialized variants for different purposes.

**Key Concept:**
- Source data is **copied**, not moved (original remains unchanged)
- Exception: `XCHG` which swaps values

---
## MOV - Move Data

The most fundamental instruction in assembly. Copies data from source to destination.

### Syntax
```asm
mov destination, source
```

### Usage Examples

#### 1. Register to Register
```asm
mov rax, rbx        ; Copy RBX value into RAX
mov r8, r9          ; Copy R9 into R8
mov eax, ebx        ; Copy EBX into EAX (32-bit)
```

#### 2. Immediate to Register
```asm
mov rax, 42         ; RAX = 42 (decimal)
mov rbx, 0x10       ; RBX = 16 (hexadecimal)
mov rcx, 0          ; RCX = 0
mov r15, -1         ; R15 = -1 (0xFFFFFFFFFFFFFFFF)
```

#### 3. Memory to Register (Load)
```asm
mov rax, [rbx]      ; Load value from memory address in RBX into RAX
mov rcx, [rsp]      ; Load value from top of stack into RCX
mov r8, [rdi+8]     ; Load from address (RDI + 8) into R8
```

#### 4. Register to Memory (Store)
```asm
mov [rax], rbx      ; Store RBX value to memory address in RAX
mov [rsp], 0        ; Store 0 to top of stack
mov [rdi+16], rcx   ; Store RCX to address (RDI + 16)
```

#### 5. Immediate to Memory
```asm
mov qword [rax], 42     ; Store 42 as 64-bit value to address in RAX
mov dword [rbx], 100    ; Store 100 as 32-bit value to address in RBX
mov byte [rcx], 0xFF    ; Store 0xFF as 8-bit value to address in RCX
```

---
## MOV Size Specifiers

When moving to/from memory, you must specify the size if it's ambiguous:

| Specifier | Size | Bits | Example |
|-----------|------|------|---------|
| `byte` | 1 byte | 8 | `mov byte [rax], 0xFF` |
| `word` | 2 bytes | 16 | `mov word [rax], 0x1234` |
| `dword` | 4 bytes | 32 | `mov dword [rax], 0x12345678` |
| `qword` | 8 bytes | 64 | `mov qword [rax], 0x123456789ABCDEF0` |

### Examples
```c
mov byte [rax], 0x41        // Store 'A' (1 byte) to memory
mov word [rbx], 0x4142      // Store 'AB' (2 bytes) to memory
mov dword [rcx], 0x41424344 // Store 'ABCD' (4 bytes) to memory
mov qword [rdx], rax        // Store RAX (8 bytes) to memory
```

---
## Memory Addressing Modes

### 1. Direct Addressing
```asm
mov rax, [0x601000]     ; Load from absolute address 0x601000
```

### 2. Register Indirect
```asm
mov rax, [rbx]          ; Load from address stored in RBX
```

### 3. Register + Offset (Displacement)
```asm
mov rax, [rbx+8]        ; Load from address (RBX + 8)
mov rcx, [rsp+16]       ; Load from address (RSP + 16)
mov r8, [rdi-4]         ; Load from address (RDI - 4)
```

### 4. Base + Index
```asm
mov rax, [rbx+rcx]      ; Load from address (RBX + RCX)
```

### 5. Base + Index * Scale + Offset
```asm
mov rax, [rbx + rcx*8]          ; Address = RBX + (RCX * 8)
mov rdx, [rsi + rdi*4 + 16]     ; Address = RSI + (RDI * 4) + 16
```

**Scale values:** 1, 2, 4, or 8 (commonly used for array indexing)

**Common use case - Array access:**
```asm
; Accessing array[i] where each element is 8 bytes
mov rax, [array_base + rdi*8]   ; RDI = index, 8 = element size
```

---
## LEA - Load Effective Address

`LEA` calculates a memory address but **does not access memory**. It performs arithmetic and stores the result in a register.

### Syntax
```asm
lea destination, [address_expression]
```

### Why LEA is Useful
- **Calculate addresses** without dereferencing
- **Perform arithmetic** in one instruction
- **Faster than separate ADD/MUL** for certain operations

### Usage Examples

#### 1. Calculate Address
```asm
lea rax, [rbx+8]        ; RAX = RBX + 8 (address calculation only)
mov rax, [rbx+8]        ; RAX = value at address (RBX + 8) - different!
```

#### 2. Arithmetic Shortcuts
```asm
lea rax, [rbx + rcx]        ; RAX = RBX + RCX
lea rax, [rbx + rbx*2]      ; RAX = RBX * 3 (RBX + RBX*2)
lea rax, [rbx + rbx*4]      ; RAX = RBX * 5
lea rax, [rbx + rcx*8 + 16] ; RAX = RBX + RCX*8 + 16
```

#### 3. Getting Variable Address
```asm
lea rdi, [buffer]       ; RDI = address of buffer
mov rdi, buffer         ; Same result (simpler syntax for this case)
```

### MOV vs LEA Comparison
```asm
; Given: RBX = 0x1000, memory at 0x1008 contains 0x42

mov rax, [rbx+8]        ; RAX = 0x42 (loads VALUE from 0x1008)
lea rax, [rbx+8]        ; RAX = 0x1008 (calculates ADDRESS)
```

---
## MOVZX - Move with Zero Extension

Moves smaller data into larger register and **zero-extends** (fills upper bits with 0).

### Syntax
```asm
movzx destination, source
```

### Usage Examples
```asm
; AL = 0xFF (255)
movzx rax, al           ; RAX = 0x00000000000000FF
movzx eax, al           ; EAX = 0x000000FF (RAX upper 32 bits = 0)

; AX = 0x1234
movzx rax, ax           ; RAX = 0x0000000000001234

; Byte from memory
movzx rax, byte [rbx]   ; Load 1 byte, zero-extend to 64 bits
movzx rcx, word [rsi]   ; Load 2 bytes, zero-extend to 64 bits
```

**Use case:** Loading unsigned values (like reading a byte from a buffer)

---
## MOVSX - Move with Sign Extension

Moves smaller data into larger register and **sign-extends** (preserves sign by filling upper bits with sign bit).

### Syntax
```asm
movsx destination, source
movsxd destination, source    ; 32-bit to 64-bit sign extension
```

### Usage Examples
```asm
; AL = 0xFF (-1 in signed 8-bit)
movsx rax, al           ; RAX = 0xFFFFFFFFFFFFFFFF (-1 in 64-bit)

; AL = 0x7F (127 in signed 8-bit)
movsx rax, al           ; RAX = 0x000000000000007F (127 in 64-bit)

; EAX = 0xFFFFFFFF (-1 in signed 32-bit)
movsxd rax, eax         ; RAX = 0xFFFFFFFFFFFFFFFF (-1 in 64-bit)
```

**Use case:** Loading signed values (like reading signed integers)

---
## XCHG - Exchange

Swaps the values of two operands.

### Syntax
```asm
xchg operand1, operand2
```

### Usage Examples
```asm
; Before: RAX = 10, RBX = 20
xchg rax, rbx           ; After: RAX = 20, RBX = 10

; Register and memory
xchg rax, [rbx]         ; Swap RAX with value at address in RBX

; Different sizes
xchg eax, ebx           ; Swap 32-bit values
xchg al, bl             ; Swap 8-bit values
```

**Note:** `XCHG` is slower than using a temporary register for simple swaps, but it's atomic (useful in multithreading).

---
## MOVS - Move String

Copies data from one memory location to another. Often used with REP prefix for bulk memory operations.

### Syntax
```asm
movsb       ; Move 1 byte from [RSI] to [RDI]
movsw       ; Move 2 bytes (word)
movsd       ; Move 4 bytes (dword)
movsq       ; Move 8 bytes (qword)
```

### Usage with REP
```asm
; Copy RCX bytes from RSI to RDI
mov rcx, 100            ; Number of iterations
lea rsi, [source]       ; Source address
lea rdi, [dest]         ; Destination address
rep movsb               ; Repeat movsb RCX times
```

**Common in:** String operations, buffer copying, memcpy implementations

---
## CMOV - Conditional Move

Moves data only if a condition is met (based on flags). Helps avoid branching.

### Syntax
```asm
cmovcc destination, source
```

### Common Conditional Moves

| Instruction | Condition | Flags Checked |
|-------------|-----------|---------------|
| `cmove` / `cmovz` | Equal / Zero | ZF = 1 |
| `cmovne` / `cmovnz` | Not Equal / Not Zero | ZF = 0 |
| `cmovg` / `cmovnle` | Greater (signed) | ZF=0 AND SF=OF |
| `cmovl` / `cmovnge` | Less (signed) | SF ≠ OF |
| `cmova` / `cmovnbe` | Above (unsigned) | CF=0 AND ZF=0 |
| `cmovb` / `cmovnae` | Below (unsigned) | CF = 1 |

### Usage Examples
```asm
cmp rax, rbx            ; Compare RAX and RBX
cmove rcx, rdx          ; If equal, RCX = RDX (otherwise RCX unchanged)

test rax, rax           ; Check if RAX is zero
cmovz rax, rbx          ; If zero, RAX = RBX
```

**Use case:** Branchless code for better CPU pipeline performance

---
## Common Patterns in CTF

### Pattern 1: Loading String Address
```asm
lea rdi, [buffer]       ; RDI = address of buffer
mov rsi, rdi            ; RSI = same address (for string operations)
```

### Pattern 2: Array Indexing
```asm
; array[i] where each element is 8 bytes
mov rax, [array_base + rdi*8]
```

### Pattern 3: Zeroing a Register
```asm
xor rax, rax            ; Faster than mov rax, 0
mov rax, 0              ; Also works but slightly slower
```

### Pattern 4: Loading Immediate Values
```asm
mov rax, 0x41414141     ; RAX = "AAAA" (in little-endian)
mov byte [buffer], 0x41 ; Write 'A' to buffer
```

### Pattern 5: Pointer Dereferencing
```asm
mov rax, [rbp-8]        ; Load local variable (pointer)
mov rbx, [rax]          ; Dereference pointer (load value it points to)
```

---
## Restrictions

### What You CANNOT Do with MOV
```asm
;INVALID - Memory to Memory
mov [rax], [rbx]        ; ❌ Cannot move directly between memory locations
; Solution: Use intermediate register
mov rcx, [rbx]
mov [rax], rcx          ; ✓ Works

; INVALID - Immediate to segment register
mov cs, 0x10            ; ❌ Cannot move immediate to segment register

; INVALID - Moving to RIP
mov rip, rax            ; ❌ Cannot directly modify instruction pointer
; Use JMP, CALL, or RET instead
```

---
## Quick Reference Table

| Instruction   | Purpose                              | Example            |
| ------------- | ------------------------------------ | ------------------ |
| `mov`         | Copy data                            | `mov rax, rbx`     |
| `lea`         | Calculate address (no memory access) | `lea rax, [rbx+8]` |
| `movzx`       | Move with zero extension             | `movzx rax, al`    |
| `movsx`       | Move with sign extension             | `movsx rax, al`    |
| `movsxd`      | Sign extend 32→64 bit                | `movsxd rax, eax`  |
| `xchg`        | Swap two values                      | `xchg rax, rbx`    |
| `movsb/w/d/q` | Move string (with RSI/RDI)           | `rep movsb`        |
| `cmovcc`      | Conditional move                     | `cmove rax, rbx`   |

---
## Others:
- For detailed instruction behavior: Intel® 64 and IA-32 Architectures Software Developer's Manual Vol. 2
- Online assembler to test: https://defuse.ca/online-x86-assembler.htm

---
## Related Source:
- [[Assembly]] - Main assembly documentation
- [[Assembly - Registers]] - Understanding registers used in data movement
- [[Assembly - Arithmetic Operations]] - Operations that follow data movement
- [[Assembly - Stack Operations]] - Special data movement with stack
- [[GDB]] - Viewing data movement in real-time