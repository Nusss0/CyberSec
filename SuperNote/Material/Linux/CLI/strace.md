## Definition
>*`(System Call Trace)`* is a Linux Command used to traces System Calls made by a program

---
## Tags 

#Material #LinuxBasic #CLI 

---
###  Usage : 
```bash
strace [options] [command] [args]
```

### Options : 
| Command                   | Description                      |
| ------------------------- | -------------------------------- |
| `-o <file>`               | Write output to file             |
| `-c`                      | Count and summarize calls        |
| `-p <PID>` <sup>[1]</sup> | Attatch to running process       |
| `-e <syscall>`            | Trace only specific system calls |
| `-f`                      | Follow forks                     |
| `-s <size>`               | Maximum strings size to display  |
| `-t`                      | Print timestamp                  |
| `-T`                      | Show time spent in each syscal   |
### Others :
-  <sup>[1]</sup> When we use strace in normal way, it starts the program with strace from the beginning. 
- For further information please use manual page.

---
## Related Source : 
[[System Calls]], [[ltrace]]