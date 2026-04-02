## Modes
- **Normal**: navigation & commands (`Esc`)
- **Insert**: typing text (`i`, `a`, `o`)
- **Visual**: select text (`v`, `V`, `Ctrl+v`)
- **Command**: run commands (`:`)

---
### Word & Line Movement
- `w` → next word
- `b` → previous word
- `e` → end of word
- `0` → start of line
- `^` → first non-space
- `$` → end of line
---
### File Navigation
- `gg` → top of file
- `G`  → bottom of file

---

## Insert Text
- `i` → insert before cursor
- `a` → insert after cursor
- `o` → new line below
- `O` → new line above

---

## Delete
- `x`  → delete character
- `dw` → delete word
- `dd` → delete line
- `D`  → delete to end of line

Delete + motion:
- `d$` → delete to end of line
- `d0` → delete to start of line

---

## Copy (Yank) & Paste
- `yy` → copy line
- `yw` → copy word
- `p`  → paste after cursor
- `P`  → paste before cursor

Visual copy:
- `v` → select
- `y` → yank
- `p` → paste

---

## Undo / Redo
- `u` → undo
- `Ctrl+r` → redo

---

## Search
- `/word` → search forward
- `n` → next match
- `N` → previous match

---

## Save & Quit
- `:w`  → save
- `:q`  → quit
- `:wq` → save & quit
- `:q!` → quit without saving

Custom (if mapped):
- `<leader>w` → save
- `<leader>q` → quit

---

## Select All
- `ggVG` → select entire file

---

## Vim Core Concept
**Operator + Motion**

Examples:
- `dw`  → delete word
- `ciw` → change inner word
- `y$`  → copy to end of line
- `diw` → delete inner word
