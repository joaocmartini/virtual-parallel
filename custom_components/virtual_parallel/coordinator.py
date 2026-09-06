"""Coordinator."""

from __future__ import annotations

import asyncio
import logging

from .dispatcher import Dispatcher

_LOGGER = logging.getLogger(__name__)


class VirtualParallelCoordinator:
    """Coordinator."""

    def __init__(self, hass):
        self.hass = hass
        self.dispatcher = Dispatcher(hass)
        self._busy = asyncio.Lock()

    async def synchronize(
        self,
        source_entity: str,
        entities: list[str],
    ) -> None:
        """Synchronize entities."""

        if self._busy.locked():
            return

        async with self._busy:
            await self.dispatcher.dispatch(
                source_entity,
                entities,
            )
