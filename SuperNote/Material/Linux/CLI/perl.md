## Definition
>*`(perl)`* is a programming language interpreter that can execute code directly from the command line using various flags.

---
## Tags 

#Material #LinuxBasic #CLI

---
###  Usage : 
```bash
perl [Option] [command]
```

### Options : 
| Flag | Description                                                   |
| ---- | ------------------------------------------------------------- |
| `-e` | Execute code from command line (one-liner)                    |
| `-p` | Loop through input lines, print each line after processing    |
| `-l` | Automatically add newline to print, remove newline from input |
| `-n` | Loop through input lines, don't auto-print                    |
| `-i` | Edit files in-place (with backup if extension given)          |
### Common Usage : 
```bash
perl -lpe '$_=pack"B*",$_'
```
**Explaination** : 
- **`-lpe` combination**: `-l` (handle newlines) + `-p` (loop and print) + `-e` (execute code)
- `$_` is special variable holding current line being processed
- `pack` is a Perl function used to convert data into binary format using template codes.
- `unpack` is the reverse operation (ASCII → binary)

### Templates in `pack` :
| Template | Description                                                  |
| -------- | ------------------------------------------------------------ |
| `B*`     | Binary string, high bit first (most common for binary→ASCII) |
| `b*`     | Binary string, low bit first                                 |
| `C`      | Unsigned char (1 byte, 0-255)                                |
| `H*`     | Hexadecimal string, high nibble first                        |
| `a`      | ASCII string with null padding                               |

### Complete Example : 
```shell
echo "01000001" | perl -lpe '$_=pack"B*",$_'
```

**Step by step:**
1. `echo "01000001"` sends binary string to pipe
2. `-l` removes the newline from "01000001\n" → "01000001"
3. `-p` creates loop: `while (<>) { ... print $_ }`
4. First iteration: `$_ = "01000001"`
5. Execute: `$_ = pack("B*", "01000001")`
   - `pack("B*", ...)` converts binary to ASCII
   - Binary "01000001" = decimal 65 = ASCII 'A'
   - Now `$_ = "A"`
6. `-p` automatically prints `$_` → prints "A"
7. `-l` adds newline back → "A\n"

**Output:** `A`

### Others :
- For further information please use manual page.

---
## Related Source : 