# Design briefs: Amiga Workbench and Windows XP

Starting points to give Claude (or yourself). Colors are from memory of the original systems — **verify them against screenshots or palettes** before you rely on them.

## Amiga Workbench

*Workbench 1.3 (1990):* blue desktop, white and orange. *Workbench 2.x/3.x (1990s):* gray, beveled.

| Role | WB 1.3 | WB 3.x |
|---|---|---|
| Desktop | `#0055aa` blue | `#aaaaaa` gray |
| Window face | `#0055aa` / white text | `#aaaaaa` |
| Text | `#ffffff` | `#000000` |
| Accent / selection | `#ff8800` orange | `#6688bb` blue |
| Edges | black, white | white (light) / black (dark) |

Look: thin 1–2 px frames, **square** corners, window title bar with *gadgets*: close at the **left**, depth (front/back) and zoom at the **right**. Font: **Topaz** (an 8×8 pixel font; a free recreation exists as "Topaz a600a1200a4000" from the Amiga community, check its license before bundling). Mouse cursor: the orange-white pointer in 1.3, the busy-bee in 3.x.

Plan for the kit: palette variables, `*-radius: 0`, 2 px bevel via `box-shadow`, `uix-fonts` for the pixel font, title bar gadgets as SVG data-URIs like HomeAssistant95's `title-buttons` (see its `fenster.css`), variants: *WB 1.3*, *WB 3.1*, *MagicWB* (more colorful icons).

## Windows XP (Luna)

| Role | Luna blue | Olive | Silver |
|---|---|---|---|
| Title bar (active) | gradient `#0058ee` → `#3593ff` → `#288eff`, rounded top corners (~8 px) | `#8a9a5f` shades | `#a0a0b8` shades |
| Window frame | `#0831d9` | olive | silver |
| Face | `#ece9d8` | same | same |
| Selection | `#316ac5` | | |
| Taskbar | `#245edb` | | |
| Start button | green `#3c9a3c` | | |
| Close button | red `#e0411f` | | |

Look: rounded 3–8 px corners, title bar with gradient, light gray-beige windows, buttons with rounded corners and a light gradient and blue hover ring, Tahoma 8–11 px, bold Trebuchet MS for titles. Background "Bliss": green hill, blue sky (a photo; use a gradient or your own image instead of the copyrighted original).

Plan: title bar gradient in `--xp-title` (a `linear-gradient` can be a theme variable), `border-radius: 8px 8px 0 0` on `ha-card .card-header`, round close button in the card header via UIX, start-menu-like sidebar (green top, blue body) using the `sidebar-*` variables and `uix-drawer-yaml`, variants: *Luna Blue*, *Olive Green*, *Silver*, *Royale Noir*.

Built: [HomeAssistantXP](https://github.com/Schumey/HomeAssistantXP) is this brief made from the kit; read its `src/` and `www/xp-panels.js` for working rules.

## Others people ask for

macOS Classic (System 7), BeOS, Windows 3.1 / 98 (already done in HomeAssistant95), NeXTSTEP, GEM/Atari ST, C64 / retro terminal green-on-black, Material You palettes.

## How to start with Claude

> "Initialise this template as `amiga` (name: Amiga Workbench). Make the palette Workbench 3.1, square corners, 2 px bevels, close gadget at the left of card headers. Tune live in my HA at <URL> and show me screenshots."
