## Definition
> *`(concatenate)`* is a Linux command used to display, combine, and create text by outputing their contents to standard output.

---
## Tags 

#Material #CLI #LinuxBasic

---
### Usage :
```bash
cat [Option] <FileName.txt>
```

### Options : 
| Command                          | Description                           |
| -------------------------------- | ------------------------------------- |
| `cat <file.txt>`                 | Display file contents                 |
| `-n`                             | Show line numbers                     |
| `-b`                             | Number non-blank lines only           |
| `-A`                             | Show all characters (tabs, line ends) |
| `-s`                             | Squeeze multiple blank lines          |
| `cat <file1> <file2>`            | Display contents of multiple files    |
| `cat > file.txt`                 | Create a new file from stdin          |
| `cat >> file.txt` <sup>[1]</sup> | Append to a file                      |
### Others :
- <sup>[1]</sup>To append file, we need a output first. This means we need to use pipeline. For example : `"Hello" | cat >> file.txt`.
 - For further information please use manual page.

---
## Related Source : 
[[pipeline]]