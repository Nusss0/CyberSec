
>User ID (UID) is a unique number assigned to each user in Linux. The kernel uses UIDs (not usernames) to determine permissions.
---
## Tags 

#Material #SystemCalls #LinuxBasic

---
## Reference Table : 
| Function      | Syscall # (x86) | Purpose                  | Header       |
| ------------- | --------------- | ------------------------ | ------------ |
| `getuid()`    | 24              | Get real UID             | `<unistd.h>` |
| `geteuid()`   | 49              | Get effective UID        | `<unistd.h>` |
| `setuid()`    | 23              | Set effective UID        | `<unistd.h>` |
| `setreuid()`  | 70              | Set real + effective UID | `<unistd.h>` |
| `setresuid()` | 164             | Set all three UIDs       | `<unistd.h>` |
| `getresuid()` | 165             | Get all three UIDs       | `<unistd.h>` |

---
## About UID

How to view our IDs : 
```bash
id
```

Special UID in LInux : 

|UID|User|Significance|
|---|---|---|
|0|root|Superuser - full system access|
|1-999|system|Reserved for system services|
|1000+|regular|Normal users|

---
## Types of UID 
| **UID Type**      | **Acronym** | **Description**       | **Purpose**                                                              |
| ----------------- | ----------- | --------------------- | ------------------------------------------------------------------------ |
| **Real UID**      | RUID        | Who you actually are. | Defined at login. Controls who can send signals to the process.          |
| **Effective UID** | EUID        | Who you claim to be.  | **The most important one.** Used for permission checks (files, ports).   |
| **Saved UID**     | SUID        | The "Restore Point".  | Allows a process to drop privileges (switch EUID) and regain them later. |

---
## Related Source : 
[[setuid()]], [[setreuid()]],