## Definition
>Linux syscall wrapped by libc used to **replaces** the current process with a new program with same PID and same UIDs. The old program is gone.

---
## Tags 

#Material #LinuxBasic #SystemCalls #OperatingSystem #C #unistd-h

---
##  Syntax : 
```c
#include <unistd.h>
int execve(const char *pathname, char *const argv[], char *const envp[]);
```
**Parameters:**
- `pathname` — path to executable (e.g., "/bin/sh")
- `argv` — argument array (can be NULL)
- `envp` — environment array (can be NULL)

**Returns:** Does NOT return on success (process is replaced), -1 on error

---
## Security Behavior : 
When `execve()` runs, the kernel applies security rules:

```
IF Real UID ≠ Effective UID:
   New program's Effective UID = Real UID (DROPPED)
   
IF Real UID = Effective UID:
   New program's Effective UID = Real UID (UNCHANGED)
```

This is WHY `setreuid()` is needed before `execve()` in SUID exploitation.

---
## Related Source : 
[[setreuid()]], [[setuid()]], [[SetUID Files]], [[User ID in Linux]]