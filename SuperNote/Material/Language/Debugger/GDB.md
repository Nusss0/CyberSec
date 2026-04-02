## Definition

> `(GNU Debugger)` used to debug programs in C, C++, and other languages. It allows you to see what's happening inside a program during execution, stop at specific address, examine memory and variables, and execute code step by step.

---
## Tags

#Material #BinaryExploitation

---

### Usage :

bash

```bash
# Start GDB
gdb <program>                      # Debug executable
gdb <program> <core>               # Debug with core dump
gdb -p <PID>                       # Attach to running process
gdb --args <program> arg1 arg2     # Debug with arguments

# Quick start
gdb -q <program>                   # Quiet mode (no intro text)
```

### Basic Commands :

|Command|Short|Description|
|---|---|---|
|`run`|`r`|Execute program from start|
|`start`|-|Run and auto-break at main()|
|`continue`|`c`|Resume execution|
|`kill`|-|Stop program execution|
|`quit`|`q`|Exit GDB|

---

### Other Commands :

#### 1. Disassembly

|Command|Short|Description|
|---|---|---|
|`disassemble <function>`|`disas <function>`|Show assembly code (usually `main`)|
|`disassemble /r`|`disas /r <function>`|Show raw instruction bytes|
|`disassemble /m`|`disas /m <function>`|Mix source and assembly|
|`disassemble /s`|`disas /s <function>`|Show source if available|

---

#### 2. Breakpoints

```bash
break <function>           # Break at function entry
break *<address>          # Break at memory address (0x...)
break <file>:<line>       # Break at specific line number
break main                # Common: break at main function
```

| Command            | Short | Description                   |
| ------------------ | ----- | ----------------------------- |
| `break <location>` | `b`   | Set breakpoint                |
| `info breakpoints` | `i b` | List all breakpoints          |
| `delete <num>`     | `d`   | Remove breakpoint             |
| `disable <num>`    | `dis` | Disable breakpoint            |
| `enable <num>`     | `en`  | Enable breakpoint             |
| `clear <location>` | -     | Delete breakpoint at location |

---

#### 3. Stepping

|Command|Short|Description|
|---|---|---|
|`step`|`s`|Step into function calls|
|`next`|`n`|Step over function calls|
|`stepi`|`si`|Execute one instruction|
|`nexti`|`ni`|Next instruction (skip calls)|
|`finish`|`fin`|Run until function returns|
|`until <location>`|`u`|Run until location|

**Key Difference** :

- `step` : goes **inside** function calls
- `next` : executes function but doesn't go **inside**

---

#### 4. Printing & Examining Variables and Memory

```bash
# Variable Printing
print/<Format> <var/register> 
p/<Format> <var/register>

# Memory Examination
x/<Count><Format><Size> <address>
```

**Print/Examine Formats:**

|Format|Description|
|---|---|
|`/x`|Hexadecimal|
|`/d`|Decimal (signed)|
|`/u`|Decimal (unsigned)|
|`/t`|Binary|
|`/c`|Character|
|`/f`|Floating point|
|`/s`|String|
|`/i`|Instruction|

**Memory Examination Format Breakdown:**

- **Count**: How many units to display
- **Format**: x(hex), d(decimal), s(string), i(instruction)
- **Size**: b(byte-1), h(halfword-2), w(word-4), g(giant-8)

**Examples:**

bash

```bash
# Print examples
p/x variable              # Print variable in hex
p/d $eax                  # Print EAX register in decimal
p/t $eax                  # Print EAX in binary

# Memory examination examples
x/10x $esp                # 10 hex words from stack pointer
x/20i $eip                # 20 instructions from instruction pointer
x/s 0x08048000            # String at specific address
x/10wx 0x08048000         # 10 words in hex at address
x/4gx $rsp                # 4 giant (8-byte) hex from stack (64-bit)
x/16xb $esp               # 16 bytes in hex from stack pointer
```

---

#### 5. Registers

**Important Registers:**

|Register|Purpose|
|---|---|
|`EIP/RIP`|Instruction Pointer (current instruction address)|
|`ESP/RSP`|Stack Pointer (top of stack)|
|`EBP/RBP`|Base Pointer (base of current stack frame)|
|`EAX/RAX`|Accumulator (often holds return values)|
|`EBX/RBX`|Base register|
|`ECX/RCX`|Counter register (loop counter)|
|`EDX/RDX`|Data register|
|`ESI/RSI`|Source Index (string operations)|
|`EDI/RDI`|Destination Index (string operations)|

**Register Commands:**

```bash
info registers / i r      # Show all registers
info all-registers        # Show all including floating-point
print $eax                # Print specific register value
set $eax = 0x10           # Modify register value
```

**Note:**

- **E** prefix = 32-bit registers (EAX, ESP, EIP)
- **R** prefix = 64-bit registers (RAX, RSP, RIP)

---

#### 6. Information Commands

```bash
info <option>
i <option>
```

**Options:**

|Command|Description|
|---|---|
|`info functions`|List all functions in program|
|`info variables`|List global/static variables|
|`info locals`|Show local variables|
|`info args`|Show function parameters|
|`info registers`|Display all registers|
|`info breakpoints`|List breakpoints|
|`info watchpoints`|List watchpoints|
|`info frame`|Current stack frame details|
|`info threads`|List all threads|

---
#### 7. Backtrace (Call Stack)

> **Backtrace** shows the **call stack** - the chain of function calls that led to the current point in execution. It displays which functions called which, in order from the current function back to `main()`.

**Basic Commands:**

```bash
backtrace               # Show full call stack
bt                      # Short version
bt full                 # Show stack WITH local variables
bt <n>                  # Show only first n frames
bt -<n>                 # Show only last n frames
```

**Navigation Commands:**
```bash
frame <n> / f <n>       # Jump to specific frame number
up                      # Move to calling frame (older)
down                    # Move to called frame (newer)
info frame              # Details of current frame
```

Example Output:
```bash
(gdb) bt
#0  0x08048456 in vulnerable_function () at prog.c:10
#1  0x0804849a in middle_function () at prog.c:15
#2  0x080484c2 in main () at prog.c:20
```

- `#0` = Current function (where execution stopped)
- `#1` = Function that called #0
- `#2` = Function that called #1

---

#### 8. Watchpoints

> **Watchpoints** automatically break execution when a **variable's value changes** or when a specific **memory location is accessed**.

```bash
watch <variable>            # Break when variable is WRITTEN
watch *<address>            # Break when memory address is WRITTEN
rwatch <variable>           # Break when variable is READ
awatch <variable>           # Break when variable is READ or WRITTEN

info watchpoints            # List all watchpoints
delete <num>                # Remove watchpoint by number
disable <num>               # Disable watchpoint
enable <num>                # Enable watchpoint
```

**Types of Watchpoints:**

|Type|Command|Triggers When|
|---|---|---|
|**Write**|`watch`|Variable/memory is modified|
|**Read**|`rwatch`|Variable/memory is read|
|**Access**|`awatch`|Variable/memory is read OR written|

**Examples:**
```bash
watch password              # Monitor when 'password' variable changes
watch *0x08049000           # Monitor specific memory address
watch buffer[5]             # Watch specific array element
watch *(int*)($ebp+4)       # Watch return address on stack
```

---

## GDB Enhanced Versions

Standard GDB can be enhanced with plugins for better usability, especially for CTF and exploit development:

| Type       | Description                           |
| ---------- | ------------------------------------- |
| **PEDA**   | Python Exploit Development Assistance |
| **pwndbg** | Modern exploit development tool       |
| **GEF**    | GDB Enhanced Features                 |

**Key Features:**

- Color-coded output
- Enhanced disassembly display
- Automatic display of registers, stack, and code
- Built-in exploit helpers (ROP gadgets, pattern generation)
- Better memory visualization

---

## Useful Tips

1. **Enable history**: GDB saves command history in `~/.gdb_history`
2. **Repeat commands**: Press Enter to repeat last command
3. **Tab completion**: Use Tab to autocomplete commands and symbols
4. **Help system**: Type `help <command>` for detailed info
5. **GDB init file**: Customize GDB with `~/.gdbinit` file

**Common GDB init customizations:**

```bash
set disassembly-flavor intel    # Use Intel syntax (easier to read)
set pagination off              # Don't pause long outputs
set history save on             # Save command history
set follow-fork-mode child      # Debug child process after fork
set print pretty on             # Pretty-print structures
set print array on              # Pretty-print arrays
```

---

## Quick Reference

| Command          | Short | What It Does              |
| ---------------- | ----- | ------------------------- |
| `run`            | `r`   | Start program             |
| `break main`     | `b`   | Break at main             |
| `continue`       | `c`   | Continue execution        |
| `step`           | `s`   | Step into functions       |
| `next`           | `n`   | Step over functions       |
| `print $eax`     | `p`   | Print register            |
| `x/10i $eip`     | -     | View 10 instructions      |
| `backtrace`      | `bt`  | Show call stack           |
| `info registers` | `i r` | Show all registers        |
| `disas main`     | -     | Disassemble main function |
| `quit`           | `q`   | Exit GDB                  |

---

## Others:

- For further information: `man gdb` or type `help` within GDB
- Use `help <command>` for specific command details