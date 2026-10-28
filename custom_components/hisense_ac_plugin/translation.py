"""Translation helpers for Hisense AC Plugin."""
from __future__ import annotations

from typing import Any

from homeassistant.core import HomeAssistant

from .const import DOMAIN

DEFAULT_LANGUAGE = "en"


def get_translations(hass: HomeAssistant) -> dict[str, str]:
    """Return the runtime translations for the configured language.

    Falls back to the base language (e.g. ``zh-CN`` -> ``zh-Hans``) and finally
    to English, so users with a language that is not shipped (e.g. Italian)
    never see Chinese or raw keys.
    """
    all_translations: dict[str, dict[str, str]] = hass.data.get(
        f"{DOMAIN}.translations", {}
    )
    lang = (hass.config.language or DEFAULT_LANGUAGE)
    if lang in all_translations:
        return all_translations[lang]
    if lang.lower().startswith("zh") and "zh-Hans" in all_translations:
        return all_translations["zh-Hans"]
    return all_translations.get(DEFAULT_LANGUAGE, {})


def translate_name(hass: HomeAssistant, key: str, default: Any) -> Any:
    """Translate ``key``: configured language, then English, then ``default``."""
    translations = get_translations(hass)
    if key in translations:
        return translations[key]
    return hass.data.get(f"{DOMAIN}.translations", {}).get(DEFAULT_LANGUAGE, {}).get(
        key, default
    )
