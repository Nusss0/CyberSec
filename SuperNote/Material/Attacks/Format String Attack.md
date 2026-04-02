## Introduction 
>The Format String exploit occurs when the submitted data of an input string is evaluated as a command by the application. In this way, the attacker could execute code, read the stack, or cause a segmentation fault in the running application, causing new behaviors that could compromise the security or the stability of the system.


To understand the attack, it’s necessary to understand the components that constitute it.
-  **Format Function** is an ANSI C conversion function, like printf, fprintf, which converts a primitive variable of the programming language into a human-readable string representation.
- **The Format String** is the argument of the Format Function and is an ASCII Z string which contains text and format parameters, like: printf (“The magic number is: %d\n”, 1911);
- **The Format String Parameter**, like %x %s defines the type of conversion of the format function.
---
## Format Functions

| Format function | Description                                       |
| --------------- | ------------------------------------------------- |
| fprint          | Writes the printf to a file                       |
| printf          | Output a formatted string                         |
| sprintf         | Prints into a string                              |
| snprintf        | Prints into a string checking the length          |
| vfprintf        | Prints the a va_arg structure to a file           |
| vprintf         | Prints the va_arg structure to stdout             |
| vsprintf        | Prints the va_arg to a string                     |
| vsnprintf       | Prints the va_arg to a string checking the length |
Below are some format parameters which can be used and their consequences:
- ”%x” Read data from the stack
- ”%s” Read character strings from the process’ memory
- ”%n” Write an integer to locations in the process’ memory

***Notes*** : To discover whether the application is vulnerable to this type of attack, it’s necessary to verify if the format function accepts and parses the format string parameters shown in table 2.

--- 
## Common parameter used in a Format String Attack

|Parameters|Output|Passed as|
|---|---|---|
|%%|% character (literal)|Reference|
|%p|External representation of a pointer to void|Reference|
|%d|Decimal|Value|
|%c|Character||
|%u|Unsigned decimal|Value|
|%x|Hexadecimal|Value|
|%s|String|Reference|
|%n|Writes the number of characters into a pointer|Reference|

***Tips :*** 
- We can use **Number** in front of the specifier for special use. 
- `%500x` This will force the output to become 500 length.
- `%4$n` This will let the `n` to write number on the **4th** args of **Argument Pointers**
- Check for [[printf()]] to view more informations.

---
## Codes Example
### Safe Code
```c
printf("%s", argv[1]);
```
if we compile it : `./example "Hello World %s%s%s%s%s%s"`
The printf in the first line will not interpret the `%s%s%s%s%s%s` in the input string, and the output will be : "Hello World %s%s%s%s%s%s".

### Vulnerable Code
```c
printf(argv[1]);
```
If we compile it :` ./example "Hello World %s%s%s%s%s%s"`
The printf will interpret the "%s%s%s%s%s%s" in input string as a reference to string pointers.

---
## Related Source 
- Sources : https://owasp.org/www-community/attacks/Format_string_attack
- [[printf()]]
