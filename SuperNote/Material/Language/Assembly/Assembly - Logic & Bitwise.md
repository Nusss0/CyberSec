## Definition
> **Logic and Bitwise Operations** are assembly instructions that perform logical operations (AND, OR, XOR, NOT) and bit manipulation (shifts, rotates) on data. These operations work at the bit level and are fundamental for bit manipulation, masking, flag testing, and optimization techniques.

---
## Tags 
#Material #Assembly #BinaryExploitation

---
## Overview

Logic and bitwise instructions operate on individual bits of data. They are used for:
- **Bit masking** - Isolating specific bits
- **Bit testing** - Checking if bits are set
- **Bit manipulation** - Setting, clearing, toggling bits
- **Optimization** - Fast multiplication/division by powers of 2
- **Cryptography** - XOR operations in encryption

**Important:** Most logic operations **affect flags** (ZF, SF, PF) but typically **clear CF and OF**.

---
## AND - Logical AND

Performs bitwise AND operation. Result bit is 1 only if both corresponding bits are 1.

### Truth Table
```
A | B | A AND B
--|---|--------
0 | 0 |   0
0 | 1 |   0
1 | 0 |   0
1 | 1 |   1
```

### Syntax
```
and destination, source
```

### Usage Examples
```
; Basic AND
mov rax, 0b11110000
mov rbx, 0b10101010
and rax, rbx            ; RAX = 0b10100000

; Clear specific bits (masking)
mov rax, 0xFF
and rax, 0xF0           ; RAX = 0xF0 (cleared lower 4 bits)

; Check if even (test lowest bit)
mov rax, 42
and rax, 1              ; RAX = 0 (even number)

; Memory operand
and qword [rbx], 0xFF   ; Keep only lowest byte
```

### Common Use Cases

**1. Isolate specific bits (masking)**
```
; Get lower 4 bits of RAX
and rax, 0x0F           ; Mask: 0000...00001111
```

**2. Clear bits**
```
; Clear bit 3 (counting from 0)
and rax, ~(1 << 3)      ; Mask: 1111...11110111
```

**3. Check alignment**
```
; Check if address is 8-byte aligned
and rax, 7              ; RAX = 0 if aligned
jz aligned
```

### Flags Affected
- **ZF**: Set if result is zero
- **SF**: Set if result is negative
- **PF**: Set based on parity
- **CF, OF**: Cleared to 0

---
## OR - Logical OR

Performs bitwise OR operation. Result bit is 1 if either corresponding bit is 1.

### Truth Table
```
A | B | A OR B
--|---|-------
0 | 0 |   0
0 | 1 |   1
1 | 0 |   1
1 | 1 |   1
```

### Syntax
```
or destination, source
```

### Usage Examples
```
; Basic OR
mov rax, 0b11110000
mov rbx, 0b10101010
or rax, rbx             ; RAX = 0b11111010

; Set specific bits
mov rax, 0x00
or rax, 0x0F            ; RAX = 0x0F (set lower 4 bits)

; Combine flags/options
mov rax, FLAG_READ      ; 0x01
or rax, FLAG_WRITE      ; 0x02
or rax, FLAG_EXECUTE    ; 0x04
; RAX = 0x07 (all flags set)
```

### Common Use Cases

**1. Set specific bits**
```
; Set bit 5
or rax, (1 << 5)        ; Set bit: 0010 0000
```

**2. Combine bit flags**
```
; Combine permissions
or rax, 0x01            ; Add READ flag
or rax, 0x04            ; Add EXECUTE flag
```

**3. Convert to uppercase (ASCII trick)**
```
; Convert lowercase letter to uppercase
; 'a' (0x61) -> 'A' (0x41)
mov al, 'a'
or al, 0x20             ; Actually this converts to lowercase
; Wrong! Use AND with ~0x20 for uppercase
```

### Flags Affected
Same as AND (ZF, SF, PF set; CF, OF cleared)

---
## XOR - Logical Exclusive OR

Performs bitwise XOR operation. Result bit is 1 if corresponding bits are different.

### Truth Table
```
A | B | A XOR B
--|---|--------
0 | 0 |   0
0 | 1 |   1
1 | 0 |   1
1 | 1 |   0
```

### Syntax
```
xor destination, source
```

### Usage Examples
```
; Basic XOR
mov rax, 0b11110000
mov rbx, 0b10101010
xor rax, rbx            ; RAX = 0b01011010

; Toggle bits
mov rax, 0xFF
xor rax, 0x0F           ; RAX = 0xF0 (toggled lower 4 bits)

; Zero a register (VERY COMMON!)
xor rax, rax            ; RAX = 0 (fastest way to zero)
xor ecx, ecx            ; ECX = 0
```

### Common Use Cases

**1. Zero a register (most common!)**
```
xor rax, rax            ; Fastest way: RAX = 0
; Better than: mov rax, 0 (uses more bytes)
```

**2. Toggle bits**
```
; Toggle bit 3
xor rax, (1 << 3)       ; Flip bit 3
```

**3. Simple encryption (XOR cipher)**
```
; Encrypt/decrypt with key
mov rax, plaintext
xor rax, key            ; Encrypted
xor rax, key            ; Decrypted (XOR is reversible!)
```

**4. Swap values without temp register**
```
; Swap RAX and RBX without using temp
xor rax, rbx
xor rbx, rax
xor rax, rbx            ; RAX and RBX swapped!
```

**5. Check if two values are equal**
```
xor rax, rbx            ; If RAX == RBX, result is 0
jz equal                ; Jump if zero flag set
```

### Flags Affected
Same as AND/OR (ZF, SF, PF set; CF, OF cleared)

### XOR Properties
- `A XOR 0 = A` (identity)
- `A XOR A = 0` (self-inverse)
- `A XOR B XOR B = A` (reversible - useful for encryption)

---
## NOT - Logical NOT (One's Complement)

Inverts all bits (flips 1 to 0, 0 to 1).

### Syntax
```
not operand
```

### Usage Examples
```
; Basic NOT
mov rax, 0b11110000
not rax                 ; RAX = 0b00001111 (in 64-bit: 0xFFFFFFFFFFFFFF0F)

; Create bit mask
mov rax, (1 << 5)       ; RAX = 0b00100000
not rax                 ; RAX = 0b11011111 (all bits except bit 5)

; Flip all bits
mov al, 0x0F            ; AL = 0b00001111
not al                  ; AL = 0b11110000
```

### Common Use Cases

**1. Create inverted mask**
```
; Clear bit 3
mov rbx, (1 << 3)       ; Create bit mask
not rbx                 ; Invert mask
and rax, rbx            ; Clear bit 3 in RAX
```

**2. Bitwise negation**
```
not rax                 ; Flip all bits
```

### Flags Affected
**NO FLAGS** are affected by NOT (unlike other logic operations)

### Note: NOT vs NEG
- `NOT`: One's complement (flip bits)
- `NEG`: Two's complement (negate number = `NOT + 1`)
```
mov rax, 5
not rax                 ; RAX = 0xFFFFFFFFFFFFFFFA (flipped bits)
mov rax, 5
neg rax                 ; RAX = -5 (two's complement)
```

---
## TEST - Logical Compare (AND without storing)

Performs bitwise AND but **doesn't store result** - only sets flags.

### Syntax
```
test operand1, operand2
```

### Usage Examples
```
; Check if zero
test rax, rax           ; Very common: check if RAX is zero
jz is_zero              ; Jump if zero

; Check if specific bit is set
test rax, (1 << 5)      ; Check if bit 5 is set
jnz bit_set             ; Jump if bit is set

; Check if odd/even
test rax, 1             ; Check lowest bit
jz even                 ; Jump if even (bit 0 = 0)
jnz odd                 ; Jump if odd (bit 0 = 1)

; Check if negative (signed)
test rax, rax
js negative             ; Jump if sign flag set
```

### Common Use Cases

**1. Check if register is zero (most common!)**
```
test rax, rax           ; Check if RAX == 0
jz handle_zero
```

**2. Check specific bit**
```
test rax, 0x04          ; Check if bit 2 is set
jnz bit_is_set
```

**3. Check multiple bits**
```
test rax, 0x0F          ; Check if any of lower 4 bits are set
jnz at_least_one_set
```

**4. Check if negative (faster than CMP)**
```
test rax, rax
js is_negative          ; Jump if SF = 1
```

### Flags Affected
Same as AND (ZF, SF, PF set; CF, OF cleared)

### TEST vs CMP
- `TEST rax, rax`: Check if zero (AND without storing)
- `CMP rax, 0`: Check if zero (SUB without storing)
- **TEST is preferred** for zero checks (shorter instruction)

---
## SHL - Shift Left

Shifts bits to the left. Zeros are shifted in from the right. Last bit shifted out goes to CF.

### Syntax
```
shl destination, count
```

### How It Works
```
Before: 0b00001010 (10)
SHL 1:  0b00010100 (20)  <- Multiplied by 2
SHL 2:  0b00101000 (40)  <- Multiplied by 4
```

### Usage Examples
```
; Shift by 1 (multiply by 2)
mov rax, 5
shl rax, 1              ; RAX = 10

; Shift by 3 (multiply by 8)
mov rax, 10
shl rax, 3              ; RAX = 80 (10 × 2³)

; Shift by CL register
mov rcx, 4
mov rax, 3
shl rax, cl             ; RAX = 48 (3 × 2⁴)

; Create bit mask
mov rax, 1
shl rax, 5              ; RAX = 0b00100000 (bit 5 set)
```

### Common Use Cases

**1. Fast multiplication by power of 2**
```
shl rax, 1              ; RAX × 2
shl rax, 2              ; RAX × 4
shl rax, 3              ; RAX × 8
shl rax, 4              ; RAX × 16
```

**2. Create bit masks**
```
mov rax, 1
shl rax, 7              ; Create mask: 0b10000000
```

**3. Calculate array offset**
```
; offset = index × 8 (for 8-byte elements)
shl rdi, 3              ; RDI × 8
```

### Flags Affected
- **CF**: Last bit shifted out
- **ZF**: Set if result is zero
- **SF**: Set if result is negative
- **OF**: Set if sign bit changed (for count=1)

---
## SHR - Shift Right (Logical)

Shifts bits to the right. Zeros are shifted in from the left. Last bit shifted out goes to CF.

### Syntax
```
shr destination, count
```

### How It Works
```
Before: 0b00101000 (40)
SHR 1:  0b00010100 (20)  <- Divided by 2
SHR 2:  0b00001010 (10)  <- Divided by 4
```

### Usage Examples
```
; Shift by 1 (divide by 2, unsigned)
mov rax, 20
shr rax, 1              ; RAX = 10

; Shift by 3 (divide by 8)
mov rax, 80
shr rax, 3              ; RAX = 10 (80 ÷ 8)

; Extract upper bits
mov rax, 0x12345678
shr rax, 16             ; RAX = 0x00001234
```

### Common Use Cases

**1. Fast division by power of 2 (unsigned)**
```
shr rax, 1              ; RAX ÷ 2
shr rax, 2              ; RAX ÷ 4
shr rax, 3              ; RAX ÷ 8
```

**2. Extract high bits**
```
; Get upper 32 bits of 64-bit value
mov rax, 0x123456789ABCDEF0
shr rax, 32             ; RAX = 0x12345678
```

**3. Align down (clear lower bits)**
```
; Align address to 16-byte boundary
shr rax, 4              ; Divide by 16
shl rax, 4              ; Multiply by 16 (clear lower 4 bits)
```

### Flags Affected
Same as SHL

---
## SAR - Shift Arithmetic Right

Shifts bits right but preserves the sign bit (for signed division).

### Syntax
```
sar destination, count
```

### How It Works (Signed)
```
Before: 0b11111000 (-8 in signed 8-bit)
SAR 1:  0b11111100 (-4)  <- Signed divide by 2
SAR 2:  0b11111110 (-2)  <- Signed divide by 4

Before: 0b00001000 (8 in signed 8-bit)
SAR 1:  0b00000100 (4)   <- Signed divide by 2
```

**Key difference from SHR:**
- **SHR**: Shifts in 0 from left (logical shift)
- **SAR**: Shifts in **sign bit** from left (arithmetic shift)

### Usage Examples
```
; Signed division by 2
mov rax, -8
sar rax, 1              ; RAX = -4 (signed)

; Compare with SHR
mov rax, -8             ; RAX = 0xFFFFFFFFFFFFFFF8
shr rax, 1              ; RAX = 0x7FFFFFFFFFFFFFFC (wrong for signed!)

mov rax, -8
sar rax, 1              ; RAX = 0xFFFFFFFFFFFFFFFC = -4 (correct!)
```

### Common Use Cases

**1. Fast signed division by power of 2**
```
sar rax, 1              ; RAX ÷ 2 (signed)
sar rax, 3              ; RAX ÷ 8 (signed)
```

**2. Sign extension**
```
; Extend sign across register
mov rax, some_signed_value
sar rax, 63             ; Fill RAX with sign bit (all 0s or all 1s)
```

### Flags Affected
Same as SHL/SHR

---
## ROL - Rotate Left

Rotates bits to the left. Bits shifted out on the left reappear on the right.

### Syntax
```
rol destination, count
```

### How It Works
```
Before: 0b10110010
ROL 1:  0b01100101  <- Leftmost bit wraps to right
ROL 2:  0b10010110
```

### Usage Examples
```
; Rotate by 1
mov rax, 0b10110010
rol rax, 1              ; RAX = 0b01100101

; Rotate by multiple
mov rax, 0x123456789ABCDEF0
rol rax, 8              ; Rotate by 1 byte
```

### Common Use Cases

**1. Circular bit manipulation**
```
rol rax, 1              ; Rotate bits circularly
```

**2. Mixing bits (in crypto/hashing)**
```
rol rax, 13             ; Common in hash functions
xor rax, rbx
rol rax, 7
```

### Flags Affected
- **CF**: Last bit rotated out
- **OF**: Set if sign bit changed (for count=1)

---
## ROR - Rotate Right

Rotates bits to the right. Bits shifted out on the right reappear on the left.

### Syntax
```
ror destination, count
```

### How It Works
```
Before: 0b10110010
ROR 1:  0b01011001  <- Rightmost bit wraps to left
ROR 2:  0b10010110
```

### Usage Examples
```
; Rotate by 1
mov rax, 0b10110010
ror rax, 1              ; RAX = 0b01011001

; Undo ROL
mov rax, some_value
rol rax, 5              ; Rotate left by 5
ror rax, 5              ; Undo (back to original)
```

### Common Use Cases

**1. Reverse ROL operation**
```
ror rax, 8              ; Undo "rol rax, 8"
```

**2. Bit mixing in cryptography**
```
ror rax, 17             ; Common in crypto algorithms
xor rax, key
```

### Flags Affected
Same as ROL

---
## Common Patterns in CTF

### Pattern 1: Zero Register
```
xor rax, rax            ; RAX = 0 (most efficient)
```

### Pattern 2: Check if Even/Odd
```
test rax, 1             ; Check lowest bit
jz even                 ; Jump if even
jnz odd                 ; Jump if odd
```

### Pattern 3: Fast Multiplication/Division
```
; Multiply by 8
shl rax, 3              ; RAX × 2³ = RAX × 8

; Divide by 4 (unsigned)
shr rax, 2              ; RAX ÷ 2² = RAX ÷ 4

; Divide by 4 (signed)
sar rax, 2              ; Signed RAX ÷ 4
```

### Pattern 4: Set/Clear/Toggle Specific Bit
```
; Set bit 5
or rax, (1 << 5)        ; Set bit

; Clear bit 5
and rax, ~(1 << 5)      ; Clear bit

; Toggle bit 5
xor rax, (1 << 5)       ; Toggle bit
```

### Pattern 5: Extract Bit Range
```
; Extract bits 4-7 from RAX
mov rbx, rax
shr rbx, 4              ; Shift to position
and rbx, 0x0F           ; Mask to get 4 bits
```

### Pattern 6: Swap Nibbles (4-bit halves of byte)
```
; Swap lower and upper 4 bits of AL
mov al, 0x12            ; AL = 0001 0010
rol al, 4               ; AL = 0010 0001 = 0x21
```

### Pattern 7: Check Power of 2
```
; Check if RAX is power of 2
test rax, rax           ; Check not zero
jz not_power_of_two
mov rbx, rax
dec rbx                 ; RBX = RAX - 1
and rbx, rax            ; Should be 0 if power of 2
jz is_power_of_two
```

### Pattern 8: Align Address
```
; Align RAX down to 16-byte boundary
and rax, ~0x0F          ; Clear lower 4 bits

; Align RAX up to 16-byte boundary
add rax, 15
and rax, ~0x0F
```

---
## Quick Reference Table

| Instruction | Operation | Example | Result |
|-------------|-----------|---------|--------|
| `and` | Bitwise AND | `and rax, 0x0F` | Mask/clear bits |
| `or` | Bitwise OR | `or rax, 0x0F` | Set bits |
| `xor` | Bitwise XOR | `xor rax, rax` | Zero register |
| `not` | Bitwise NOT | `not rax` | Flip all bits |
| `test` | AND (no store) | `test rax, rax` | Check zero |
| `shl` | Shift left | `shl rax, 3` | Multiply by 8 |
| `shr` | Shift right (logical) | `shr rax, 2` | Divide by 4 (unsigned) |
| `sar` | Shift right (arithmetic) | `sar rax, 2` | Divide by 4 (signed) |
| `rol` | Rotate left | `rol rax, 8` | Circular shift left |
| `ror` | Rotate right | `ror rax, 8` | Circular shift right |

---
## Important Notes

### Shift Counts
- Count can be immediate (1-63 for 64-bit)
- Count can be in CL register only (not other registers)
- Shifts by 0 do nothing

### Performance
- Logic operations are **very fast** (1 cycle)
- Shifts/rotates by 1 are fast
- Variable shifts (using CL) may be slower

### Use Cases Summary
- **AND**: Masking, clearing bits, testing bits
- **OR**: Setting bits, combining flags
- **XOR**: Toggling bits, zeroing registers, simple encryption
- **NOT**: Inverting bits, creating masks
- **TEST**: Checking bits/zero without modifying
- **SHL/SHR**: Fast multiply/divide by powers of 2
- **SAR**: Signed division by powers of 2
- **ROL/ROR**: Bit mixing, crypto operations

---
## Others:
- For detailed instruction behavior: Intel® 64 and IA-32 Architectures Software Developer's Manual Vol. 2
- Bit manipulation tricks: https://graphics.stanford.edu/~seander/bithacks.html

---
## Related Source:
- [[Assembly]] - Main assembly documentation
- [[Assembly - Registers]] - Registers affected by logic operations
- [[Assembly - Arithmetic Operations]] - Arithmetic vs logic operations
- [[Assembly - Control Flow]] - Using flags set by logic operations
- [[GDB]] - Viewing bit-level changes in real-time