# Changelog

## 0.5.0

- `mytheme-css.js` passes its `?v=` on to `mytheme.css`. Before, browsers kept the old stylesheet after an update.
- `mytheme.css` sets the theme font on `body`: HA sets Roboto there, and dialogs inherited it.
- Docs synced with HomeAssistantXP 1.5.7:
  - `integration-patterns.md`: a fixed bar must never give dashboards a fixed page height (they scroll the document at every width); pages with `ha-top-app-bar-fixed` and a bar height variable.
  - `frontend-pitfalls.md`: UIX selector lists, `.` in `uix-config-yaml`, unstyled dialogs during the opening animation, `!important` across shadow boundaries and passing values down as custom properties; frontend map for body font, text fields, buttons and toggle groups, settings and other tab bars (with a base line), editors, dialogs with their own header, more-info back button, tile mode bars and number buttons, MapLibre map, logbook, media bar, iframe panels, timeflow card; module stylesheets and per-component stylesheets.
  - `CLAUDE.md`: three new key facts; `ideas.md` points to HomeAssistantXP.

## 0.4.0

- Docs synced with HomeAssistant95 4.10.4: dialog frame as an overlay (`::after`) instead of an inset `box-shadow`, so footers with their own background no longer hide the bottom edge.

## 0.3.0

- Docs synced with HomeAssistant95 4.10.3: fixed bars must not use a fixed page height on narrow layouts (page could not be scrolled in the Companion app); picker `.clear` margin; `ha-panel-app` header (UIX type `app`).

## 0.2.0

- Docs synced with HomeAssistant95 4.10.0: new `docs/integration-patterns.md` (modules and options, user files the integration never overwrites with a merge switch, events and calls for talking to HA, fixed bars at the page edge).
- `docs/frontend-pitfalls.md`: `ha-icon` size variable, sidebar menu button, media card `.background` / `ha-slider` width.
- `CLAUDE.md`: rules for `width: 100%` overrides, user files and parallel sessions.

## 0.1.0

- Template: generator (`tools/build.py`), starter theme with a dark and an auto variant, integration with options flow, docs.
