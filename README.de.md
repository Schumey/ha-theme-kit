# HA Theme Kit

🇬🇧 [English](README.md) · 🇩🇪 **Deutsch**

Eine Vorlage, um ein eigenes **Home-Assistant-Design** zu bauen und über HACS zu verteilen, gedacht für die Arbeit mit [Claude Code](https://claude.com/claude-code). Sie stammt aus [HomeAssistant95](https://github.com/Schumey/HomeAssistant95), einem Windows-95-Design mit 15 Themes, Startmenü und mehr.

Du willst Amiga Workbench, Windows XP, System 7 oder einen ganz eigenen Look? **Use this template** klicken, den Ordner in Claude Code öffnen und sagen, was du willst.

## Was dabei ist

- **Theme-Quelle + Generator**: eine YAML-Datei mit Farbpalette als Variablen, Varianten als Anker und `@include` für gemeinsame CSS-Bausteine. `python tools/build.py` schreibt je Theme eine fertige Datei.
- **Fertige HACS-Integration** (`custom_components/<domain>/`): installiert die gewählten Themes nach `/config/themes/`, stellt JS/CSS bereit und hat eine Optionsseite.
- **`CLAUDE.md` und `docs/`**: was wir über das HA-Frontend, UIX/card-mod, Live-Abstimmung im Browser und den Release-Ablauf gelernt haben (englisch), damit Claude es nicht neu herausfinden muss. Neu: [Integrations-Muster](docs/integration-patterns.md) (Module und Optionen, Nutzerdateien, die nie überschrieben werden, mit HA aus einem Modul reden, feste Leisten am Seitenrand).
- **Design-Vorlagen** für Amiga und Windows XP in [docs/ideas.md](docs/ideas.md).

## Schnellstart

<!-- init:start -->
```bash
git clone https://github.com/DEINNAME/dein-repo.git && cd dein-repo   # oder „Use this template“ auf GitHub
pip install pyyaml
python tools/init.py --domain amiga --name "Amiga Workbench" --github deinname
```
<!-- init:end -->

Dann Claude Code im Ordner starten und den Look beschreiben. Den Ablauf kennt es aus der `CLAUDE.md`. `src/*.src.yaml` bearbeiten, mit `python tools/build.py` bauen, `custom_components/<domain>/` nach HA kopieren (oder pushen und das Repo in HACS als benutzerdefiniertes Repository hinzufügen) und unter **Profil → Design** wählen.

In der `configuration.yaml` muss stehen:

```yaml
frontend:
  themes: !include_dir_merge_named themes
```

## Lizenz

MIT. Schriften, Mauszeiger und Logos der nachgebauten Systeme können eigene Lizenzen haben; Farben und Formen sind deine Nachbildung.
