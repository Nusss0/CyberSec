## Definition
>C standard library (libc) function that formats and prints data to stdout. It reads a **format string** as instructions, then consumes arguments from the stack to match each format specifier. It is a **variadic function** — accepts any number of arguments after the format string, with no way to verify how many were actually passed.

---
## Tags

#Material #C #libc #FormatString #stdio-h 

---
## Quick Reference — Format Specifiers

|Specifier|Action|Type Expected|Direction|
|---|---|---|---|
|`%d` / `%i`|Print signed decimal integer|`int`|READ|
|`%u`|Print unsigned decimal integer|`unsigned int`|READ|
|`%x` / `%X`|Print unsigned hex (lower/upper)|`unsigned int`|READ|
|`%o`|Print unsigned octal|`unsigned int`|READ|
|`%s`|Print string|`char *`|READ|
|`%c`|Print single character|`int` (cast to `char`)|READ|
|`%p`|Print pointer address|`void *`|READ|
|`%f`|Print float/double|`double`|READ|
|`%n`|**WRITE** bytes printed so far to address|`int *`|**WRITE**|
|`%%`|Print literal `%`|(none)|—|

## Quick Reference — Width & Length Modifiers

|Modifier|Meaning|Example|
|---|---|---|
|`%10x`|Minimum 10 characters wide, right-aligned|`" ff"`|
|`%-10x`|Minimum 10 characters wide, left-aligned|`"ff "`|
|`%010x`|Pad with zeros|`"00000000ff"`|
|`%hhn`|Write 1 byte (`char`)|Used for partial writes|
|`%hn`|Write 2 bytes (`short`)|Used for partial writes|
|`%n`|Write 4 bytes (`int`)|Default write size|
|`%ln`|Write 8 bytes (`long`)|64-bit write|
|`%N$x`|Direct parameter access — read Nth arg|`%4$x` reads arg 4|
|`%N$n`|Direct parameter access — write to Nth arg|`%4$n` writes to arg 4|

---
## Syntax

```c
#include <stdio.h>

int printf(const char *format, ...);
```

**Library:** libc (linked by default) **Header:** `<stdio.h>` **Man page:** `man 3 printf`

### Parameters

- `format` — the format string containing text and specifiers
- `...` — variadic arguments matching each specifier in the format string

### Returns

- Number of characters printed on success
- Negative value on error

---
## How It Works Internally

`printf` uses **two independent pointers**:
1. **Format string pointer** — walks through the format string byte by byte, always moving forward
2. **Argument pointer** — starts at the first argument slot on the stack, only advances when the format string pointer encounters a `%` specifier

```
Format string pointer:  always walking through the format string
     ↓
     H  e  l  l  o  %  d  ,  %  x  \0
                     |        |
                     ↓        ↓
Argument pointer:  slot 1   slot 2
                   read     read
```

`printf` has **no argument count metadata**. It determines how many arguments to consume purely by counting specifiers in the format string.

---
## Variants

|Function|Output Destination|Extra Parameter|
|---|---|---|
|`printf`|stdout|—|
|`fprintf`|FILE stream|`FILE *stream`|
|`sprintf`|char buffer (no size limit, dangerous)|`char *str`|
|`snprintf`|char buffer (size-limited)|`char *str, size_t size`|
|`dprintf`|file descriptor|`int fd`|

**Man page:** `man 3 printf` (covers all variants)

---
## Security — Format String Vulnerability

### Vulnerable Pattern
```c
printf(user_input);    // VULNERABLE — user controls the format string
```
### Safe Pattern
```c
printf("%s", user_input);  // SAFE — user input treated as data only
```

### Why It's Dangerous
When user input is passed directly as the format string:
1. User controls what specifiers `printf` processes
2. `printf` blindly reads stack slots as arguments (no validation)
3. `%x` / `%p` → **leaks stack contents** (information disclosure)
4. `%n` → **writes to arbitrary memory** (code execution)

### The `%n` Attack Summary
1. Embed target address in input buffer (it lands on the stack)
2. Use `%x` or `%N$` to advance argument pointer to your buffer's position
3. `%n` writes the bytes-printed count into that address
4. Control the written value with width padding (e.g., `%100x`)

### Overwrite Targets
- Return addresses → redirect execution
- GOT entries → hijack library calls
- `.dtors` → execute code at program exit

---
## Related Source
[[Format String Attack]]