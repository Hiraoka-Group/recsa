from copy import deepcopy

import pytest

from recsa import Assembly, AuxEdge, Component
from recsa.algorithms.isomorphism import pure_is_isomorphic


@pytest.fixture
def assem_without_bonds() -> Assembly:
    assem = Assembly()
    assem = assem.with_added_component('M1', 'M')
    assem = assem.with_added_components([('L1', 'L'), ('L2', 'L')])
    assem = assem.with_added_components([('X1', 'X'), ('X2', 'X')])
    return assem


@pytest.fixture
def component_structures() -> dict[str, Component]:
    M_COMP = Component(
        'M', {'a', 'b', 'c', 'd'},
        {
            AuxEdge('a', 'b', 'cis'), AuxEdge('b', 'c', 'cis'),
            AuxEdge('c', 'd', 'cis'), AuxEdge('d', 'a', 'cis'),})
    L_COMP = Component('L', {'a', 'b'})
    X_COMP = Component('X', {'a'})
    return {'M': M_COMP, 'L': L_COMP, 'X': X_COMP}


@pytest.fixture
def assem1(assem_without_bonds: Assembly) -> Assembly:
    return assem_without_bonds.with_added_bonds([
        ('M1.a', 'L1.a'), ('M1.b', 'L2.a'),  # cis
        ('M1.c', 'X1.a'), ('M1.d', 'X2.a')])


@pytest.fixture
def assem2(assem_without_bonds: Assembly) -> Assembly:
    return assem_without_bonds.with_added_bonds([
        ('M1.a', 'L1.a'), ('M1.c', 'L2.a'),  # trans
        ('M1.b', 'X1.a'), ('M1.d', 'X2.a')])


def test_pure_is_isomorphic_with_isomorphic_assemblies(
        assem1: Assembly, component_structures: dict[str, Component]
        ) -> None:
    assem3 = deepcopy(assem1)
    assert pure_is_isomorphic(assem1, assem3, component_structures)


def test_pure_is_isomorphic_with_clearly_non_isomorphic_assemblies(
        assem1: Assembly, component_structures: dict[str, Component]):
    assem2 = assem1.with_removed_bond('M1.a', 'L1.a')
    assert not pure_is_isomorphic(assem1, assem2, component_structures)
    

def test_pure_is_isomorphic_with_relabelled_assemblies(
        assem1: Assembly, component_structures: dict[str, Component]
        ) -> None:
    # Should be isomorphic
    assem2 = assem1.rename_component_ids({'M1': 'M1_'})
    assert pure_is_isomorphic(assem1, assem2, component_structures)


def test_pure_is_isomorphic_with_stereo_isomers(
        assem1: Assembly, assem2: Assembly, 
        component_structures: dict[str, Component]
        ) -> None:
    # Should not be isomorphic, though roughly isomorphic
    assert not pure_is_isomorphic(assem1, assem2, component_structures)



if __name__ == '__main__':
    pytest.main(['-vv', __file__])
