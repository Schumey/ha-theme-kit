"""Turns the template into your own theme project (run once, right after cloning).

  python tools/init.py --domain amiga --name "Amiga Workbench" --github yourname

--domain  short lowercase id: folder name, integration domain, CSS variable prefix
--name    display name of the integration (theme names are set in src/*.src.yaml)
--github  your GitHub user name (manifest links, codeowner)

Replaces the placeholders "mytheme", "My Theme" and "YOURNAME" in every text file
and renames the files and folders called mytheme*. Then builds the themes.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "__pycache__", "docs"}
TEXT = {".py", ".json", ".yaml", ".yml", ".css", ".js", ".md"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--domain", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--github", required=True)
    args = ap.parse_args()
    if not re.fullmatch(r"[a-z][a-z0-9_]{1,30}", args.domain):
        sys.exit("--domain: lowercase letters, digits and _ only, starting with a letter")
    if not (ROOT / "custom_components" / "mytheme").exists():
        sys.exit("Already initialised (custom_components/mytheme is gone).")

    # CLAUDE.md and the README files are rewritten too; docs/ keeps the generic words
    # "mytheme" because it describes the template itself.
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix not in TEXT:
            continue
        if SKIP_DIRS & set(path.relative_to(ROOT).parts) or path.name == "init.py":
            continue
        text = path.read_text(encoding="utf-8")
        new = (text.replace("My Theme", args.name)
                   .replace("mytheme", args.domain)
                   .replace("YOURNAME", args.github))
        if new != text:
            path.write_text(new, encoding="utf-8", newline="\n")

    # rename deepest first
    for path in sorted(ROOT.rglob("*mytheme*"), key=lambda p: -len(p.parts)):
        if SKIP_DIRS & set(path.relative_to(ROOT).parts):
            continue
        path.rename(path.with_name(path.name.replace("mytheme", args.domain)))

    # drop the "not initialised yet" notes (between <!-- init:start --> and <!-- init:end -->)
    marker = re.compile(r"<!-- init:start -->.*?<!-- init:end -->\n?", re.S)
    for path in ROOT.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        if marker.search(text):
            path.write_text(marker.sub("", text), encoding="utf-8", newline="\n")

    subprocess.run([sys.executable, str(ROOT / "tools" / "build.py")], check=True)
    print(f"Done. Your integration is custom_components/{args.domain}/ — "
          "next: edit src/*.src.yaml, then run tools/build.py.")


if __name__ == "__main__":
    main()
