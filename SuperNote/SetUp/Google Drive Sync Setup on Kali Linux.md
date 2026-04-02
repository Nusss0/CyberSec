>A simple guide to sync Google Drive locally using rclone with auto-sync on Obsidian open/close.

---
## Tags 

#LinuxSetup 

---
## 1. Install rclone

```bash
sudo apt update
sudo apt install rclone fuse3
```

---

## 2. Configure rclone

```bash
rclone config
```

**Follow these prompts:**

| Prompt | Answer |
|--------|--------|
| `n/s/q>` | `n` (new remote) |
| `name>` | `GoogleDrive` |
| `Storage>` | `drive` (or number for Google Drive) |
| `client_id>` | Leave blank, press Enter |
| `client_secret>` | Leave blank, press Enter |
| `scope>` | `1` (full access) |
| `root_folder_id>` | Leave blank, press Enter |
| `service_account_file>` | Leave blank, press Enter |
| `Edit advanced config?` | `n` |
| `Use auto config?` | `y` |

Browser opens → Login to Google → Grant permission → Return to terminal.

| Prompt | Answer |
|--------|--------|
| `Configure as team drive?` | `n` |
| `y/e/d>` | `y` (confirm) |
| `e/n/d/r/c/s/q>` | `q` (quit config) |

**Verify:**

```bash
rclone listremotes
```

Should show: `GoogleDrive:`

---

## 3. Initial Sync

```bash
mkdir -p ~/GoogleDrive
rclone bisync GoogleDrive: ~/GoogleDrive --resync
```

> `--resync` is required only on first run to establish baseline.

---

## 4. Manual Sync Alias (Optional)

Add to `~/.zshrc` (or `~/.bashrc`):

```bash
echo "alias gdrivesync='rclone bisync GoogleDrive: ~/GoogleDrive'" >> ~/.zshrc
source ~/.zshrc
```

**Usage:**

```bash
gdrivesync
```

---

## 5. Auto-Sync Every 5 Minutes

### Create Service File

```bash
vim ~/.config/systemd/user/rclone-bisync.service
```

```ini
[Unit]
Description=Rclone bisync Google Drive
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=/usr/bin/rclone bisync GoogleDrive: %h/GoogleDrive

[Install]
WantedBy=default.target
```

### Create Timer File

```bash
vim ~/.config/systemd/user/rclone-bisync.timer
```

```ini
[Unit]
Description=Run rclone bisync every 5 minutes

[Timer]
OnBootSec=1min
OnUnitActiveSec=5min
Persistent=true

[Install]
WantedBy=timers.target
```

### Enable Timer

```bash
systemctl --user daemon-reload
systemctl --user enable rclone-bisync.timer
systemctl --user start rclone-bisync.timer
sudo loginctl enable-linger $USER
```

### Verify

```bash
systemctl --user status rclone-bisync.timer
systemctl --user list-timers
```

---

## 6. Obsidian Sync Wrapper

Automatically sync when opening and closing Obsidian.  *Make sure the path of the Obsidian AppImage was same as below*

### Create Wrapper Script

```bash
vim ~/.local/bin/obsidian-sync
```

```bash
#!/bin/bash

# Notify start sync
notify-send "Google Drive" "Syncing before Obsidian opens..." -i sync

# Sync before opening
rclone bisync GoogleDrive: ~/GoogleDrive

# Notify sync complete
notify-send "Google Drive" "Sync complete. Opening Obsidian." -i emblem-ok

# Launch Obsidian (waits until closed) AppImage Location
~/.local/bin/Obsidian.AppImage "$@"

# Notify closing sync
notify-send "Google Drive" "Syncing after Obsidian closes..." -i sync

# Sync after closing
rclone bisync GoogleDrive: ~/GoogleDrive

# Notify done
notify-send "Google Drive" "Sync complete." -i emblem-ok
```

```bash
chmod +x ~/.local/bin/obsidian-sync
```

### Update Desktop Entry

```bash
vim ~/.local/share/applications/obsidian.desktop
```

Change `Exec=` line to:

```
Exec=/home/nus/.local/bin/obsidian-sync
```

Refresh:

```bash
update-desktop-database ~/.local/share/applications/
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Manual sync | `gdrivesync` |
| Check timer status | `systemctl --user status rclone-bisync.timer` |
| View next sync time | `systemctl --user list-timers` |
| Force immediate sync | `systemctl --user start rclone-bisync.service` |
| Stop auto-sync | `systemctl --user stop rclone-bisync.timer` |
| Disable auto-sync | `systemctl --user disable rclone-bisync.timer` |

---

## Troubleshooting

**Sync fails after first run:**
```bash
rclone bisync GoogleDrive: ~/GoogleDrive --resync
```

**Check rclone remotes:**
```bash
rclone listremotes
```

**View sync logs:**
```bash
journalctl --user -u rclone-bisync.service
```

**Test rclone connection:**
```bash
rclone ls GoogleDrive: --max-depth 1
```