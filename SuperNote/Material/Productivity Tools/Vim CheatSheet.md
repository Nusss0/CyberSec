---
tags:
  - Material
  - Productivity
  - Tools
---
> Vim is a modal text editor: keys do different things depending on the current mode. Most commands below run in Normal mode unless stated otherwise.

---
## Modes

> Vim has four core modes. `Esc` always returns you to Normal mode.

- **Normal** — Navigation and commands (enter with `Esc`)
- **Insert** — Typing text (enter with `i`, `a`, `o`)
- **Visual** — Selecting text (enter with `v`, `V`, `Ctrl+v`)
- **Command** — Running commands (enter with `:`)

---
## Core Concept: Operator + Motion

> Vim's power comes from combining an **operator** (what to do) with a **motion** (where to do it). Learn a few of each and they multiply into many commands.

Operators:

- `d` — Delete
- `c` — Change (delete, then start insert mode)
- `y` — Yank (copy)
- `>` / `<` — Indent / unindent one level

Combining examples:

- `dw` — Delete to next word
- `d$` — Delete to end of line
- `d0` — Delete to start of line
- `y$` — Copy to end of line
- `ciw` — Change inner word
- `diw` — Delete inner word

> `iw` is a **text object** ("inner word") — it targets the whole word regardless of where the cursor sits in it. See the Text Objects section below.

---
## Essentials

> The core movements, edits, and clipboard commands for day-to-day editing.

### Cursor Movement (Normal / Visual Mode)

- `h` `j` `k` `l` — Left, down, up, right
- `w` / `b` — Next / previous word
- `W` / `B` — Next / previous space-separated word
- `e` / `ge` — Next / previous end of word
- `0` / `$` — Start / end of line
- `^` — First non-blank character of line

### File Navigation

- `gg` / `G` — Top / bottom of file
- `:[num]` then `Enter` — Go to that line

### Insert Text

- `i` / `a` — Insert mode before / after cursor
- `I` / `A` — Insert mode at beginning / end of line
- `o` / `O` — Add blank line below / above current line
- `Esc` or `Ctrl+[` — Exit insert mode

### Delete

- `x` / `X` — Delete current / previous character
- `dw` — Delete word
- `dd` — Delete line
- `D` — Delete to end of line
- `c` — Delete, then start insert mode
- `cc` — Delete line, then start insert mode

### Marking Text (Visual Mode)

- `v` — Start visual mode
- `V` — Start linewise visual mode
- `Ctrl+v` — Start visual block mode
- `ggVG` — Select the entire file
- `Esc` or `Ctrl+[` — Exit visual mode

### Copy (Yank) & Paste

- `yy` — Yank (copy) a line
- `yw` — Yank a word
- `p` / `P` — Paste after / before cursor
- `d` / `c` — Copy the deleted text by default

Visual-mode copy: `v` to select, `y` to yank, `p` to paste.

### Search / Replace

- `/pattern` — Search forward for pattern
- `?pattern` — Search backward for pattern
- `n` / `N` — Repeat search in same / opposite direction
- `:%s/old/new/g` — Replace all `old` with `new` in file
- `:%s/old/new/gc` — Replace all with confirmation

### Exiting

- `:w` — Write (save), don't quit
- `:wq` — Write (save) and quit
- `:q` — Quit (fails if anything changed)
- `:q!` — Quit and discard changes

### General

- `u` — Undo
- `Ctrl+r` — Redo

[!note] If mapped in your config: `<leader>w` → save, `<leader>q` → quit. These only exist if you define them in your `.vimrc`; they are not Vim defaults.

---