"""Dispatcher do Virtual Parallel."""

from __future__ import annotations

import asyncio
import logging

_LOGGER = logging.getLogger(__name__)


class Dispatcher:
    """Responsável por enviar os comandos."""

    def __init__(self, hass):
        self.hass = hass

    async def dispatch(self, source_entity, entities):

        source_state = self.hass.states.get(source_entity)

        if source_state is None:
            return

        state = source_state.state

        tasks = []

        for entity in entities:

            if entity == source_entity:
                continue

            target = self.hass.states.get(entity)

            if target is None:
                continue

            if target.state == state:
                continue

            domain = entity.split(".", 1)[0]

            service = "turn_on" if state == "on" else "turn_off"

            tasks.append(
                self.hass.services.async_call(
                    domain,
                    service,
                    {
                        "entity_id": entity
                    },
                    blocking=False,
                )
            )

        if tasks:
            _LOGGER.debug(
                "Sincronizando %d entidades",
                len(tasks),
            )

            await asyncio.gather(*tasks)
