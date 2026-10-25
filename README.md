# HA Theme Kit

🇬🇧 **English** · 🇩🇪 [Deutsch](README.de.md)

A template for building your own **Home Assistant design** and shipping it through HACS, made to be driven by [Claude Code](https://claude.com/claude-code). It is distilled from [HomeAssistant95](https://github.com/Schumey/HomeAssistant95), a Windows 95 design with 15 themes, a start menu and more.

Want an Amiga Workbench, Windows XP, System 7 or your own look? Click **Use this template**, open the folder in Claude Code and say what you want.

## What you get

- **Theme source + generator**: one YAML file with a palette of variables, variants as anchors, and `@include` for shared CSS blocks. `python tools/build.py` writes one finished file per theme.
- **A ready HACS integration** (`custom_components/<domain>/`): installs the chosen themes into `/config/themes/`, serves your JS/CSS and offers an options page.
- **`CLAUDE.md` and `docs/`**: what we learned about HA's frontend, UIX/card-mod, live tuning in a browser, integration patterns (options, user files, fixed bars) and release routine — so Claude does not rediscover it.
- **Design briefs** for Amiga and Windows XP in [docs/ideas.md](docs/ideas.md).

## Quick start

<!-- init:start -->
```bash
git clone https://github.com/YOURNAME/your-repo.git && cd your-repo   # or "Use this template" on GitHub
pip install pyyaml
python tools/init.py --domain amiga --name "Amiga Workbench" --github yourname
```
<!-- init:end -->

Then start Claude Code in the folder and describe the look. It knows the workflow from `CLAUDE.md`. Edit `src/*.src.yaml`, build with `python tools/build.py`, copy `custom_components/<domain>/` to your HA (or push and add the repo to HACS as a custom repository) and pick the theme under **Profile → Theme**.

Your `configuration.yaml` needs:

```yaml
frontend:
  themes: !include_dir_merge_named themes
```

## Docs

| | |
|---|---|
| [Workflow](docs/workflow.md) | Tuning rules live in a running HA |
| [Frontend pitfalls](docs/frontend-pitfalls.md) | Theme variables, UIX paths, card-mod trap, DOM map |
| [Integration patterns](docs/integration-patterns.md) | Modules and options, user files, talking to HA, fixed bars |
| [Ideas](docs/ideas.md) | Amiga and Windows XP briefs |
| [Publishing](docs/publishing.md) | HACS, releases |

## License

MIT. Fonts, cursors and logos of the systems you imitate may have their own licenses; the colors and shapes are your recreation.
