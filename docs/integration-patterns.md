# Integration patterns

Things the HomeAssistant95 integration does that a theme project usually ends up needing too. All of it lives in `custom_components/<domain>/`.

## Modules and options

- One switch per JS/CSS module: `MODULES` in `const.py` maps an option to a file in `www/`, `DEFAULT_OPTIONS` sets the default, `config_flow.py` shows a `BooleanSelector` for it, and `strings.json` plus `translations/*.json` carry the label. Add all five places or the option shows up unnamed.
- `__init__.py` registers the enabled modules with `add_extra_js_url(hass, f"/<domain>/<file>?v=<manifest version>")`. The version suffix is what renews the browser cache on every release.
- Modules that are off by default (screensavers, taskbars, anything that changes the layout) get `False` in `DEFAULT_OPTIONS`. A new module that only adds a card can be on by default.
- A module that other modules use (HA95: the Start menu publishes `window.ha95ColorIcon`) should degrade gracefully when the other one is not loaded, and retry once after a second.

## User files the integration must never overwrite

A theme project often wants a user-editable file (a menu, a list of favorites). Pattern:

1. Ship a default under `custom_components/<domain>/defaults/` (keep it identical to the file in `examples/`).
2. On setup copy it to `/config/www/` **only if the target does not exist** (`_ensure_…_config` in `__init__.py`). `/config/www/` is served as `/local/`; a new `www/` folder needs one HA restart.
3. When a release adds entries to the default, give users a way to get them without losing their edits: a one-shot switch in the options dialog that runs a merge (see `custom_components/ha95/startmenu_merge.py` in [HomeAssistant95](https://github.com/Schumey/HomeAssistant95)). It matches entries by a stable key (`path`, `action` …, never the name, because users translate and rename), inserts each missing entry right after a neighbour the user already has, writes a timestamped backup first, and reports through `persistent_notification.async_create`.
4. Keep that switch out of the stored options: `user_input.pop(KEY, False)` in `async_step_init` before `async_create_entry`.

## Things worth knowing when talking to HA from a module

| Goal | How |
|---|---|
| Message at the bottom | `haRoot.dispatchEvent(new CustomEvent("hass-notification", {bubbles: true, composed: true, detail: {message, duration}}))` |
| Open / close the sidebar | `hass-toggle-menu` on `home-assistant` (bubbles, composed) |
| Open a more-info dialog | `hass-more-info` with `detail: {entityId}`; listen on `window` with `capture: true` to see all of them. While a dialog is open the URL has `?more-info-entity-id=…`. |
| Close the more-info dialog | `home-assistant.shadowRoot.querySelector("ha-more-info-dialog").closeDialog()`. `history.back()` can jump to another page. |
| Navigate | `history.pushState(null, "", path)` then `window.dispatchEvent(new CustomEvent("location-changed", {detail: {replace: false}}))` |
| Notification count | `hass.connection.subscribeMessage(cb, {type: "persistent_notification/subscribe"})` (first message `current`, then `added`/`removed`/`updated`) |
| Check for updates everywhere | `hass.callService("homeassistant", "update_entity", {entity_id: [all update.*]})` plus, with a Supervisor, `hass.callWS({type: "supervisor/api", endpoint: "/refresh_updates", method: "post", timeout: null})` and `/store/reload` (fails quietly without Supervisor) |
| Tell light from dark | `hass.themes.darkMode` |

## A fixed bar at the edge of the page (taskbar, dock)

`home-assistant` scrolls with the **document**, so make room instead of shrinking it:

- `home-assistant { display: block; box-sizing: border-box; padding-bottom: <bar height>; }` in the document head.
- The sidebar is `position: fixed` at `100vh`: add `ha-sidebar { height: calc(100vh - <bar> ) !important; max-height: calc(100dvh - <bar>) !important }` in the shadow root of `home-assistant-main`. It appears late, so retry for ~20 s.
- Popovers (menus) are in the top layer and cover the bar. Clamp their position to `innerHeight - barHeight - menuHeight` or they hang over it.
- Dialogs sit above the bar by themselves; give the bar a low `z-index`. Toasts hang a few pixels over it.
- Do not shrink `home-assistant` with `position: fixed; inset` or a fixed `height` everywhere: on a phone (narrow layout, Companion app) the page then ends at window height and can no longer be scrolled.
- Panels that need a definite height (iframe, add-on and custom panels, `hass.panels[hass.panelUrl].component_name` is `iframe`, `custom` or `app`) and settings pages on wide windows (> 870 px, they scroll inside) are the exception: switch a class on `<html>` and give `home-assistant` `height: calc(100dvh - <bar>); contain: layout` only then. `contain: layout` also keeps `position: fixed` buttons above the bar.
- **Never for dashboards:** `lovelace` panels scroll the document at every width. With a fixed height the document is never taller than the window, so nothing below the first screen can be reached. Condition: `(innerWidth > 870 && panel !== "lovelace") || ["iframe", "custom", "app"].includes(panel)`.
- Pages with `ha-top-app-bar-fixed` set `height: 100vh` themselves and run under the bar: publish the bar height as a variable on `<html>` (`--<domain>-taskbar-height`, 0 without the bar) and give their `:host` `height: calc(100dvh - var(...)) !important`.
