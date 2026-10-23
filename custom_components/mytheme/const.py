"""Constants of the My Theme integration."""

DOMAIN = "mytheme"
URL_BASE = "/mytheme"

CONF_THEMES = "themes"
CONF_CSS = "css"

# option switch -> file in www/ (add more modules here, plus a field in config_flow.py)
MODULES = {
    CONF_CSS: "mytheme-css.js",
}

DEFAULT_OPTIONS = {
    CONF_CSS: True,
}
