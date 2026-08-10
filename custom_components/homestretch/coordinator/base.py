"""
Core DataUpdateCoordinator implementation for homestretch.

For more information on coordinators:
https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from custom_components.homestretch.const import LOGGER
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

if TYPE_CHECKING:
    from custom_components.homestretch.data import HomestretchConfigEntry


class HomestretchDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data for all entities."""

    config_entry: HomestretchConfigEntry

    async def _async_setup(self) -> None:
        """Set up the coordinator (one-time initialization before first refresh)."""
        LOGGER.debug("Coordinator setup complete for %s", self.config_entry.entry_id)

    async def _async_update_data(self) -> Any:
        """Fetch data for entities."""
        # ponytail: stub — returns empty data until Homestretch fetching lands
        return {}
