---
tags:
  - CPTS
  - Material
  - HTB
  - Networking
  - Shell
---
> Penetration testing/hacking is an enormous field with countless technologies. The terms below are the most common ones encountered repeatedly and must be firmly grasped. This is not an exhaustive list, but is enough to get started with fundamental Modules and easy HTB boxes.

---

## What is a Shell?

> On a Linux system, the shell is a program that takes input from the user via the keyboard and passes these commands to the operating system to perform a specific function.

In the early days of computing, the shell was the only interface available for interacting with systems. Since then, many more operating system types and versions have emerged along with the graphic user interface (GUI) to complement command-line interfaces (shell), such as the Linux terminal, Windows command-line (cmd.exe), and Windows PowerShell.

> [!info] Bash
> Most Linux systems use **Bash** (Bourne Again Shell) as a shell program to interact with the operating system. Bash is an enhanced version of `sh`, the Unix systems' original shell program. Other shells include Zsh, Tcsh, Ksh, and Fish shell.

"Getting a shell" on a box (system) means the target host has been exploited, and shell-level access (typically bash or sh) has been obtained, allowing commands to be run interactively as if logged in to the host. A shell may be obtained by exploiting a web application or network/service vulnerability, or by obtaining credentials and logging into the target host remotely.

There are three main types of shell connections:

- **Reverse shell** — Initiates a connection back to a "listener" on our attack box.
- **Bind shell** — "Binds" to a specific port on the target host and waits for a connection from our attack box.
- **Web shell** — Runs operating system commands via the web browser, typically not interactive or semi-interactive. It can also be used to run single commands (i.e., leveraging a file upload vulnerability and uploading a PHP script to run a single command).

Each type of shell has its use case, and the helper program used to get a shell can be written in many languages (Python, Perl, Go, Bash, Java, awk, PHP, etc.). These can be small scripts or larger, more complex programs to facilitate a connection from the target host back to our attacking system.

---

## What is a Port?

> Ports are virtual points where network connections begin and end. They are software-based and managed by the host operating system.

A port can be thought of as a window or door on a house (the house being a remote system) — if left open or not locked correctly, unauthorized access can often be gained.

Ports are associated with a specific process or service and allow computers to differentiate between different traffic types (SSH traffic flows to a different port than web requests, even though the access requests are sent over the same network connection).

Each port is assigned a number, and many are standardized across all network-connected devices, though a service can be configured to run on a non-standard port. For example, HTTP messages typically go to port 80, while HTTPS messages go to port 443 unless configured otherwise. At a very high level, ports help computers understand how to handle the various types of data they receive.

There are two categories of ports:

> [!info] TCP (Transmission Control Protocol)
> Connection-oriented, meaning that a connection between a client and a server must be established before data can be sent. The server must be in a listening state awaiting connection requests from clients.

> [!info] UDP (User Datagram Protocol)
> Utilizes a connectionless communication model. There is no "handshake" and therefore introduces a certain amount of unreliability since there is no guarantee of data delivery. UDP is useful when error correction/checking is either not needed or is handled by the application itself. It is suitable for applications that run time-sensitive tasks, since dropping packets is faster than waiting for delayed packets due to retransmission.

There are 65,535 TCP ports and 65,535 different UDP ports, each denoted by a number.

> [!info]- Most well-known TCP and UDP ports
> - **20/21 (TCP)** — FTP
> - **22 (TCP)** — SSH
> - **23 (TCP)** — Telnet
> - **25 (TCP)** — SMTP
> - **80 (TCP)** — HTTP
> - **161 (TCP/UDP)** — SNMP
> - **389 (TCP/UDP)** — LDAP
> - **443 (TCP)** — SSL/TLS (HTTPS)
> - **445 (TCP)** — SMB
> - **3389 (TCP)** — RDP

> [!important] Memorize the common ports
> As pentesters, it is essential to have a firm grasp of many TCP and UDP ports and be able to recognize them from just their number quickly (i.e., port 21 is FTP, port 80 is HTTP, port 88 is Kerberos) without having to look it up. This comes with practice and repetition, and helps prioritize enumeration efforts and attacks more efficiently.

---

## What is a Web Server

> A web server is an application that runs on the back-end server, which handles all of the HTTP traffic from the client-side browser, routes it to the request's destination pages, and finally responds to the client-side browser.

Web servers usually run on TCP ports 80 or 443, and are responsible for connecting end-users to various parts of the web application, in addition to handling their various responses.

As web applications tend to be open for public interaction and facing the internet, they may lead to the back-end server being compromised if they suffer from any vulnerabilities. Web applications can provide a vast attack surface, making them a high-value target for attackers and pentesters.

> [!info] OWASP Top 10
> A standardized list of the top 10 web application vulnerabilities maintained by the Open Web Application Security Project (OWASP). This list is considered the top 10 most dangerous vulnerabilities and is not an exhaustive list of all possible web application vulnerabilities. Web application security assessment methodologies are often based around the OWASP Top 10 as a starting point for the top categories of flaws that an assessor should be checking for.

> [!info]- OWASP Top 10 (2021)
> 1. **Broken Access Control** — Restrictions are not appropriately implemented to prevent users from accessing other users' accounts, viewing sensitive data, accessing unauthorized functionality, modifying data, etc.
> 2. **Cryptographic Failures** — Failures related to cryptography which often lead to sensitive data exposure or system compromise.
> 3. **Injection** — User-supplied data is not validated, filtered, or sanitized by the application. Some examples are SQL injection, command injection, LDAP injection, etc.
> 4. **Insecure Design** — These issues happen when the application is not designed with security in mind.
> 5. **Security Misconfiguration** — Missing appropriate security hardening across any part of the application stack, insecure default configurations, open cloud storage, verbose error messages which disclose too much information.
> 6. **Vulnerable and Outdated Components** — Using components (both client-side and server-side) that are vulnerable, unsupported, or out of date.
> 7. **Identification and Authentication Failures** — Authentication-related attacks that target user's identity, authentication, and session management.
> 8. **Software and Data Integrity Failures** — Code and infrastructure that does not protect against integrity violations. An example is where an application relies upon plugins, libraries, or modules from untrusted sources, repositories, and content delivery networks (CDNs).
> 9. **Security Logging and Monitoring Failures** — This category helps detect, escalate, and respond to active breaches. Without logging and monitoring, breaches cannot be detected.
> 10. **Server-Side Request Forgery** — SSRF flaws occur whenever a web application is fetching a remote resource without validating the user-supplied URL. It allows an attacker to coerce the application to send a crafted request to an unexpected destination, even when protected by a firewall, VPN, or another type of network access control list (ACL).

---

