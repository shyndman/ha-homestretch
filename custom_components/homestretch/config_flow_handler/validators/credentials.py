"""
Credential validators.

Validation functions for user credentials and authentication.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant


async def validate_credentials(hass: HomeAssistant, username: str, password: str) -> None:
    """
    Validate user credentials.

    Raises an exception if credentials are invalid.
    """
    # ponytail: no backend yet — accepts anything; wire real validation with the Homestretch client


__all__ = [
    "validate_credentials",
]
