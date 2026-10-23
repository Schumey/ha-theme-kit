"""My Theme – design for Home Assistant.

Copies the selected themes to /config/themes/mytheme/, serves the files in www/
under /mytheme/ and registers them as frontend scripts. Change the selection
under Settings → Devices & services → My Theme → Configure.
"""
from __future__ import annotations

import logging
import re
from pathlib import Path

from homeassistant.components.frontend import add_extra_js_url, remove_extra_js_url
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.loader import async_get_integration

from .const import CONF_CSS, CONF_THEMES, DEFAULT_OPTIONS, DOMAIN, MODULES, URL_BASE

_LOGGER = logging.getLogger(__name__)

HERE = Path(__file__).parent
THEMES_SRC = HERE / "themes"
WWW = HERE / "www"
THEME_NAME = re.compile(r"^# theme-name: (.*)$", re.M)


def theme_names() -> dict[str, str]:
    """File name without .yaml -> theme name (read from the header line)."""
    names = {}
    for path in sorted(THEMES_SRC.glob("*.yaml")):
        match = THEME_NAME.search(path.read_text(encoding="utf-8")[:300])
        names[path.stem] = match.group(1) if match else path.stem
    return names


def _sync_themes(target: Path, selected: list[str]) -> None:
    """Copy the selected themes, remove deselected ones from the target folder."""
    target.mkdir(parents=True, exist_ok=True)
    for src in THEMES_SRC.glob("*.yaml"):
        dst = target / src.name
        if src.stem in selected:
            data = src.read_bytes()
            if not dst.exists() or dst.read_bytes() != data:
                dst.write_bytes(data)
        elif dst.exists():
            dst.unlink()


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    version = (await async_get_integration(hass, DOMAIN)).version
    store = hass.data.setdefault(DOMAIN, {})

    if not store.get("static"):
        await hass.http.async_register_static_paths(
            [StaticPathConfig(URL_BASE, str(WWW), True)]
        )
        store["static"] = True

    options = {**DEFAULT_OPTIONS, **entry.options}
    selected = options.get(CONF_THEMES)
    if selected is None:
        selected = list(await hass.async_add_executor_job(theme_names))
    await hass.async_add_executor_job(
        _sync_themes, Path(hass.config.path("themes", DOMAIN)), selected
    )
    try:
        await hass.services.async_call("frontend", "reload_themes", blocking=True)
    except Exception:  # noqa: BLE001 - not fatal if the user has no themes: in configuration.yaml
        _LOGGER.warning(
            "Could not reload themes. Does configuration.yaml contain "
            "'frontend: themes: !include_dir_merge_named themes'?"
        )

    # ?v=<manifest version> keeps the browser cache from serving old files after an update
    urls = [
        f"{URL_BASE}/{name}?v={version}"
        for key, name in MODULES.items()
        if options.get(key, DEFAULT_OPTIONS[key])
    ]
    for url in urls:
        add_extra_js_url(hass, url)
    store[entry.entry_id] = urls

    entry.async_on_unload(entry.add_update_listener(_async_options_updated))
    return True


async def _async_options_updated(hass: HomeAssistant, entry: ConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    for url in hass.data[DOMAIN].pop(entry.entry_id, []):
        remove_extra_js_url(hass, url)
    return True
