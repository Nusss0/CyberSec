## Definition
> **Registers** are small, fast storage locations built directly into the CPU. They hold data that the processor is currently working with. In x86-64 architecture, registers are 64 bits (8 bytes) wide and are the primary way assembly instructions manipulate data.

---
## Tags 
#Material #Assembly #BinaryExploitation 

---
## Why Registers Matter

Registers are:
- **Fastest storage** - Much faster than RAM or cache
- **Limited in number** - Only 16 general-purpose registers in x64
- **Direct CPU access** - Instructions operate directly on registers
- **Essential for understanding** - Every assembly instruction uses registers

---
## Register Naming Convention (x64)

x86-64 has backward compatibility with 32-bit (x86) and 16-bit architectures, so registers have multiple names depending on the size you're accessing:

| 64-bit | 32-bit | 16-bit | 8-bit High | 8-bit Low |
| ------ | ------ | ------ | ---------- | --------- |
| `RAX`  | `EAX`  | `AX`   | `AH`       | `AL`      |
| `RBX`  | `EBX`  | `BX`   | `BH`       | `BL`      |
| `RCX`  | `ECX`  | `CX`   | `CH`       | `CL`      |
| `RDX`  | `EDX`  | `DX`   | `DH`       | `DL`      |
| `RSI`  | `ESI`  | `SI`   | -          | `SIL`     |
| `RDI`  | `EDI`  | `DI`   | -          | `DIL`     |
| `RSP`  | `ESP`  | `SP`   | -          | `SPL`     |
| `RBP`  | `EBP`  | `BP`   | -          | `BPL`     |

**Important Notes:**
- Writing to `EAX` (32-bit) **zeros out** the upper 32 bits of `RAX`
- Writing to `AX` (16-bit) keeps the upper 48 bits of `RAX` unchanged
- Writing to `AL` (8-bit) keeps everything else unchanged
- `AH` can ONLY be used with RAX, RBX, RCX, RDX (legacy registers)

---
## General Purpose Registers

| Register | Full Name         | Common Use                                                                                                     | Notes                                |
| -------- | ----------------- | -------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| `RAX`    | Accumulator       | Return values, arithmetic operations                                                                           | Function return value stored here    |
| `RBX`    | Base              | Base pointer for memory access<br>If +, then it points to parameters<br>If -, then it points to local variable | Callee-saved (must preserve)         |
| `RCX`    | Counter           | Loop counter, string operations                                                                                | 4th argument in function calls       |
| `RDX`    | Data              | I/O operations, arithmetic extensions                                                                          | 3rd argument in function calls       |
| `RSI`    | Source Index      | Source pointer for string operations                                                                           | 2nd argument in function calls       |
| `RDI`    | Destination Index | Destination pointer for string ops                                                                             | 1st argument in function calls       |
| `RSP`    | Stack Pointer     | **Points to top of stack**                                                                                     | **Never use for general storage!**   |
| `RBP`    | Base Pointer      | Base of current stack frame                                                                                    | Often used to access local variables |

**Modern Usage (x64 Linux Calling Convention):**
- **RDI**: 1st function argument
- **RSI**: 2nd function argument  
- **RDX**: 3rd function argument
- **RCX**: 4th function argument
- **R8**: 5th function argument
- **R9**: 6th function argument
- **RAX**: Return value from functions

---
### Extended Registers (R8-R15)

x86-64 added 8 new general-purpose registers:

| Register | Size Variants | Purpose |
|----------|---------------|---------|
| `R8` | `R8D`, `R8W`, `R8B` | General purpose, 5th function arg |
| `R9` | `R9D`, `R9W`, `R9B` | General purpose, 6th function arg |
| `R10` | `R10D`, `R10W`, `R10B` | General purpose |
| `R11` | `R11D`, `R11W`, `R11B` | General purpose |
| `R12` | `R12D`, `R12W`, `R12B` | General purpose |
| `R13` | `R13D`, `R13W`, `R13B` | General purpose |
| `R14` | `R14D`, `R14W`, `R14B` | General purpose |
| `R15` | `R15D`, `R15W`, `R15B` | General purpose |

**Naming Pattern:**
- `R8` - Full 64-bit register
- `R8D` - Lower 32 bits (Double word)
- `R8W` - Lower 16 bits (Word)
- `R8B` - Lower 8 bits (Byte)

---
## Special Purpose Registers

### Instruction Pointer
| Register | Purpose | Can Modify? |
|----------|---------|-------------|
| `RIP` | Points to **next instruction** to execute | **No** - Use JMP, CALL, RET instead |

**Important:**
- You cannot directly write to RIP with `mov rip, value`
- Control flow instructions (JMP, CALL, RET) modify RIP indirectly
- In GDB, you see RIP showing current instruction address

---
### Flags Register (RFLAGS)

Contains status flags set by arithmetic and logic operations:

| Flag | Name          | Purpose            | Set When                        |
| ---- | ------------- | ------------------ | ------------------------------- |
| `ZF` | Zero Flag     | Result is zero     | Operation result = 0            |
| `SF` | Sign Flag     | Result is negative | Most significant bit = 1        |
| `CF` | Carry Flag    | Unsigned overflow  | Carry out of MSB                |
| `OF` | Overflow Flag | Signed overflow    | Signed result too large/small   |
| `PF` | Parity Flag   | Even parity        | Even number of 1 bits in result |

**Used by conditional jumps:**
```asm
cmp rax, rbx        ; Compare RAX and RBX (sets flags)
je equal            ; Jump if Equal (checks ZF flag)
jg greater          ; Jump if Greater (checks SF, OF, ZF)
```

---
## Caller-Saved vs Callee-Saved Registers

Important for understanding function calls and stack frames:

### Caller-Saved (Volatile)
**The calling function must save these if needed:**

| Registers | Notes |
|-----------|-------|
| RAX | Return value - always overwritten |
| RCX | 4th argument |
| RDX | 3rd argument |
| RSI | 2nd argument |
| RDI | 1st argument |
| R8-R11 | Arguments and temporary |

**What this means:**
- Functions can freely modify these
- If you need their values after a function call, save them first

---
### Callee-Saved (Non-Volatile)
**The called function must preserve these:**

| Registers | Notes |
|-----------|-------|
| RBX | General purpose |
| RBP | Base pointer |
| R12-R15 | General purpose |
| RSP | **Stack pointer - ALWAYS preserved** |

**What this means:**
- If a function uses these, it must restore them before returning
- Safe to use across function calls

---
## Register Quick Reference

### Most Commonly Used (in CTF/Reverse Engineering)

| Register | Primary Use | Remember |
|----------|-------------|----------|
| `RAX` | Return values, accumulator | "A" = Answer/Accumulator |
| `RDI` | 1st function argument | "D" = Destination Index |
| `RSI` | 2nd function argument | "S" = Source Index |
| `RDX` | 3rd function argument | "D" = Data |
| `RCX` | 4th function argument, counter | "C" = Counter |
| `RSP` | Stack pointer | **Don't touch!** |
| `RBP` | Base/frame pointer | Access local variables |
| `RIP` | Instruction pointer | Current instruction |

---
## Viewing Registers in GDB
```bash
# In GDB
info registers              # Show all general-purpose registers
i r                         # Short version
info all-registers          # Include special registers

# Print specific register
p/x $rax                    # Print RAX in hex
p/d $rcx                    # Print RCX in decimal

# Set register value
set $rax = 0x42             # Change RAX to 0x42
```

---
## Others:
- For detailed register specifications: Intel® 64 and IA-32 Architectures Software Developer's Manual

---
## Related Source:
- [[Assembly]] - Main assembly documentation
- [[Assembly - Stack Operations]] - How registers interact with the stack
- [[GDB]] - Viewing and modifying registers during debugging