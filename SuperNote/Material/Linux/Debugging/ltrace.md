## Definition
>*`(Library Trace)`* is a Super Powerful Linux Command used to record library calls made by a process. It shows you what functions a program calls from shared libraries *(strcmp, printf, etc)* along with their arguments and return values.

---
## Tags 

#Material #LinuxBasic #CLI #ReverseEngineering

---
###  Usage : 
```bash
ltrace [Option] [command] [args]
```
### Options : 
| Command                   | Description                               |
| ------------------------- | ----------------------------------------- |
| `-s <length>`             | Maximum string length to display          |
| `-o <filename>`           | Write output to a file instead of stderr  |
| `-p <PID>` <sup>[1]</sup> | Attach to running process by PID          |
| `-c`                      | Count and summarize library calls.        |
| `-f`                      | Trace child processes (follows forks)     |
| `-i`                      | Print instruction pointer at time of call |
### Others :
- <sup>[1]</sup> When we use ltrace in normal way, it starts the program with ltrace from the beginning. But with PID we could use ltrace to a running program.
- **SUID bit is ignored when process is being traced** (security feature). Programs being traced with `ptrace` (which `ltrace` uses) **cannot gain SUID privileges**. This prevents attackers from using debuggers to exploit SUID programs.
- Command is the program / binary we want to trace, for example (*`./someProgram`*, *`./check`*, *`ls`*)
- Args is arguments passed to that program, for example (*`ltrace ls /home`*, *this will trace every step and function called to list directory /home*).
- If the program doesn't need arguments, it will either skip it or show an invalid argument message.
- In rare case, it could show up an error message.
- For further information please use manual page.

---
## Related Source : 
[[PID]],  [[fork]], [[ltrace]]