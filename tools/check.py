"""Pre-release check: python tools/check.py [x.y.z]

Checks that the generated themes are current, JSON/JS/Python files are valid,
and (if a version is given) that manifest, CHANGELOG and file headers agree.
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors = []


def fail(msg):
    errors.append(msg)
    print("FAIL", msg)


def main():
    comp = [p for p in (ROOT / "custom_components").iterdir() if (p / "manifest.json").exists()]
    if len(comp) != 1:
        sys.exit("expected exactly one integration in custom_components/")
    integ = comp[0]

    r = subprocess.run([sys.executable, str(ROOT / "tools" / "build.py"), "--check"],
                       capture_output=True, text=True)
    if r.returncode:
        fail(r.stderr.strip() or "themes not current")

    for p in ROOT.rglob("*.json"):
        if ".git" in p.parts:
            continue
        try:
            json.loads(p.read_text(encoding="utf-8"))
        except ValueError as e:
            fail(f"{p.relative_to(ROOT)}: {e}")

    for p in integ.rglob("*.py"):
        try:
            compile(p.read_text(encoding="utf-8"), str(p), "exec")
        except SyntaxError as e:
            fail(f"{p.relative_to(ROOT)}: {e}")

    node = shutil.which("node")
    for p in (integ / "www").glob("*.js"):
        if node and subprocess.run([node, "--check", str(p)], capture_output=True).returncode:
            fail(f"node --check failed: {p.name}")

    if len(sys.argv) > 1:
        version = sys.argv[1]
        manifest = json.loads((integ / "manifest.json").read_text(encoding="utf-8"))
        if manifest["version"] != version:
            fail(f"manifest.json has {manifest['version']}, expected {version}")
        for p in [*(integ / "www").glob("*.js"), *(integ / "www").glob("*.css")]:
            m = re.search(r"Version: (\S+)", p.read_text(encoding="utf-8")[:400])
            if not m or m.group(1) != version:
                fail(f"{p.name}: version line missing or != {version}")
        log = (ROOT / "CHANGELOG.md")
        if not log.exists() or f"## {version}" not in log.read_text(encoding="utf-8"):
            fail(f"CHANGELOG.md has no '## {version}' section")

    print("OK" if not errors else f"{len(errors)} problem(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
