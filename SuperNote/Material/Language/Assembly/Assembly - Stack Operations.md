## Definition
> **Stack Operations** are assembly instructions that interact with the stack - a Last-In-First-Out (LIFO) data structure used for temporary storage, function calls, local variables, and return addresses. The stack is fundamental to program execution and function calling conventions.

---
## Tags 
#Material #Assembly #BinaryExploitation

---
## Overview

The stack is a region of memory that:
- **Grows downward** (from high addresses to low addresses)
- Stores temporary data, local variables, return addresses
- Managed by **RSP (Stack Pointer)** register
- Uses PUSH/POP for adding/removing data

**Key Concepts:**
- **RSP** always points to the **top of stack** (lowest address with data)
- **PUSH** decrements RSP, then stores data
- **POP** loads data, then increments RSP
- Stack must remain **aligned** (16-byte boundary on x64 for function calls)

---
## Stack Structure

### Memory Layout
```
High Memory Address
+------------------+
|   Stack Base     | <- RBP (Base Pointer) - optional frame reference
|                  |
|   Local Vars     |
|                  |
|   Saved Regs     |
|                  |
|   Return Addr    |
|                  |
|   Arguments      |
+------------------+ <- RSP (Stack Pointer) - current top
|   (grows down)   |
|        ↓         |
Low Memory Address
```

### Stack Growth Direction
```
Before PUSH:
RSP -> [0x7fffffffe100] = ???

After PUSH RAX (RAX = 0x42):
       [0x7fffffffe100] = ??? (old data)
RSP -> [0x7fffffffe0F8] = 0x42 (RSP decreased by 8)
```

---
## PUSH - Push onto Stack

Decrements RSP by operand size, then stores value at new RSP location.

### Syntax
```asm
push operand
```

### How It Works (64-bit)
```asm
; PUSH RAX equivalent to:
sub rsp, 8              ; Decrement stack pointer by 8 bytes
mov [rsp], rax          ; Store RAX at new top of stack
```

### Usage Examples
```asm
; Push register
push rax                ; Store RAX on stack

; Push immediate value
push 42                 ; Store constant 42 on stack
push 0x41414141         ; Store "AAAA" on stack

; Push memory
push qword [rbx]        ; Push value from memory onto stack

; Push multiple registers
push rax
push rbx
push rcx
```

### Common Use Cases

**1. Save register values (callee-saved)**
```asm
; Function prologue - save registers we'll use
push rbx
push r12
push r13
; ... use rbx, r12, r13 ...
; ... restore before returning ...
```

**2. Pass arguments (old calling convention)**
```asm
; Push arguments in reverse order
push 30                 ; 3rd argument
push 20                 ; 2nd argument  
push 10                 ; 1st argument
call function
add rsp, 24             ; Clean up stack (3 × 8 bytes)
```

**3. Save temporary values**
```asm
; Need to use RAX but want to keep its value
push rax                ; Save RAX
; ... use RAX for something else ...
pop rax                 ; Restore RAX
```

**4. Store local variables (manual allocation)**
```asm
push 0                  ; Allocate space for local variable (initialize to 0)
push 0                  ; Another local variable
; Access via [rsp] and [rsp+8]
```

---
## POP - Pop from Stack

Loads value from current RSP location, then increments RSP by operand size.

### Syntax
```asm
pop operand
```

### How It Works (64-bit)
```asm
; POP RAX equivalent to:
mov rax, [rsp]          ; Load value from top of stack into RAX
add rsp, 8              ; Increment stack pointer by 8 bytes
```

### Usage Examples
```asm
; Pop into register
pop rax                 ; Load top of stack into RAX

; Pop into memory
pop qword [rbx]         ; Load top of stack into memory at [RBX]

; Pop multiple registers (reverse order of PUSH)
pop rcx
pop rbx
pop rax
```

### Common Use Cases

**1. Restore saved registers (callee-saved)**
```asm
; Function epilogue - restore registers
pop r13
pop r12
pop rbx
ret
```

**2. Discard stack values**
```asm
; Remove items without loading them
add rsp, 16             ; Discard 2 values (2 × 8 bytes)
; or
pop rax                 ; Pop but ignore (if you need to load)
pop rax                 ; Pop another
```

**3. Retrieve function return value from stack (rare)**
```asm
call function
pop rax                 ; Get result from stack (unusual pattern)
```

---
## Stack Pointer (RSP)

The **RSP register** always points to the top of the stack (lowest occupied address).

### Direct RSP Manipulation
```asm
; Allocate stack space (move RSP down)
sub rsp, 32             ; Reserve 32 bytes on stack

; Deallocate stack space (move RSP up)
add rsp, 32             ; Free 32 bytes

; Access stack data
mov rax, [rsp]          ; Access top of stack
mov rbx, [rsp+8]        ; Access second item
mov rcx, [rsp+16]       ; Access third item
```

### Stack Allocation for Local Variables
```asm
; Function prologue - allocate space for locals
push rbp                ; Save old base pointer
mov rbp, rsp            ; Set up new base pointer
sub rsp, 64             ; Allocate 64 bytes for local variables

; Access local variables
mov qword [rbp-8], 10   ; local_var1 = 10
mov qword [rbp-16], 20  ; local_var2 = 20

; Function epilogue - clean up
mov rsp, rbp            ; Restore stack pointer
pop rbp                 ; Restore base pointer
ret
```

---
## Base Pointer (RBP)

The **RBP register** optionally marks the base of the current stack frame.

### Why Use RBP?

**Without RBP:**
```asm
; RSP changes throughout function
sub rsp, 16             ; RSP = original - 16
mov [rsp], rax          ; Store at RSP
push rbx                ; RSP = original - 24 (changed!)
mov [rsp+8], rcx        ; Where is this now? Confusing!
```

**With RBP:**
```asm
; RBP stays constant, easier to reference locals
push rbp
mov rbp, rsp            ; RBP = base of frame
sub rsp, 16             ; Allocate locals

mov [rbp-8], rax        ; local1 (always RBP-8)
mov [rbp-16], rcx       ; local2 (always RBP-16)
push rbx                ; RSP changes, but RBP doesn't!
; RBP offsets still work correctly!

mov rsp, rbp
pop rbp
ret
```

### Stack Frame Structure
```
High Address
+------------------+
| Previous Frame   |
+------------------+
| Return Address   | <- Pushed by CALL
+------------------+
| Saved RBP        | <- Pushed by function prologue
+------------------+ <- RBP points here
| Local Var 1      | <- [RBP-8]
+------------------+
| Local Var 2      | <- [RBP-16]
+------------------+
| Local Var 3      | <- [RBP-24]
+------------------+ <- RSP points here
Low Address
```

---
## Stack Alignment

Modern x64 calling convention requires **16-byte stack alignment** before CALL instructions.

### Why Alignment Matters
```asm
; If RSP is not 16-byte aligned before CALL:
; - SSE/AVX instructions may crash
; - Some library functions assume alignment
; - Performance penalty on misaligned access
```

### Ensuring Alignment
```asm
; At function entry, RSP is (16n + 8) due to return address
; We need to subtract 8 more to align to 16

push rbp                ; RSP = 16n (aligned!)
mov rbp, rsp

; Allocate locals in multiples of 16
sub rsp, 32             ; 32 = multiple of 16 (stays aligned)

; Before calling another function
; RSP must be 16-byte aligned
call other_function     ; Safe!
```

### Checking Alignment
```asm
; Check if RSP is 16-byte aligned
test rsp, 0x0F          ; Check lower 4 bits
jz aligned              ; If zero, aligned
jnz not_aligned         ; If not zero, misaligned
```

---
## Common Stack Patterns

### Pattern 1: Function Prologue/Epilogue
```asm
; Standard function prologue
function:
    push rbp            ; Save caller's base pointer
    mov rbp, rsp        ; Set up our base pointer
    sub rsp, 32         ; Allocate space for local variables
    
    ; Function body
    
    ; Standard function epilogue
    mov rsp, rbp        ; Restore stack pointer (or: add rsp, 32)
    pop rbp             ; Restore caller's base pointer
    ret
```

### Pattern 2: Saving/Restoring Callee-Saved Registers
```asm
function:
    push rbp
    mov rbp, rsp
    
    ; Save callee-saved registers
    push rbx
    push r12
    push r13
    
    ; Function body using RBX, R12, R13
    
    ; Restore in reverse order
    pop r13
    pop r12
    pop rbx
    
    mov rsp, rbp
    pop rbp
    ret
```

### Pattern 3: Temporary Storage
```asm
; Need to use RAX but save its value
push rax                ; Save
mov rax, [rbx]
add rax, 10
mov [rcx], rax
pop rax                 ; Restore
```

### Pattern 4: Manual Stack Variables
```asm
; Create local variables without SUB RSP
push 0                  ; local_var1 (initialized to 0)
push 0                  ; local_var2 (initialized to 0)

; Access variables
mov qword [rsp], 42     ; local_var2 = 42
mov qword [rsp+8], 100  ; local_var1 = 100

; Clean up
add rsp, 16             ; Remove 2 variables
```

### Pattern 5: Stack Pivot (Advanced - CTF)
```asm
; Change stack to different location (for exploits)
lea rax, [new_stack]
mov rsp, rax            ; Pivot stack to new location
```

---
## Stack in Function Calls

### x64 Linux Calling Convention

**Arguments:** First 6 in registers, rest on stack
1. RDI
2. RSI
3. RDX
4. RCX
5. R8
6. R9
7. Stack (7th argument at [RSP+8] after CALL)

**Return value:** RAX

**Example:**
```asm
; Calling function(10, 20, 30, 40, 50, 60, 70, 80)
mov rdi, 10             ; 1st arg
mov rsi, 20             ; 2nd arg
mov rdx, 30             ; 3rd arg
mov rcx, 40             ; 4th arg
mov r8, 50              ; 5th arg
mov r9, 60              ; 6th arg
push 80                 ; 8th arg (pushed first)
push 70                 ; 7th arg
call function
add rsp, 16             ; Clean up 2 stack arguments
```

---
## Stack Buffer Operations

### Allocating Buffer on Stack
```asm
; Allocate 128-byte buffer
sub rsp, 128            ; Reserve space
lea rdi, [rsp]          ; RDI = buffer address

; Use buffer
mov byte [rdi], 'A'
mov byte [rdi+1], 'B'

; Clean up
add rsp, 128            ; Free space
```

### Copying Data to Stack
```asm
; Copy data to stack buffer
sub rsp, 64             ; Allocate 64 bytes
lea rdi, [rsp]          ; Destination = stack
lea rsi, [data]         ; Source = data
mov rcx, 64             ; Count = 64 bytes
rep movsb               ; Copy

; Use copied data
mov rax, [rsp]

; Clean up
add rsp, 64
```

---
## Stack in CTF/Binary Exploitation

### Buffer Overflow Basics
```asm
; Vulnerable function
vulnerable:
    push rbp
    mov rbp, rsp
    sub rsp, 16             ; 16-byte buffer
    
    ; Read too much data into buffer (VULNERABLE!)
    lea rdi, [rbp-16]       ; Buffer address
    mov rsi, 100            ; Read 100 bytes into 16-byte buffer!
    call read
    
    ; Stack layout:
    ; [RBP-16] to [RBP-1]  : buffer (16 bytes)
    ; [RBP]                : saved RBP (8 bytes)
    ; [RBP+8]              : return address (8 bytes)
    
    ; If we write past buffer, we can overwrite return address!
    
    mov rsp, rbp
    pop rbp
    ret                     ; Returns to overwritten address!
```

### Stack Canaries (Protection)
```asm
; Function with stack canary
function:
    push rbp
    mov rbp, rsp
    
    ; Read canary from fs:0x28
    mov rax, [fs:0x28]      ; Get canary value
    mov [rbp-8], rax        ; Store on stack
    
    sub rsp, 64             ; Allocate buffer
    
    ; Function body
    
    ; Check canary before return
    mov rax, [rbp-8]        ; Load stored canary
    xor rax, [fs:0x28]      ; Compare with original
    jne stack_corrupted     ; If different, stack overflow detected!
    
    mov rsp, rbp
    pop rbp
    ret

stack_corrupted:
    call __stack_chk_fail   ; Terminate program
```

---
## Stack Diagrams

### Example 1: Simple Function Call
```asm
main:
    push rbp                ; Save main's RBP
    mov rbp, rsp
    
    mov rdi, 10
    call add_five           ; CALL pushes return address
    
    mov rsp, rbp
    pop rbp
    ret

add_five:
    push rbp                ; Save main's RBP
    mov rbp, rsp
    
    add rdi, 5
    mov rax, rdi            ; Return value
    
    pop rbp
    ret
```

**Stack during add_five execution:**
```
+------------------+
| main's old RBP   | <- [RBP+16]
+------------------+
| main's saved RBP | <- [RBP+8]
+------------------+
| Return to main   | <- [RBP] (pushed by CALL)
+------------------+
| add_five's RBP   | <- RBP points here, RSP here too
+------------------+
```

### Example 2: With Local Variables
```asm
function:
    push rbp
    mov rbp, rsp
    sub rsp, 32             ; 4 local variables (8 bytes each)
    
    mov qword [rbp-8], 10   ; local1
    mov qword [rbp-16], 20  ; local2
    mov qword [rbp-24], 30  ; local3
    mov qword [rbp-32], 40  ; local4
```

**Stack layout:**
```
+------------------+
| Return Address   | <- [RBP+8]
+------------------+
| Saved RBP        | <- RBP points here
+------------------+
| local1 = 10      | <- [RBP-8]
+------------------+
| local2 = 20      | <- [RBP-16]
+------------------+
| local3 = 30      | <- [RBP-24]
+------------------+
| local4 = 40      | <- [RBP-32], RSP points here
+------------------+
```

---
## Common Mistakes

### Mistake 1: Unbalanced PUSH/POP
```asm
; Wrong!
push rax
push rbx
pop rax                 ; Pops RBX value into RAX!
; Missing: pop rbx

; Correct - reverse order
push rax
push rbx
pop rbx
pop rax
```

### Mistake 2: Stack Misalignment
```asm
; Wrong - RSP not 16-byte aligned before CALL
sub rsp, 8              ; Misaligns stack
call function           ; May crash or behave incorrectly

; Correct - align to 16 bytes
sub rsp, 16             ; Keeps alignment
call function
add rsp, 16
```

### Mistake 3: Not Restoring RSP
```asm
; Wrong!
function:
    push rbp
    mov rbp, rsp
    sub rsp, 32
    
    ; ... function body ...
    
    pop rbp             ; RSP still -32 from entry!
    ret                 ; Returns to wrong address!

; Correct
function:
    push rbp
    mov rbp, rsp
    sub rsp, 32
    
    mov rsp, rbp        ; Restore RSP first!
    pop rbp
    ret
```

### Mistake 4: Corrupting Stack
```asm
; Wrong - writing past buffer
sub rsp, 16             ; 16-byte buffer
lea rdi, [rsp]
mov rcx, 100
rep stosb               ; Writes 100 bytes! Corrupts stack!

; Correct - respect buffer size
sub rsp, 16
lea rdi, [rsp]
mov rcx, 16             ; Only write 16 bytes
rep stosb
```

---
## Quick Reference

### Basic Operations

| Instruction | Effect on RSP | Effect on Stack |
|-------------|---------------|-----------------|
| `push rax` | RSP -= 8 | Store RAX at new RSP |
| `pop rax` | RSP += 8 | Load from old RSP into RAX |
| `sub rsp, N` | RSP -= N | Allocate N bytes |
| `add rsp, N` | RSP += N | Deallocate N bytes |

### Standard Function Structure
```asm
function:
    ; Prologue
    push rbp
    mov rbp, rsp
    sub rsp, <locals_size>
    
    ; Save callee-saved registers
    push rbx
    push r12
    
    ; Function body
    
    ; Restore callee-saved registers
    pop r12
    pop rbx
    
    ; Epilogue
    mov rsp, rbp
    pop rbp
    ret
```

### Stack Access Patterns
```asm
[rsp]       ; Top of stack
[rsp+8]     ; Second item
[rsp+16]    ; Third item

[rbp-8]     ; First local variable
[rbp-16]    ; Second local variable
[rbp+8]     ; Return address
[rbp+16]    ; First stack argument (if any)
```

---
## Important Notes

### Stack Rules
1. **Always** balance PUSH/POP operations
2. **Always** maintain 16-byte alignment before CALL
3. **Always** restore RSP before RET
4. **Never** access memory beyond allocated stack space
5. **Save** callee-saved registers (RBX, R12-R15, RBP)

### Performance Tips
- Stack operations are fast (cached in L1)
- Prefer registers over stack when possible
- Minimize stack frame size
- Use `lea` instead of `sub rsp; mov` when possible

### Security Considerations
- Buffer overflows can overwrite return addresses
- Stack canaries detect corruption
- NX bit prevents code execution on stack
- ASLR randomizes stack addresses

---
## Others:
- For detailed calling conventions: System V AMD64 ABI
- For stack security: https://www.cs.rit.edu/~spr/CSCI262/notes/stack-smashing.pdf

---
## Related Source:
- [[Assembly]] - Main assembly documentation
- [[Assembly - Registers]] - RSP and RBP registers
- [[Assembly - Data Movement]] - MOV operations with stack
- [[Assembly - Control Flow]] - CALL and RET instructions
- [[GDB]] - Viewing stack with backtrace and examining memory