## Definition
>Techniques for inserting binary payloads into vulnerable programs using Python, enabling precise control over buffer overflow exploits through command-line payload generation and stdin delivery.

---
## Tags

#Material #Python #BinaryExploitation 

---
## Core Concepts

### 1. Payload Structure

A payload consists of:

- **Padding/Filler**: Bytes to fill the buffer (usually 'A' or NOP sled)
- **Target Value**: The value to overwrite (addresses, variables, etc.)
- **Optional Data**: Additional data for complex exploits

**Example structure:**

```
[20 bytes padding][4 bytes target value]
[AAAAAAAAAAAAAAAAAAAA][\xef\xbe\xad\xde]
```

### 2. Stdin vs Command-Line Arguments

**Stdin (Standard Input):**

- Program reads using `scanf()`, `gets()`, `read()`
- Delivery: Use pipe `|`
- Example: `payload | ./program`

**Command-Line Arguments:**

- Program reads from `argv[]`
- Delivery: Use command substitution `$()`
- Example: `./program $(payload)`

**How to identify:**

- Check source code for input method
- Use `ltrace` to see which function is called
- If program shows prompt "Enter input:", it's likely stdin

### 3. Keeping Shell Interactive

When exploiting with stdin, the shell spawns but closes immediately because stdin ends. Solution: **chain with `cat`** to keep stdin open.

**Without cat:**
```bash
python -c 'payload' | ./program
# Shell spawns → stdin closes → shell exits
```

**With cat:**
```bash
(python -c 'payload'; cat) | ./program
# Shell spawns → cat keeps stdin open → you can interact
```

---
## Usage

### Python 2 Method

**Basic payload:**
```bash
python -c 'print("A"*20 + "\xef\xbe\xad\xde")'
```

**With stdin delivery:**
```bash
(python -c 'print("A"*20 + "\xef\xbe\xad\xde")'; cat) | ./program
```

**Advantages:**
- Simpler syntax
- Direct string printing works with bytes

**Disadvantages:**
- Python 2 is deprecated
- May not be available on modern systems

### Python 3 Method

**Basic payload:**
```bash
python3 -c 'import sys; sys.stdout.buffer.write(b"A"*20 + b"\xef\xbe\xad\xde")'
```

**With stdin delivery:**
```bash
(python3 -c 'import sys; sys.stdout.buffer.write(b"Offset" + b"Payload")'; cat) | ./program
```

**Why the extra complexity?**
- Python 3 distinguishes between **strings** (text) and **bytes** (binary data)
- `sys.stdout` expects strings, but we need raw bytes
- `sys.stdout.buffer` gives direct access to binary output
- `b"..."` prefix creates bytes literal

**Key differences:**

|Aspect|Python 2|Python 3|
|---|---|---|
|String prefix|`"..."`|`b"..."`|
|Output method|`print()`|`sys.stdout.buffer.write()`|
|Import needed|No|Yes (`import sys`)|

### Command-Line Argument Delivery

**For programs that read from argv:**

**Python 2:**
```bash
./program $(python -c 'print("A"*20 + "\xef\xbe\xad\xde")')
```

**Python 3:**
```bash
./program $(python3 -c 'import sys; sys.stdout.buffer.write(b"A"*20 + b"\xef\xbe\xad\xde")')
```

**Note:** No `cat` needed here because we're not using stdin.

---
## Syntax Breakdown

### The Parentheses and Semicolon: `(cmd1; cmd2)`
**Purpose:** Group commands so their combined output goes through the pipe.

**Without grouping:**
```bash
python -c 'payload'; cat | ./program
# Only cat output goes to program (WRONG)
```

**With grouping:**
```bash
(python -c 'payload'; cat) | ./program
# Both python AND cat output go to program (CORRECT)
```

**How `;` works:**
- Executes commands sequentially
- First: `python` outputs payload
- Then: `cat` keeps stdin open

### The Pipe: `|`

**Purpose:** Connects stdout of left command to stdin of right command.
```bash
command1 | command2
# command1's output → command2's input
```

**In exploitation:**
````bash
(payload_generator; cat) | vulnerable_program
#       ↓                         ↓
#   generates bytes        reads from stdin
```

### Why `cat` With No Arguments

`cat` without arguments:
- Reads from **stdin** (your keyboard)
- Outputs to **stdout**
- **Stays running** until you press Ctrl+D

**In our context:**
```
python outputs payload → program reads it → spawns shell
                ↓
        cat keeps running → shell has input → you can type commands
````
