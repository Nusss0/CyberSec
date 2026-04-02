## Definition
>key-value pairs that the operating system stores for programs to use.

---
## Tags 

#Material #GeneralConcepts #OperatingSystem

---
## Example :
```shell
echo $PATH
echo $HOME
echo $USER
```
These are environment variable and each program could read that.

---
## Creating Custom Environment Variables :

```bash
export MYVAR="Hello World"
echo $MYVAR          # prints: Hello World
```

We could access it through C program using `getenv()` :
```c
char *value = getenv("MYVAR");
printf("%s\n", value);  // prints: Hello World
```

---


---
## Related Source : 
[[getenv()]]