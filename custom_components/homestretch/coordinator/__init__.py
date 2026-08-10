"""
Data update coordinator package for homestretch.

This package provides the coordinator infrastructure for managing periodic
data updates and distributing them to all entities in the integration.

For more information on coordinators:
https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
"""

from __future__ import annotations

from .base import HomestretchDataUpdateCoordinator

__all__ = ["HomestretchDataUpdateCoordinator"]
