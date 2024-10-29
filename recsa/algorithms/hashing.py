from collections.abc import Mapping

import networkx as nx

from recsa import Assembly, Component
from recsa.algorithms.aux_edge_existence import has_aux_edges


def calc_wl_hash_of_assembly(
        assembly: Assembly, 
        component_structures: Mapping[str, Component]
        ) -> str:
    if has_aux_edges(assembly, component_structures):
        return calc_pure_wl_hash(assembly, component_structures)
    else:
        return calc_rough_wl_hash(assembly)


def calc_rough_wl_hash(assembly: Assembly) -> str:
    # Since nx.weisfeiler_lehman_graph_hash() is not supported for
    # MultiGraph, which is used for the rough graph, we need to convert
    # it to Graph, i.e., remove parallel edges.
    # Consequently, the result of this function will be the same for
    # assemblies with the same rough graph except for the existence of
    # parallel edges.
    rough_g = assembly.rough_g_snapshot
    rough_g_without_parallel_edges = _multi_graph_to_graph(rough_g)
    return nx.weisfeiler_lehman_graph_hash(
        rough_g_without_parallel_edges, node_attr='component_kind')


def _multi_graph_to_graph(G_multi: nx.MultiGraph) -> nx.Graph:
    G_single = nx.Graph()
    for u, v, data in G_multi.edges(data=True):
        G_single.add_edge(u, v)
    for node, data in G_multi.nodes(data=True):
        G_single.nodes[node].update(data)
    return G_single


def calc_pure_wl_hash(
        assembly: Assembly, 
        component_structures: Mapping[str, Component]
        ) -> str:
    g = assembly.g_snapshot(component_structures)
    _add_attr_for_hash(g)
    
    return nx.weisfeiler_lehman_graph_hash(
        g, node_attr='for_hash', edge_attr='for_hash')


def _add_attr_for_hash(g: nx.Graph) -> None:
    for node, data in g.nodes(data=True):
        if data['core_or_bindsite'] == 'core':
            data['for_hash'] = data['component_kind']
        else:
            data['for_hash'] = None

    for u, v, data in g.edges(data=True):
        if 'aux_kind' in data:
            data['for_hash'] = data['aux_kind']
        else:
            data['for_hash'] = None
