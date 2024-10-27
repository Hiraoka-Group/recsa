from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, field_validator

from recsa import AuxEdge, Component

__all__ = ['load_structure_data']


@dataclass
class Args:
    component_structures: dict[str, Component]
    components: dict[str, str]
    bond_id_to_bindsites: dict[str, frozenset[str]]


class AuxEdgeData(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)

    bindsites: tuple[str, str]
    kind: str


class ComponentStructureData(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)

    bindsites: list[str]
    aux_edges: list[AuxEdgeData] | None = None


class ComponentData(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)

    id: str
    kind: str


class BondData(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)

    id: str
    bindsites: tuple[str, str]


class StructureData(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)
    
    comp_kinds: dict[str, ComponentStructureData]
    components: list[ComponentData]
    bonds: list[BondData] | None = None

    @field_validator('bonds')
    def validate_bonds(cls, value):
        return value or set()


def load_structure_data(file_path: str | Path) -> Args:
    """Load structure data from a YAML file."""
    file_path = Path(file_path)
    data = load_yaml(file_path)
    return convert_data_to_args(data)


def load_yaml(file_path: str | Path) -> StructureData:
    """Load YAML file and return the data as a dictionary."""
    file_path = Path(file_path)
    with file_path.open('r') as f:
        data = yaml.safe_load(f)
    return StructureData(**data)


def convert_data_to_args(data: StructureData) -> Args:
    comp_kinds = {
        kind_id: Component(
            set(comp_data.bindsites),
            {AuxEdge(edge.bindsites[0], edge.bindsites[1], edge.kind)
             for edge in comp_data.aux_edges or []})
        for kind_id, comp_data in data.comp_kinds.items()
    }
    components = {comp.id: comp.kind for comp in data.components}
    bonds = {bond.id: frozenset(bond.bindsites) for bond in data.bonds or []}
    
    return Args(comp_kinds, components, bonds)
