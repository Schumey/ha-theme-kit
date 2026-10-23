# Workflow: tuning a theme live

Blind-written selectors rarely hit the real DOM. The loop that worked:

1. **Open your HA in a browser Claude can drive** (Claude Code's built-in browser or Claude in Chrome). Log in yourself; Claude should never type your password.
2. **Make a test dashboard** with one card of every kind you care about (tile, entities, thermostat, humidifier, light, markdown, history graph, buttons, heading, gauge, calendar …). Keep the YAML in the repo (`examples/test-dashboard.yaml`) so you re-check after every HA update.
3. **Try rules live.** Inject CSS into the real shadow roots with JavaScript, e.g.

   ```js
   const s = new CSSStyleSheet();
   s.replaceSync("ha-card { border-radius: 0 !important }");
   document.querySelector("home-assistant").shadowRoot.adoptedStyleSheets.push(s);
   ```

   For UIX paths use `uix_style_path($0)` / `uix_tree($0)` in the console on a selected element.
4. **Test colors** without rebuilding: `document.documentElement.style.setProperty("--mytheme-face", "#abcdef")`.
5. Screenshot, adjust, repeat. For exact sizes use `getBoundingClientRect()`, not eyeballing (screenshots are scaled down).
6. When it looks right, move the rule into `src/mytheme.src.yaml` or a block in `src/blocks/`, run `python tools/build.py`.
7. **Deploy to a real HA:** copy the integration folder to `/config/custom_components/<domain>/` (File editor / Samba / HACS custom repository), restart HA once (Python changed) or reload the integration (themes only), then *Developer tools → YAML → Reload themes* and pick the theme under *Profile → Theme*.

Notes

- Remote access: if the browser is not on your LAN, a VPN URL (Tailscale) works; `localhost` and `file://` are often blocked in sandboxed browsers, so a local test server is not an option. Inject changed JS modules piece by piece via JavaScript instead.
- Always make a backup copy of any file in your HA before overwriting it.
- Let Claude read the HA frontend, UIX and (if used) Custom Sidebar sources on GitHub before it guesses a selector.
