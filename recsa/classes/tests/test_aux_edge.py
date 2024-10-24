import pytest

import recsa as rx
from recsa import AuxEdge


def test_AuxEdge_initialization():
    edge = AuxEdge('site1', 'site2', 'cis')
    assert edge.local_bindsite1 == 'site1'
    assert edge.local_bindsite2 == 'site2'
    assert edge.aux_kind == 'cis'


def test_AuxEdge_same_binding_sites():
    with pytest.raises(rx.RecsaValueError):
        AuxEdge('site1', 'site1', 'cis')


def test_AuxEdge_equality():
    edge1 = AuxEdge('site1', 'site2', 'cis')
    edge2 = AuxEdge('site2', 'site1', 'cis')
    assert edge1 == edge2


def test_AuxEdge_inequality():
    edge1 = AuxEdge('site1', 'site2', 'cis')
    edge2 = AuxEdge('site1', 'site3', 'cis')
    assert edge1 != edge2


def test_AuxEdge_hash():
    edge1 = AuxEdge('site1', 'site2', 'cis')
    edge2 = AuxEdge('site2', 'site1', 'cis')
    assert hash(edge1) == hash(edge2)


def test_AuxEdge_repr():
    edge = AuxEdge('site1', 'site2', 'cis')
    assert repr(edge) == "AuxEdge('site1', 'site2', 'cis')"


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
