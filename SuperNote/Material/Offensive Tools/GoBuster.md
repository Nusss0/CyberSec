---
tags:
  - Tools
  - Networking
---
## Definition
>a versatile tool that allows for performing DNS, vhost, and directory brute-forcing. It has additional functionality, such as enumeration of public AWS S3 buckets. 
---
###  Usage : 
```shell
gobuster <mode> <options> <value> [<options> <value>]
```

### Modes :
| **Command** | **Description**                                                                                                                                                                                                       |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `dir`       | **directory/file enumeration mode**: GoBuster takes each name from the wordlist and requests it as a path against the target URL, reporting which directories and files exist based on the HTTP status code returned. |
| `dns`       | **subdomain brute-forcing mode**: brute-forces subdomains of a given domain.                                                                                                                                          |
| `vhost`     | virtual host brute-forcing mode.                                                                                                                                                                                      |

### Option : 
| Option | Value                                                                                                                           | Description               |
| ------ | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------- |
| `-u`   | webserver to scan `(e.g. http://10.10.10.121/)`                                                                                 | Specify target **URL**    |
| `-w`   | the file of names GoBuster tries one by one against the target<br>(`e.g. /usr/share/seclists/Discovery/Web-Content/common.txt`) | Specify Wordlist          |
| `-d`   | the target domain (e.g. `inlanefreight.com`)                                                                                    | Specify domain (dns mode) |

### Others :
- For further information please use manual page.

---
## Related Source : 
[[Web Enumeration]]