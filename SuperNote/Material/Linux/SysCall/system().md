## Definition
>to Executes a shell command.

---
## Tags 

#Material #SystemCalls #GeneralConcepts

---
### Syntax :
```c
system(command)
```

### How it works :
- Spawns `/bin/sh -c "command"`
- Shell parses the command string (splits by spaces, handles wildcards, etc.)
- Runs with **effective UID/GID** (affected by SUID bit)
- Returns exit status of command
### Others :
- `/bin/sh` = the shell program
- `-c` = flag meaning "execute the following command string"
- `"command"` = the command to execute

---
## Related Source : 