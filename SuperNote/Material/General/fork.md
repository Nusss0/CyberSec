## Definition
>*(fork)* is a function to duplicates the calling process. It will create a child process which is as same as the parent process.

---
## Tags 

#Material #GeneralConcepts #OperatingSystem 

---
### Concepts : 
- A running process could clone itself by using `fork()` system call.
- The process will continue from the EXACT position where `fork()` is called.
- The new child process also gets a new PID.

### Simple Example :
```c
int main() {
    int x = 10;
    
    printf("Before fork: x = %d, PID = %d\n", x, getpid());
    
    int pid = fork();  // Creates copy HERE
    
    if (pid == 0) { // Check if child process exist
        // Child process
        x = 20;
        printf("Child: x = %d, PID = %d\n", x, getpid());
    } else {
        // Parent process
        x = 30;
        printf("Parent: x = %d, PID = %d\n", x, getpid());
    }
    
    return 0;
}
```

**Output:**
```shell
Before fork: x = 10, PID = 1234
Parent: x = 30, PID = 1234
Child: x = 20, PID = 5678
```

In this example, we could see there are only ONE `Before fork` and after `fork()` called, the remaining process run twice.

### Others :
- We could take a benefit from this feature, like parallel work. So the child and parent can do different task simultaneously.

---
## Related Source : 
[[process]], 