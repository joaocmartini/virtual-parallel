"""Dispatcher do Virtual Parallel."""

from __future__ import annotations

import asyncio
import logging

from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)


class Dispatcher:
    """Responsável por enviar os comandos."""

    VALID_STATES = {"on", "off"}

    def __init__(self, hass: HomeAssistant):
        self.hass = hass

    async def dispatch(
        self,
        source_entity: str,
        entities: list[str],
    ) -> None:
        """Sincroniza as entidades de um circuito virtual."""

        source_state = self.hass.states.get(source_entity)

        # A entidade de origem não existe.
        if source_state is None:
            _LOGGER.debug(
                "Virtual Parallel: origem %s não existe.",
                source_entity,
            )
            return

        state = source_state.state

        # IMPORTANTE:
        # Somente ON e OFF são estados válidos para sincronização.
        #
        # unavailable, unknown ou qualquer outro estado
        # NÃO podem ser interpretados como OFF.
        if state not in self.VALID_STATES:
            _LOGGER.debug(
                "Virtual Parallel: ignorando mudança da origem "
                "%s para o estado %s.",
                source_entity,
                state,
            )
            return

        tasks = []

        for entity in entities:

            # Não sincroniza a própria entidade.
            if entity == source_entity:
                continue

            target = self.hass.states.get(entity)

            # Entidade de destino não existe.
            if target is None:
                _LOGGER.debug(
                    "Virtual Parallel: destino %s não existe.",
                    entity,
                )
                continue

            # IMPORTANTE:
            # Nunca enviar comando para uma entidade que esteja
            # unavailable ou unknown.
            if target.state not in self.VALID_STATES:
                _LOGGER.debug(
                    "Virtual Parallel: ignorando destino %s "
                    "porque está no estado %s.",
                    entity,
                    target.state,
                )
                continue

            # Já está no estado desejado.
            if target.state == state:
                continue

            domain = entity.split(".", 1)[0]

            if state == "on":
                service = "turn_on"
            else:
                service = "turn_off"

            tasks.append(
                self.hass.services.async_call(
                    domain,
                    service,
                    {
                        "entity_id": entity,
                    },
                    blocking=False,
                )
            )

        if tasks:
            _LOGGER.debug(
                "Virtual Parallel: sincronizando %d entidades "
                "para o estado %s.",
                len(tasks),
                state,
            )

            await asyncio.gather(*tasks)
