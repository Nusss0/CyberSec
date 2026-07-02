## Definition
>*`(link)`* is a Linux Command used to create links between files (symbolic/symlink or hard link).

---
## Tags 

#Material #LinuxBasic #CLI

---
###  Usage : 
```bash
ln [Option] [Target] [Linkname]
```

### Options : 
| Command   | Description                                                                                         |
| --------- | --------------------------------------------------------------------------------------------------- |
| `<blank>` | Create hard link                                                                                    |
| `-s`      | Create symbolic link                                                                                |
| `-f`      | Force - Remove existing Linkname                                                                    |
| `-n`      | Treat symlink to directory as normal file. Prevents creating links **inside** the target directory. |
| `-v`      | Shows what `ln` is doing. It print name of each linked file.                                        |
### Others :
- Symbolic link point to file path (can cross filesystem, can link directories)
- Hard link (Same filesystem only, cannot link directories)
- To simplify : Symbolic link -> shortcut to a file. Hard link -> One file with two names, so changing one will affect the others.
- For further information please use manual page.

---
## Related Source : 