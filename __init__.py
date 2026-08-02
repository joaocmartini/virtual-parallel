"""Virtual Parallel integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .manager import CircuitManager
from .parallel import VirtualParallel


async def async_setup(
    hass: HomeAssistant,
    config: dict,
) -> bool:
    """Set up Virtual Parallel."""

    hass.data.setdefault(DOMAIN, {})

    if "manager" not in hass.data[DOMAIN]:
        hass.data[DOMAIN]["manager"] = CircuitManager()

    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up config entry."""

    manager: CircuitManager = hass.data[DOMAIN]["manager"]

    data = dict(entry.data)

    if entry.options:
        data.update(entry.options)

    manager.add(
        entry.entry_id,
        data.get("name", entry.title),
        data.get("entities", []),
    )

    vp = VirtualParallel(
        hass,
        entry.entry_id,
    )

    await vp.async_setup()

    hass.data[DOMAIN][entry.entry_id] = vp

    entry.async_on_unload(
        entry.add_update_listener(async_reload_entry)
    )

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload config entry."""

    vp: VirtualParallel = hass.data[DOMAIN].pop(entry.entry_id)

    await vp.async_unload()

    manager: CircuitManager = hass.data[DOMAIN]["manager"]

    manager.remove(entry.entry_id)

    return True


async def async_reload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> None:
    """Reload entry."""

    await hass.config_entries.async_reload(entry.entry_id)
