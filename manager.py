"""Circuit Manager."""

from __future__ import annotations

import logging

_LOGGER = logging.getLogger(__name__)


class Circuit:
    """Representa um circuito virtual."""

    def __init__(
        self,
        entry_id: str,
        name: str,
        entities: list[str],
    ):
        self.entry_id = entry_id
        self.name = name
        self.entities = set(entities)

    @property
    def count(self):
        return len(self.entities)

    def contains(self, entity_id: str) -> bool:
        return entity_id in self.entities

    def add_entity(self, entity_id: str):
        self.entities.add(entity_id)

    def remove_entity(self, entity_id: str):
        self.entities.discard(entity_id)

    def replace_entities(self, entities: list[str]):
        self.entities = set(entities)

    def rename(self, name: str):
        self.name = name

    def as_dict(self):
        return {
            "entry_id": self.entry_id,
            "name": self.name,
            "entities": sorted(self.entities),
        }


class CircuitManager:
    """Gerencia todos os circuitos."""

    def __init__(self):
        self._circuits: dict[str, Circuit] = {}

    def add(
        self,
        entry_id: str,
        name: str,
        entities: list[str],
    ) -> Circuit:

        circuit = Circuit(
            entry_id,
            name,
            entities,
        )

        self._circuits[entry_id] = circuit

        _LOGGER.info(
            "Circuito '%s' criado (%d entidades)",
            name,
            circuit.count,
        )

        return circuit

    def update(
        self,
        entry_id: str,
        name: str,
        entities: list[str],
    ):

        circuit = self.get(entry_id)

        if circuit is None:
            return self.add(
                entry_id,
                name,
                entities,
            )

        circuit.rename(name)
        circuit.replace_entities(entities)

        _LOGGER.info(
            "Circuito '%s' atualizado",
            name,
        )

        return circuit

    def remove(self, entry_id: str):
        self._circuits.pop(entry_id, None)

    def get(self, entry_id: str):
        return self._circuits.get(entry_id)

    def all(self):
        return list(self._circuits.values())

    def find_by_entity(
        self,
        entity_id: str,
    ):

        for circuit in self._circuits.values():

            if circuit.contains(entity_id):
                return circuit

        return None

    def export(self):

        return {
            circuit.entry_id: circuit.as_dict()
            for circuit in self._circuits.values()
        }
