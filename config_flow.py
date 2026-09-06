"""Config flow for Virtual Parallel."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.selector import (
    EntitySelector,
    EntitySelectorConfig,
    SelectSelector,
    SelectSelectorConfig,
)

from .const import DOMAIN

CONF_NAME = "name"
CONF_ENTITIES = "entities"
CONF_MASTER = "master"


class VirtualParallelConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):
    """Virtual Parallel."""

    VERSION = 3

    async def async_migrate_entry(
        self,
        config_entry,
    ):
        """Migrate an existing config entry to version 3."""

        if config_entry.version < 3:
            data = dict(config_entry.data)

            if CONF_MASTER not in data:
                entities = data.get(CONF_ENTITIES, [])
                data[CONF_MASTER] = (
                    entities[0] if entities else None
                )

            self.hass.config_entries.async_update_entry(
                config_entry,
                data=data,
                version=3,
            )

        return True

    async def async_step_user(
        self,
        user_input=None,
    ):
        """Create circuit."""

        if user_input is not None:
            self._name = user_input[CONF_NAME]
            self._entities = user_input[CONF_ENTITIES]

            return await self.async_step_master()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_NAME,
                        default="",
                    ): str,

                    vol.Required(
                        CONF_ENTITIES,
                        default=[],
                    ): EntitySelector(
                        EntitySelectorConfig(
                            domain=["switch"],
                            multiple=True,
                        )
                    ),
                }
            ),
        )

    async def async_step_master(
        self,
        user_input=None,
    ):
        """Select the master entity."""

        if user_input is not None:
            master = user_input.get(CONF_MASTER)

            if master not in self._entities:
                master = (
                    self._entities[0]
                    if self._entities
                    else None
                )

            return self.async_create_entry(
                title=self._name,
                data={
                    CONF_NAME: self._name,
                    CONF_ENTITIES: self._entities,
                    CONF_MASTER: master,
                },
            )

        options = []

        for entity_id in self._entities:
            state = self.hass.states.get(entity_id)

            if state is not None:
                label = state.name or entity_id
            else:
                label = entity_id

            options.append(
                {
                    "value": entity_id,
                    "label": label,
                }
            )

        return self.async_show_form(
            step_id="master",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_MASTER,
                        default=(
                            self._entities[0]
                            if self._entities
                            else None
                        ),
                    ): SelectSelector(
                        SelectSelectorConfig(
                            options=options,
                            mode="dropdown",
                        )
                    ),
                }
            ),
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Return options flow."""

        return VirtualParallelOptionsFlow(
            config_entry
        )


class VirtualParallelOptionsFlow(
    config_entries.OptionsFlow
):
    """Options Flow."""

    def __init__(self, config_entry):
        self._config_entry = config_entry

    async def async_step_init(
        self,
        user_input=None,
    ):
        """Edit circuit."""

        if user_input is not None:
            self._name = user_input.get(
                CONF_NAME,
                self._config_entry.title,
            )

            self._entities = user_input.get(
                CONF_ENTITIES,
                [],
            )

            return await self.async_step_master()

        defaults = {
            CONF_NAME: self._config_entry.options.get(
                CONF_NAME,
                self._config_entry.data.get(
                    CONF_NAME,
                    self._config_entry.title,
                ),
            ),
            CONF_ENTITIES: self._config_entry.options.get(
                CONF_ENTITIES,
                self._config_entry.data.get(
                    CONF_ENTITIES,
                    [],
                ),
            ),
        }

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_NAME,
                        default=defaults[CONF_NAME],
                    ): str,

                    vol.Required(
                        CONF_ENTITIES,
                        default=defaults[CONF_ENTITIES],
                    ): EntitySelector(
                        EntitySelectorConfig(
                            domain=["switch"],
                            multiple=True,
                        )
                    ),
                }
            ),
        )

    async def async_step_master(
        self,
        user_input=None,
    ):
        """Select the master entity."""

        if user_input is not None:
            master = user_input.get(CONF_MASTER)

            if master not in self._entities:
                master = (
                    self._entities[0]
                    if self._entities
                    else None
                )

            return self.async_create_entry(
                title="",
                data={
                    CONF_NAME: self._name,
                    CONF_ENTITIES: self._entities,
                    CONF_MASTER: master,
                },
            )

        current_master = (
            self._config_entry.options.get(
                CONF_MASTER
            )
            or self._config_entry.data.get(
                CONF_MASTER
            )
        )

        if current_master not in self._entities:
            current_master = (
                self._entities[0]
                if self._entities
                else None
            )

        options = []

        for entity_id in self._entities:
            state = self.hass.states.get(entity_id)

            if state is not None:
                label = state.name or entity_id
            else:
                label = entity_id

            options.append(
                {
                    "value": entity_id,
                    "label": label,
                }
            )

        return self.async_show_form(
            step_id="master",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_MASTER,
                        default=current_master,
                    ): SelectSelector(
                        SelectSelectorConfig(
                            options=options,
                            mode="dropdown",
                        )
                    ),
                }
            ),
        )
