## Definition
>a C function that reads environment variables.

---
## Tags 

#Material #C #stdlib #functions

--- 
## What are Environment Variables?
Environment variables are **key-value pairs** that the operating system stores for programs to use.

For example :
```shell
echo $PATH
echo $HOME
echo $USER
```
These are environment variable and each program could read that.

---
## How does `getenv()` works?
```c
   char *value = getenv("USER");
```
It will take a variable name as an input (**String**). It will search in system for the variable. It will return the value of the variable, otherwise it will return `Null`.

---


---
## Related Source : 
[[Environment Variables]]