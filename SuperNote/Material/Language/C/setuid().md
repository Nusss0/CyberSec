## Definition
>is a POSIX syscall wrapped by libc that used to sets the **Effective UID** of the calling process.

---
## Tags 

#Material #LinuxBasic #SystemCalls #OperatingSystem #C #unistd-h

---
## Syntax :
```c
#include <unistd.h>
int setuid(uid_t uid);
```
**Returns:** 0 on success, -1 on error

---
## Behavior of `setuid()`
```
If caller is ROOT:
   setuid(X) → Real=X, Effective=X, Saved=X (ALL change)

If caller is NON-ROOT:
   setuid(real_uid)  → Effective=real_uid ✅
   setuid(saved_uid) → Effective=saved_uid ✅
   setuid(other)     → DENIED ❌ (returns -1)
```

---
## Why setuid() Alone Fails for Exploitation
For example, in `narnia1` context :
```
Real UID    = narnia1 (1001)
Effective   = narnia2 (1002)  ← from SUID bit
Saved UID   = narnia2 (1002)

After execve("/bin/sh"):
   Kernel DROPS effective UID back to real UID
   → Shell runs as narnia1, not narnia2
```
**Problem:** `setuid()` only changes effective UID. Real UID stays as narnia1, so `execve()` drops privilege.

The solution is to use `setreuid()`, which will set our Real UID and also Effective UID.

---
## Others :
- We could use `setuid(geteuid())` to get the Effective UID of SUID file.

---
## Related Source : 
[[setreuid()]], [[SetUID Files]], [[User ID in Linux]]