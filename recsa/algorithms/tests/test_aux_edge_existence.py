import pytest

from recsa import Assembly, AuxEdge, Component, has_aux_edges


def test_has_aux_edges_true():
    COMPONENT_STRUCTURES = {
        'M': Component(
            {'a', 'b', 'c', 'd'}, 
            {AuxEdge('a', 'b', 'cis'), AuxEdge('b', 'c', 'cis'),
             AuxEdge('c', 'd', 'cis'), AuxEdge('d', 'a', 'cis')}),
        'X': Component({'a'})}
    MX4 = Assembly(
        COMPONENT_STRUCTURES,
        {'M1': 'M', 'X1': 'X', 'X2': 'X', 'X3': 'X', 'X4': 'X'},
        [('M1.a', 'X1.a'), ('M1.b', 'X2.a'), ('M1.c', 'X3.a'), ('M1.d', 'X4.a')])
    assert has_aux_edges(MX4, COMPONENT_STRUCTURES)


def test_has_aux_edges_false():
    COMPONENT_STRUCTURES = {
        'M': Component({'a', 'b', 'c', 'd'}),  # No aux edges
        'X': Component({'a'})}
    MX4 = Assembly(
        COMPONENT_STRUCTURES,
        {'M1': 'M', 'X1': 'X', 'X2': 'X', 'X3': 'X', 'X4': 'X'},
        [('M1.a', 'X1.a'), ('M1.b', 'X2.a'), ('M1.c', 'X3.a'), ('M1.d', 'X4.a')])
    assert not has_aux_edges(MX4, COMPONENT_STRUCTURES)


def test_has_aux_edges_false2():
    COMPONENT_STRUCTURES = {
        'M': Component({'a', 'b', 'c', 'd'}),  # No aux edges
        'L': Component(
            {'a', 'b', 'c', 'd'},
            {AuxEdge('a', 'b', 'cis'), AuxEdge('b', 'c', 'cis'),
             AuxEdge('c', 'd', 'cis'), AuxEdge('d', 'a', 'cis')}),  # Aux edges but not in assembly
        'X': Component({'a'})}
    MX4 = Assembly(
        COMPONENT_STRUCTURES,
        {'M1': 'M', 'X1': 'X', 'X2': 'X', 'X3': 'X', 'X4': 'X'},
        [('M1.a', 'X1.a'), ('M1.b', 'X2.a'), ('M1.c', 'X3.a'), ('M1.d', 'X4.a')])
    assert not has_aux_edges(MX4, COMPONENT_STRUCTURES)


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
