> Callouts (a.k.a. admonitions) are colored, icon-labeled blocks built into Obsidian. Syntax is a blockquote whose first line is `> [!type]`, with content on the `>` lines below it.

---

## Quick Reference

|Type|Aliases|
|---|---|
|`note`|—|
|`info`|—|
|`tip`|`hint`, `important`|
|`todo`|—|
|`question`|`help`, `faq`|
|`success`|`check`, `done`|
|`warning`|`caution`, `attention`|
|`failure`|`fail`, `missing`|
|`danger`|`error`|
|`bug`|—|
|`example`|—|
|`quote`|`cite`|
|`abstract`|`summary`, `tldr`|

Each type has its own icon and color. Aliases render identically to their base type (e.g. `[!important]` = `[!tip]`).

---

## Basic Syntax

```markdown
> [!note]
> This is the content of the callout.
> It can span multiple lines.
```

Every content line must start with `>`.

---

## Custom Titles

Text placed after the type replaces the default header.

> [!warning] Don't test out of scope
> Written scope is your shield.

An empty title (type followed by a blank) hides the header text but keeps the icon.

---

## Collapsible Callouts

Add `+` (starts expanded) or `-` (starts folded) directly after the type.

> [!info]- Country law reference (click to expand)
> Big table or reference material that stays hidden until needed.


- `+` → collapsible, open by default
- `-` → collapsible, folded by default

Best use: reference material you look up on demand rather than read every time.

---

## Nesting

Stack `>` characters to place callouts inside callouts.


> [!example] Lateral movement chain
> > [!note] Step 1
> > Foothold on web server.
> >
> > > [!note] Step 2
> > > Escalate privileges.


---
## All Types — Placeholder Gallery

Live, ready-to-use blocks (these render in Obsidian). Replace the title and body text with your own.

> [!note] Title placeholder Body placeholder.

> [!info] Title placeholder Body placeholder.

> [!tip] Title placeholder Body placeholder.

> [!todo] Title placeholder Body placeholder.

> [!question] Title placeholder Body placeholder.

> [!success] Title placeholder Body placeholder.

> [!warning] Title placeholder Body placeholder.

> [!failure] Title placeholder Body placeholder.

> [!danger] Title placeholder Body placeholder.

> [!bug] Title placeholder Body placeholder.

> [!example] Title placeholder Body placeholder.

> [!quote] Title placeholder Body placeholder.

> [!abstract] Title placeholder Body placeholder.
---

## Related Source

- Obsidian Help — Callouts (built-in feature; supported in Live Preview and Reading view).