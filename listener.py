"""Listener do Virtual Parallel."""

from __future__ import annotations

import logging

from homeassistant.core import Event
from homeassistant.helpers.event import async_track_state_change_event

_LOGGER = logging.getLogger(__name__)


class EntityListener:
    """Escuta alterações das entidades."""

    def __init__(self, hass, manager, dispatcher):
        self.hass = hass
        self.manager = manager
        self.dispatcher = dispatcher

        self._listeners = []

    async def start(self):
        """Inicia todos os listeners."""

        for circuit in self.manager.all():

            for entity in circuit.entities:

                unsub = async_track_state_change_event(
                    self.hass,
                    [entity],
                    self._state_changed,
                )

                self._listeners.append(unsub)

        _LOGGER.info(
            "Virtual Parallel: %d listeners iniciados",
            len(self._listeners),
        )

    async def stop(self):
        """Remove todos os listeners."""

        for unsub in self._listeners:
            unsub()

        self._listeners.clear()

    async def _state_changed(self, event: Event):

        if event.data.get("new_state") is None:
            return

        entity = event.data["entity_id"]

        circuit = self.manager.find_by_entity(entity)

        if circuit is None:
            return

        await self.dispatcher.dispatch(
            entity,
            list(circuit.entities),
        )
