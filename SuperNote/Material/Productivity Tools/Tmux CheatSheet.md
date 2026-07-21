---
tags:
  - Material
  - Productivity
  - Tools
---
> tmux is a terminal multiplexer: it lets one terminal hold multiple sessions, windows, and panes. The **prefix** (`Ctrl+b` by default) is pressed before any in-tmux keybinding — press it, release, then press the command key. Commands starting with `tmux` are run at the shell, not with the prefix.

---
## Sessions

> A session is a single collection of windows, persistent in the background even after you detach.

Shell commands:

- `tmux new` / `tmux new-session` — Start a new session
- `tmux new -s mysession` — Start a new session named `mysession`
- `tmux new-session -A -s mysession` — Start a new session, or attach if `mysession` already exists
- `tmux kill-session -t mysession` — Kill session `mysession`
- `tmux kill-session -a` — Kill all sessions but the current one
- `tmux kill-session -a -t mysession` — Kill all sessions but `mysession`
- `tmux ls` / `tmux list-sessions` — Show all sessions
- `tmux a` / `tmux attach` — Attach to last session
- `tmux a -t mysession` — Attach to session `mysession`

Prefix keybindings:

- `Ctrl+b` `$` — Rename current session
- `Ctrl+b` `d` — Detach from session
- `Ctrl+b` `D` — Choose a client to detach (maximize by detaching others)
- `Ctrl+b` `s` — Session and window preview (interactive list)
- `Ctrl+b` `(` — Move to previous session
- `Ctrl+b` `)` — Move to next session

---
## Windows

> A window is one full-screen workspace within a session, like a tab. Windows are numbered along the status bar at the bottom.

- `tmux new -s mysession -n mywindow` — Start session `mysession` with window `mywindow` (shell command)
- `Ctrl+b` `c` — Create window
- `Ctrl+b` `,` — Rename current window
- `Ctrl+b` `&` — Close current window
- `Ctrl+b` `w` — List windows
- `Ctrl+b` `p` — Previous window
- `Ctrl+b` `n` — Next window
- `Ctrl+b` `[0-9]` — Switch to window by number
- `Ctrl+b` `l` — Toggle last active window
- `Ctrl+b` `<` — Open window actions menu

Window management commands (run in command mode via `Ctrl+b` `:`):

- `swap-window -s 2 -t 1` — Swap window 2 (source) with window 1 (destination)
- `swap-window -t -1` — Move current window one position left
- `move-window -s src_ses:win -t target_ses:win` — Move window from source to target (e.g., `movew -s foo:0 -t bar:9`)
- `move-window -s src_session:src_window` — Reposition window in the current session (e.g., `movew -s 0:9`)
- `move-window -r` — Renumber windows to remove gaps in the sequence

---
## Panes

> A pane is a subdivision within a single window. One window can hold many panes side by side or stacked.

- `Ctrl+b` `;` — Toggle last active pane
- `Ctrl+b` `%` — Split into left/right panes (`split-window -h`)
- `Ctrl+b` `"` — Split into top/bottom panes (`split-window -v`)
- `Ctrl+b` `{` — Move current pane left
- `Ctrl+b` `}` — Move current pane right
- `Ctrl+b` `[arrow]` — Switch to the pane in that direction
- `Ctrl+b` `Space` — Toggle between pane layouts
- `Ctrl+b` `o` — Switch to next pane
- `Ctrl+b` `q` — Show pane numbers
- `Ctrl+b` `q` `[0-9]` — Select pane by number
- `Ctrl+b` `z` — Toggle pane zoom (fullscreen the current pane)
- `Ctrl+b` `!` — Convert pane into its own window
- `Ctrl+b` `Ctrl+[arrow]` — Resize current pane (holding the second key repeats)
- `Ctrl+b` `x` — Close current pane
- `Ctrl+b` `<` — Open pane actions menu

Pane commands (run in command mode via `Ctrl+b` `:`):

- `join-pane -s 2 -t 1` — Merge window 2 into window 1 as a pane
- `join-pane -s 2.1 -t 1.0` — Move pane 1 of window 2 to after pane 0 of window 1
- `setw synchronize-panes` — Toggle synchronize-panes (send typed input to all panes at once)

---
## Copy Mode

> Copy mode lets you scroll back through output and select/copy text with the keyboard.

- `setw -g mode-keys vi` — Use vi keys in the buffer (command mode)
- `Ctrl+b` `[` — Enter copy mode
- `Ctrl+b` `PgUp` — Enter copy mode and scroll one page up
- `q` — Quit copy mode

[!info]- Navigation inside copy mode (vi keys)
- `g` — Go to top line
- `G` — Go to bottom line
- `Ctrl+u` / `Ctrl+d` — Scroll up / down
- `h` `j` `k` `l` — Move cursor left / down / up / right
- `w` / `b` — Move cursor forward / backward one word
- `/` — Search forward
- `?` — Search backward
- `n` / `N` — Next / previous keyword occurrence

Selecting and copying:

- `Space` — Start selection
- `Esc` — Clear selection
- `Enter` — Copy selection
- `Ctrl+b` `]` — Paste contents of buffer_0

Buffer commands (run in command mode via `Ctrl+b` `:`):

- `show-buffer` — Display buffer_0 contents
- `capture-pane` — Copy the entire visible pane contents to a buffer
- `list-buffers` — Show all buffers
- `choose-buffer` — Show all buffers and paste the selected one
- `save-buffer buf.txt` — Save buffer contents to `buf.txt`
- `delete-buffer -b 1` — Delete buffer_1

---
## Misc

- `Ctrl+b` `:` — Enter command mode

Configuration and info commands:

- `set -g OPTION` — Set `OPTION` for all sessions
- `setw -g OPTION` — Set `OPTION` for all windows
- `set mouse on` — Enable mouse mode
- `tmux -V` — Print tmux version (shell command)

---
## Help

- `tmux list-keys` / `list-keys` — List key bindings (shortcuts)
- `tmux info` — Show every session, window, pane, etc.
