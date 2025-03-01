import pytest

from recsa.pipelines.bondset_enumeration import validate_adj_bonds


def test_valid():
    bonds = [1, 2, 3, 4]
    bond_to_adj_bonds = {
        1: {2},
        2: {1, 3},
        3: {2, 4},
        4: {3},
    }
    # Should not raise any exception
    validate_adj_bonds(bond_to_adj_bonds, bonds)


def test_invalid_keys():
    bonds = [1, 2, 3, 4]
    bond_to_adj_bonds = {
        1: {2},
        2: {1, 3},
        3: {2, 4},
        5: {3},  # Invalid key
    }
    with pytest.raises(
            ValueError, 
            match='Keys in "adj_bonds" must be the same as "bonds".'):
        validate_adj_bonds(bond_to_adj_bonds, bonds)


def test_invalid_values():
    bonds = [1, 2, 3, 4]
    bond_to_adj_bonds = {
        1: {2},
        2: {1, 3},
        3: {2, 5},  # Invalid value
        4: {3},
    }
    with pytest.raises(
            ValueError, 
            match='All elements in "adj_bonds" must be in "bonds".'):
        validate_adj_bonds(bond_to_adj_bonds, bonds)


if __name__ == '__main__':
    pytest.main(['-v', __file__])
