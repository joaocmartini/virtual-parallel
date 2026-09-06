"""Listener do Virtual Parallel."""

from __future__ import annotations

import logging

from homeassistant.core import Event
from homeassistant.helpers.event import async_track_state_change_event

_LOGGER = logging.getLogger(__name__)


class EntityListener:
    """Escuta alterações das entidades."""

    VALID_STATES = {"on", "off"}

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
        """Processa alterações de estado."""

        old_state = event.data.get("old_state")
        new_state = event.data.get("new_state")

        if new_state is None:
            return

        entity = event.data["entity_id"]

        circuit = self.manager.find_by_entity(entity)

        if circuit is None:
            return

        # ---------------------------------------------------------
        # IMPORTANTE:
        # unavailable e unknown NÃO são estados de sincronização.
        #
        # Isso impede que uma entidade que ficou indisponível
        # seja interpretada como OFF e altere as outras entidades.
        # ---------------------------------------------------------

        if new_state.state not in self.VALID_STATES:
            _LOGGER.debug(
                "Virtual Parallel: ignorando %s porque está em %s.",
                entity,
                new_state.state,
            )
            return

        # Ignora eventos que não representam uma mudança real
        # entre ON e OFF.
        if (
            old_state is not None
            and old_state.state in self.VALID_STATES
            and old_state.state == new_state.state
        ):
            return

        # ---------------------------------------------------------
        # PARALELO BIDIRECIONAL
        #
        # Qualquer entidade que esteja disponível e mude para
        # ON/OFF continua podendo comandar as demais.
        #
        # Portanto:
        # Master -> seguidores
        # Seguidor -> Master
        # Seguidor -> outros seguidores
        #
        # continua exatamente como antes.
        # ---------------------------------------------------------

        _LOGGER.info(
            "Virtual Parallel: %s mudou para %s. Sincronizando circuito %s.",
            entity,
            new_state.state,
            circuit.name,
        )

        await self.dispatcher.dispatch(
            entity,
            list(circuit.entities),
        )
