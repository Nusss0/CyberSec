---
tags:
  - Material
  - HTB
  - CPTS
  - Tools
---
> Tools such as SSH, Netcat, Tmux, and Vim are essential and used daily by most information security professionals. They are not intended to be penetration testing tools, but they are critical to the penetration testing process, so they must be mastered.

---
## SSH

> Secure Shell (SSH) is a network protocol that runs on port 22 by default and provides users such as system administrators a secure way to access a computer remotely.

SSH can be configured with password authentication or passwordless public-key authentication using an SSH public/private key pair. It can be used to remotely access systems on the same network, over the internet, facilitate connections to resources in other networks using port forwarding/proxying, and upload/download files to and from remote systems.

SSH uses a client-server model, connecting a user running an SSH client application (such as OpenSSH) to an SSH server. While attacking a box or during a real-world assessment, cleartext credentials or an SSH private key are often obtained and can be leveraged to connect directly to a system via SSH. An SSH connection is typically much more stable than a reverse shell connection and can often be used as a "jump host" to enumerate and attack other hosts in the network, transfer tools, and set up persistence.

>[!info]- Login with credentials
>
>```shell
nusss@htb[/htb]$ ssh Bob@10.10.10.10
>
>Bob@remotehost's password: *********
>
>Bob@remotehost#
>```
>Login uses the username @ the remote server IP.

It is also possible to read local private keys on a compromised system or add our public key to gain SSH access to a specific user. SSH also provides a way to map local ports on the remote machine to our localhost.

---
## Netcat

> Netcat (`ncat`, or `nc`) is a network utility for interacting with TCP/UDP ports. Its primary usage is for connecting to shells.

In addition to shells, netcat can connect to any listening port and interact with the service running on that port. For example, SSH handles connections over port 22. We can connect to TCP port 22 with netcat.

> [!info]- Banner grabbing with netcat
> ```shellsession
> nusss@htb[/htb]$ netcat 10.10.10.10 22
>
> SSH-2.0-OpenSSH_8.4p1 Debian-3
> ```
> Port 22 sent us its banner, stating that SSH is running on it.

>[!info] **Banner Grabbing** is this technique of reading the banner a service sends; it helps identify what service is running on a particular port.

Netcat comes pre-installed in most Linux distributions and can also be downloaded for Windows. A PowerShell alternative called **PowerCat** also exists. Netcat can also be used to transfer files between machines.

---
## Socat

> Socat is a network utility similar to netcat, with a few features netcat does not support, like forwarding ports and connecting to serial devices.

Socat can also be used to upgrade a shell to a fully interactive TTY. It is a handy utility that should be part of every penetration tester's toolkit. A standalone Socat binary can be transferred to a system after obtaining remote code execution to get a more stable reverse shell connection.

---
## Tmux

> Terminal multiplexers, like tmux or Screen, expand a standard Linux terminal's features, such as having multiple windows within one terminal and jumping between them. tmux is the more common of the two.

Install with `sudo apt install tmux -y`. tmux is a powerful tool and can be used for many things, including logging, which is very important during any technical engagement.

See: [[Tmux CheatSheet]]

---
## Vim

> Vim is a text editor for writing code or editing text files on Linux systems. It relies entirely on the keyboard, so the mouse is not needed, which increases productivity and efficiency once mastered.

Vim or Vi is usually found installed on compromised Linux systems, so learning it allows editing files even on remote systems. It also supports extensions and plugins that significantly extend its usage. Opening a file: `vim /etc/hosts`. Files open in read-only normal mode; hit `i` to enter insert mode (shown by `-- INSERT --`), and `Esc` to return to normal mode.

See: [[Vim CheatSheet]]
