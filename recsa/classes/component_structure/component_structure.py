from collections.abc import Iterable
from functools import cached_property

import networkx as nx

from ..aux_edge import LocalAuxEdge
from ..validations import (validate_name_of_binding_site,
                           validate_name_of_component_kind)
from .bindsite_existence_check import check_bindsites_of_aux_edges_exists

__all__ = ['ComponentStructure']


class ComponentStructure:
    """A component of an assembly."""

    def __init__(
            self, kind: str, 
            bindsites: Iterable[str],
            aux_edges: Iterable[LocalAuxEdge] | None = None):
        """
        Parameters
        ----------
        component_kind : str
            The component type, e.g., 'M', 'L', 'L1', 'X', etc.
        binding_sites : Iterable[str]
            The binding sites. Each binding site should be a string.
        aux_edges : Mapping[tuple[str, str], str], optional
            Mapping of auxiliary edges. The keys are tuples of two binding
            sites, and the values are the auxiliary kinds. The binding sites
            should be in the binding_sites.
            Duplicate pairs of binding sites raise an error regardless of the
            order of the binding sites.
        """
        validate_name_of_component_kind(kind)
        self._kind = kind

        for bindsite in bindsites:
            validate_name_of_binding_site(bindsite)
        self._bindsites = frozenset(bindsites)

        if aux_edges is not None:
            self._aux_edges = frozenset(aux_edges)
        else:
            self._aux_edges = frozenset()
        check_bindsites_of_aux_edges_exists(
            self._aux_edges, self._bindsites)
    
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, ComponentStructure):
            return False
        return (
            self._kind == value._kind and
            self._bindsites == value._bindsites and
            self._aux_edges == value._aux_edges)

    @property
    def component_kind(self) -> str:
        return self._kind
    
    @property
    def binding_sites(self) -> frozenset[str]:
        return self._bindsites

    @property
    def aux_edges(self) -> frozenset[LocalAuxEdge]:
        return self._aux_edges
    
    @cached_property
    def g_snapshot(self) -> nx.Graph:
        return self._to_graph()

    def _to_graph(self) -> nx.Graph:
        G = nx.Graph()
        G.add_node(
            'core', core_or_bindsite='core',
            component_kind=self.component_kind)
        for bindsite in self.binding_sites:
            G.add_node(bindsite, core_or_bindsite='bindsite')
            G.add_edge('core', bindsite)
        for aux_edge in self.aux_edges:
            G.add_edge(*aux_edge.bindsites, aux_type=aux_edge.aux_kind)
        return G
