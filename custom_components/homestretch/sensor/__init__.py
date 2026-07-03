"""Sensor platform for homestretch."""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.homestretch.const import PARALLEL_UPDATES as PARALLEL_UPDATES

if TYPE_CHECKING:
    from custom_components.homestretch.data import HomestretchConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback


async def async_setup_entry(
    hass: HomeAssistant,
    entry: HomestretchConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    # ponytail: no entities yet — Homestretch sensors go here
    async_add_entities([])
