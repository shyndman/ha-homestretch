"""
Custom types for homestretch.

This module defines the runtime data structure attached to each config entry.
Access pattern: entry.runtime_data.coordinator
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .coordinator import HomestretchDataUpdateCoordinator


type HomestretchConfigEntry = ConfigEntry[HomestretchData]


@dataclass
class HomestretchData:
    """Runtime data for homestretch config entries."""

    coordinator: HomestretchDataUpdateCoordinator
    integration: Integration
