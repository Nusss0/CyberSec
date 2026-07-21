---
tags:
  - Material
  - HTB
  - Networking
---
---

> When performing service scanning, we will often run into web servers running on ports 80 and 443. Webservers host web applications (sometimes more than one) which often provide a considerable attack surface and a very high-value target during a penetration test.

> [!important]
> Proper web enumeration is critical, especially when an organization is not exposing many services or those services are appropriately patched.

---
## Gobuster

> After discovering a web application, it is always worth checking to see if we can uncover any hidden files or directories on the webserver that are not intended for public access. Sometimes we will find hidden functionality or pages/directories exposing sensitive data that can be leveraged to access the web application or even remote code execution on the web server itself.

GoBuster is a versatile tool that allows for performing DNS, vhost, and directory brute-forcing. It has additional functionality, such as enumeration of public AWS S3 buckets. For this section we are interested in the directory (and file) brute-forcing mode, specified with the `dir` switch.

### Directory/File Enumeration

Run a simple scan using the dirb `common.txt` wordlist:

```shell
gobuster dir -u http://10.10.10.121/ -w /usr/share/seclists/Discovery/Web-Content/common.txt
```

> [!info]- HTTP status codes seen in output
> - `200` — request was successful
> - `301` — redirect (not a failure case)
> - `403` — forbidden; we are not allowed to access the resource

The scan identifies a WordPress installation at `/wordpress`.

> [!note]
> WordPress is the most commonly used CMS (Content Management System) and has an enormous potential attack surface. If found still in setup mode, it allows gaining remote code execution (RCE) on the server.

---
## DNS Subdomain Enumeration

> There also may be essential resources hosted on subdomains, such as admin panels or applications with additional functionality that could be exploited.

GoBuster enumerates subdomains of a given domain using the `dns` mode. First, clone the SecLists repo, which contains many useful lists for fuzzing and exploitation:

```shell
git clone https://github.com/danielmiessler/SecLists
```

```shell
sudo apt install seclists -y
```

> [!caution]
> Add a DNS server such as `1.1.1.1` to `/etc/resolv.conf` before running.

```shell
gobuster dns -d inlanefreight.com -w /usr/share/SecLists/Discovery/DNS/namelist.txt
```

This reveals subdomains (e.g. `blog`, `customer`, `my`, `ns1`–`ns3`) that could be examined further.

---
## Web Enumeration Tips

A few additional tips that help complete machines on HTB and in the real world.

### Banner Grabbing / Web Server Headers

> Web server headers provide a good picture of what is hosted on a web server. They can reveal the specific application framework in use, the authentication options, and whether the server is missing essential security options or has been misconfigured.

Use cURL to retrieve server header information:

```shell
curl -IL https://www.inlanefreight.com
```

> [!info]- EyeWitness
> Another handy tool. It takes screenshots of target web applications, fingerprints them, and identifies possible default credentials.

### Whatweb

> We can extract the version of web servers, supporting frameworks, and applications using the command-line tool `whatweb`. This information can help us pinpoint the technologies in use and begin to search for potential vulnerabilities.

```shell
whatweb 10.10.10.121
```

`whatweb` can also automate web application enumeration across a network:

```shell
whatweb --no-errors 10.10.10.0/24
```

### Certificates

> SSL/TLS certificates are another potentially valuable source of information if HTTPS is in use.

Viewing the certificate can reveal details such as the email address and company name, which could potentially be used to conduct a phishing attack if this is within the scope of an assessment.

### Robots.txt

> It is common for websites to contain a robots.txt file, whose purpose is to instruct search engine web crawlers such as Googlebot which resources can and cannot be accessed for indexing.

> [!note]
> The robots.txt file can provide valuable information such as the location of private files and admin pages, since disallowed entries point to resources the owner doesn't want indexed.

### Source Code

> It is also worth checking the source code for any web pages we come across. We can hit [CTRL + U] to bring up the source code window in a browser.

Source code can reveal developer comments containing sensitive data — for example, credentials for a test account that could be used to log in to the website.

---
## Related Source

-