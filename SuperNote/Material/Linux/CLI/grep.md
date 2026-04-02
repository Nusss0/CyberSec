## Definition
>*(grep)* is a Linux Command used to search for patterns in each File / Standard Output.

---
## Tags 

#Material #LinuxBasic #CLI

---
###  Usage : 
```bash
grep [Option] "Pattern" <FileName.txt>
```
### Options : 
| Command                        | Description                        |
| ------------------------------ | ---------------------------------- |
| `<blank>`                      | Display lines that contain Pattern |
| `-i`                           | Case insensitive search            |
| `-v`                           | Invert match (exclude pattern)     |
| `-n`                           | Show line number                   |
| `-r <Directory>`<sup>[1]</sup> | Recursive search                   |
| `-w`                           | Match whole word only              |
| `-c`                           | Count matching lines               |
### Others :
- <sup>[1]</sup> Recursively search through all subfolder. 
- "Pattern" is a suffix search not whole word.
- Use `.` instead of `<FileName.txt` to search all file in current folder.
- For further information please use manual page.


---
## Related Source : 