"""Virtual Parallel."""

from __future__ import annotations

import logging

from .listener import EntityListener
from .dispatcher import Dispatcher
from .manager import CircuitManager

_LOGGER = logging.getLogger(__name__)


class VirtualParallel:
    """Virtual Parallel."""

    def __init__(self, hass, entry_id: str):
        self.hass = hass
        self.entry_id = entry_id

        self.manager: CircuitManager = hass.data["virtual_parallel"]["manager"]

        self.dispatcher = Dispatcher(hass)

        self.listener = EntityListener(
            hass,
            self.manager,
            self.dispatcher,
        )

    async def async_setup(self):
        """Start."""

        await self.listener.start()

        _LOGGER.info("Virtual Parallel iniciado")

    async def async_unload(self):
        """Stop."""

        await self.listener.stop()
