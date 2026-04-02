## Definition
>Check if a file can be accessed with specific permissions.

---
## Tags 

#Material #SystemCalls 

---
### Syntax : 
```c
access(path, mode)
```
**Parameters** : 
- Path : file path to check
- Mode : permission type (4 : read permission)

### Examples : 
```c
access("/etc/passwd", 4)  // Can real user read this file?
```
### Concepts : 
- Use real UID (the user who runs the program).
- NOT affected by SUID.
- Returns 0 = success (accessible), -1 = failure (not accessible)

### Others :
- 

---
## Related Source : 