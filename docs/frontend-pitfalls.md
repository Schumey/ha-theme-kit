# HA frontend, UIX and card-mod: what we learned

Collected while building HomeAssistant95 (HA 2025.10 – 2026.10). Frontend internals change with HA updates: after each HA release open the dashboard test page and the settings pages and check the rules still hit.

## Theme variables first

Plain theme keys work everywhere (also Companion app, no extra install). Start with them: base colors, `ha-card-*`, `ha-button-*`, `ha-switch-*`, `ha-slider-*`, `ha-color-form-background*`, `header-height`, `state-climate-*-color`, `state-humidifier-on-color`, `sidebar-*`, `graph-color-N`..

- HA computes `rgb-*-color` only from hex values. If you set `primary-color: var(--x)`, also write `rgb-primary-color: "0, 85, 170"`.
- Variables do **not** work when a component sets them itself in `:host` (e.g. `--control-circular-slider-*`, `--control-slider-*`). Use UIX on that element.
- `modes: light:/dark:` inside a theme makes it follow Profile → Theme → Mode.
- Theme names with several files: the integration copies finished single-theme files to `/config/themes/<domain>/`. The user needs `frontend: themes: !include_dir_merge_named themes` in `configuration.yaml`.

## card-mod and UIX

- **card-mod 4.2.1** is unmaintained. Since HA 2026.8 it hangs the UI once a theme has any `card-mod-…-yaml` key. A theme therefore only has simple `card-mod-*` keys (basic look).
- **UIX** is the successor. Its theme keys are `uix-<type>-yaml`; `card-mod-theme: <theme name>` is enough to name the theme.
- Types seen in practice: `card`, `row`, `root`, `top-app-bar-fixed`, `drawer`, `config`, `more-info`, `dialog`, `toast`, `heading-badge`, `assist-chip`, `grid-section`.
- `uix-fonts` (UIX 8.4.0+) loads a web font everywhere, including settings pages, where a Lovelace resource would not reach.

### Paths

- Spaces separate steps. `>` and `:scope` do not work.
- Middle steps take only the **first** matching element.
- `$` jumps into the shadow root of all hits; `$$` searches across all shadow roots (not as the first step).
- Attributes work inside a step: `ha-icon-button[slot=actionItems]`.
- A step is a `querySelectorAll` from the first hit of the previous step, so a selector list without spaces works: `"ha-config-entities,ha-config-helpers $ hass-tabs-subpage-data-table $"` reaches whichever page is shown.
- Paths start at the **parent of the `uix-node`**. For `card`, `row`, `root` and `top-app-bar-fixed` that is the shadow root, so the light DOM (slotted buttons, page content) of `top-app-bar-fixed` is out of reach. Rules for the settings pages belong to `uix-config-yaml`, which hangs on `ha-panel-config`.
- **Find the path in the browser console:** UIX ships `uix_style_path(element)` and `uix_tree(element)`. Use them before writing any new path.
- In `uix-config-yaml` and `uix-profile-yaml` the `.` rules land in the shadow root of the `uix-node` itself, so `:host` there styles nothing useful. Address the pages by path (`ha-panel-config` / `ha-panel-profile` have no shadow root; the pages are in their light DOM).
- Theme variables like `--ha-card-box-shadow` apply everywhere (settings, profile); a look meant only for dashboard cards belongs in the card rules.
- UIX styles a dialog only after it opened: a screenshot taken during the opening animation shows it unstyled. Check with `getComputedStyle`, not with the first screenshot.
- A `<style>` you inject loses against a component's `adoptedStyleSheets` at equal specificity. Use `!important`.
- `:host(:has(…))` does not work in Chrome.
- `!important` across a shadow boundary is reversed: an `!important` rule inside a component beats an `!important` `::part()` rule from outside. To change such a value from outside, let the inner rule read a custom property (`box-shadow: var(--x-shadow, <default>) !important`) and set the property from outside; custom properties inherit into slotted children and shadow roots.
- `:host-context(a)` and `:host([attr])` cannot be combined in one selector. Pass the context down as a custom property instead (see the tab base line below).

## Frontend map (HA 2026.10)

| Thing | Where |
|---|---|
| Select field | `ha-select` → `ha-picker-field` → `ha-combo-box-item` (label in `data-aria-label`). The theme picker on the profile page is `ha-theme-picker` → `ha-generic-picker` → `ha-picker-field`. Its clear button `.clear` has `margin: 0 -8px`, which pushes it under a custom `.arrow`: reset with `margin: 0 !important`. |
| Add-on / app page | `ha-panel-app` (UIX type `app`, `uix-app-yaml`): shadow root with `div.header` (`ha-icon-button` 48×48, `.main-title`) and the `iframe`. Unstyled by themes unless you style it. |
| Date/time | `ha-date-input` / `ha-base-time-input` with `ha-input` → `wa-input` (parts `base`, `label`, `input`, `hint`) |
| Switch | `ha-switch` (Web Awesome), parts `control`, `thumb` |
| Slider | `ha-slider`, parts `track`, `indicator`, `thumb` |
| Dialogs | UIX type `dialog` on `ha-dialog` / `ha-adaptive-dialog`; class `type-<tag without ha->`, e.g. `type-quick-bar`, `type-dialog-box`. The `uix-node` is in the dialog's light DOM; `.` acts in the dialog's shadow root (title, `ha-dialog-footer` with `ha-button[slot=primaryAction|secondaryAction]`). `&.type-quick-bar …` limits a rule to one dialog. |
| Toasts | UIX type `toast` on `ha-toast` (inside `notification-manager`), `$` is its shadow root (`.toast`) |
| Quick bar | `ha-quick-bar` (in the shadow root of `home-assistant`) → `ha-adaptive-dialog` → `ha-picker-combo-box`. Open with `quickBar.showDialog({})`; synthetic key presses are unreliable. |
| Round sliders | `ha-control-slider`, `ha-control-circular-slider` set variables in `:host`; use UIX with `$$`, e.g. `"hui-card-features $$ ha-control-slider $"` |
| View tabs | in `hui-root`: `ha-tab-group` > `ha-tab-group-tab` (part `base`), reachable from `uix-root-yaml` `.` |
| Narrow sidebar | a modal dialog; everything outside is inert. Popups must hang as `popover` in the shadow root of `ha-sidebar`. |
| Sidebar | `ha-sidebar $` has `div.menu` (title) and `div.panels-list` (all entries). Entries are `ha-list-item-button` with `ha-icon` (custom, `icon` name) or `ha-svg-icon` (built in, only `href`). |
| More-info dialog | `ha-more-info-dialog $ ha-adaptive-dialog $ ha-dialog $ ha-dialog-header $`. In `uix-more-info-yaml` paths start **at `ha-adaptive-dialog` itself**: `"$ ha-dialog $ ha-dialog-header $"`. Buttons (`ha-icon-button[slot=headerNavigationIcon\|headerActionItems]`) and title (`.title` with `.breadcrumb`, `.main`) live in the shadow root of `ha-more-info-dialog`. |
| Bottom sheet (phones) | `ha-adaptive-dialog` uses `ha-bottom-sheet` instead of `ha-dialog`. Header is `ha-dialog-header` in the sheet's light DOM (`"$ ha-dialog-header $"`), the drag handle `.handle-wrapper` is in `"$ ha-bottom-sheet $"` (absolute at the top, covers the title otherwise). |
| Dialog frame | A frame drawn as inset `box-shadow` on `wa-dialog::part(dialog)` is painted *under* children, so a footer with its own background (e.g. the add-on update dialog) hides the bottom edge. Draw it as an overlay instead: `wa-dialog::part(dialog) { position: relative; box-shadow: none !important }` plus `::part(dialog)::after { content: ""; position: absolute; inset: 0; z-index: 10; pointer-events: none; box-shadow: var(--dialog-box-shadow) }` in `uix-dialog-yaml` `.`. |
| Card titles | `ha-card` draws the `header` as `h1.card-header` in its own shadow root: path `"ha-card $"` |
| Header buttons | in `hui-root` under `.action-items`; one sits in an `ha-dropdown` and is smaller without fixed sizes |
| Sidebar menu button | `ha-sidebar $ .menu ha-icon-button` is 48 px in a 36 px header: set `--ha-icon-button-size` (e.g. 28px) on it |
| Media card | `hui-media-control-card` has class `type-media-control`; its shadow root has `.background` (video area, `inset` is ignored because HA sets `width: 100%`: use `width: auto !important`), `.player`, `.controls` with `.start` / `.end`, `.more-info`, and `ha-slider` (also `width: 100%`: use `width: auto !important; align-self: stretch` when it should reach past negative margins) |
| Settings pages | app bar `ha-top-app-bar-fixed`, icons in `ha-config-navigation-list` (`.icon-background`) |
| Body font | HA sets `font-family: Roboto` on `body` in `index.html`. Dialogs (`ha-dialog` in the shadow root of `home-assistant`) inherit that instead of the theme font. Fix in a module stylesheet: `body { font-family: var(--ha-font-family-body, Roboto, Noto, sans-serif) }`. |
| Text fields | `ha-input` → `wa-input`; the field is `::part(base)`, the Material underline its `::after`. UIX card/row rules do not reach settings pages and dialogs, so style it per component (see JS modules). `ha-base-time-input` uses `ha-input` for hours and minutes: exempt it with `:host-context(ha-base-time-input)`. |
| Buttons | `ha-button` with `appearance` `accent` / `filled` / `outlined` / `plain`. Accent hover reads `--button-color-fill-loud-hover` (HA teal), not the `wa-color-brand-*` variables: override `.button:hover` inside the component. |
| Toggle groups | `ha-button-toggle-group` → `wa-button-group` with `ha-button`s; the selected one has `appearance="accent"` (e.g. "By target / By type" in the add-trigger dialog). |
| Settings tabs | `hass-tabs-subpage` shadow root: `.toolbar` with `#tabbar` → `a` → `ha-tab` (`$ div`, `[active]` on the host). The space above the tabs is `--safe-area-inset-top` on `:host`. |
| Other tab bars | `ha-tab-group` → `ha-tab-group-tab` (`$ .tab`, part `base`). Developer tools: the group has `slot="subRow"` in `ha-top-app-bar-fixed`; dialogs (card editor, badge picker) use it too. `--track-width: 0; --indicator-color: transparent` on the group removes the underline. **Tabs on a base line:** draw the line on the group (`[part~=base] { box-shadow: inset 0 -1px … }`), let inactive tabs end 1 px above the bottom and the active one reach 1 px further; set both offsets as custom properties on the group, the tabs read them. |
| Editors | Automation, script and scene editors and traces (`ha-automation-editor`, `ha-script-editor`, `ha-scene-editor`, `ha-automation-trace`, `ha-script-trace`) are `hass-subpage` pages: `"ha-automation-editor,ha-script-editor $ hass-subpage $"` in `uix-config-yaml`. |
| Dialogs with their own header | Some dialogs (`hui-dialog-create-badge`, card pickers) put their own `ha-dialog-header slot="header"` (with tabs) into the light DOM of `ha-dialog`; the built-in header then has size 0. `"ha-dialog-header $"` in `uix-dialog-yaml` reaches both. |
| More-info sub views | Settings and history views replace the close button with a back button `ha-icon-button-prev[slot=headerNavigationIcon]` at the same place. Do not give it the close button's look. |
| Tile features | Mode bars: `ha-control-select` (`.container::before` is the tinted background, `.option`, `.option.selected`, colour `--control-select-color`), reach with `"hui-card-features $$ ha-control-select $"`. Target temperature: `ha-control-number-buttons` (`.value` with `.value::before` tint, `.button.minus` / `.button.plus` absolutely positioned). |
| Map (2026.10) | MapLibre, not Leaflet: zoom buttons `ha-map $ .maplibregl-ctrl-group button`; the extra buttons `hui-map-card $ #buttons ha-icon-button`; the people/zones list `hui-map-overview $ .panel` with `.tabs`, `.tabs .pill` (sliding background) and `button[aria-selected]`. |
| Logbook | `ha-logbook-entry $ .node-glyph`, the tinted circle is `.node-glyph::before`. |
| Media page | Player bar `ha-bar-media-player $ ha-slider.progress-slider`. |
| iframe panels (HACS, add-ons) | Their own document: theme variables arrive, but modules, UIX and module stylesheets do not, and a constructed `CSSStyleSheet` cannot be adopted by another document. |
| Timeflow card | `custom:timeflow-card`, compact style: `.card-content-compact` (grid areas `icon`, `title`, `progress`); `progress-circle` knows its value only as the property `progress`, copy it to a CSS variable from a module to draw a bar. |

## Icons

`ha-icon` takes its size from `--mdc-icon-size`. `--mdi-icon-size` (the variable `ha-svg-icon` reads) does not reach through, and `width`/`height` on `ha-icon` are ignored, so an icon stays 24 px.

## Fixed bars and layout

See [integration-patterns.md](integration-patterns.md#a-fixed-bar-at-the-edge-of-the-page-taskbar-dock): the page scrolls with the document, the sidebar is fixed at `100vh`, popovers cover a bar.

## Touch

On tap the browser fires a fake `mouseover`/`mouseenter` before `click`. Write hover logic with `pointerover`/`pointerenter` and `pointerType === "mouse"`.

## JS modules

- Do not use `:scope` selectors on shadow roots inside a MutationObserver (endless loop, UI frozen).
- Register modules via the integration (`add_extra_js_url`). Add `?v=<manifest version>`: caches then renew on every release.
- Keep a `Version: x.y.z` line in each file header; `tools/check.py` compares them.
- Files a module loads itself need the same suffix: `new URL("x.css", import.meta.url)` drops the query, so the browser keeps the old stylesheet after an update. Copy it over: `url.search = new URL(import.meta.url).search`.
- **Styling components everywhere** (settings pages, dialogs) without a UIX path per page: give each component tag its own constructed stylesheet and add it whenever a shadow root of that tag sets `adoptedStyleSheets` (wrap the `ShadowRoot.prototype.adoptedStyleSheets` setter once and handle roots that already exist). Rules then use plain selectors inside the component (`.tab`, `wa-input::part(base)`), and `:host-context(x)` limits them to one place.
