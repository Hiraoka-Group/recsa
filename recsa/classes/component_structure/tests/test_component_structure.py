import pytest

from recsa import AuxEdge, Component, RecsaValueError


@pytest.fixture
def comp() -> Component:
    return Component('M', {'a', 'b'})

@pytest.fixture
def comp_with_aux_edges() -> Component:
    return Component('M', {'a', 'b'}, {AuxEdge('a', 'b', 'cis')})


def test_init_with_valid_args(comp) -> None:
    assert comp.component_kind == 'M'
    assert set(comp.binding_sites) == {'a', 'b'}


def test_init_with_valid_args_with_single_aux_edge(comp_with_aux_edges) -> None:
    assert comp_with_aux_edges.component_kind == 'M'
    assert set(comp_with_aux_edges.binding_sites) == {'a', 'b'}
    assert comp_with_aux_edges.aux_edges == {AuxEdge('a', 'b', 'cis')}


def test_init_with_valid_args_with_multiple_aux_edges() -> None:
    component = Component('M', {'a', 'b', 'c'}, {
        AuxEdge('a', 'b', 'cis'), AuxEdge('a', 'c', 'cis'), 
        AuxEdge('b', 'c', 'trans')})
    
    assert component.component_kind == 'M'
    assert set(component.binding_sites) == {'a', 'b', 'c'}
    assert component.aux_edges == {
        AuxEdge('a', 'b', 'cis'), AuxEdge('a', 'c', 'cis'), 
        AuxEdge('b', 'c', 'trans')}


def test_init_with_invalid_aux_edge_whose_binding_sites_not_in_binding_sites() -> None:
    with pytest.raises(RecsaValueError):
        Component('M', {'a', 'b'}, {AuxEdge('a', 'c', 'cis')})


def test_init_with_empty_binding_sites() -> None:
    # Empty binding sites is allowed.
    component = Component('M', set())
    assert component.binding_sites == set()


def test_init_with_empty_aux_edges() -> None:
    # Empty aux_edges is allowed.
    component = Component('M', {'a', 'b'}, set())
    assert component.aux_edges == set()


def test_clear_g_cache(comp) -> None:
    comp._Component__g_cache = 1
    assert comp._Component__g_cache == 1

    comp._Component__add_binding_site('c')
    assert comp._Component__g_cache is None


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
