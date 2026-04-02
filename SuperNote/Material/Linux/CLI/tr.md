## Definition
>*`(translate)`* is a Linux Command used to translate, delete, or squeeze characters from standard input.

---
## Tags 

#Material #CLI #LinuxBasic 

---
###  Usage : 
```bash
tr [Option] [SET1][SET2]
```

### Options : 
| Command         | Description                                                   |
| --------------- | ------------------------------------------------------------- |
| `-d`            | Delete character                                              |
| `[SET1] [SET2]` | Replace character from Set1 to Set2                           |
| `-s`            | Squeeze contigous repeated character  into a single character |
| `-cd`           | Keep only character in `[SET]` delete everything else.        |

### Others :
- Usually we use in this way : `echo "Hello World" | tr [Option] [SETS]`
- We could use `-` for range (e.g `a-z`).
- For further information please use manual page.

---
## Related Source : 