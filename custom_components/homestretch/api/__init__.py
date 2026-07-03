"""
API package for homestretch.

Architecture:
    Three-layer data flow: Entities → Coordinator → API Client.
    Only the coordinator should call the API client. Entities must never
    import or call the API client directly.

Exception hierarchy:
    HomestretchApiClientError (base)
    ├── HomestretchApiClientCommunicationError (network/timeout)
    └── HomestretchApiClientAuthenticationError (401/403)

Coordinator exception mapping:
    ApiClientAuthenticationError → ConfigEntryAuthFailed (triggers reauth)
    ApiClientCommunicationError → UpdateFailed (auto-retry)
    ApiClientError             → UpdateFailed (auto-retry)
"""

from .client import (
    HomestretchApiClient,
    HomestretchApiClientAuthenticationError,
    HomestretchApiClientCommunicationError,
    HomestretchApiClientError,
)

__all__ = [
    "HomestretchApiClient",
    "HomestretchApiClientAuthenticationError",
    "HomestretchApiClientCommunicationError",
    "HomestretchApiClientError",
]
