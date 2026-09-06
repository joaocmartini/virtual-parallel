"""Storage for Virtual Parallel."""

from __future__ import annotations

from homeassistant.helpers.storage import Store

from .const import DOMAIN


class VirtualParallelStorage:
    """Persistência dos circuitos."""

    STORAGE_VERSION = 2
    STORAGE_KEY = DOMAIN

    def __init__(self, hass):
        self.store = Store(
            hass,
            self.STORAGE_VERSION,
            self.STORAGE_KEY,
        )

    async def load(self):
        """Carrega todos os circuitos."""

        data = await self.store.async_load()

        if data is None:
            data = {
                "circuits": {}
            }

        return data

    async def save(self, data):
        """Salva toda a estrutura."""

        await self.store.async_save(data)

    async def get_circuit(self, entry_id):
        """Obtém um circuito."""

        data = await self.load()

        return data["circuits"].get(entry_id)

    async def set_circuit(
        self,
        entry_id,
        circuit,
    ):
        """Cria ou atualiza um circuito."""

        data = await self.load()

        data["circuits"][entry_id] = circuit

        await self.save(data)

    async def remove_circuit(
        self,
        entry_id,
    ):
        """Remove um circuito."""

        data = await self.load()

        data["circuits"].pop(entry_id, None)

        await self.save(data)

    async def list_circuits(self):
        """Lista todos os circuitos."""

        data = await self.load()

        return data["circuits"]
