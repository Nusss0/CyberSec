## Definition
> *`(Set User ID)`* is a special permission in Linux that allows a program to run with **File Owner Privileges**.

---
## Tags 

#Material #LinuxBasic 

---
### How to check SetUID file ?
So, the easiest way is by using `file` command. We could see the output below as example.
```shell
bandit20-do: setuid ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, BuildID[sha1]=38f1351d0068ccbbace0e437f34859de85e63025, for GNU/Linux 3.2.0, not stripped
```
bandit20-do is a file name, and the type is SetUID. Another way to recognize SetUID file is by using the most simple command `ls -l`. See the output below :
```shell
-rwsr-x--- 1 bandit20 bandit19 14884 Oct 14 09:26 bandit20-do
```
We could see **`s`** component instead of **`x`**. With this, we know that `bandit20-do` is a SetUID file.

### What is SetUID file?
SetUID file can grant us the power of the owner. For example, there are a file name *`bandit20-do`*, and we could see that the owner is `bandit20`. When we (`bandit19`) try to run the file/program, the program runs with `bandit20` power.

In conclusion, whoever run a `setuid file`, it could run the file/program as the owner.

To ease our understanding, we try to run *`bandit20-do`* file, and this is the output :
```shell
bandit19@bandit:~$ ./bandit20-do
Run a command as another user.
Example: ./bandit20-do whoami
```
If we see the result above, we could see that, the file `bandit20-do` will take our **Input** as a Command with user `bandit20` privileges. To prove that, we could try :
```shell
bandit19@bandit:~$ ./bandit20-do whoami
bandit20
```
And it return `bandit20` instead of `bandit19`. This means whatever Command we give, we could run it as user `bandit20`.

---
## Related Source : 
[[file]]