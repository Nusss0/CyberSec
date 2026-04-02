## Definition
>A way for programs to request services from the operating system kernel.

---
## Tags 

#Material #GeneralConcepts #OperatingSystem #SystemCalls

---
### Concepts : 
- Programs run in several privileges levels. There are User Mode, Kernel Mode, and etc.
- If our programs has UserMode privileges only, but we need the Kernel privileges, then the solution is System Calls
- System call allows us to ask the kernel to do something.
### Common System Calls : 
| SysCall  | Definition             |
| -------- | ---------------------- |
| `fork`   | Create new process     |
| `exec`   | Run different program  |
| `exit`   | Terminate Process      |
| `wait`   | Wait for child process |
| `kill`   | Send signal to process |
| `open`   | Open file              |
| `read`   | Read from file         |
| `write`  | Write to file          |
| `close`  | Close file             |
| `lseek`  | Move file position     |
| `getpid` | Get process ID         |
| `getuid` | Get user ID            |
| `time`   | Get current time       |

### Special System Calls : 
| SysCall      | Definition            |
| ------------ | --------------------- |
| [[access()]] | Check file permission |
| [[system()]] | Execute shell command |

### Others :
- 

---
## Related Source : 
[[access()]], 