"""Config flow for Virtual Parallel."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.selector import (
    EntitySelector,
    EntitySelectorConfig,
)

from .const import DOMAIN

CONF_NAME = "name"
CONF_ENTITIES = "entities"


class VirtualParallelConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Virtual Parallel."""

    VERSION = 2

    async def async_step_user(self, user_input=None):
        """Create circuit."""

        if user_input is not None:
            return self.async_create_entry(
                title=user_input[CONF_NAME],
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=self._schema(),
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Return options flow."""

        return VirtualParallelOptionsFlow(config_entry)

    @staticmethod
    def _schema(defaults=None):

        defaults = defaults or {}

        return vol.Schema(
            {
                vol.Required(
                    CONF_NAME,
                    default=defaults.get(CONF_NAME, ""),
                ): str,
                vol.Required(
                    CONF_ENTITIES,
                    default=defaults.get(CONF_ENTITIES, []),
                ): EntitySelector(
                    EntitySelectorConfig(
                        domain=["switch"],
                        multiple=True,
                    )
                ),
            }
        )


class VirtualParallelOptionsFlow(config_entries.OptionsFlow):
    """Options Flow."""

    def __init__(self, config_entry):
        self._config_entry = config_entry

    async def async_step_init(self, user_input=None):

        if user_input is not None:

            return self.async_create_entry(
                title="",
                data=user_input,
            )

        defaults = {
            CONF_NAME: self._config_entry.options.get(
                CONF_NAME,
                self._config_entry.title,
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
            data_schema=VirtualParallelConfigFlow._schema(
                defaults
            ),
        )
