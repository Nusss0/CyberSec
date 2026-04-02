## Definition

>C standard library (libc) function that works **identically to `printf()`** in how it processes format strings and consumes arguments — but instead of printing to **stdout**, it writes the output **into a char buffer** with a size limit.

---
## Tags

#Material #C #libc #FormatString #stdio-h 

---
## Quick Reference — Comparison with `printf()`

|Aspect|`printf()`|`snprintf()`|
|---|---|---|
|Output destination|stdout (screen)|char buffer (memory)|
|Size limit|No|Yes (`size` parameter)|
|Format string processing|Identical|Identical|
|Argument consumption|Identical|Identical|
|Two-pointer system|Same|Same|
|Returns|Chars printed|Chars it **would have** written (ignoring size limit)|

Everything about format specifiers, the two-pointer system, and argument slot consumption is exactly the same as `printf()`. See the `printf()` note for full details on those.

---
## Syntax

```c
#include <stdio.h>

int snprintf(char *buffer, size_t size, const char *format, ...);
```

**Library:** libc (linked by default) **Header:** `<stdio.h>` **Man page:** `man 3 snprintf`

### Parameters

- `buffer` — destination where output gets written to
- `size` — max bytes to write including `\0` (prevents buffer overflow)
- `format` — the format string (instructions)
- `...` — variadic arguments matching each specifier in the format string

### Returns

- The number of bytes it **would have written** if `size` was unlimited (excluding `\0`)
- This is NOT the actual bytes written — it's the hypothetical full count
- Returns negative value on error

---
## Return Value vs Actual Output

This is the most important detail of `snprintf`:

```c
char buf[10];
int ret = snprintf(buf, 10, "ABCDEFGHIJKLMNO");  // 15 chars

// ret = 15        ← what it WANTED to write
// buf = "ABCDEFGHI\0"  ← what it ACTUALLY wrote (9 chars + null, capped at size 10)
```

The internal **bytes counter keeps counting past the size limit**. Only the output to `buffer` is truncated.

---
### Security — Format String Vulnerability

### Vulnerable Pattern

```c
snprintf(buffer, sizeof buffer, user_input);  // VULNERABLE — user controls format string
```

### Safe Pattern

```c
snprintf(buffer, sizeof buffer, "%s", user_input);  // SAFE — user input is data only
```

`snprintf` prevents classic **buffer overflow** (output is capped at `size`). But if user input is passed directly as the format string, **format string attacks still work** because:

1. User controls what specifiers get processed
2. `%x` still leaks stack data
3. `%n` still writes to arbitrary addresses

### Why `%n` Still Works Despite Size Limit

`%n` writes the **internal counter**, not the truncated output length.

```c
char buf[64];
snprintf(buf, 64, "%500x%n", junk, &target);

// buf only holds 63 chars + null (truncated)
// but internal counter = 500
// %n writes 500 to &target
```

The size limit protects the buffer from overflow. It does **not** protect against `%n` writes.

### Stack Feedback Loop (snprintf-specific behavior)

When `buffer` is a local variable, it sits on the stack. The argument pointer also reads from the stack. This means `snprintf` can **read its own output**:

```
snprintf writes "AAAA" to buffer[0..3]
    ↓
%x reads from stack → lands on buffer[0..3]
    ↓
reads 0x41414141 (the "AAAA" it just wrote)
    ↓
writes "41414141" to buffer[4..11]
    ↓
next %x reads buffer[4..7] → reads "4141" → 0x31343134
    ↓
...snprintf is reading its own output
```

This does NOT happen with `printf(buf)` because `printf` writes to stdout, never modifying the buffer in memory.

---
## Others

- `man 3 snprintf` — covers `snprintf`, `printf`, `fprintf`, `sprintf` and all variants
- `snprintf` is the safe replacement for `sprintf` (which has no size limit and is dangerous)
- Safe against buffer overflow, but **not** safe against format string attacks
---
## Related Source
[[printf()]], [[Format String Attack]]