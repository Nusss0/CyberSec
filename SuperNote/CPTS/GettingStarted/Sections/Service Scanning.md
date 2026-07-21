---
tags:
  - Material
  - HTB
  - CPTS
---
> Service scanning identifies the operating system and any available services running on a target. A service is an application running on a computer that performs a useful function for other users or computers. We are interested in services that are misconfigured or vulnerable, so we can coerce them into performing unintended actions such as executing a command of our choosing.

---
## Ports and Services

> Computers are assigned an IP address to be uniquely identified on a network. Services running on them are assigned a port number to be made accessible.

Port numbers range from 1 to 65,535. The well-known ports 1 to 1,023 are reserved for privileged services.

> [!info] Port 0 is a reserved port in TCP/IP networking and is not used in TCP or UDP messages. If a service attempts to bind to port 0, it binds to the next available port above 1,024, because port 0 is treated as a "wild card" port.

To access a service remotely, we connect using the correct IP address and port number, using a language the service understands. Manually examining all 65,535 ports would be laborious, so scanning tools automate this. One of the most commonly used is **Nmap** (Network Mapper).

---
## Nmap

> Nmap (Network Mapper) is a scanning tool used to discover open ports and the services running on them.

The most basic scan targets an IP directly. Without additional options, Nmap scans only the 1,000 most common ports by default.

```shell
nmap 10.129.42.253
```

> [!info]- Basic scan output
> ```shell
> Starting Nmap 7.80 ( https://nmap.org ) at 2021-02-25 16:07 EST
> Nmap scan report for 10.129.42.253
> Host is up (0.11s latency).
> Not shown: 995 closed ports
> PORT    STATE SERVICE
> 21/tcp  open  ftp
> 22/tcp  open  ssh
> 80/tcp  open  http
> 139/tcp open  netbios-ssn
> 445/tcp open  microsoft-ds
>
> Nmap done: 1 IP address (1 host up) scanned in 2.19 seconds
> ```

Reading the output headings:

- **PORT** — the port number and protocol. Nmap runs a TCP scan by default unless a UDP scan is requested.
- **STATE** — confirms the port is open. Other states like `filtered` can appear if a firewall only allows access from specific addresses.
- **SERVICE** — the service name typically mapped to that port number. The default scan does not confirm what is actually listening; until Nmap interacts with the service, it could be something else.

> [!info] Some ports commonly indicate an OS. Port 3389 (Remote Desktop Services) is a strong indication of a Windows machine; port 22 (SSH) indicates Linux/Unix, though SSH can also run on Windows.

### Advanced Scan

Flags for a more detailed scan:

- `-sC` — run Nmap's default scripts for more detailed information.
- `-sV` — version scan: fingerprint services to identify the protocol, application name, and version (backed by a database of over 1,000 service signatures).
- `-p-` — scan all 65,535 TCP ports.

```shell
nmap -sV -sC -p- 10.129.42.253
```

> [!info]- Advanced scan output (-sV -sC -p-)
> ```shell
> PORT    STATE SERVICE     VERSION
> 21/tcp  open  ftp         vsftpd 3.0.3
> | ftp-anon: Anonymous FTP login allowed (FTP code 230)
> |_drwxr-xr-x    2 ftp      ftp          4096 Feb 25 19:25 pub
> 22/tcp  open  ssh         OpenSSH 8.2p1 Ubuntu 4ubuntu0.1 (Ubuntu Linux; protocol 2.0)
> 80/tcp  open  http        Apache httpd 2.4.41 ((Ubuntu))
> |_http-server-header: Apache/2.4.41 (Ubuntu)
> |_http-title: PHP 7.4.3 - phpinfo()
> 139/tcp open  netbios-ssn Samba smbd 4.6.2
> 445/tcp open  netbios-ssn Samba smbd 4.6.2
> Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
> ```

The **VERSION** heading reports the service version and, where possible, the operating system. The `-sC` and `-sV` options increase scan duration because they perform many more checks than a simple TCP handshake, and scanning all 65,535 ports takes far longer than 1,000.

Application versions can help reveal the OS version. For OpenSSH `8.2p1 Ubuntu 4ubuntu0.1`, reformatting to the Ubuntu package changelog format (`1:8.2p1-4ubuntu0.1`) and searching reveals it is included in Ubuntu Focal Fossa 20.04 (released April 23, 2020).

> [!caution] This cross-referencing technique is not entirely reliable, as it is possible to install more recent application packages on an older OS version.

The `-sC` script scan also reports server headers (`http-server-header`) and the page title (`http-title`). A title of `PHP 7.4.3 - phpinfo()` indicates a PHPInfo file, often manually created to confirm PHP is installed, and reveals the PHP version — worth noting if vulnerable.

### Nmap Scripts

`-sC` runs many useful default scripts, but sometimes a specific script is required. For example, auditing a Citrix installation for CVE-2019-19781.

```shell
locate scripts/citrix
```

Syntax for running a specific script:

```shell
nmap --script <script name> -p<port> <host>
```

> [!tip] Check out the Network Enumeration with Nmap module for a more detailed study of the tool.

---
## Attacking Network Services

### Banner Grabbing

> [!info] **Banner Grabbing** is a technique to quickly fingerprint a service. A service often identifies itself by displaying a banner once a connection is initiated.

Nmap attempts to grab banners with `nmap -sV --script=banner <target>`. It can also be done manually with Netcat.

```shell
nc -nv 10.129.42.253 21
```

This reveals the vsFTPd version on the server is 3.0.3. Automating with Nmap's scripting engine across a range:

```shell
nmap -sV --script=banner -p21 10.10.10.0/24
```

---
## FTP

> FTP is a standard protocol worth gaining familiarity with, as this service can often contain interesting data.

A scan of the default FTP port (21) reveals the vsftpd 3.0.3 installation, that anonymous authentication is enabled, and that a `pub` directory is available.

```shell
nmap -sC -sV -p21 10.129.42.253
```

Connect using the `ftp` command-line utility:

```shell
ftp -p 10.129.42.253
```

> [!info]- FTP session (anonymous login and file download)
> ```shell
> Name (10.129.42.253:user): anonymous
> 230 Login successful.
>
> ftp> ls
> drwxr-xr-x    2 ftp      ftp          4096 Feb 25 19:25 pub
>
> ftp> cd pub
> 250 Directory successfully changed.
>
> ftp> ls
> -rw-r--r--    1 ftp      ftp            18 Feb 25 19:25 login.txt
>
> ftp> get login.txt
> 226 Transfer complete.
>
> ftp> exit
> 221 Goodbye.
> ```

FTP supports common commands such as `cd` and `ls`, and allows downloading files with `get`. Inspecting the downloaded `login.txt` reveals credentials that could further access to the system.

```shell
cat login.txt

admin:ftp@dmin123
```

---
## SMB

> SMB (Server Message Block) is a prevalent protocol on Windows machines that provides many vectors for vertical and lateral movement.

Sensitive data, including credentials, can be in network file shares, and some SMB versions may be vulnerable to RCE exploits such as EternalBlue. Nmap has many scripts for enumerating SMB, such as `smb-os-discovery.nse`, which extracts the reported OS version.

```shell
nmap --script smb-os-discovery.nse -p445 10.10.10.40
```

> [!info]- smb-os-discovery output (legacy Windows 7 host)
> ```shell
> | smb-os-discovery:
> |   OS: Windows 7 Professional 7601 Service Pack 1 (Windows 7 Professional 6.1)
> |   Computer name: CEO-PC
> |   Workgroup: WORKGROUP
> |_  System time: 2020-12-27T00:59:46+00:00
> ```

A legacy Windows 7 host could be further enumerated to confirm if it is vulnerable to EternalBlue; the Metasploit Framework has modules to validate and exploit it. Scanning the module target reveals a Linux kernel, Samba 4.6.2, and hostname GS-SVCSCAN.

```shell
nmap -A -p445 10.129.42.253
```

### Shares

> SMB allows users and administrators to share folders and make them accessible remotely. These shares often contain files with sensitive information such as passwords.

`smbclient` can enumerate and interact with SMB shares. The `-L` flag lists available shares; `-N` suppresses the password prompt.

```shell
smbclient -N -L \\\\10.129.42.253
```

This reveals the non-default share `users`. Connecting as the guest user returns `NT_STATUS_ACCESS_DENIED`, indicating guest access is not permitted. Connecting with credentials for user bob (`bob:Welcome1`):

```shell
smbclient -U bob \\\\10.129.42.253\\users
```

> [!info]- smbclient session (authenticated, file download)
> ```shell
> smb: \> ls
>   bob                                 D        0  Thu Feb 25 16:42:23 2021
>
> smb: \> cd bob
>
> smb: \bob\> ls
>   passwords.txt                       N      156  Thu Feb 25 16:42:23 2021
>
> smb: \bob\> get passwords.txt
> ```

This gains access to the `users` share and the interesting file `passwords.txt`, downloaded with `get`.

---
## SNMP

> SNMP community strings provide information and statistics about a router or device. The manufacturer default community strings of `public` and `private` are often left unchanged.

In SNMP versions 1 and 2c, access is controlled using a plaintext community string; if the name is known, access is gained. Encryption and authentication were only added in version 3. Examining process parameters might reveal credentials passed on the command line (reusable elsewhere given password reuse), along with routing information, services bound to additional interfaces, and installed software versions.

```shell
snmpwalk -v 2c -c public 10.129.42.253 1.3.6.1.2.1.1.5.0
```

The `private` community string times out (no response). The tool `onesixtyone` can brute force community string names using a dictionary file such as `dict.txt`.

```shell
onesixtyone -c dict.txt 10.129.42.254
```

---
## Conclusion

> Service scanning and enumeration is a vast subject. The aspects covered here apply to many networks, including HTB machines.

---
## Related Source

[[Nmap]], [[FTP]], [[SMB]]