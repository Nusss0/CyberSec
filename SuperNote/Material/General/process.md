## Definition
>*(process)* is a running program.

---
## Tags 

#Material #GeneralConcepts #OperatingSystem

---
### Simple example :
Given a file `./check`, where check is a program file. When we run this file, the Operating System willl : 
- Loads the program into memory
- Assigns it with a Unique ID (PID : Process ID)
- Gives it resources (GPU, CPU, etc)
- Executes the codes
- etc.

### Others : 
- To run another process, a running process could call a system call called [[exec]]().
- A running process could clone itself using [[fork]]() system call.

---
## Related Source : 
[[fork]], [[exec]], [[System Calls]]