## Definition
>is a POSIX syscall wrapped by libc that used to sets **both** real and effective UIDs in one call.
---
## Tags 

#Material #LinuxBasic #SystemCalls #OperatingSystem #C #unistd-h

---
## Syntax : 
```c
#include <unistd.h>
int setreuid(uid_t ruid, uid_t euid);
```
**Parameters:**
- `ruid` — new real UID (-1 to keep unchanged)
- `euid` — new effective UID (-1 to keep unchanged)

**Returns:** 0 on success, -1 on error

---
## Permission Rules :
| Caller   | Can Set Real UID To               | Can Set Effective UID To          |
| -------- | --------------------------------- | --------------------------------- |
| Root     | ANY                               | ANY                               |
| Non-root | Current Real or Current Effective | Current Real, Effective, or Saved |

---
## Others :
- We could use `setreuid(geteuid(),geteuid())` to get the Effective UID of SUID file.

---
## Related Source : 
[[SetUID Files]], [[User ID in Linux]], [[geteuid()]]