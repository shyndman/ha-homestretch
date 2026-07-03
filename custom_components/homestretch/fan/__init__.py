"""Fan platform for homestretch."""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.homestretch.const import PARALLEL_UPDATES as PARALLEL_UPDATES
from homeassistant.components.fan import FanEntityDescription

from .air_purifier_fan import ENTITY_DESCRIPTIONS as FAN_DESCRIPTIONS, HomestretchFan

if TYPE_CHECKING:
    from custom_components.homestretch.data import HomestretchConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

# Combine all entity descriptions from different modules
ENTITY_DESCRIPTIONS: tuple[FanEntityDescription, ...] = (*FAN_DESCRIPTIONS,)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: HomestretchConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the fan platform."""
    async_add_entities(
        HomestretchFan(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )
